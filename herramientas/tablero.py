#!/usr/bin/env python3
"""El tablero: tu búsqueda en una página, en tu computadora.

Muestra las vacantes por estado, lo nuevo que encontró el barrido, las postuladas que llevan
días sin respuesta y el experimento del paso 3: cuántas respondieron por carril y por CV. Desde
ahí se cambia el estado, se anotan las entrevistas y se agregan vacantes.

    python3 herramientas/tablero.py
    python3 herramientas/tablero.py --cerebro ejemplo      el de Toffy, para mirar y jugar
    python3 herramientas/tablero.py --puerto 8800 --sin-abrir

Los datos son los de mi-cerebro/vacantes.json y mi-cerebro/barrido/. El tablero no tiene otra
copia: lo que cambies ahí lo ven el barrido y el asistente, y al revés.

Solo escucha en 127.0.0.1, así que nadie más de tu red lo ve, y cada vez que arranca inventa una
clave que va en el link. Se cierra con Ctrl+C.

Con el ejemplo, los cambios quedan en memoria y se pierden al cerrar: sirve para probar.

Sin dependencias: solo Python 3.8 o más nuevo.
"""
import copy
import json
import secrets
import sys
import threading
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import barrido  # noqa: E402
import vacantes  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DIAS_SIN_RESPUESTA = 14
MAX_CUERPO = 200_000


class Tablero:
    """Lee y escribe los archivos de la persona. Con demo=True trabaja sobre una copia en memoria."""

    def __init__(self, cerebro, demo=False, hoy=None):
        self.cerebro = Path(cerebro)
        self.demo = demo
        self.lock = threading.Lock()
        self._hoy = hoy
        if demo:
            self._registro = vacantes.cargar(self.cerebro)
            self._hallazgos = barrido.cargar_hallazgos(self.cerebro)

    def hoy(self, registro):
        return self._hoy or registro.get("congelado_en") or date.today().isoformat()

    def leer(self):
        if self.demo:
            return copy.deepcopy(self._registro), copy.deepcopy(self._hallazgos)
        return vacantes.cargar(self.cerebro), barrido.cargar_hallazgos(self.cerebro)

    def escribir(self, registro, hallazgos):
        if self.demo:
            self._registro, self._hallazgos = registro, hallazgos
            return
        vacantes.guardar(self.cerebro, registro)
        barrido.guardar_hallazgos(self.cerebro, hallazgos)

    def datos(self):
        registro, hallazgos = self.leer()
        config, _ = barrido.cargar_config(self.cerebro)
        hoy = self.hoy(registro)
        carriles = sorted(set(config.get("titulos", {})) | {v["carril"] for v in registro["vacantes"] if v.get("carril")})
        cvs = sorted({p.stem for p in (self.cerebro / "cv").glob("*.md")} |
                     {v["cv"] for v in registro["vacantes"] if v.get("cv")})
        return {
            "modo": "demo" if self.demo else "real",
            "hoy": hoy,
            "vacantes": registro["vacantes"],
            "historial": registro["historial"],
            "resumen": vacantes.resumen(registro),
            "semanas": vacantes.semanas(registro, 8, hoy),
            "seguimiento": [v["id"] for v in vacantes.seguimiento(registro, DIAS_SIN_RESPUESTA, hoy)],
            "dias_sin_respuesta": DIAS_SIN_RESPUESTA,
            "hallazgos": [h for h in hallazgos["hallazgos"] if h["estado"] == "nuevo"],
            "ultima_corrida": (hallazgos["corridas"] or [None])[-1],
            "empresas_en_barrido": len(config.get("empresas", [])),
            "estados": list(vacantes.ESTADOS),
            "carriles": carriles,
            "cvs": cvs,
        }

    def accion(self, ruta, cuerpo):
        """Aplica un cambio sobre lo último que hay en disco, y devuelve los datos actualizados."""
        with self.lock:
            registro, hallazgos = self.leer()
            hoy = self.hoy(registro)
            if ruta == "/api/cambiar":
                _, reales = vacantes.cambiar(registro, str(cuerpo.get("id")), dict(cuerpo.get("cambios") or {}), hoy)
                mensaje = "Guardado" if reales else "No había nada que cambiar"
            elif ruta == "/api/alta":
                v = vacantes.alta(registro, dict(cuerpo.get("campos") or {}), hoy)
                mensaje = f"Agregada: {v['empresa']}"
            elif ruta == "/api/hallazgo":
                barrido.decidir(registro, hallazgos, str(cuerpo.get("id")), str(cuerpo.get("accion")),
                                {k: v for k, v in dict(cuerpo.get("extra") or {}).items() if v}, hoy)
                h = next(x for x in hallazgos["hallazgos"] if x["id"] == str(cuerpo.get("id")))
                mensaje = f"{h['empresa']}: " + ("quedó para revisar" if h["estado"] == "pasado" else "no vuelve a aparecer")
            else:
                raise vacantes.Error("No existe esa acción")
            self.escribir(registro, hallazgos)
        salida = self.datos()
        salida["mensaje"] = mensaje
        return salida


