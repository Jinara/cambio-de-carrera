#!/usr/bin/env python3
"""El barrido: mira los boards de empleo de las empresas que elegiste y guarda lo nuevo que encaja.

Detectar no es postular. El barrido no decide si conviene mandar: deja la lista en
mi-cerebro/barrido/ y el veredicto se hace leyendo el aviso completo (paso 4, parte 3).

    python3 herramientas/barrido.py                      barre y avisa lo nuevo
    python3 herramientas/barrido.py probar "Nombre"      busca en qué board publica una empresa
    python3 herramientas/barrido.py probar URL --agregar y la suma a mi-cerebro/barrido.json
    python3 herramientas/barrido.py hallazgos            lo encontrado que falta decidir
    python3 herramientas/barrido.py pasar h3 [carril=A cv=...]   al registro, para revisar
    python3 herramientas/barrido.py ignorar h3

Opciones: --cerebro CARPETA, --sin-aviso (no manda la notificación del sistema).

Lee los filtros de mi-cerebro/barrido.json. Tiene que correr en tu computadora: los agentes
programados en la nube no tienen salida a los boards.

Sin dependencias: solo Python 3.8 o más nuevo.
"""
import json
import platform
import re
import shutil
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vacantes  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BOARDS = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{}/jobs",
    "lever": "https://api.lever.co/v0/postings/{}",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{}",
    "recruitee": "https://{}.recruitee.com/api/offers/",
}
# Cómo se reconoce cada board en la URL de una página de empleos.
URL_BOARD = [
    ("greenhouse", r"greenhouse\.io/(?:v1/boards/)?([a-z0-9_-]+)"),
    ("lever", r"lever\.co/(?:v0/postings/)?([a-z0-9_.-]+)"),
    ("ashby", r"ashbyhq\.com/(?:posting-api/job-board/)?([a-z0-9_.%-]+)"),
    ("recruitee", r"^([a-z0-9-]+)\.recruitee\.com"),
]
# Palabras que no cambian el puesto: el mismo aviso publicado una vez por país sigue siendo uno.
NO_CAMBIAN_EL_PUESTO = {"remote", "remoto", "remota", "hybrid", "hibrido", "hibrida", "presencial",
                        "latam", "latin", "america", "americas", "south", "sur", "global", "worldwide",
                        "argentina", "bolivia", "brasil", "brazil", "chile", "colombia", "ecuador", "espana", "spain",
                        "guatemala", "mexico", "panama", "paraguay", "peru", "uruguay", "venezuela", "usa"}
PM = re.compile(r"\bpm\b")
TOKENS_URL = re.compile(r"([0-9]{6,})|/o/([a-z0-9-]{8,})|jobs/([a-z0-9-]{8,})")


# ─────────────────────────────── texto ───────────────────────────────

def plano(texto):
    """Minúsculas, sin tildes y sin puntuación, con un espacio a cada lado para buscar palabras enteras."""
    texto = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return " " + re.sub(r"[^a-z0-9]+", " ", texto.lower()).strip() + " "


def contiene(texto, terminos):
    """Qué términos aparecen como palabras enteras. 'ar' no aparece dentro de 'marketing'."""
    t = plano(texto)
    return [x for x in terminos if plano(x) != "  " and plano(x) in t]


def titulo_clave(titulo, lugares=()):
    """El título comparable entre dos publicaciones del mismo puesto."""
    t = PM.sub("product manager", plano(titulo))
    quitar = NO_CAMBIAN_EL_PUESTO | {w for lugar in lugares for w in plano(lugar).split()}
    return " ".join(w for w in t.split() if w not in quitar)


# ─────────────────────────────── configuración ───────────────────────────────

VACIA = {
    "empresas": [],
    "titulos": {},
    "titulos_no": [],
    "ubicacion_si": [],
    "ubicacion_no": [],
    "ubicacion_salva": [],
}


def cargar_config(cerebro):
    p = Path(cerebro) / "barrido.json"
    if not p.exists():
        return dict(VACIA), p
    config = dict(VACIA)
    config.update(json.loads(p.read_text(encoding="utf-8")))
    return config, p


def guardar_config(ruta, config):
    vacantes.escribir_json(ruta, config)


def carriles_del_titulo(titulo, config):
    """Los carriles cuyo título aparece, salvo que el título tenga una palabra de las que no."""
    if contiene(titulo, config.get("titulos_no", [])):
        return []
    return [c for c, terminos in config.get("titulos", {}).items() if contiene(titulo, terminos)]


