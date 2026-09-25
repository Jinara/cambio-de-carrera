#!/usr/bin/env python3
"""Revisa un texto antes de que salga hacia afuera.

Busca tres cosas en cualquier texto:
  1. Números retirados, los que anotaste en numeros-retirados.txt porque resultaron mal.
  2. Marcas de dato sin verificar: [SIN FUENTE], [POR CONFIRMAR], [DATO], [PREGUNTAR].
  3. Raya larga (— o –) usada como puntuación.

Y con --cv revisa además lo que hace que un CV no suene a nadie:
  4. Viñetas de experiencia que empiezan nombrando el puesto en vez de lo que hiciste
     ("Orientación en la elaboración de proyectos" en vez de "Orienté a 14 tesistas").
  5. Viñetas que empiezan con un verbo que no dice nada (apoyé, participé, colaboré).
  6. Bloques de experiencia que quedaron sin ninguna viñeta.
  7. Un CV entero sin un solo número.

Uso:
    python3 herramientas/chequear.py mi-cerebro/cv/cv-producto.md
    python3 herramientas/chequear.py --cv mi-cerebro/cv/cv-producto.md
    pbpaste | python3 herramientas/chequear.py -

La lista de retirados se busca sola: primero al lado del archivo y después subiendo carpetas
(así encuentra mi-cerebro/numeros-retirados.txt o ejemplo/numeros-retirados.txt). Si no existe,
ese chequeo se saltea.

Si una línea de verdad tiene que salir así, se le pone `<!-- voz-ok -->` al final y se salta
el chequeo 4 y 5 de esa línea sola. Es para los casos raros, no para silenciar el freno.

Sale con código 1 si encuentra algo, así otros scripts lo usan de freno.
"""
import pathlib
import re
import sys

NOMBRE_LISTA = "numeros-retirados.txt"
MARCAS = re.compile(r"\[(SIN FUENTE|POR CONFIRMAR|POR VERIFICAR|DATO|PREGUNTAR)[^\]]*\]")
RAYA = re.compile(r"[—–]")

# --- el chequeo de CV ---------------------------------------------------------------

VINETA = re.compile(r"^\s*[-*•]\s+(.*)$")
TITULO2 = re.compile(r"^\s*##\s+(.*)$")
TITULO3 = re.compile(r"^\s*###\s+(.*)$")
ESCAPE = re.compile(r"<!--\s*voz-ok.*?-->", re.I)
NOTAS = re.compile(r"^\s*<!--\s*notas\s*-->", re.I)

# Un sustantivo que nombra la función del puesto. Ningún verbo en primera persona
# termina así, por eso se puede bloquear sin miedo a confundirlo con uno.
SUFIJOS_NOMINALES = (
    "ción", "ciones", "sión", "siones", "miento", "mientos", "aje", "ajes",
    "encia", "encias", "ancia", "ancias", "anza", "anzas", "azgo", "azgos",
    "ado", "ados", "ada", "adas", "ido", "idos", "ida", "idas", "ura", "uras",
)

# Las que no llevan sufijo delator y hay que nombrar a mano.
NOMINALES_FIJAS = {
    "apoyo", "ayuda", "soporte", "manejo", "uso", "control", "registro",
    "análisis", "analisis", "asistencia", "seguimiento", "cargo", "labores",
    "tareas", "funciones", "responsable", "encargado", "encargada", "miembro",
    "parte", "participante", "colaborador", "colaboradora",
}

# Verbos que sí son verbos, pero que no dicen qué decidiste. Los nombra AGENTS.md.
VERBOS_FLOJOS = {
    "apoyé", "apoye", "participé", "participe", "colaboré", "colabore",
    "asistí", "asisti", "ayudé", "ayude", "acompañé", "acompane",
}


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


def primera_palabra(texto):
    """La primera palabra de una viñeta, sin negritas, comillas ni puntuación."""
    limpio = re.sub(r"[*_`\"'«»(\[]", "", texto).strip()
    m = re.match(r"([A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)", limpio)
    return m.group(1) if m else ""