def hacer_handler(tablero, token, puerto):
    hosts = {f"127.0.0.1:{puerto}", f"localhost:{puerto}"}
    origenes = {f"http://{h}" for h in hosts}

    class Handler(BaseHTTPRequestHandler):
        server_version = "tablero"
        sys_version = ""

        def log_message(self, *args):
            pass

        def responder(self, codigo, cuerpo, tipo="application/json; charset=utf-8"):
            datos = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo, ensure_ascii=False).encode()
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(datos)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy",
                             "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
                             "connect-src 'self'; img-src data:; form-action 'none'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(datos)

        def permitido(self):
            """Tres chequeos: que venga a esta dirección (no a un nombre que apunte acá), que traiga
            la clave del link, y que si el navegador dice de qué página viene, sea esta."""
            if self.headers.get("Host") not in hosts:
                return False
            origen = self.headers.get("Origin")
            if origen and origen not in origenes:
                return False
            return secrets.compare_digest(self.headers.get("X-Tablero", ""), token)

        def do_GET(self):
            if self.headers.get("Host") not in hosts:
                return self.responder(403, {"error": "Dirección no permitida"})
            ruta = urlsplit(self.path).path
            if ruta in ("/", "/index.html"):
                return self.responder(200, PAGINA.encode(), "text/html; charset=utf-8")
            if ruta == "/api/datos":
                if not self.permitido():
                    return self.responder(403, {"error": "Falta la clave. Abre el link que imprimió la terminal."})
                try:
                    return self.responder(200, tablero.datos())
                except (ValueError, OSError) as e:
                    return self.responder(500, {"error": f"No se pudieron leer tus archivos: {e}"})
            return self.responder(404, {"error": "No existe"})

        def do_POST(self):
            if not self.permitido():
                return self.responder(403, {"error": "Falta la clave. Abre el link que imprimió la terminal."})
            if not (self.headers.get("Content-Type") or "").startswith("application/json"):
                return self.responder(415, {"error": "Tiene que ser JSON"})
            try:
                largo = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                largo = -1
            if not 0 < largo <= MAX_CUERPO:
                return self.responder(413, {"error": "Pedido vacío o demasiado grande"})
            try:
                cuerpo = json.loads(self.rfile.read(largo).decode("utf-8"))
                if not isinstance(cuerpo, dict):
                    raise ValueError("se esperaba un objeto")
                return self.responder(200, tablero.accion(urlsplit(self.path).path, cuerpo))
            except vacantes.Error as e:
                return self.responder(400, {"error": str(e)})
            except (ValueError, UnicodeDecodeError) as e:
                return self.responder(400, {"error": f"Pedido inválido: {e}"})

    return Handler


def arrancar(cerebro, puerto=8765, abrir=True, hoy=None):
    demo = cerebro == (RAIZ / "ejemplo").resolve()
    if not demo and not (cerebro / "vacantes.json").exists() and not (cerebro / "barrido" / "hallazgos.json").exists():
        print("Todavía no hay vacantes en " + str(cerebro) + ". El tablero arranca vacío: puedes agregar la primera desde ahí.\n")
    tablero = Tablero(cerebro, demo=demo, hoy=hoy)
    token = secrets.token_urlsafe(24)
    servidor = None
    for p in range(puerto, puerto + 20):
        try:
            servidor = ThreadingHTTPServer(("127.0.0.1", p), hacer_handler(tablero, token, p))
            break
        except OSError:
            continue
    if not servidor:
        sys.exit(f"⛔ No encontré un puerto libre entre {puerto} y {puerto + 19}. Prueba con --puerto 9000.")
    url = f"http://127.0.0.1:{servidor.server_address[1]}/#t={token}"
    print(("Tablero del ejemplo (los cambios no se guardan)" if demo else "Tablero de " + str(cerebro)))
    print(f"\n  {url}\n\nPara cerrarlo: Ctrl+C", flush=True)
    if abrir:
        webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrado.")
    finally:
        servidor.server_close()


