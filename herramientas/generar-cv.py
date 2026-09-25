#!/usr/bin/env python3
"""Convierte un CV en markdown a PDF y DOCX de una columna, que los ATS leen bien.

Uso:
    python3 herramientas/generar-cv.py mi-cerebro/cv/cv-producto.md [más archivos...]

Deja los archivos en una carpeta build/ al lado del markdown.

Antes de generar pasa el texto por chequear.py: si encuentra un número retirado, un dato marcado
[SIN FUENTE] o una raya larga, no genera ninguno. Si uno de los CV está mal, no sale ninguno.

Formato del markdown (ver plantillas/04-cv.md):
    # Nombre Apellido
    Título que buscas
    Ciudad · correo · teléfono · linkedin

    ## Resumen
    Un párrafo.

    ## Experiencia
    ### Empresa · Puesto
    ene-2022 → hoy · Ciudad
    Una línea de contexto de la empresa (opcional).
    - Viñeta con un número o una decisión.

Los comentarios HTML se ignoran, y todo lo que venga después de <!-- notas --> también.

Necesita Chrome, Chromium, Edge o Brave para el PDF. Para el DOCX usa pandoc si está instalado,
y si no textutil (viene con macOS). Si no hay ninguno, genera solo el PDF y avisa.
"""
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from chequear import buscar_lista, frenar  # noqa: E402

CSS = """@page{size:A4;margin:12mm 14mm}
*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;font-size:10pt;line-height:1.25;color:#000;margin:0}
h1{font-size:17pt;margin:0 0 2pt}
.rol{font-size:11pt;margin:0 0 4pt}
.contacto{font-size:9pt;line-height:1.4;margin:0 0 8pt}
h2{font-size:11pt;margin:9pt 0 3pt;padding-bottom:2pt;border-bottom:1px solid #000;
   text-transform:uppercase;letter-spacing:.5pt}
h3{font-size:10.5pt;margin:6pt 0 1pt}
.meta{font-size:9pt;margin:0 0 2pt}
p{margin:0 0 4pt}
ul{margin:0 0 4pt;padding-left:13pt}
li{margin:0 0 1.5pt}
.puesto{break-inside:avoid;page-break-inside:avoid}"""

NAVEGADORES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def navegador():
    for n in NAVEGADORES:
        if n and (pathlib.Path(n).exists() or shutil.which(n)):
            return n
    return None


def en_linea(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\*(.+?)\*", r"\1", t)


def limpiar_md(md):
    md = md.split("<!-- notas -->")[0]
    # Los comentarios se vacían dejando sus saltos de línea, así los avisos dan la línea real.
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), md, flags=re.S)