def ubicacion_sirve(ubicacion, config):
    """Pasa si nombra un lugar de los que sí y ninguno de los que no.

    El veto no aplica si el mismo texto nombra un lugar de los que salvan: muchos avisos dicen
    "United States, LATAM, Remote", y esos sirven. Sin lugares de los que sí, pasa todo lo que
    no esté vetado.
    """
    si, no, salva = config.get("ubicacion_si", []), config.get("ubicacion_no", []), config.get("ubicacion_salva", [])
    if si and not contiene(ubicacion, si):
        return False
    if contiene(ubicacion, no) and not contiene(ubicacion, salva):
        return False
    return True


# ─────────────────────────────── los boards ───────────────────────────────

class NoExiste(Exception):
    """El board contestó que esa empresa no está."""


def traer(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "cambio-de-carrera/1.0 (barrido personal)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NoExiste(url)
        raise


def normalizar(board, datos):
    """Cada board devuelve otra forma. Sale una lista de {id, puesto, ubicacion, url}.

    La ubicación es solo lo que el aviso escribe. Las marcas de "remoto" de cada board no se suman:
    muchas empresas marcan remoto un puesto que es remoto dentro de su país, y el texto lo aclara.
    """
    out = []
    if board == "greenhouse":
        for j in datos.get("jobs", []):
            out.append({"id": j.get("id"), "puesto": j.get("title", ""),
                        "ubicacion": (j.get("location") or {}).get("name", ""), "url": j.get("absolute_url", "")})
    elif board == "lever":
        for j in datos if isinstance(datos, list) else []:
            cat = j.get("categories") or {}
            lugares = [cat.get("location") or ""] + list(cat.get("allLocations") or [])
            out.append({"id": j.get("id"), "puesto": j.get("text", ""),
                        "ubicacion": ", ".join(dict.fromkeys(l for l in lugares if l)), "url": j.get("hostedUrl", "")})
    elif board == "ashby":
        for j in datos.get("jobs", []):
            if j.get("isListed") is False:
                continue
            lugares = [j.get("location") or ""] + [s.get("location", "") for s in j.get("secondaryLocations") or []]
            out.append({"id": j.get("id") or j.get("jobUrl"), "puesto": (j.get("title") or "").strip(),
                        "ubicacion": ", ".join(dict.fromkeys(l for l in lugares if l)), "url": j.get("jobUrl", "")})
    elif board == "recruitee":
        for j in datos.get("offers", []):
            lugares = [j.get("location") or "", j.get("country") or ""]
            lugares += [l.get("country") or l.get("name") or "" for l in j.get("locations") or []]
            out.append({"id": j.get("slug") or j.get("id"), "puesto": j.get("title", ""),
                        "ubicacion": ", ".join(dict.fromkeys(l for l in lugares if l)), "url": j.get("careers_url", "")})
    return out


def board_de_url(texto):
    """De la URL de una página de empleos, el board y el nombre que usa para la empresa."""
    u = urlparse(texto if "://" in texto else "https://" + texto)
    host_y_ruta = (u.netloc + u.path).lower()
    for board, patron in URL_BOARD:
        m = re.search(patron, host_y_ruta)
        if m and m.group(1) not in ("jobs", "v1", "v0", "api", "www", "boards", "job-boards"):
            return board, m.group(1)
    return None


def candidatos(nombre):
    palabras = plano(nombre).split()
    return list(dict.fromkeys(x for x in ("".join(palabras), "-".join(palabras), palabras[0] if palabras else "") if x))


# ─────────────────────────────── estado del barrido ───────────────────────────────

def cargar_hallazgos(cerebro):
    p = Path(cerebro) / "barrido" / "hallazgos.json"
    if not p.exists():
        return {"hallazgos": [], "corridas": []}
    datos = json.loads(p.read_text(encoding="utf-8"))
    datos.setdefault("hallazgos", [])
    datos.setdefault("corridas", [])
    return datos


def guardar_hallazgos(cerebro, datos):
    vacantes.escribir_json(Path(cerebro) / "barrido" / "hallazgos.json", datos)


def ya_conocidas(registro, hallazgos, lugares):
    """Lo que no se vuelve a avisar: todo lo del registro, y todo lo que el barrido ya encontró."""
    ids, tokens, puestos = set(), set(), set()
    for h in hallazgos["hallazgos"]:
        ids.add(h["clave"])
        puestos.add((plano(h["empresa"]), titulo_clave(h["puesto"], lugares)))
    for v in registro["vacantes"]:
        for grupo in TOKENS_URL.findall((v.get("url") or "").lower()):
            tokens.update(t for t in grupo if t)
        puestos.add((plano(v.get("empresa")), titulo_clave(v.get("puesto"), lugares)))
    return ids, tokens, puestos


def nuevo_id_hallazgo(hallazgos):
    usados = {h["id"] for h in hallazgos["hallazgos"]}
    n = len(usados) + 1
    while f"h{n}" in usados:
        n += 1
    return f"h{n}"


def barrer(config, registro, hallazgos, traer=traer, ahora=None):
    """Una pasada por todas las empresas. Devuelve (nuevos, fallos, miradas).

    Solo se guarda lo que encajó: si un board corrige el título o la ubicación de un aviso que
    hoy no pasa, en la próxima pasada se vuelve a evaluar.
    """
    ahora = ahora or datetime.now().isoformat(timespec="minutes")
    lugares = config.get("ubicacion_si", []) + config.get("ubicacion_no", []) + config.get("ubicacion_salva", [])
    ids, tokens, puestos = ya_conocidas(registro, hallazgos, lugares)
    nuevos, fallos, miradas = [], [], 0

    def una(empresa):
        url = BOARDS[empresa["board"]].format(empresa["slug"])
        try:
            return empresa, normalizar(empresa["board"], traer(url)), None
        except Exception as e:  # un board caído no frena a los demás
            return empresa, [], f"{empresa['nombre']} ({empresa['board']}/{empresa['slug']}): {e}"

    with ThreadPoolExecutor(max_workers=6) as pool:
        resultados = list(pool.map(una, config.get("empresas", [])))

    for empresa, avisos, error in resultados:
        if error:
            fallos.append(error)
            continue
        miradas += 1
        for a in avisos:
            clave = f"{empresa['board']}:{empresa['slug']}:{a['id']}"
            if clave in ids:
                continue
            carriles = carriles_del_titulo(a["puesto"], config)
            if not carriles or not ubicacion_sirve(a["ubicacion"], config):
                continue
            url = (a["url"] or "").lower()
            if any(t in url for t in tokens):
                continue
            puesto = (plano(empresa["nombre"]), titulo_clave(a["puesto"], lugares))
            if puesto in puestos:
                continue
            h = {"id": nuevo_id_hallazgo(hallazgos), "clave": clave, "empresa": empresa["nombre"],
                 "puesto": a["puesto"], "ubicacion": a["ubicacion"], "url": a["url"], "carriles": carriles,
                 "encontrado": ahora, "estado": "nuevo"}
            hallazgos["hallazgos"].append(h)
            ids.add(clave)
            puestos.add(puesto)
            nuevos.append(h)
    return nuevos, fallos, miradas


# ─────────────────────────────── avisar ───────────────────────────────

def notificar(texto):
    """Notificación del sistema. El texto va como argumento, nunca pegado dentro del script."""
    sistema = platform.system()
    try:
        if sistema == "Darwin":
            subprocess.run(["osascript", "-e", "on run argv", "-e",
                            'display notification (item 1 of argv) with title "Barrido de vacantes"',
                            "-e", "end run", texto], check=False, timeout=15)
        elif sistema == "Linux" and shutil.which("notify-send"):
            subprocess.run(["notify-send", "Barrido de vacantes", texto], check=False, timeout=15)
    except Exception:
        pass  # sin notificación el reporte igual queda escrito


def reporte(nuevos, fallos, miradas, total, ahora):
    lineas = [f"# Barrido {ahora.replace('T', ' ')}", ""]
    if total == 0:
        lineas.append("No hay empresas en `mi-cerebro/barrido.json`. Se agregan con `barrido.py probar`.")
    elif miradas == 0:
        lineas.append(f"🔴 **No se pudo mirar nada.** Fallaron los {total} boards, así que esto no quiere decir "
                      "que no haya vacantes nuevas. Suele pasar cuando la computadora recién se despierta y "
                      "todavía no tiene red.")
    elif nuevos:
        lineas.append(f"**{len(nuevos)} nueva(s) que encajan con tus filtros** (se miraron {miradas} de {total}):\n")
        for h in nuevos:
            lineas.append(f"- `{h['id']}` **{h['empresa']}** · {h['puesto']} · {h['ubicacion'] or 'sin ubicación'} "
                          f"· carril {'/'.join(h['carriles'])}\n  {h['url']}")
    else:
        lineas.append(f"Nada nuevo que encaje. Se miraron {miradas} de {total} boards.")
    if fallos and miradas:
        lineas += ["", "## Boards que fallaron", *[f"- {f}" for f in fallos]]
    lineas += ["", "> Esto encuentra avisos, no decide. Antes de postular va el veredicto: qué pide el aviso,",
               "> qué cumples y si conviene. Y verifica que siga abierto en la página de la empresa."]
    return "\n".join(lineas) + "\n"


# ─────────────────────────────── comandos ───────────────────────────────

def cmd_barrer(cerebro, avisar=True):
    config, _ = cargar_config(cerebro)
    registro = vacantes.cargar(cerebro)
    hallazgos = cargar_hallazgos(cerebro)
    ahora = datetime.now().isoformat(timespec="minutes")
    total = len(config["empresas"])
    if total == 0:
        print("No hay empresas en mi-cerebro/barrido.json. Se agregan con: barrido.py probar \"Nombre\" --agregar")
        return
    nuevos, fallos, miradas = barrer(config, registro, hallazgos, ahora=ahora)
    texto = reporte(nuevos, fallos, miradas, total, ahora)
    print(texto)
    ciego = total > 0 and miradas == 0
    hallazgos["corridas"] = (hallazgos["corridas"] + [
        {"fecha": ahora, "empresas": total, "miradas": miradas, "nuevos": len(nuevos), "fallos": fallos}])[-60:]
    guardar_hallazgos(cerebro, hallazgos)
    (Path(cerebro) / "barrido" / "ultimo.md").write_text(texto, encoding="utf-8")
    if avisar and ciego:
        notificar(f"No se pudo mirar ningún board ({total}). No quiere decir que no haya nada.")
    elif avisar and nuevos:
        resto = f" (+{len(nuevos) - 1} más)" if len(nuevos) > 1 else ""
        notificar(f"{nuevos[0]['empresa']}: {nuevos[0]['puesto']}{resto}")


def cmd_probar(cerebro, texto, agregar=False, nombre=None):
    config, ruta_config = cargar_config(cerebro)
    directo = board_de_url(texto) if ("." in texto or "/" in texto) else None
    if directo:
        intentos = [directo]
        nombre = nombre or directo[1].replace("-", " ").title()
    else:
        intentos = [(b, s) for s in candidatos(texto) for b in BOARDS]
        nombre = nombre or texto

    def una(par):
        board, slug = par
        try:
            return board, slug, normalizar(board, traer(BOARDS[board].format(slug), timeout=12)), None
        except NoExiste:
            return board, slug, None, None
        except Exception as e:
            return board, slug, None, str(e)

    with ThreadPoolExecutor(max_workers=8) as pool:
        resultados = list(pool.map(una, intentos))
    encontrados = [r for r in resultados if r[2] is not None]
    errores = [r for r in resultados if r[3]]

    if not encontrados:
        print(f"No encontré a {nombre} en {', '.join(BOARDS)}.")
        if errores:
            print("Y algunos boards no contestaron, así que puede ser la red:")
            for b, s, _, e in errores:
                print(f"  {b}/{s}: {e}")
        print("\nSi tienes la URL de su página de empleos, pruébala directo. Si publica en otro lado "
              "(su propio sitio, LinkedIn, un portal), el barrido no la puede mirar: para esa, alertas por correo.")
        return 1
    for board, slug, avisos, _ in encontrados:
        encajan = [a for a in avisos if carriles_del_titulo(a["puesto"], config) and ubicacion_sirve(a["ubicacion"], config)]
        print(f"✅ {nombre} publica en {board} como '{slug}': {len(avisos)} avisos abiertos hoy, "
              f"{len(encajan)} pasan tus filtros.")
        for a in (encajan or avisos)[:5]:
            print(f"   · {a['puesto']} · {a['ubicacion'] or 'sin ubicación'}")
    if agregar:
        board, slug, _, _ = encontrados[0]
        if any(e["board"] == board and e["slug"] == slug for e in config["empresas"]):
            print(f"\nYa estaba en {ruta_config.name}.")
        else:
            config["empresas"].append({"nombre": nombre, "board": board, "slug": slug})
            guardar_config(ruta_config, config)
            print(f"\nAgregada a {ruta_config}.")
    elif len(encontrados):
        print("\nPara sumarla al barrido, repite con --agregar (y --nombre \"Cómo se llama\" si el nombre no quedó bien).")
    return 0


def cmd_hallazgos(cerebro):
    nuevos = [h for h in cargar_hallazgos(cerebro)["hallazgos"] if h["estado"] == "nuevo"]
    for h in nuevos:
        print(f"{h['id']:<5} {h['encontrado'][:10]}  {'/'.join(h['carriles']):<4} {h['empresa'][:20]:<20} "
              f"{h['puesto']} · {h['ubicacion'] or 'sin ubicación'}\n      {h['url']}")
    print(f"\n{len(nuevos)} sin decidir")


def decidir(registro, hallazgos, hid, accion, extra=None, hoy=None):
    """Pasa un hallazgo al registro, para revisar, o lo ignora. Devuelve el mensaje para la persona."""
    h = next((x for x in hallazgos["hallazgos"] if x["id"] == hid), None)
    if not h:
        raise vacantes.Error(f"No existe el hallazgo {hid}")
    if h["estado"] != "nuevo":
        raise vacantes.Error(f"{hid} ya estaba decidido: {h['estado']}")
    if accion == "pasar":
        campos = {"empresa": h["empresa"], "puesto": h["puesto"], "url": h["url"], "estado": "revisar",
                  "notas": f"Del barrido, {h['encontrado'][:10]} · {h['ubicacion'] or 'sin ubicación'}"}
        if len(h["carriles"]) == 1:
            campos["carril"] = h["carriles"][0]
        campos.update(extra or {})
        v = vacantes.alta(registro, campos, hoy)
        h["estado"], h["vacante"] = "pasado", v["id"]
        return f"{hid} pasó al registro como {v['id']}, para revisar"
    if accion == "ignorar":
        h["estado"] = "ignorado"
        return f"{hid} ignorado. No vuelve a aparecer."
    raise vacantes.Error(f"No sé hacer '{accion}' con un hallazgo: pasar o ignorar")


def cmd_decidir(cerebro, hid, accion, extra):
    registro, hallazgos = vacantes.cargar(cerebro), cargar_hallazgos(cerebro)
    mensaje = decidir(registro, hallazgos, hid, accion, extra)
    if accion == "pasar":
        vacantes.guardar(cerebro, registro)
    guardar_hallazgos(cerebro, hallazgos)
    print(f"✅ {mensaje}")


def main(argv):
    cerebro = RAIZ / "mi-cerebro"
    avisar, agregar, nombre = "--sin-aviso" not in argv, "--agregar" in argv, None
    argv = [a for a in argv if a not in ("--sin-aviso", "--agregar")]
    for opcion in ("--cerebro", "--nombre"):
        if opcion in argv:
            i = argv.index(opcion)
            if i + 1 >= len(argv):
                sys.exit(f"⛔ Falta el valor de {opcion}")
            if opcion == "--cerebro":
                cerebro = (Path.cwd() / Path(argv[i + 1]).expanduser()).resolve()
            else:
                nombre = argv[i + 1]
            argv = argv[:i] + argv[i + 2:]
    if cerebro == (RAIZ / "ejemplo").resolve() and (not argv or argv[0] in ("probar", "pasar", "ignorar")):
        sys.exit("El ejemplo no sale a internet ni se modifica: sus empresas son inventadas. "
                 "Para ver lo que encontró: barrido.py hallazgos --cerebro ejemplo")
    try:
        if not argv:
            cmd_barrer(cerebro, avisar)
        elif argv[0] == "probar" and len(argv) > 1:
            return cmd_probar(cerebro, " ".join(argv[1:]), agregar, nombre)
        elif argv[0] == "hallazgos":
            cmd_hallazgos(cerebro)
        elif argv[0] in ("pasar", "ignorar") and len(argv) > 1:
            cmd_decidir(cerebro, argv[1], argv[0], vacantes.pares(argv[2:]))
        else:
            sys.exit(__doc__)
    except vacantes.Error as e:
        sys.exit(f"⛔ {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