def main(argv):
    cerebro, puerto, abrir, hoy = RAIZ / "mi-cerebro", 8765, "--sin-abrir" not in argv, None
    argv = [a for a in argv if a != "--sin-abrir"]
    while argv:
        opcion = argv.pop(0)
        if opcion in ("--cerebro", "--puerto", "--hoy") and argv:
            valor = argv.pop(0)
            if opcion == "--cerebro":
                cerebro = (Path.cwd() / Path(valor).expanduser()).resolve()
            elif opcion == "--puerto":
                puerto = int(valor)
            else:
                hoy = valor
        else:
            sys.exit(__doc__)
    arrancar(cerebro, puerto, abrir, hoy)


PAGINA = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tu búsqueda</title>
<style>
:root {
  --fondo: #f6f4ef; --papel: #ffffff; --tinta: #1f2328; --suave: #5f6670; --borde: #e3dfd6;
  --acento: #2f6f62; --acento-suave: #e3efeb; --alerta: #a4471e; --alerta-suave: #f8e7de;
  --oro: #8a6a12; --oro-suave: #f5ecd2; --gris-suave: #eeece7; --azul: #2f5b8a; --azul-suave: #e2ebf5;
  --sombra: 0 1px 2px rgba(0,0,0,.06);
}
@media (prefers-color-scheme: dark) {
  :root {
    --fondo: #16181b; --papel: #1f2226; --tinta: #e8e6e1; --suave: #a2a7ae; --borde: #33373d;
    --acento: #7cc4b2; --acento-suave: #1f3530; --alerta: #f0a07a; --alerta-suave: #3a261d;
    --oro: #e3c46e; --oro-suave: #37301b; --gris-suave: #2a2d31; --azul: #8fb6e0; --azul-suave: #1e2a38;
    --sombra: none;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--fondo); color: var(--tinta);
  font: 15px/1.45 ui-sans-serif, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
main { max-width: 1240px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 26px; margin: 0; letter-spacing: -.01em; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .08em; color: var(--suave); margin: 36px 0 12px; }
a { color: var(--azul); }
button, input, select, textarea { font: inherit; color: inherit; }
button { cursor: pointer; border: 1px solid var(--borde); background: var(--papel); border-radius: 8px; padding: 6px 12px; }
button:hover { border-color: var(--suave); }
button.primario { background: var(--acento); border-color: var(--acento); color: var(--papel); font-weight: 600; }
.cabeza { display: flex; flex-wrap: wrap; gap: 12px 24px; align-items: end; justify-content: space-between; }
.cabeza > .acciones { flex: 1 1 320px; max-width: 520px; justify-content: flex-end; }
.sub { color: var(--suave); margin-top: 4px; }
.acciones { display: flex; flex-wrap: wrap; gap: 8px; }
.aviso { border-radius: 10px; padding: 10px 14px; margin-top: 16px; }
.aviso.demo { background: var(--oro-suave); color: var(--oro); }
.aviso.mal { background: var(--alerta-suave); color: var(--alerta); }
.aviso.bien { background: var(--gris-suave); color: var(--suave); }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-top: 20px; }
.kpi { background: var(--papel); border: 1px solid var(--borde); border-radius: 12px; padding: 14px 16px; box-shadow: var(--sombra); }
.kpi .num { font-size: 30px; font-weight: 650; letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
.kpi .que { color: var(--suave); font-size: 13px; }
.kpi.tarde .num { color: var(--alerta); }
.hallazgos { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.hallazgo { background: var(--papel); border: 1px dashed var(--acento); border-radius: 12px; padding: 12px 14px; }
.hallazgo .acciones { margin-top: 10px; align-items: center; }
.hallazgo button { padding: 4px 10px; font-size: 14px; }
.filtro { flex: 1 1 240px; min-width: 0; padding: 8px 12px; border: 1px solid var(--borde); border-radius: 8px; background: var(--papel); }
.columnas { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 14px; align-items: start; }
.columna { background: var(--gris-suave); border-radius: 12px; padding: 10px; min-width: 0; }
.columna > summary, .columna > .titulo { list-style: none; font-weight: 650; padding: 4px 6px 10px; display: flex; justify-content: space-between; cursor: default; }
.columna > summary { cursor: pointer; }
.columna > summary::-webkit-details-marker { display: none; }
.cuenta { color: var(--suave); font-weight: 500; font-variant-numeric: tabular-nums; }
.tarjeta { display: block; width: 100%; text-align: left; background: var(--papel); border: 1px solid var(--borde); border-radius: 10px;
  padding: 10px 12px; margin-bottom: 8px; box-shadow: var(--sombra); }
.tarjeta:hover { border-color: var(--acento); }
.tarjeta .empresa { font-weight: 650; overflow-wrap: anywhere; }
.tarjeta .puesto { overflow-wrap: anywhere; }
.tarjeta .cuando { color: var(--suave); font-size: 13px; margin-top: 6px; }
.tarjeta.tarde { border-left: 4px solid var(--alerta); }
.tarjeta.tarde .cuando { color: var(--alerta); }
.chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
.chip { font-size: 12px; border-radius: 999px; padding: 1px 8px; background: var(--acento-suave); color: var(--acento); }
.chip.cv { background: var(--azul-suave); color: var(--azul); }
.chip.estado { background: var(--gris-suave); color: var(--suave); }
.vacia { color: var(--suave); font-size: 13px; padding: 4px 6px 8px; }
.dos { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.caja { background: var(--papel); border: 1px solid var(--borde); border-radius: 12px; padding: 14px 16px; box-shadow: var(--sombra); min-width: 0; }
.tabla { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--borde); }
th { color: var(--suave); font-weight: 500; font-size: 13px; }
td.n, th.n { text-align: right; }
.barra { height: 8px; background: var(--gris-suave); border-radius: 4px; min-width: 60px; }
.barra > div { height: 100%; background: var(--acento); border-radius: 4px; }
.nota { color: var(--suave); font-size: 13px; margin: 10px 0 0; }
svg { display: block; width: 100%; height: 190px; }
svg text { fill: var(--suave); font-size: 11px; }
svg .col { fill: var(--acento); }
dialog { border: 1px solid var(--borde); border-radius: 14px; padding: 0; width: min(560px, calc(100vw - 32px)); max-height: calc(100vh - 32px); overflow: auto; background: var(--papel); color: var(--tinta); }
dialog::backdrop { background: rgba(0,0,0,.35); }
dialog form { padding: 18px 20px; }
dialog h3 { margin: 0 0 4px; font-size: 18px; overflow-wrap: anywhere; }
.campos { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px 12px; margin-top: 14px; }
.campos label { display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: var(--suave); min-width: 0; }
.campos .ancho { grid-column: 1 / -1; }
.campos input, .campos select, .campos textarea { border: 1px solid var(--borde); border-radius: 8px; padding: 7px 9px; background: var(--fondo); color: var(--tinta); width: 100%; }
.campos textarea { min-height: 90px; resize: vertical; }
.pie-dialogo { display: flex; justify-content: space-between; gap: 8px; margin-top: 16px; flex-wrap: wrap; }
.historial { margin: 8px 0 0; padding: 0; list-style: none; font-size: 13px; color: var(--suave); }
details.hist { margin-top: 16px; font-size: 13px; color: var(--suave); }
details.hist summary { cursor: pointer; }
.historial li { padding: 3px 0; border-top: 1px solid var(--borde); overflow-wrap: anywhere; }
.toast { position: fixed; left: 50%; bottom: 20px; transform: translateX(-50%); background: var(--tinta); color: var(--fondo);
  padding: 8px 14px; border-radius: 8px; max-width: calc(100vw - 32px); }
.toast.error { background: var(--alerta); color: #fff; }
footer { color: var(--suave); font-size: 13px; margin-top: 40px; }
</style>
</head>
<body>
<main id="app"><p>Cargando…</p></main>
<div class="toast" id="toast" hidden></div>
<dialog id="dialogo"></dialog>
<script>
"use strict";
const TOKEN = new URLSearchParams(location.hash.slice(1)).get("t") || "";
const ETIQUETA = { revisar: "Por revisar", postulada: "Postulada", respondieron: "Respondieron", entrevistando: "Entrevistando",
  oferta: "Oferta", rechazada: "Rechazada", descartada: "Descartada" };
const COLUMNAS = [
  { titulo: "Por revisar", estados: ["revisar"] },
  { titulo: "Postuladas", estados: ["postulada"] },
  { titulo: "En conversación", estados: ["respondieron", "entrevistando"] },
  { titulo: "Ofertas", estados: ["oferta"] },
  { titulo: "Cerradas", estados: ["rechazada", "descartada"], plegada: true },
];
let D = null, filtro = "", firma = "";

function el(tag, attrs, ...hijos) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") e.className = v;
    else if (k === "text") e.textContent = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v === true ? "" : v);
  }
  for (const h of hijos.flat()) if (h !== null && h !== undefined && h !== false) e.append(h.nodeType ? h : document.createTextNode(String(h)));
  return e;
}
const svg = (tag, attrs) => { const e = document.createElementNS("http://www.w3.org/2000/svg", tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); return e; };
const enlaceSeguro = (url) => /^https?:\/\//i.test(url || "") ? url : null;

