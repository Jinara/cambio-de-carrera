#!/usr/bin/env python3
"""Revisa un texto antes de que salga hacia afuera.

Busca tres cosas:
  1. Números retirados, los que anotaste en numeros-retirados.txt porque resultaron mal.
  2. Marcas de dato sin verificar: [SIN FUENTE], [POR CONFIRMAR], [DATO], [PREGUNTAR].
  3. Raya larga (— o –) usada como puntuación.

Uso:
    python3 herramientas/chequear.py mi-cerebro/cv/cv-producto.md
    pbpaste | python3 herramientas/chequear.py -

La lista de retirados se busca sola: primero al lado del archivo y después subiendo carpetas
(así encuentra mi-cerebro/numeros-retirados.txt o ejemplo/numeros-retirados.txt). Si no existe,
ese chequeo se saltea.

Sale con código 1 si encuentra algo, así otros scripts lo usan de freno.
"""
import pathlib
import re
import sys

NOMBRE_LISTA = "numeros-retirados.txt"
MARCAS = re.compile(r"\[(SIN FUENTE|POR CONFIRMAR|POR VERIFICAR|DATO|PREGUNTAR)[^\]]*\]")
RAYA = re.compile(r"[—–]")


def buscar_lista(desde):
    carpeta = pathlib.Path(desde).resolve()
    carpeta = carpeta if carpeta.is_dir() else carpeta.parent
    for c in [carpeta, *carpeta.parents]:
        candidata = c / NOMBRE_LISTA
        if candidata.exists():
            return candidata
        candidata = c / "mi-cerebro" / NOMBRE_LISTA
        if candidata.exists():
            return candidata
    return None


def reglas(lista):
    if not lista:
        return []
    salida = []
    for ln in lista.read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            patron, _, correccion = ln.partition("\t")
            salida.append((re.compile(patron.strip(), re.I), correccion.strip()))
    return salida


def buscar(texto, lista=None):
    """Devuelve [(línea, qué se encontró, qué hacer)]."""
    hallazgos = []
    retirados = reglas(lista)
    for n, ln in enumerate(texto.splitlines(), 1):
        for patron, correccion in retirados:
            m = patron.search(ln)
            if m:
                hallazgos.append((n, m.group(0), f"número retirado. {correccion}"))
        for m in MARCAS.finditer(ln):
            hallazgos.append((n, m.group(0), "dato sin verificar, no puede salir"))
        if RAYA.search(ln):
            hallazgos.append((n, ln.strip()[:60], "raya larga: coma, punto, dos puntos o paréntesis"))
    return hallazgos


def frenar(texto, origen, lista=None):
    """Para los generadores: si hay algo, lo muestra y corta sin generar nada."""
    hallazgos = buscar(texto, lista)
    if hallazgos:
        print(f"⛔ {origen} no puede salir todavía:")
        for n, visto, que_hacer in hallazgos:
            print(f"   línea {n}: «{visto}» → {que_hacer}")
        sys.exit(1)


if __name__ == "__main__":
    total = 0
    for arg in sys.argv[1:] or ["-"]:
        if arg == "-":
            texto, lista = sys.stdin.read(), buscar_lista(pathlib.Path.cwd())
        else:
            texto, lista = pathlib.Path(arg).read_text(encoding="utf-8"), buscar_lista(arg)
        for n, visto, que_hacer in buscar(texto, lista):
            print(f"{arg}:{n}: «{visto}» → {que_hacer}")
            total += 1
    print("✅ Listo para salir." if not total else f"⛔ {total} cosas para arreglar.")
    sys.exit(1 if total else 0)