def a_html(md, titulo):
    lineas = limpiar_md(md).splitlines()
    cuerpo, parrafo, vinetas = [], [], []
    en_puesto = False
    esperando = None  # "encabezado" después del h1, "meta" después de un h3

    def cerrar_bloques():
        nonlocal parrafo, vinetas
        if vinetas:
            cuerpo.append("<ul>" + "".join(f"<li>{en_linea(v)}</li>" for v in vinetas) + "</ul>")
            vinetas = []
        if parrafo:
            cuerpo.append(f"<p>{en_linea(' '.join(parrafo))}</p>")
            parrafo = []

    encabezado = []
    for ln in lineas:
        s = ln.strip()
        if esperando == "encabezado":
            if s:
                encabezado.append(s)
                continue
            rol, *contacto = encabezado or [""]
            cuerpo.append(f"<p class='rol'>{en_linea(rol)}</p>")
            if contacto:
                cuerpo.append("<p class='contacto'>" + "<br>".join(en_linea(c) for c in contacto) + "</p>")
            esperando = None
            continue
        if s.startswith("# "):
            cuerpo.append(f"<h1>{en_linea(s[2:])}</h1>")
            esperando = "encabezado"
        elif s.startswith("## "):
            cerrar_bloques()
            if en_puesto:
                cuerpo.append("</div>")
                en_puesto = False
            cuerpo.append(f"<h2>{en_linea(s[3:])}</h2>")
        elif s.startswith("### "):
            cerrar_bloques()
            if en_puesto:
                cuerpo.append("</div>")
            cuerpo.append(f"<div class='puesto'><h3>{en_linea(s[4:])}</h3>")
            en_puesto, esperando = True, "meta"
        elif s.startswith("- "):
            if parrafo:
                cuerpo.append(f"<p>{en_linea(' '.join(parrafo))}</p>")
                parrafo = []
            vinetas.append(s[2:])
            esperando = None
        elif s and ln.startswith("  ") and vinetas:
            vinetas[-1] += " " + s
        elif s:
            if esperando == "meta":
                cuerpo.append(f"<p class='meta'>{en_linea(s)}</p>")
                esperando = None
            else:
                # Una línea que arranca en negrita (**Datos:** ...) es su propio renglón.
                if s.startswith("**") and parrafo:
                    cuerpo.append(f"<p>{en_linea(' '.join(parrafo))}</p>")
                    parrafo = []
                parrafo.append(s)
        else:
            cerrar_bloques()
    if esperando == "encabezado" and encabezado:
        rol, *contacto = encabezado
        cuerpo.append(f"<p class='rol'>{en_linea(rol)}</p>")
        if contacto:
            cuerpo.append("<p class='contacto'>" + "<br>".join(en_linea(c) for c in contacto) + "</p>")
    cerrar_bloques()
    if en_puesto:
        cuerpo.append("</div>")
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f"<title>{html.escape(titulo)}</title><style>{CSS}</style></head><body>"
            + "\n".join(cuerpo) + "</body></html>")


def contar_paginas(pdf):
    datos = pdf.read_bytes()
    return len(re.findall(rb"/Type\s*/Page[^s]", datos)) or "?"


def main(archivos):
    if not archivos:
        sys.exit(__doc__)
    rutas = [pathlib.Path(a) for a in archivos]
    for r in rutas:
        if not r.exists():
            sys.exit(f"⛔ No existe: {r}")

    # Primero se revisan todos. Si uno tiene algo mal, no sale ninguno.
    for r in rutas:
        crudo = r.read_text(encoding="utf-8")
        frenar(limpiar_md(crudo), r.name, buscar_lista(r), cv=crudo)

    chrome = navegador()
    if not chrome:
        sys.exit("⛔ No encontré Chrome, Chromium, Edge ni Brave. Instala uno, o pásale la ruta: "
                 "CHROME=/ruta/al/navegador python3 herramientas/generar-cv.py ...")

    for r in rutas:
        salida = r.parent / "build"
        salida.mkdir(exist_ok=True)
        base = salida / r.stem
        h = base.with_suffix(".html")
        h.write_text(a_html(r.read_text(encoding="utf-8"), r.stem), encoding="utf-8")

        pdf = base.with_suffix(".pdf")
        pdf.unlink(missing_ok=True)
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", h.resolve().as_uri()], capture_output=True)
        if not pdf.exists():
            sys.exit(f"⛔ El navegador no generó {pdf.name}. Prueba abrir {h} y guardarlo como PDF.")

        docx = base.with_suffix(".docx")
        if shutil.which("pandoc"):
            res = subprocess.run(["pandoc", str(h), "-o", str(docx)], capture_output=True, text=True)
        elif shutil.which("textutil"):
            res = subprocess.run(["textutil", "-convert", "docx", str(h), "-output", str(docx)],
                                 capture_output=True, text=True)
        else:
            res = None
        docx_ok = res is not None and res.returncode == 0
        nota = "+ docx" if docx_ok else "(sin docx: instala pandoc si te lo piden en Word)"
        print(f"  ✅ {r.name}: {contar_paginas(pdf)} página(s) {nota} → {salida}")


if __name__ == "__main__":
    main(sys.argv[1:])