function dias(desde, hasta) {
  if (!desde) return null;
  const a = Date.UTC(...desde.split("-").map((x, i) => i === 1 ? x - 1 : +x));
  const b = Date.UTC(...hasta.split("-").map((x, i) => i === 1 ? x - 1 : +x));
  return Math.round((b - a) / 86400000);
}
const haceDias = (n) => n === 0 ? "hoy" : n === 1 ? "ayer" : `hace ${n} días`;
const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const fechaCorta = (f) => f ? `${+f.slice(8, 10)}-${MESES[+f.slice(5, 7) - 1]}` : "";

function aviso(texto, error) {
  const t = document.getElementById("toast");
  t.textContent = texto; t.className = "toast" + (error ? " error" : ""); t.hidden = false;
  clearTimeout(aviso.t); aviso.t = setTimeout(() => { t.hidden = true; }, error ? 6000 : 2500);
}

async function api(ruta, cuerpo) {
  const r = await fetch(ruta, { method: cuerpo ? "POST" : "GET", cache: "no-store",
    headers: Object.assign({ "X-Tablero": TOKEN }, cuerpo ? { "Content-Type": "application/json" } : {}),
    body: cuerpo ? JSON.stringify(cuerpo) : undefined });
  const datos = await r.json().catch(() => ({ error: "Respuesta rara del tablero" }));
  if (!r.ok) throw new Error(datos.error || "Algo falló");
  return datos;
}

