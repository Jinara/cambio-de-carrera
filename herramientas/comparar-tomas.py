#!/usr/bin/env python3
"""Compara varias tomas de la misma respuesta de simulacro y marca lo que se puede medir solo.

Uso:
    herramientas/transcribir.sh herramientas/audios/lumbrera-p1*.m4a > tomas-p1.txt
    python3 herramientas/comparar-tomas.py tomas-p1.txt --objetivo 60
    python3 herramientas/comparar-tomas.py toma1.txt toma2.txt --objetivo 90-120

Acepta la salida de transcribir.sh (bloques con ARCHIVO y DURACION) o archivos de texto sueltos,
uno por toma. El orden de las tomas es el orden en que aparecen.

Lo que marca:
  1. El número que baila: la misma cosa ("personas", "locales", "%") con cifras distintas entre
     tomas. Un número que cambia entre tomas no está anclado a su fuente.
  2. El reloj: cuánto duró cada toma contra el objetivo, y si una toma se alargó respecto de la
     anterior (señal de que la historia todavía se está buscando en voz alta).
  3. Frases que se repiten dentro de una misma toma: texto memorizado que se soltó del riel.
  4. Un posible comentario sobre la propia toma en la última oración ("perdón", "sonó raro").
  5. Números retirados de numeros-retirados.txt, también dichos en palabras.

No juzga el arco ni si la respuesta contesta la pregunta. Eso lo hace quien da el feedback.
"""
import argparse
import pathlib
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from chequear import buscar, buscar_lista  # noqa: E402

VALORES = {
    "cero": 0, "uno": 1, "una": 1, "un": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12,
    "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiun": 21, "veintiuno": 21,
    "veintiuna": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25,
    "veintiseis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29, "treinta": 30,
    "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90,
    "cien": 100, "ciento": 100, "doscientos": 200, "doscientas": 200, "trescientos": 300,
    "trescientas": 300, "cuatrocientos": 400, "cuatrocientas": 400, "quinientos": 500,
    "quinientas": 500, "seiscientos": 600, "seiscientas": 600, "setecientos": 700,
    "setecientas": 700, "ochocientos": 800, "ochocientas": 800, "novecientos": 900,
    "novecientas": 900,
}
MULTIPLICADORES = {"mil": 1_000, "millon": 1_000_000, "millones": 1_000_000}
VACIAS = {
    "de", "del", "la", "las", "el", "los", "al", "a", "por", "en", "y", "o", "que", "mas", "menos",
    "casi", "unos", "unas", "como", "cada", "hasta", "desde", "entre", "sobre", "con", "sin", "se",
    "me", "mi", "mis", "lo", "le", "les", "su", "sus", "es", "era", "fue", "son", "eran", "ya",
    "hoy", "tambien", "muy", "solo", "punto", "aproximadamente", "no", "si", "cuando", "esta",
    "estan", "este", "esto", "eso", "fueron", "iban", "todo", "toda", "todos", "otro", "otra", "para",
    "va", "vez", "forma", "misma", "mismo", "porque", "pero", "aunque", "donde", "mucho", "poco",
}
META = re.compile(
    r"perd[oó]n|me trab[eé]|otra vez|de nuevo|no me sal|son[oó] (raro|mal|rob)|suena (raro|mal|rob)|"
    r"rob[oó]tic|recit|no es una conversaci|qu[eé] raro|rar[ií]simo|\buy\b|\buf\b|no s[eé] qu[eé] dije",
    re.I,
)


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def raiz(palabra):
    p = sin_tildes(palabra.lower())
    if p.endswith("ces") and len(p) > 4:
        return p[:-3] + "z"
    if p.endswith("es") and len(p) > 5 and p[-3] not in "aeiou":
        return p[:-2]
    if p.endswith("s") and len(p) > 3:
        return p[:-1]
    return p


def numero_de_digitos(tok):
    tok = tok.rstrip("%")
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", tok):
        return float(re.sub(r"[.,]", "", tok))
    if re.fullmatch(r"\d+[.,]\d+", tok):
        return float(tok.replace(",", "."))
    return float(tok)


def formato(v):
    if v >= 1_000_000 and v % 1_000_000 == 0:
        return f"{int(v // 1_000_000)} millones"
    if float(v).is_integer():
        return f"{int(v):,}".replace(",", ".")
    return f"{v:g}".replace(".", ",")