def nombra_el_puesto(palabra):
    """True si la palabra nombra la función del cargo en vez de lo que hizo la persona."""
    p = palabra.lower()
    if not p:
        return False
    if p in NOMINALES_FIJAS:
        return True
    # Un verbo en primera persona del pretérito termina en é o í. Nunca en un sufijo nominal.
    if p.endswith(("é", "í")):
        return False
    return p.endswith(SUFIJOS_NOMINALES)


def revisar_cv(texto):
    """Lo que hace que un CV no suene a nadie. Solo mira la sección de experiencia."""
    hallazgos = []
    en_experiencia = False
    bloque = None
    linea_bloque = 0
    vinetas_del_bloque = 0
    vinetas_totales = 0
    vinetas_con_numero = 0

    def cerrar_bloque():
        if bloque and vinetas_del_bloque == 0:
            hallazgos.append((linea_bloque, bloque[:60],
                              "bloque de experiencia sin ninguna viñeta: ponle dos líneas o fusiónalo"))

    for n, ln in enumerate(texto.splitlines(), 1):
        if NOTAS.match(ln):
            break
        m2 = TITULO2.match(ln)
        if m2:
            cerrar_bloque()
            bloque, vinetas_del_bloque = None, 0
            en_experiencia = "experiencia" in m2.group(1).lower()
            continue
        if not en_experiencia:
            continue
        m3 = TITULO3.match(ln)
        if m3:
            cerrar_bloque()
            bloque, linea_bloque, vinetas_del_bloque = m3.group(1).strip(), n, 0
            continue
        mv = VINETA.match(ln)
        if not mv:
            continue
        vinetas_del_bloque += 1
        vinetas_totales += 1
        cuerpo = mv.group(1).strip()
        if re.search(r"\d", cuerpo):
            vinetas_con_numero += 1
        if ESCAPE.search(cuerpo):
            continue
        palabra = primera_palabra(cuerpo)
        if not palabra:
            continue
        if palabra.lower() in VERBOS_FLOJOS:
            hallazgos.append((n, cuerpo[:60],
                              f"«{palabra}» no dice qué decidiste. Mira la lista de verbos de AGENTS.md"))
        elif nombra_el_puesto(palabra):
            hallazgos.append((n, cuerpo[:60],
                              f"empieza con «{palabra}», que nombra el puesto y lo firmaría "
                              "cualquiera que lo haya ocupado. Empieza por lo que hiciste tú"))

    cerrar_bloque()

    if vinetas_totales and not vinetas_con_numero:
        hallazgos.append((0, "toda la experiencia",
                          "ninguna viñeta tiene un número. No tienen que ser grandes, tienen que ser tuyos"))
    return sorted(hallazgos, key=lambda h: h[0])


def frenar(texto, origen, lista=None, cv=None):
    """Para los generadores: si hay algo, lo muestra y corta sin generar nada.

    `cv` es el markdown crudo del CV, sin pasar por limpiar_md: los chequeos de CV
    necesitan los comentarios intactos para ver el escape `<!-- voz-ok -->`.
    """
    hallazgos = buscar(texto, lista) + (revisar_cv(cv) if cv else [])
    if hallazgos:
        print(f"⛔ {origen} no puede salir todavía:")
        for n, visto, que_hacer in sorted(hallazgos, key=lambda h: h[0]):
            donde = f"línea {n}" if n else "en todo el archivo"
            print(f"   {donde}: «{visto}» → {que_hacer}")
        sys.exit(1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--cv"]
    modo_cv = "--cv" in sys.argv[1:]
    total = 0
    for arg in args or ["-"]:
        if arg == "-":
            texto, lista = sys.stdin.read(), buscar_lista(pathlib.Path.cwd())
        else:
            texto, lista = pathlib.Path(arg).read_text(encoding="utf-8"), buscar_lista(arg)
        hallazgos = buscar(texto, lista) + (revisar_cv(texto) if modo_cv else [])
        for n, visto, que_hacer in sorted(hallazgos, key=lambda h: h[0]):
            donde = f"{arg}:{n}" if n else f"{arg}"
            print(f"{donde}: «{visto}» → {que_hacer}")
            total += 1
    print("✅ Listo para salir." if not total else f"⛔ {total} cosas para arreglar.")
    sys.exit(1 if total else 0)