async function cargar() {
  if (!TOKEN) {
    document.getElementById("app").replaceChildren(el("h1", { text: "Falta la clave" }),
      el("p", { text: "Abre el link completo que imprimió la terminal, el que termina en #t=…" }));
    return;
  }
  try {
    const nuevo = await api("/api/datos"), f = JSON.stringify(nuevo);
    if (f === firma) return;  // sin cambios no se redibuja: un clic en curso no se pierde
    firma = f; D = nuevo; pintar();
  }
  catch (e) { aviso(e.message, true); }
}

async function hacer(ruta, cuerpo) {
  try { D = await api(ruta, cuerpo); firma = ""; pintar(); aviso(D.mensaje || "Listo"); return true; }
  catch (e) { aviso(e.message, true); return false; }
}

function ultimoCambioDeEstado(id) {
  let f = null;
  for (const h of D.historial) if (h.id === id && (h.campo === "estado" || h.campo === "alta")) f = h.fecha;
  return f;
}

function pintar() {
  const r = D.resumen, app = document.getElementById("app");
  const enConversacion = (r.por_estado.respondieron || 0) + (r.por_estado.entrevistando || 0);
  const tasa = r.enviadas ? Math.round(100 * r.respondieron / r.enviadas) : 0;
  const estaSemana = D.semanas.length ? D.semanas[D.semanas.length - 1].enviadas : 0;

  const cabeza = el("div", { class: "cabeza" },
    el("div", {}, el("h1", { text: "Tu búsqueda" }), el("div", { class: "sub", text: `Al ${fechaCorta(D.hoy)} · ${D.vacantes.length} vacantes en el registro` })),
    el("div", { class: "acciones" },
      el("input", { class: "filtro", type: "search", placeholder: "Buscar empresa, puesto o nota", value: filtro,
        oninput: (e) => { filtro = e.target.value; pintarColumnas(); } }),
      el("button", { class: "primario", onclick: () => abrirAlta(), text: "Agregar vacante" })));

  const avisos = [];
  if (D.modo === "demo") avisos.push(el("div", { class: "aviso demo", text: "Es el ejemplo de Toffy. Puedes mover todo: los cambios no se guardan y se pierden al cerrar." }));
  const c = D.ultima_corrida;
  if (D.empresas_en_barrido && !c) avisos.push(el("div", { class: "aviso mal", text: "El barrido tiene empresas pero nunca corrió. Pruébalo con: python3 herramientas/barrido.py" }));
  if (c) {
    const d = dias(c.fecha.slice(0, 10), D.hoy);
    if (c.miradas === 0) avisos.push(el("div", { class: "aviso mal", text: `El último barrido (${fechaCorta(c.fecha)}) no pudo mirar ningún board. No quiere decir que no haya nada.` }));
    else if (d >= 3) avisos.push(el("div", { class: "aviso mal", text: `El barrido no corre desde hace ${d} días. Si lo programaste, revisa que siga activo.` }));
    else avisos.push(el("div", { class: "aviso bien", text: `Último barrido ${haceDias(d)}: miró ${c.miradas} de ${c.empresas} empresas${c.fallos.length ? `, fallaron ${c.fallos.length}` : ""}.` }));
  }

  const kpi = (num, que, extra) => el("div", { class: "kpi" + (extra || "") }, el("div", { class: "num", text: num }), el("div", { class: "que", text: que }));
  const kpis = el("div", { class: "kpis" },
    kpi(r.enviadas, "postulaciones enviadas"),
    kpi(r.enviadas ? `${r.respondieron} de ${r.enviadas}` : "·", `respondieron${r.enviadas ? ` (${tasa}%)` : ""}`),
    kpi(enConversacion + (r.por_estado.oferta || 0), "en conversación u oferta"),
    kpi(D.seguimiento.length, `sin respuesta hace ${D.dias_sin_respuesta} días o más`, D.seguimiento.length ? " tarde" : ""),
    kpi(estaSemana, "enviadas esta semana"));

  const bloques = [cabeza, ...avisos, kpis];

  if (D.hallazgos.length) {
    bloques.push(el("h2", { text: `Nuevas del barrido (${D.hallazgos.length})` }));
    bloques.push(el("div", { class: "hallazgos" }, D.hallazgos.map((h) => el("div", { class: "hallazgo" },
      el("div", { class: "empresa" }, el("strong", { text: h.empresa })),
      el("div", { text: h.puesto }),
      el("div", { class: "sub", text: `${h.ubicacion || "sin ubicación"} · encontrada ${fechaCorta(h.encontrado)}` }),
      el("div", { class: "chips" }, h.carriles.map((x) => el("span", { class: "chip", text: `carril ${x}` }))),
      el("div", { class: "acciones" },
        el("button", { onclick: () => hacer("/api/hallazgo", { id: h.id, accion: "pasar" }), text: "A revisar" }),
        el("button", { onclick: () => hacer("/api/hallazgo", { id: h.id, accion: "ignorar" }), text: "No me interesa" }),
        enlaceSeguro(h.url) ? el("a", { href: h.url, target: "_blank", rel: "noopener noreferrer", text: "Ver aviso" }) : null)))));
    bloques.push(el("p", { class: "nota", text: "Pasarla a revisar no es postular: primero va el veredicto, leyendo el aviso completo en la página de la empresa." }));
  }

  bloques.push(el("h2", { text: "Las vacantes" }), el("div", { class: "columnas", id: "columnas" }));
  bloques.push(el("div", { class: "dos" }, experimento(), ritmo()));
  bloques.push(el("footer", { text: D.modo === "demo" ? "Datos del ejemplo: ejemplo/vacantes.json." : "Los datos viven en mi-cerebro/vacantes.json. Este tablero corre solo en tu computadora." }));
  app.replaceChildren(...bloques);
  pintarColumnas();
}

