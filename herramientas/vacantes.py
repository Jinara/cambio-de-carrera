#!/usr/bin/env python3
"""El registro de vacantes: qué se encontró, qué se mandó, con qué CV y qué pasó después.

Vive en mi-cerebro/vacantes.json. Lo leen el barrido (para no avisar dos veces lo mismo) y el
tablero. Cada cambio de un campo queda en el historial con su fecha, así después se puede
contestar "¿cuándo respondieron?" sin depender de la memoria.

    python3 herramientas/vacantes.py lista [estado]
    python3 herramientas/vacantes.py ver ID
    python3 herramientas/vacantes.py alta empresa="Acme" puesto="Product Analyst" url=... \\
                                          carril=A cv=cv-a-operaciones estado=revisar notas="..."
    python3 herramientas/vacantes.py cambiar ID estado=postulada enviado=2026-09-16
    python3 herramientas/vacantes.py seguimiento [días]
    python3 herramientas/vacantes.py resumen

Con --cerebro CARPETA se usa otra carpeta (por ejemplo, --cerebro ejemplo).

Sin dependencias: solo Python 3.8 o más nuevo.
"""
import json
import os
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCHIVO = "vacantes.json"
ESTADOS = ("revisar", "postulada", "respondieron", "entrevistando", "oferta", "rechazada", "descartada")
CAMPOS = ("empresa", "puesto", "url", "carril", "cv", "estado", "cargada", "enviado", "entrevistas", "notas")
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Error(Exception):
    """Un error que se le muestra a la persona tal cual."""


# ─────────────────────────────── lectura y escritura ───────────────────────────────

def ruta(cerebro):
    return Path(cerebro) / ARCHIVO


def cargar(cerebro):
    p = ruta(cerebro)
    if not p.exists():
        return {"vacantes": [], "historial": []}
    datos = json.loads(p.read_text(encoding="utf-8"))
    datos.setdefault("vacantes", [])
    datos.setdefault("historial", [])
    return datos