def extraer_numeros(texto):
    """Devuelve [(valor, unidad, fragmento)] y el texto con los números en palabras pasados a cifras."""
    tokens = re.findall(r"\d+(?:[.,]\d+)*%?|[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", texto)
    norm = [sin_tildes(t.lower()) for t in tokens]
    salida, digitalizado, i = [], [], 0
    while i < len(tokens):
        t, n = tokens[i], norm[i]
        inicio = i
        valor, es_numero, porcentaje = None, False, False
        if re.fullmatch(r"\d+(?:[.,]\d+)*%?", t):
            valor, es_numero, porcentaje = numero_de_digitos(t), True, t.endswith("%")
            i += 1
            if i < len(tokens) and norm[i] in MULTIPLICADORES:
                valor *= MULTIPLICADORES[norm[i]]
                i += 1
        elif n in VALORES or n in MULTIPLICADORES:
            # "un cuarenta por ciento": el "un" es artículo, la cifra arranca en la palabra siguiente.
            if (n in ("un", "una", "uno") and i + 1 < len(tokens) and norm[i + 1] in VALORES):
                digitalizado.append(t)
                i += 1
                continue
            total, actual, j = 0, 0, i
            while j < len(tokens):
                w = norm[j]
                if w in VALORES:
                    actual += VALORES[w]
                elif w in MULTIPLICADORES and MULTIPLICADORES[w] == 1_000:
                    actual = max(actual, 1) * 1_000
                    total, actual = total + actual, 0
                elif w in MULTIPLICADORES:
                    total, actual = (total + actual or 1) * 1_000_000, 0
                elif (w == "y" and j + 1 < len(tokens) and norm[j + 1] in VALORES
                      and VALORES[norm[j + 1]] < 10 and j > i and VALORES.get(norm[j - 1], 0) >= 30):
                    pass
                else:
                    break
                j += 1
            valor = total + actual
            # "un", "una" y "uno" sueltos casi siempre son artículos, no cifras.
            if j - i == 1 and n in ("un", "una", "uno"):
                valor = None
            else:
                es_numero = True
                if j + 1 < len(tokens) and norm[j] == "coma" and norm[j + 1] in VALORES:
                    decimal = VALORES[norm[j + 1]]
                    valor += decimal / (10 ** len(str(decimal)))
                    j += 2
            i = j if es_numero else i + 1
        else:
            digitalizado.append(t)
            i += 1
            continue

        if not es_numero or valor is None:
            digitalizado.append(t)
            continue
        if i + 1 < len(tokens) and norm[i] == "por" and norm[i + 1] == "ciento":
            porcentaje, i = True, i + 2
        # La unidad: la primera palabra con contenido después del número. En un porcentaje solo
        # cuenta si viene con "de" ("80% del gasto"); si no, la palabra siguiente es cualquier cosa.
        unidad, k = None, i
        buscar_unidad = not porcentaje or (i < len(tokens) and norm[i] in ("de", "del"))
        while buscar_unidad and k < len(tokens) and k < i + 4:
            if re.fullmatch(r"\d.*", tokens[k]) or norm[k] in VALORES:
                break
            if norm[k] not in VACIAS and len(norm[k]) >= 4:
                unidad = raiz(tokens[k])
                break
            k += 1
        if porcentaje:
            unidad = "%" + (f" {unidad}" if unidad else "")
        previa = norm[inicio - 1] if inicio > 0 else ""
        if (not porcentaje and re.fullmatch(r"\d{4}", tokens[inicio]) and 1950 <= valor <= 2100
                and (unidad is None or previa in ("el", "en", "desde", "hasta", "de", "ano"))):
            unidad = "año (¿fecha?)"
        fragmento = " ".join(tokens[inicio:min(k + 1, len(tokens))])
        salida.append([valor, unidad, fragmento, inicio, i])
        digitalizado.append(formato(valor) + ("%" if porcentaje else ""))
    # "de 7,6 a 4,6 centavos": la primera cifra toma la unidad de la segunda.
    for a, b in zip(salida, salida[1:]):
        if a[1] is None and b[1] is not None and b[3] - a[4] <= 1:
            a[1] = b[1]
    return [(v, u or "(sin unidad)", f) for v, u, f, *_ in salida], " ".join(digitalizado)


def leer_tomas(rutas):
    tomas = []
    for ruta in rutas:
        texto = pathlib.Path(ruta).read_text(encoding="utf-8")
        bloques = re.split(r"^=+\s*$", texto, flags=re.M)
        encontradas = False
        for b in bloques:
            m = re.search(r"^ARCHIVO:\s*(.+)$", b, re.M)
            if not m:
                continue
            encontradas = True
            d = re.search(r"^DURACION:\s*(\d+)", b, re.M)
            cuerpo = b.split("-" * 10, 1)[-1]
            cuerpo = re.sub(r"^-+\s*$", "", cuerpo, flags=re.M).strip()
            tomas.append({"nombre": m.group(1).strip(), "segundos": int(d.group(1)) if d else None,
                          "texto": cuerpo})
        if not encontradas:
            tomas.append({"nombre": pathlib.Path(ruta).name, "segundos": None, "texto": texto.strip()})
    return tomas