function pintarColumnas() {
  const cont = document.getElementById("columnas");
  if (!cont) return;
  const q = filtro.trim().toLowerCase();
  const pasa = (v) => !q || [v.empresa, v.puesto, v.notas, v.cv, v.carril].some((x) => (x || "").toLowerCase().includes(q));
  const tarde = new Set(D.seguimiento);
  cont.replaceChildren(...COLUMNAS.map((col) => {
    let vs = D.vacantes.filter((v) => col.estados.includes(v.estado) && pasa(v));
    if (col.estados[0] === "postulada") vs.sort((a, b) => (a.enviado || "").localeCompare(b.enviado || ""));
    else vs.sort((a, b) => (ultimoCambioDeEstado(b.id) || "").localeCompare(ultimoCambioDeEstado(a.id) || ""));
    const tarjetas = vs.length ? vs.map((v) => tarjeta(v, tarde.has(v.id), col.estados.length > 1)) : [el("div", { class: "vacia", text: q ? "Nada con ese filtro" : "Nada por ahora" })];
    const titulo = [el("span", { text: col.titulo }), el("span", { class: "cuenta", text: vs.length })];
    if (col.plegada) return el("details", { class: "columna", open: !!q }, el("summary", {}, titulo), tarjetas);
    return el("section", { class: "columna" }, el("div", { class: "titulo" }, titulo), tarjetas);
  }));
}