def escribir_json(p, datos):
    """Escribe en un archivo temporal y lo renombra: si algo se corta a la mitad, el archivo
    anterior queda entero."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix="." + p.stem + "-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, p)


def guardar(cerebro, datos):
    escribir_json(ruta(cerebro), datos)


# ─────────────────────────────── reglas ───────────────────────────────

def validar(campos):
    limpio = {}
    for k, v in campos.items():
        if k not in CAMPOS:
            raise Error(f"Campo desconocido: {k}. Los que hay: {', '.join(CAMPOS)}")
        if k == "estado" and v not in ESTADOS:
            raise Error(f"Estado desconocido: {v}. Tiene que ser uno de: {', '.join(ESTADOS)}")
        if k in ("cargada", "enviado") and v not in (None, "") and not FECHA.match(str(v)):
            raise Error(f"La fecha de {k} va como AAAA-MM-DD, no como {v}")
        if k == "entrevistas":
            try:
                v = int(v or 0)
            except ValueError:
                raise Error(f"entrevistas tiene que ser un número, no {v}")
        limpio[k] = v if v != "" else None
    return limpio


def nuevo_id(datos, empresa):
    base = "".join(c for c in empresa.lower() if c.isalpha())[:3] or "vac"
    usados = {v["id"] for v in datos["vacantes"]}
    n = 1
    while f"{base}{n}" in usados:
        n += 1
    return f"{base}{n}"


def buscar(datos, vid):
    for v in datos["vacantes"]:
        if v["id"] == vid:
            return v
    raise Error(f"No existe la vacante {vid}")


def alta(datos, campos, hoy=None):
    campos = validar(campos)
    if not campos.get("empresa") or not campos.get("puesto"):
        raise Error("Una vacante necesita al menos empresa y puesto")
    v = {"id": nuevo_id(datos, campos["empresa"]), "estado": "revisar",
         "cargada": hoy or date.today().isoformat(), "entrevistas": 0}
    v.update({k: val for k, val in campos.items() if val is not None})
    datos["vacantes"].append(v)
    datos["historial"].append({"fecha": v["cargada"], "id": v["id"], "campo": "alta",
                               "antes": None, "despues": v["estado"]})
    return v


def cambiar(datos, vid, cambios, hoy=None):
    """Aplica los cambios y deja en el historial solo los campos que de verdad cambiaron."""
    v = buscar(datos, vid)
    cambios = validar(cambios)
    hoy = hoy or date.today().isoformat()
    # Pasar a postulada sin fecha de envío es el olvido más común: se completa con hoy.
    if cambios.get("estado") == "postulada" and not (cambios.get("enviado") or v.get("enviado")):
        cambios["enviado"] = hoy
    reales = {}
    for k, val in cambios.items():
        if v.get(k) != val:
            datos["historial"].append({"fecha": hoy, "id": vid, "campo": k,
                                       "antes": v.get(k), "despues": val})
            v[k] = val
            reales[k] = val
    return v, reales


def dias_desde(fecha, hoy=None):
    if not fecha:
        return None
    hoy = date.fromisoformat(hoy) if hoy else date.today()
    return (hoy - date.fromisoformat(fecha)).days


def seguimiento(datos, dias=14, hoy=None):
    """Postuladas sin respuesta hace `dias` o más: las que conviene mirar o dar por perdidas."""
    return sorted((v for v in datos["vacantes"]
                   if v.get("estado") == "postulada" and (dias_desde(v.get("enviado"), hoy) or 0) >= dias),
                  key=lambda v: v.get("enviado") or "")


def resumen(datos):
    """Conteo por estado, y el experimento del paso 3: cuántas respondieron por carril y por CV."""
    por_estado = {e: 0 for e in ESTADOS}
    for v in datos["vacantes"]:
        por_estado[v.get("estado", "revisar")] = por_estado.get(v.get("estado", "revisar"), 0) + 1
    respondidas = ("respondieron", "entrevistando", "oferta", "rechazada")
    enviadas = [v for v in datos["vacantes"] if v.get("enviado")]

    def agrupar(clave):
        grupos = {}
        for v in enviadas:
            g = grupos.setdefault(v.get(clave) or "sin anotar", {"enviadas": 0, "respondieron": 0})
            g["enviadas"] += 1
            if v.get("estado") in respondidas:
                g["respondieron"] += 1
        return grupos

    return {"por_estado": por_estado, "enviadas": len(enviadas),
            "respondieron": sum(1 for v in enviadas if v.get("estado") in respondidas),
            "por_carril": agrupar("carril"), "por_cv": agrupar("cv")}


def semanas(datos, cuantas=8, hoy=None):
    """Cuántas se mandaron cada semana (de lunes a domingo), las últimas `cuantas`."""
    hoy = date.fromisoformat(hoy) if hoy else date.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    salida = [{"desde": (lunes - timedelta(weeks=n)).isoformat(), "enviadas": 0} for n in range(cuantas - 1, -1, -1)]
    for v in datos["vacantes"]:
        if not v.get("enviado"):
            continue
        d = date.fromisoformat(v["enviado"])
        n = (lunes - (d - timedelta(days=d.weekday()))).days // 7
        if 0 <= n < cuantas:
            salida[cuantas - 1 - n]["enviadas"] += 1
    return salida


# ─────────────────────────────── línea de comandos ───────────────────────────────

def pares(args):
    salida = {}
    for a in args:
        if "=" not in a:
            raise Error(f"Cada dato va como campo=valor. Esto no lo es: {a}")
        k, _, val = a.partition("=")
        salida[k] = val
    return salida


def imprimir_lista(vacantes):
    for v in vacantes:
        print(f"{v['id']:<7} {v.get('estado', ''):<13} {v.get('enviado') or '·':<10}  "
              f"{(v.get('carril') or '·'):<2} {v['empresa'][:18]:<18} {v['puesto']}")
    print(f"\n{len(vacantes)} vacante(s)")


def main(argv):
    cerebro = RAIZ / "mi-cerebro"
    if "--cerebro" in argv:
        i = argv.index("--cerebro")
        cerebro = (Path.cwd() / Path(argv[i + 1]).expanduser()).resolve()
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        sys.exit(__doc__)
    cmd, resto = argv[0], argv[1:]
    if cerebro == (RAIZ / "ejemplo").resolve() and cmd in ("alta", "cambiar"):
        sys.exit("El ejemplo no se modifica. Para jugar con él sin romperlo: python3 herramientas/tablero.py --cerebro ejemplo")
    datos = cargar(cerebro)
    try:
        if cmd == "lista":
            vs = [v for v in datos["vacantes"] if not resto or v.get("estado") == resto[0]]
            imprimir_lista(sorted(vs, key=lambda v: (v.get("cargada") or "", v["id"])))
        elif cmd == "ver" and resto:
            v = buscar(datos, resto[0])
            print(json.dumps(v, ensure_ascii=False, indent=1))
            for h in datos["historial"]:
                if h["id"] == v["id"]:
                    print(f"  {h['fecha']}  {h['campo']}: {h['antes']} → {h['despues']}")
        elif cmd == "alta":
            v = alta(datos, pares(resto))
            guardar(cerebro, datos)
            print(f"✅ Alta: {v['id']} · {v['empresa']} · {v['puesto']} · {v['estado']}")
        elif cmd == "cambiar" and resto:
            v, reales = cambiar(datos, resto[0], pares(resto[1:]))
            guardar(cerebro, datos)
            print(f"✅ {v['id']}: " + (", ".join(f"{k}={val}" for k, val in reales.items()) or "no había nada que cambiar"))
        elif cmd == "seguimiento":
            dias = int(resto[0]) if resto else 14
            vs = seguimiento(datos, dias)
            print(f"Postuladas sin respuesta hace {dias} días o más:\n")
            imprimir_lista(vs)
        elif cmd == "resumen":
            print(json.dumps(resumen(datos), ensure_ascii=False, indent=1))
        else:
            sys.exit(__doc__)
    except Error as e:
        sys.exit(f"⛔ {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