def frases_repetidas(texto, minimo=4, maximo=10):
    palabras = [sin_tildes(p.lower()) for p in re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", texto)]
    elegidas = []
    for n in range(maximo, minimo - 1, -1):
        cuenta = Counter(tuple(palabras[i:i + n]) for i in range(len(palabras) - n + 1))
        for grupo, c in cuenta.items():
            frase = " ".join(grupo)
            if (c > 1 and sum(w not in VACIAS for w in grupo) >= 2
                    and not any(frase in larga for larga, _ in elegidas)):
                elegidas.append((frase, c))
    return sorted(elegidas, key=lambda x: (-x[1], -len(x[0])))[:5]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivos", nargs="+")
    ap.add_argument("--objetivo", help="segundos objetivo: 60, o un rango como 90-120")
    args = ap.parse_args()

    tomas = leer_tomas(args.archivos)
    if not tomas:
        sys.exit("⛔ No encontré ninguna toma.")
    lista = buscar_lista(args.archivos[0])
    minimo = maximo = None
    if args.objetivo:
        partes = [int(x) for x in args.objetivo.split("-")]
        minimo, maximo = partes[0], partes[-1]

    for t in tomas:
        t["numeros"], t["digitalizado"] = extraer_numeros(t["texto"])

    print(f"# Comparación de {len(tomas)} tomas\n")

    print("## 1. El reloj\n")
    print("| Toma | Segundos | Palabras | Contra el objetivo |")
    print("|---|---|---|---|")
    anterior = None
    alargadas = []
    for t in tomas:
        s = t["segundos"]
        palabras = len(t["texto"].split())
        estado = "·"
        if s is not None and minimo is not None:
            if s < minimo * 0.9:
                estado = f"corta por {minimo - s} s"
            elif s > maximo * 1.1:
                estado = f"larga por {s - maximo} s"
            else:
                estado = "en el objetivo"
        if (s is not None and anterior is not None
                and s > anterior["segundos"] * 1.15 and s - anterior["segundos"] >= 10):
            alargadas.append((anterior["nombre"], anterior["segundos"], t["nombre"], s))
        print(f"| {t['nombre']} | {s if s is not None else '?'} | {palabras} | {estado} |")
        anterior = t if s is not None else anterior
    print()
    for a, sa, b, sb in alargadas:
        print(f"⚠️ **{b} se alargó** respecto de {a} ({sa} s → {sb} s). Si no fue a propósito, la "
              "historia todavía se está buscando en voz alta.")
    if alargadas:
        print()

    print("## 2. El número que baila\n")
    por_unidad = defaultdict(lambda: defaultdict(set))
    for idx, t in enumerate(tomas):
        for valor, unidad, _ in t["numeros"]:
            if "(¿fecha?)" not in unidad and unidad != "(sin unidad)":
                por_unidad[unidad][idx].add(valor)
    def baila(d):
        conjuntos = list(d.values())
        return any(not (a <= b or b <= a) for x, a in enumerate(conjuntos) for b in conjuntos[x + 1:])
    bailan = {u: d for u, d in por_unidad.items() if baila(d)}
    if not bailan:
        print("✅ Ninguna cifra cambia entre las tomas donde aparece.\n")
    else:
        print("| Qué | " + " | ".join(t["nombre"] for t in tomas) + " |")
        print("|---|" + "---|" * len(tomas))
        for unidad, d in sorted(bailan.items()):
            celdas = [" y ".join(formato(v) for v in sorted(d[i])) if i in d else "·"
                      for i in range(len(tomas))]
            print(f"| {unidad} | " + " | ".join(celdas) + " |")
        print("\n⚠️ Cada fila es una cifra que no se dijo igual en todas las tomas. Se revisa contra "
              "02-evidencia.md: la que tiene fuente es la que va, y las otras se retiran.\n")

    print("## 3. Frases que se repiten dentro de una toma\n")
    hubo = False
    for t in tomas:
        rep = frases_repetidas(t["texto"])
        if rep:
            hubo = True
            print(f"- **{t['nombre']}:** " + "; ".join(f"\"{f}\" ×{c}" for f, c in rep))
    print("✅ Ninguna.\n" if not hubo else "\nSi la frase no cierra la idea, es texto memorizado que se soltó del riel.\n")

    print("## 4. Lo último que se dijo\n")
    hubo = False
    for t in tomas:
        oraciones = [o.strip() for o in re.split(r"(?<=[.?!])\s+", t["texto"]) if o.strip()]
        if oraciones and META.search(oraciones[-1]):
            hubo = True
            print(f"- **{t['nombre']}:** \"{oraciones[-1]}\"")
    print("✅ Nada.\n" if not hubo else
          "\nUn comentario sobre la propia toma al final vale oro: la persona se dio cuenta sola. "
          "Se le pregunta qué notó.\n")

    print("## 5. Números retirados\n")
    hubo = False
    if not lista:
        print("· No encontré numeros-retirados.txt, se saltea.\n")
    else:
        for t in tomas:
            vistos = set()
            for texto in (t["texto"], t["digitalizado"]):
                for _, visto, que_hacer in buscar(texto, lista):
                    if que_hacer.startswith("número retirado") and visto.lower() not in vistos:
                        vistos.add(visto.lower())
                        hubo = True
                        print(f"- **{t['nombre']}:** «{visto}» → {que_hacer}")
        print("✅ Ninguno.\n" if not hubo else "")


if __name__ == "__main__":
    main()