function tarjeta(v, esTarde, mostrarEstado) {
  let cuando;
  if (v.estado === "revisar") cuando = `Cargada ${haceDias(dias(v.cargada, D.hoy))}`;
  else if (v.estado === "postulada") cuando = v.enviado ? `Enviada ${haceDias(dias(v.enviado, D.hoy))}${esTarde ? ", sin respuesta" : ""}` : "Sin fecha de envío";
  else {
    const f = ultimoCambioDeEstado(v.id);
    cuando = `${ETIQUETA[v.estado]} ${f ? haceDias(dias(f, D.hoy)) : ""}${v.entrevistas ? ` · ${v.entrevistas} entrevista${v.entrevistas > 1 ? "s" : ""}` : ""}`;
  }
  return el("button", { class: "tarjeta" + (esTarde ? " tarde" : ""), onclick: () => abrirDetalle(v.id) },
    el("div", { class: "empresa", text: v.empresa }),
    el("div", { class: "puesto", text: v.puesto }),
    el("div", { class: "chips" },
      mostrarEstado ? el("span", { class: "chip estado", text: ETIQUETA[v.estado] }) : null,
      v.carril ? el("span", { class: "chip", text: `carril ${v.carril}` }) : null,
      v.cv ? el("span", { class: "chip cv", text: v.cv }) : null),
    el("div", { class: "cuando", text: cuando }));
}

function experimento() {
  const r = D.resumen;
  const tabla = (titulo, grupos) => {
    const filas = Object.entries(grupos).sort((a, b) => a[0].localeCompare(b[0]));
    if (!filas.length) return el("p", { class: "nota", text: `Todavía no hay postulaciones enviadas con ${titulo.toLowerCase()}.` });
    return el("div", { class: "tabla" }, el("table", {},
      el("thead", {}, el("tr", {}, el("th", { text: titulo }), el("th", { class: "n", text: "Enviadas" }), el("th", { class: "n", text: "Respondieron" }), el("th", { text: "" }))),
      el("tbody", {}, filas.map(([k, g]) => el("tr", {},
        el("td", { text: k }), el("td", { class: "n", text: g.enviadas }), el("td", { class: "n", text: g.respondieron }),
        el("td", {}, el("div", { class: "barra", title: `${Math.round(100 * g.respondieron / g.enviadas)}%` },
          el("div", { style: `width:${Math.round(100 * g.respondieron / g.enviadas)}%` }))))))));
  };
  const chica = Object.values(r.por_carril).some((g) => g.enviadas < 10);
  return el("div", { class: "caja" },
    el("h2", { text: "El experimento", style: "margin-top:0" }),
    tabla("Carril", r.por_carril), el("div", { style: "height:10px" }), tabla("CV", r.por_cv),
    chica ? el("p", { class: "nota", text: "Con menos de 10 enviadas por grupo, la diferencia entre carriles todavía puede ser azar. Anótalo con la muestra antes de sacar conclusiones." }) : null);
}

function ritmo() {
  const s = D.semanas, max = Math.max(1, ...s.map((x) => x.enviadas));
  const ancho = 320, alto = 150, base = 120, paso = ancho / s.length;
  const g = svg("svg", { viewBox: `0 0 ${ancho} ${alto}`, role: "img", "aria-label": "Postulaciones enviadas por semana" });
  s.forEach((x, i) => {
    const h = Math.round(90 * x.enviadas / max);
    g.append(svg("rect", { class: "col", x: i * paso + 6, y: base - h, width: paso - 12, height: Math.max(h, 1), rx: 3 }));
    const n = svg("text", { x: i * paso + paso / 2, y: base - h - 5, "text-anchor": "middle" }); n.textContent = x.enviadas || ""; g.append(n);
    const t = svg("text", { x: i * paso + paso / 2, y: base + 16, "text-anchor": "middle" }); t.textContent = fechaCorta(x.desde); g.append(t);
  });
  return el("div", { class: "caja" }, el("h2", { text: "Enviadas por semana", style: "margin-top:0" }), g,
    el("p", { class: "nota", text: "Cada barra es una semana, de lunes a domingo. Lo que sirve mirar es si el ritmo se sostiene, no el número de una semana." }));
}

function campo(etiqueta, control, ancho) { return el("label", { class: ancho ? "ancho" : null }, etiqueta, control); }
function lista(id, opciones) { return el("datalist", { id }, opciones.map((o) => el("option", { value: o }))); }

function lineaHistorial(h) {
  const f = fechaCorta(h.fecha);
  if (h.campo === "alta") return `${f} · entró al registro como ${ETIQUETA[h.despues] || h.despues}`;
  if (h.campo === "notas") return `${f} · cambiaron las notas`;
  if (h.campo === "estado") return `${f} · ${ETIQUETA[h.antes] || h.antes} → ${ETIQUETA[h.despues] || h.despues}`;
  return `${f} · ${h.campo}: ${h.antes ?? "vacío"} → ${h.despues ?? "vacío"}`;
}

function abrirDetalle(id) {
  const v = D.vacantes.find((x) => x.id === id);
  if (!v) return;
  const historial = D.historial.filter((h) => h.id === id).reverse();
  const dlg = document.getElementById("dialogo");
  const estado = el("select", { name: "estado" }, D.estados.map((e) => el("option", { value: e, selected: e === v.estado, text: ETIQUETA[e] })));
  const form = el("form", { method: "dialog" },
    el("h3", { text: v.empresa }), el("div", { class: "sub", text: v.puesto }),
    enlaceSeguro(v.url) ? el("div", { style: "margin-top:6px" }, el("a", { href: v.url, target: "_blank", rel: "noopener noreferrer", text: "Ver aviso" })) : null,
    el("div", { class: "campos" },
      campo("Estado", estado),
      campo("Enviada el", el("input", { type: "date", name: "enviado", value: v.enviado || "" })),
      campo("Entrevistas", el("input", { type: "number", min: "0", name: "entrevistas", value: v.entrevistas || 0 })),
      campo("Carril", el("input", { name: "carril", list: "l-carriles", value: v.carril || "" })),
      campo("CV que mandaste", el("input", { name: "cv", list: "l-cvs", value: v.cv || "" }), true),
      campo("Link del aviso", el("input", { type: "url", name: "url", value: v.url || "" }), true),
      campo("Notas", el("textarea", { name: "notas", text: v.notas || "" }), true)),
    lista("l-carriles", D.carriles), lista("l-cvs", D.cvs),
    el("div", { class: "pie-dialogo" },
      el("button", { value: "cancelar", formnovalidate: true, text: "Cerrar" }),
      el("button", { class: "primario", value: "guardar", text: "Guardar" })),
    el("details", { class: "hist" }, el("summary", { text: "Historial" }),
      el("ul", { class: "historial" }, historial.map((h) => el("li", { text: lineaHistorial(h) })))));
  form.addEventListener("submit", async (e) => {
    if (e.submitter && e.submitter.value !== "guardar") return;
    e.preventDefault();
    const datos = new FormData(form), cambios = {};
    for (const k of ["estado", "enviado", "entrevistas", "carril", "cv", "url", "notas"]) {
      const nuevo = (datos.get(k) || "").toString();
      const viejo = v[k] === null || v[k] === undefined ? "" : String(v[k]);
      if (nuevo !== viejo) cambios[k] = nuevo;
    }
    if (!Object.keys(cambios).length) { dlg.close(); return; }
    if (await hacer("/api/cambiar", { id, cambios })) dlg.close();
  });
  dlg.replaceChildren(form);
  dlg.showModal();
}

function abrirAlta() {
  const dlg = document.getElementById("dialogo");
  const form = el("form", { method: "dialog" },
    el("h3", { text: "Agregar vacante" }),
    el("div", { class: "sub", text: "Queda para revisar. Pasa a postulada cuando la mandes." }),
    el("div", { class: "campos" },
      campo("Empresa", el("input", { name: "empresa", required: true })),
      campo("Puesto", el("input", { name: "puesto", required: true })),
      campo("Link del aviso", el("input", { type: "url", name: "url" }), true),
      campo("Carril", el("input", { name: "carril", list: "l-carriles" })),
      campo("Estado", el("select", { name: "estado" }, D.estados.map((e) => el("option", { value: e, text: ETIQUETA[e] })))),
      campo("CV", el("input", { name: "cv", list: "l-cvs" }), true),
      campo("Notas", el("textarea", { name: "notas" }), true)),
    lista("l-carriles", D.carriles), lista("l-cvs", D.cvs),
    el("div", { class: "pie-dialogo" },
      el("button", { value: "cancelar", formnovalidate: true, text: "Cancelar" }),
      el("button", { class: "primario", value: "guardar", text: "Agregar" })));
  form.addEventListener("submit", async (e) => {
    if (e.submitter && e.submitter.value !== "guardar") return;
    e.preventDefault();
    const campos = {};
    for (const [k, val] of new FormData(form).entries()) if (String(val).trim()) campos[k] = String(val).trim();
    if (await hacer("/api/alta", { campos })) dlg.close();
  });
  dlg.replaceChildren(form);
  dlg.showModal();
}

const ocupado = () => document.getElementById("dialogo").open || (document.activeElement && document.activeElement.classList.contains("filtro"));
window.addEventListener("focus", () => { if (!ocupado()) cargar(); });
setInterval(() => { if (!document.hidden && !ocupado()) cargar(); }, 60000);
cargar();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main(sys.argv[1:])
