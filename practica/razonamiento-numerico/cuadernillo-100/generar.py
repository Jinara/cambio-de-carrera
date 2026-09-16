#!/usr/bin/env python3
"""Cuadernillo de práctica de razonamiento numérico, sin calculadora.

Arma 100 preguntas en 4 tandas de 25 (una de cada tipo por tanda) y aparte la hoja de
respuestas: la cuenta paso a paso, el porqué, qué error lleva a cada opción incorrecta y el
truco para hacerla de cabeza.

Ningún número se escribe a mano: todo lo calcula este archivo con fracciones exactas, y un
verificador independiente vuelve a resolver cada pregunta por otro camino antes de generar.
Semilla fija, así sale siempre igual.

Uso:  python3 generar.py
Sale: preguntas.pdf y respuestas.pdf en esta misma carpeta.

Necesita Chrome, Chromium, Edge o Brave para el PDF (o su ruta en la variable CHROME).
"""
import os, random, re, shutil, subprocess, pathlib, sys, tempfile
from fractions import Fraction as F

AQUI = pathlib.Path(__file__).resolve().parent
NAVEGADORES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
SEMILLA = 20260913
LETRAS = "ABCD"


# ─────────────────────────────── formato de números ───────────────────────────────

def fnum(x, dec=2):
    """Punto para los miles y coma para los decimales: 1.200 y 33,3. Signo menos tipográfico."""
    x = F(x)
    neg = x < 0
    x = abs(x)
    if x.denominator == 1:
        s = f"{x.numerator:,}".replace(",", ".")
    else:
        ent, frac = f"{round(float(x), dec):,.{dec}f}".split(".")
        frac = frac.rstrip("0")
        s = ent.replace(",", ".") + ("," + frac if frac else "")
    return ("−" if neg else "") + s

def pct(fr, dec=1):
    """Fracción a porcentaje: F(1,4) -> 25%."""
    return fnum(F(fr) * 100, dec) + "%"

def pesos(x, dec=2):
    return "$" + fnum(x, dec)

def cambio(fr):
    fr = F(fr)
    if fr == 0:
        return "Igual"
    return pct(abs(fr)) + (" más" if fr > 0 else " menos")

def exacto(x, dec=2):
    x = F(x)
    return F(round(x * 10 ** dec), 10 ** dec) == x

def tabla(encabezados, filas):
    th = "".join(f"<th>{h}</th>" for h in encabezados)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<table class="datos"><tr>{th}</tr>{tr}</table>'


# ─────────────────────────────── la pregunta ───────────────────────────────

class P:
    def __init__(self, tipo, enunciado, correcta, trampas, cuenta, porque, truco=None,
                 datos=None, fijas=None):
        self.tipo = tipo
        self.enunciado = enunciado
        self.valor, self.texto = correcta
        self.candidatas = trampas          # [(texto, error)] en orden de preferencia
        self.cuenta = cuenta
        self.porque = porque
        self.truco = truco
        self.datos = datos or {}
        self.fijas = fijas                 # opciones en orden fijo (cuando son etiquetas)
        self.opciones = None
        self.letra = None
        self.errores = {}

    def elegir_trampas(self):
        vistas, elegidas = {self.texto}, []
        for texto, error in self.candidatas:
            if texto in vistas:
                continue
            vistas.add(texto)
            elegidas.append((texto, error))
            if len(elegidas) == 3:
                break
        assert len(elegidas) == 3, f"{self.tipo}: no alcanzan las trampas distintas"
        return elegidas

    def armar(self, rng, letra):
        if self.fijas:
            self.opciones = list(self.fijas)
            self.errores = {t: e for t, e in self.candidatas if t in self.opciones}
            faltan = [t for t in self.opciones if t != self.texto and t not in self.errores]
            assert not faltan, f"{self.tipo}: opción fija sin explicación: {faltan}"
        else:
            trampas = self.elegir_trampas()
            rng.shuffle(trampas)
            idx = LETRAS.index(letra)
            self.opciones = [None] * 4
            self.opciones[idx] = self.texto
            libres = [i for i in range(4) if i != idx]
            for i, (t, e) in zip(libres, trampas):
                self.opciones[i] = t
                self.errores[t] = e
        assert len(set(self.opciones)) == 4, f"{self.tipo}: opciones repetidas {self.opciones}"
        assert self.opciones.count(self.texto) == 1
        self.letra = LETRAS[self.opciones.index(self.texto)]


# ─────────────────────────────── los 25 tipos ───────────────────────────────
# Cada generador recibe v = 0..3 (una variante por tanda, de más fácil a más difícil).

def g_crecimiento(v):
    a, b, ctx = [
        (200, 250, "Una app tenía {a} usuarios activos en abril y {b} en junio. ¿En qué porcentaje crecieron los usuarios activos?"),
        (400, 520, "Una tienda recibió {a} pedidos en marzo y {b} en mayo. ¿En qué porcentaje crecieron los pedidos?"),
        (80, 140, "Un equipo de soporte resolvía {a} tickets por semana y ahora resuelve {b}. ¿En qué porcentaje aumentó?"),
        (160, 360, "Un servicio pasó de {a} suscriptores a {b} en un año. ¿En qué porcentaje creció?"),
    ][v]
    d, g = b - a, F(b - a, a)
    return P("Crecimiento porcentual", ctx.format(a=fnum(a), b=fnum(b)), (g * 100, pct(g)),
        [(pct(F(b, a)), f"Es {fnum(b)} ÷ {fnum(a)} = {fnum(F(b, a))} sin quitarle el 1. Ese número compara lo nuevo con lo viejo, pero no dice cuánto creció."),
         (pct(F(d, b)), f"Divide el aumento sobre {fnum(b)}, el número nuevo. La base tiene que ser el de antes."),
         (fnum(d) + "%", f"Es el aumento en unidades ({fnum(d)}) escrito como si fuera un porcentaje.")],
        [f"Cuánto creció: {fnum(b)} − {fnum(a)} = {fnum(d)}",
         f"Sobre el de antes: {fnum(d)} ÷ {fnum(a)} = {fnum(g)}",
         f"Por 100: {pct(g)}"],
        "El crecimiento se mide contra el punto de partida, así que siempre se divide sobre el número de antes.",
        f"Atajo: {fnum(b)} ÷ {fnum(a)} = {fnum(F(b, a))} y le quitas el 1. Te queda {fnum(g)}, o sea {pct(g)}."
        + (" Y como se multiplicó por más de 2, tenía que dar más de 100%." if b > 2 * a else ""),
        datos=dict(a=a, b=b))

def g_caida(v):
    a, b, ctx = [
        (50, 40, "El tiempo promedio de entrega bajó de {a} a {b} minutos. ¿En qué porcentaje bajó?"),
        (120, 90, "Una tienda tenía {a} devoluciones al mes y ahora tiene {b}. ¿En qué porcentaje bajaron las devoluciones?"),
        (250, 150, "El costo de envío de un pedido pasó de {pa} a {pb}. ¿En qué porcentaje bajó?"),
        (64, 16, "Los reclamos semanales de un servicio bajaron de {a} a {b}. ¿En qué porcentaje bajaron?"),
    ][v]
    d, g = a - b, F(a - b, a)
    enun = ctx.format(a=fnum(a), b=fnum(b), pa=pesos(a), pb=pesos(b))
    return P("Caída porcentual", enun, (g * 100, pct(g)),
        [(pct(F(b, a)), f"Es {fnum(b)} ÷ {fnum(a)}: lo que quedó, no lo que bajó."),
         (pct(F(d, b)), f"Divide lo que bajó sobre {fnum(b)}, el número nuevo. La base es el de antes, {fnum(a)}."),
         (fnum(d) + "%", f"Es la baja en unidades ({fnum(d)}) escrita como si fuera un porcentaje.")],
        [f"Cuánto bajó: {fnum(a)} − {fnum(b)} = {fnum(d)}",
         f"Sobre el de antes: {fnum(d)} ÷ {fnum(a)} = {fnum(g)}",
         f"Por 100: {pct(g)}"],
        "Una baja también se mide contra el punto de partida. Acá el de antes es el número grande.",
        f"Atajo: {fnum(b)} ÷ {fnum(a)} = {fnum(F(b, a))} y se lo quitas a 1: 1 − {fnum(F(b, a))} = {fnum(g)}.",
        datos=dict(a=a, b=b))

def g_pct_numero(v):
    p, n, ctx = [
        (F(15), 80, "De {n} envíos, el {p}% llega con retraso. ¿Cuántos envíos llegan con retraso?"),
        (F(35), 60, "Una tienda tiene {n} productos y el {p}% está en oferta. ¿Cuántos productos están en oferta?"),
        (F(45), 240, "De {n} personas encuestadas, el {p}% prefiere pagar con transferencia. ¿Cuántas personas son?"),
        (F(25, 2), 640, "Un depósito guarda {n} cajas y el {p}% llegó dañado. ¿Cuántas cajas llegaron dañadas?"),
    ][v]
    c = n * p / 100
    decenas = (p // 10) * 10
    diez = F(n, 10)
    if p == F(25, 2):
        cuenta = [f"12,5% es 1/8 (la mitad de la mitad de la mitad)",
                  f"{fnum(n)} ÷ 8 = {fnum(c)}"]
        truco = "Las fracciones de la tabla de trucos ahorran cuentas: 12,5% = 1/8, 25% = 1/4, 75% = 3/4."
    else:
        resto = p - decenas
        cuenta = [f"10% de {fnum(n)}: corres la coma un lugar = {fnum(diez)}"]
        if decenas > 10:
            cuenta.append(f"{fnum(decenas)}% = {fnum(decenas // 10)} × {fnum(diez)} = {fnum(diez * decenas / 10)}")
        if resto:
            cuenta.append(f"{fnum(resto)}% es la mitad del 10% = {fnum(diez / 2)}")
            cuenta.append(f"{fnum(p)}% = {fnum(diez * decenas / 10)} + {fnum(diez / 2)} = {fnum(c)}")
        truco = "Con el 10% como bloque armas casi cualquier porcentaje: el 5% es su mitad y el 1% es su décima parte."
    return P("Porcentaje de un número", ctx.format(n=fnum(n), p=fnum(p)), (c, fnum(c)),
        [(fnum(n - c), f"Es el resto ({fnum(100 - p)}%), los que no. La pregunta es por el {fnum(p)}%."),
         (fnum(c * 10), "La coma quedó corrida un lugar: es diez veces la respuesta."),
         (fnum(n * decenas / 100), f"Calcula solo el {fnum(decenas)}% y se olvida del resto del porcentaje.")],
        cuenta,
        "Un porcentaje es una parte de cada 100. El 10% de algo siempre es ese algo dividido por 10.",
        truco, datos=dict(p=p, n=n))

def _bloques(q, n):
    """Pasos para sacar q% de n con el truco del 10%."""
    diez = F(n, 10)
    decenas, resto = (q // 10) * 10, q % 10
    pasos = [f"10% de {fnum(n)} = {fnum(diez)}"]
    if resto == 0:
        pasos.append(f"{q}% = {q // 10} × {fnum(diez)} = {fnum(diez * q / 10)}")
    else:
        pasos.append(f"{decenas}% = {decenas // 10} × {fnum(diez)} = {fnum(diez * decenas / 10)}")
        pasos.append(f"5% es la mitad del 10% = {fnum(diez / 2)}")
        pasos.append(f"{q}% = {fnum(diez * decenas / 10)} + {fnum(diez / 2)} = {fnum(n * F(q, 100))}")
    return pasos

def g_complemento(v):
    if v == 3:
        n, p1, p2 = 400, 25, 40
        pasaron = n * F(100 - p1, 100)
        nofueron = pasaron * F(p2, 100)
        fueron = pasaron - nofueron
        enun = (f"Se postularon {n} personas. El {p1}% no pasó el primer filtro. De las que pasaron, "
                f"el {p2}% no se presentó a la entrevista. ¿Cuántas personas se presentaron a la entrevista?")
        return P("El NO", enun, (fueron, fnum(fueron)),
            [(fnum(nofueron), "Son las que no se presentaron. La pregunta es por las que sí."),
             (fnum(n * F(100 - p1 - p2, 100)), f"Resta los dos porcentajes del total (100% − {p1}% − {p2}% = {100 - p1 - p2}% de {n}), como si los dos fueran sobre la misma base."),
             (fnum(n * F(100 - p2, 100)), f"Aplica el {100 - p2}% a las {n} personas y se olvida del primer filtro.")],
            [f"Pasaron el filtro: {100 - p1}% de {n} = {fnum(pasaron)}",
             f"No se presentaron: {p2}% de {fnum(pasaron)} = {fnum(nofueron)}",
             f"Se presentaron: {fnum(pasaron)} − {fnum(nofueron)} = {fnum(fueron)}"],
            f"Cada porcentaje va sobre su propia base. El {p2}% es de las {fnum(pasaron)} que pasaron, no de las {n} del principio.",
            f"Directo: {n} × 0,75 × 0,6 = {fnum(fueron)}. Cada filtro multiplica por lo que queda.",
            datos=dict(n=n, p1=p1, p2=p2, modo="doble"))
    n, p, ctx = [
        (50, 30, "En un equipo de {n} personas, el {p}% trabaja remoto. ¿Cuántas personas NO trabajan remoto?"),
        (80, 45, "De {n} clientes, el {p}% pagó con tarjeta. ¿Cuántos clientes NO pagaron con tarjeta?"),
        (240, 35, "De {n} pedidos, el {p}% salió con envío express. ¿Cuántos pedidos NO salieron con envío express?"),
    ][v]
    si = n * F(p, 100)
    no = n - si
    return P("El NO", ctx.format(n=n, p=p), (no, fnum(no)),
        [(fnum(si), "Son los que sí. La pregunta tenía un NO."),
         (fnum(n - p), f"Resta el {p} del porcentaje como si fuera una cantidad: {n} − {p}."),
         (fnum(100 - p), f"Es el porcentaje de los que no ({100 - p}%), pero la pregunta pide cuántos son.")],
        [f"Los que no son el 100% − {p}% = {100 - p}%"] + _bloques(100 - p, n),
        "Cuando la pregunta tiene un NO, lo más rápido es calcular directo el porcentaje de los que no.",
        "Antes de calcular, repite la pregunta con tus palabras y con la base adelante: de tantos, ¿cuántos NO?",
        datos=dict(n=n, p=p, modo="simple"))

def g_parte_total(v):
    filas, pide, unidad, pregunta = [
        ([("Tienda online", 180), ("Local", 120), ("Mayoristas", 60), ("Otros", 40)], ["Local"],
         ("Canal", "Ventas (miles de $)"), "¿Qué porcentaje de las ventas viene del Local?"),
        ([("Sueldos", 450), ("Alquiler", 150), ("Pauta", 250), ("Otros", 150)], ["Pauta"],
         ("Gasto del mes", "Miles de $"), "¿Qué porcentaje del gasto se va en Pauta?"),
        ([("Norte", 240), ("Sur", 160), ("Centro", 280), ("Oeste", 120)], ["Norte", "Sur"],
         ("Zona", "Clientes"), "¿Qué porcentaje de los clientes está en Norte y Sur juntos?"),
        ([("Plan A", 125), ("Plan B", 375), ("Plan C", 250), ("Plan D", 250)], ["Plan A"],
         ("Plan", "Suscripciones"), "¿Qué porcentaje de las suscripciones es del Plan A?"),
    ][v]
    total = sum(x for _, x in filas)
    parte = sum(x for nom, x in filas if nom in pide)
    s = F(parte, total)
    omit_nom, omit = min(((nom, x) for nom, x in filas if nom not in pide), key=lambda t: t[1])
    nombre = " + ".join(pide)
    enun = tabla(list(unidad), [(nom, fnum(x)) for nom, x in filas]) + pregunta
    cuenta = [f"Total: {' + '.join(fnum(x) for _, x in filas)} = {fnum(total)}"]
    if len(pide) > 1:
        cuenta.append(f"La parte: {' + '.join(fnum(x) for nom, x in filas if nom in pide)} = {fnum(parte)}")
    cuenta += [f"Parte sobre total: {fnum(parte)} ÷ {fnum(total)} = {fnum(s, 3)}", f"Por 100: {pct(s)}"]
    tr = [(pct(F(parte, total - parte)), f"Divide sobre el resto ({fnum(total - parte)}) en vez de sobre el total."),
          (pct(F(parte, total - omit)), f"Se olvida la fila {omit_nom} al sumar el total ({fnum(total - omit)} en vez de {fnum(total)})."),
          (pct(1 - s), f"Es la parte que no es {nombre}: lo contrario de lo que se pregunta.")]
    if len(pide) > 1:
        tr.append((pct(F(filas[[n for n, _ in filas].index(pide[0])][1], total)), f"Cuenta solo {pide[0]} y se olvida de {pide[1]}."))
    return P("Parte sobre total", enun, (s * 100, pct(s)), tr, cuenta,
        "Para saber qué parte del total es algo, la cuenta es siempre la misma: la parte arriba y el total abajo.",
        "Estima antes de dividir. Si la parte es menos de la mitad del total, la respuesta tiene que ser menos de 50%, y eso ya descarta opciones.",
        datos=dict(filas=filas, pide=pide))

def g_promedio(v):
    if v == 3:
        prom, n, nuevo = 25, 4, 40
        suma = prom * n
        r = F(suma + nuevo, n + 1)
        enun = (f"Un vendedor promedió {prom} ventas por mes durante {n} meses. En el mes {n + 1} vendió {nuevo}. "
                f"¿Cuál es su promedio de los {n + 1} meses?")
        return P("Promedio simple", enun, (r, fnum(r)),
            [(fnum(F(prom + nuevo, 2)), f"Promedia el promedio viejo con el dato nuevo: ({prom} + {nuevo}) ÷ 2. El promedio viejo representa {n} meses, no uno."),
             (fnum(F(suma + nuevo, n)), f"Divide por {n} en vez de por {n + 1}: se olvida de que ahora hay un mes más."),
             (fnum(prom + F(nuevo, n + 1)), f"Le suma al promedio viejo {nuevo} ÷ {n + 1}, sin recuperar la suma de los meses anteriores.")],
            [f"Suma de los {n} meses: {n} × {prom} = {suma}",
             f"Con el mes nuevo: {suma} + {nuevo} = {suma + nuevo}",
             f"Entre {n + 1} meses: {suma + nuevo} ÷ {n + 1} = {fnum(r)}"],
            "Un promedio es una suma repartida. Para sumarle un dato, primero recuperas la suma y después divides por la cantidad nueva.",
            f"Otra forma: el mes nuevo está {nuevo - prom} arriba del promedio. Repartido entre {n + 1} meses sube {fnum(F(nuevo - prom, n + 1))}: {prom} + {fnum(F(nuevo - prom, n + 1))} = {fnum(r)}.",
            datos=dict(modo="agrega", prom=prom, n=n, nuevo=nuevo))
    datos, ctx = [
        ([8, 20, 11, 25], "Un repartidor hizo {d} entregas en 4 días. ¿Cuál es su promedio de entregas por día?"),
        ([120, 140, 150, 110, 180], "Una cafetería vendió {d} cafés en 5 días. ¿Cuál es el promedio diario?"),
        ([48, 52, 63, 39, 45, 53], "Un equipo cerró {d} tickets en 6 semanas. ¿Cuál es el promedio semanal?"),
    ][v]
    n, suma = len(datos), sum(datos)
    m = F(suma, n)
    lista = ", ".join(str(x) for x in datos[:-1]) + f" y {datos[-1]}"
    ref = 10 * ((m - 1) // 10)
    desv = [x - ref for x in datos]
    desv_txt = ", ".join(("+" if x >= 0 else "−") + str(abs(x)) for x in desv)
    return P("Promedio simple", ctx.format(d=lista), (m, fnum(m)),
        [(fnum(F(min(datos) + max(datos), 2), 1), f"Promedia solo el más chico y el más grande ({min(datos)} y {max(datos)})."),
         (fnum(F(suma, n - 1), 1), f"Divide la suma por {n - 1} en vez de por {n}."),
         (fnum(F(suma - datos[-1], n - 1), 1), f"Se olvida el último dato ({datos[-1]}).")],
        [f"Suma: {' + '.join(str(x) for x in datos)} = {suma}",
         f"Entre la cantidad de datos: {suma} ÷ {n} = {fnum(m)}"],
        "El promedio reparte la suma en partes iguales: es lo que tocaría a cada uno si todos fueran iguales.",
        f"Sin sumar números grandes: toma {fnum(ref)} de referencia. Los desvíos son {desv_txt}, suman {sum(desv)}, y repartidos entre {n} dan {fnum(F(sum(desv), n))}. Promedio: {fnum(ref)} + {fnum(F(sum(desv), n))} = {fnum(m)}.",
        datos=dict(modo="lista", datos=datos))

def g_regla3(v):
    if v == 3:
        g, precio, g2 = 750, 600, 2000
        r = F(precio, g) * g2
        enun = f"Un paquete de {g} g de café cuesta {pesos(precio)}. Al mismo precio por gramo, ¿cuánto cuestan 2 kg?"
        return P("Regla de tres directa", enun, (r, pesos(r)),
            [(pesos(F(precio, g) * 1000), "Es el precio de 1 kg: te quedaste a mitad de camino."),
             (pesos(precio * 2), f"Toma los {g} g como si fueran 1 kg y multiplica por 2."),
             (pesos(F(precio * g, g2)), f"Regla de tres al revés: {fnum(precio)} × {fnum(g)} ÷ {fnum(g2)}. Más café tiene que costar más.")],
            ["2 kg son 2.000 g",
             f"{g} g cuestan {pesos(precio)}, así que 250 g cuestan {pesos(F(precio, 3))}",
             f"2.000 g son 8 veces 250 g: 8 × {pesos(F(precio, 3))} = {pesos(r)}"],
            "Antes de la regla de tres, las dos cantidades tienen que estar en la misma unidad: gramos con gramos.",
            "Busca un bloque cómodo que entre justo en los dos números. Acá 250 g entra 3 veces en 750 y 8 veces en 2.000.",
            datos=dict(modo="unidad", q=precio, t=g, t2=g2))
    q, t, t2, ctx, u = [
        (20, 4, 5, "Un equipo revisa {q} solicitudes en {t} horas a ritmo constante. ¿Cuántas revisa en {t2} horas?", "hora"),
        (45, 9, 14, "Una máquina empaca {q} cajas en {t} minutos. ¿Cuántas empaca en {t2} minutos?", "minuto"),
        (18, 240, 400, "Un auto gasta {q} litros cada {t} km. ¿Cuántos litros gasta en {t2} km?", "km"),
    ][v]
    r = F(q, t) * t2
    return P("Regla de tres directa", ctx.format(q=q, t=t, t2=t2), (r, fnum(r)),
        [(fnum(q * t2), f"Multiplica {q} × {t2} y se olvida de dividir por {t}."),
         (fnum(q + t2 - t), f"Suma la diferencia ({t2} − {t} = {t2 - t}) en vez de mantener la proporción."),
         (fnum(F(q * t, t2), 1), f"Regla de tres al revés: {q} × {t} ÷ {t2}. Acá, si una cantidad sube, la otra también.")],
        [f"Por {u}: {q} ÷ {t} = {fnum(F(q, t), 3)}",
         f"Para {t2}: {fnum(F(q, t), 3)} × {t2} = {fnum(r)}"],
        "Es proporción directa: si una cantidad se duplica, la otra también. Por eso se saca cuánto toca por unidad y se multiplica.",
        "Pregúntate primero si al subir una cantidad la otra sube o baja. Si suben juntas, la respuesta tiene que ser más grande que el dato de partida.",
        datos=dict(modo="directa", q=q, t=t, t2=t2))

def g_ponderado(v):
    grupos, ctx = [
        ([(20, 70), (30, 80)], "La clase A tiene 20 estudiantes con un puntaje promedio de 70. La clase B tiene 30 estudiantes con un promedio de 80. ¿Cuál es el promedio de los 50 estudiantes juntos?"),
        ([(30, 200), (10, 400)], "Una tienda hizo 30 ventas con un ticket promedio de $200 y 10 ventas con un ticket promedio de $400. ¿Cuál es el ticket promedio de las 40 ventas?"),
        ([(12, 6), (18, 11)], "En el equipo 1, 12 personas hicieron en promedio 6 horas extra. En el equipo 2, 18 personas hicieron en promedio 11. ¿Cuál es el promedio de horas extra de las 30 personas?"),
        ([(10, 50), (20, 65), (10, 90)], "Tres sucursales: una tiene 10 vendedores con 50 ventas promedio, otra 20 vendedores con 65 y otra 10 vendedores con 90. ¿Cuál es el promedio de ventas por vendedor?"),
    ][v]
    n_tot = sum(n for n, _ in grupos)
    suma = sum(n * m for n, m in grupos)
    r = F(suma, n_tot)
    simple = F(sum(m for _, m in grupos), len(grupos))
    grande = max(grupos)[1]
    din = "$" if v == 1 else ""
    fm = lambda x: din + fnum(x, 1)
    tr = [(fm(simple), "Es el promedio simple de los promedios, como si todos los grupos fueran del mismo tamaño.")]
    if len(grupos) == 2:
        (n1, m1), (n2, m2) = grupos
        tr.append((fm(F(n1 * m2 + n2 * m1, n_tot)), "Cruza los pesos: le da a cada grupo el tamaño del otro."))
    tr.append((fm(grande), "Se queda con el promedio del grupo más grande, sin mezclar con los otros."))
    if len(grupos) == 3:
        tr.append((fm(F(grupos[0][1] + grupos[-1][1], 2)), "Promedia solo el promedio más bajo y el más alto."))
    truco = None
    if len(grupos) == 2:
        lo, hi = sorted([simple, F(grande)])
        truco = (f"Sin cuentas largas: si los grupos fueran del mismo tamaño daría {fm(simple)}. Como el grupo más grande "
                 f"tiene promedio {fm(grande)}, la respuesta tiene que estar entre {fm(lo)} y {fm(hi)}.")
    return P("Promedio ponderado", ctx, (r, fm(r)), tr,
        ["Total: " + " + ".join(f"{n} × {fnum(m)}" for n, m in grupos) + " = " + " + ".join(fnum(n * m) for n, m in grupos) + f" = {fnum(suma)}",
         f"Entre todos: {fnum(suma)} ÷ {n_tot} = {fnum(r, 1)}"],
        "Cada grupo pesa según su tamaño. Por eso se recupera el total de cada grupo, se suma todo y se divide por la cantidad total.",
        truco, datos=dict(grupos=grupos))

def g_razon(v):
    if v == 3:
        a, b, dif = 7, 2, 35
        parte = F(dif, a - b)
        total = parte * (a + b)
        enun = (f"En un curso, la razón de aprobados a desaprobados es {a}:{b}. Hay {dif} aprobados más que "
                f"desaprobados. ¿Cuántas personas hay en el curso?")
        return P("Razones", enun, (total, fnum(total)),
            [(fnum(parte * a), "Son solo los aprobados."),
             (fnum(parte * b), "Son solo los desaprobados."),
             (fnum(dif * (a + b)), f"Toma los {dif} como si fueran una parte, cuando son {a - b} partes.")],
            [f"La diferencia es de {a} − {b} = {a - b} partes",
             f"{a - b} partes son {dif}, así que una parte es {dif} ÷ {a - b} = {fnum(parte)}",
             f"El curso son {a} + {b} = {a + b} partes: {a + b} × {fnum(parte)} = {fnum(total)}"],
            f"Una razón {a}:{b} no da cantidades: dice que el grupo se reparte en {a + b} partes iguales. Lo que haya que averiguar primero es cuánto vale una parte.",
            f"El total siempre es múltiplo de {a + b}. Descarta las opciones que no lo sean.",
            datos=dict(modo="dif", a=a, b=b, valor=dif))
    a, b, conocido, valor, na, nb, arta, artb, lugar = [
        (5, 4, "a", 20, "niños", "niñas", "los", "las", "un club"),
        (2, 3, "b", 36, "clientes nuevos", "clientes que repiten", "los", "los", "una tienda"),
        (3, 5, "a", 45, "personas remotas", "personas presenciales", "las", "las", "una empresa"),
    ][v]
    k = a if conocido == "a" else b
    otro = b if conocido == "a" else a
    parte = F(valor, k)
    total = parte * (a + b)
    nomk = na if conocido == "a" else nb
    nomo = nb if conocido == "a" else na
    arto = artb if conocido == "a" else arta
    artk = arta if conocido == "a" else artb
    enun = f"En {lugar}, la razón de {na} a {nb} es {a}:{b}. Hay {valor} {nomk}. ¿Cuántas personas hay en total?"
    return P("Razones", enun, (total, fnum(total)),
        [(fnum(parte * otro), f"Son solo {arto} {nomo}."),
         (fnum(valor + a + b), f"Le suma los números de la razón ({a} + {b}) a los {valor}."),
         (fnum(F(valor, otro) * (a + b)), f"Toma {artk} {valor} {nomk} como si fueran {arto} {nomo}, que son {otro} partes y no {k}.")],
        [f"{k} partes son {valor} {nomk}, así que una parte es {valor} ÷ {k} = {fnum(parte)}",
         f"{nomo.capitalize()}: {otro} partes = {fnum(parte * otro)}",
         f"Total: {a + b} partes = {fnum(total)}"],
        f"Una razón {a}:{b} no da cantidades: dice que el grupo se reparte en {a + b} partes iguales, {a} de un lado y {b} del otro.",
        f"El total siempre es múltiplo de {a + b}. Descarta las opciones que no lo sean.",
        datos=dict(modo="grupo", a=a, b=b, conocido=conocido, valor=valor))

def g_reparto(v):
    if v == 3:
        aportes, ganancia, i = [20000, 30000, 50000], 60000, 1
        tot = sum(aportes)
        r = F(ganancia * aportes[i], tot)
        enun = (f"Tres socias pusieron {pesos(aportes[0])}, {pesos(aportes[1])} y {pesos(aportes[2])}. Reparten "
                f"{pesos(ganancia)} de ganancia en proporción a lo que puso cada una. ¿Cuánto recibe la que puso {pesos(aportes[i])}?")
        return P("Reparto proporcional", enun, (r, pesos(r)),
            [(pesos(F(ganancia, 3)), "Reparte en partes iguales, sin mirar cuánto puso cada una."),
             (pesos(aportes[i]), "Es lo que puso, no lo que le toca de la ganancia."),
             (pesos(F(ganancia * aportes[i], aportes[0] + aportes[1])), "Se olvida de la tercera socia al sumar los aportes.")],
            [f"Aportes: {pesos(aportes[0])} + {pesos(aportes[1])} + {pesos(aportes[2])} = {pesos(tot)}",
             f"La que puso {pesos(aportes[i])} puso {pct(F(aportes[i], tot))} del total",
             f"{pct(F(aportes[i], tot))} de {pesos(ganancia)} = {pesos(r)}"],
            "Repartir en proporción a lo aportado es darle a cada una el mismo porcentaje de la ganancia que puso del total.",
            "Comprueba que las tres partes sumen la ganancia: 12.000 + 18.000 + 30.000 = 60.000.",
            datos=dict(modo="aportes", aportes=aportes, total=ganancia, i=i))
    total, partes = [(10000, [3, 2]), (24000, [5, 3]), (18000, [3, 2, 1])][v]
    s = sum(partes)
    una = F(total, s)
    r = una * max(partes)
    quien = "Dos socias" if len(partes) == 2 else "Tres socias"
    razon = " a ".join(str(p) for p in partes)
    enun = f"{quien} reparten {pesos(total)} en proporción {razon}. ¿Cuánto recibe la que más recibe?"
    tr = [(pesos(F(total, len(partes))), "Reparte en partes iguales."),
          (pesos(una * min(partes)), "Es lo que recibe la que menos recibe.")]
    if len(partes) == 3:
        tr.append((pesos(F(total * partes[0], partes[0] + partes[1])), "Se olvida de la tercera socia al sumar las partes."))
    tr.append((pesos(una), "Es el valor de una sola parte: falta multiplicar por las partes que le tocan."))
    return P("Reparto proporcional", enun, (r, pesos(r)), tr,
        [f"Partes en total: {' + '.join(str(p) for p in partes)} = {s}",
         f"Una parte: {pesos(total)} ÷ {s} = {pesos(una)}",
         f"La que más recibe tiene {max(partes)} partes: {max(partes)} × {pesos(una)} = {pesos(r)}"],
        f"Repartir {razon} es partir el total en {s} pedazos iguales y darle a cada una los pedazos que le tocan.",
        "Comprueba que lo de todas sume el total: " + " + ".join(pesos(una * p) for p in partes) + f" = {pesos(total)}.",
        datos=dict(modo="partes", total=total, partes=partes))

def g_inversa(v):
    p, d, p2, ctx, u, quien = [
        (4, 6, 3, "{p} personas terminan un trabajo en {d} días. ¿En cuántos días lo terminan {p2} personas trabajando al mismo ritmo?", "días-persona", "personas"),
        (3, 12, 4, "{p} impresoras iguales terminan un pedido en {d} horas. ¿Cuántas horas tardan {p2} impresoras?", "horas-impresora", "impresoras"),
        (6, 10, 4, "Un equipo de {p} personas termina una mudanza en {d} horas. Si solo van {p2} personas, ¿cuántas horas tardan?", "horas-persona", "personas"),
        (5, 18, 6, "{p} máquinas procesan un lote en {d} horas. Si se suma una máquina más, ¿cuántas horas tardan las {p2}?", "horas-máquina", "máquinas"),
    ][v]
    w = p * d
    r = F(w, p2)
    return P("Proporción inversa", ctx.format(p=p, d=d, p2=p2), (r, fnum(r)),
        [(fnum(F(d * p2, p), 1), f"Regla de tres directa: {d} × {p2} ÷ {p}. Pero con {'menos' if p2 < p else 'más'} {quien} se tarda {'más' if p2 < p else 'menos'}."),
         (fnum(d + p - p2), f"{'Suma' if p2 < p else 'Resta'} al tiempo la diferencia de {quien} ({abs(p - p2)}), en vez de mantener la proporción."),
         (fnum(w), f"Es el trabajo total ({p} × {d}), falta repartirlo entre {p2}.")],
        [f"Trabajo total: {p} × {d} = {w} {u}",
         f"Con {p2}: {w} ÷ {p2} = {fnum(r)}"],
        f"Más {quien} terminan antes: las dos cantidades van al revés. Lo que no cambia es el trabajo total, así que se reparte entre la cantidad nueva.",
        f"Comprueba multiplicando: {p2} × {fnum(r)} tiene que dar {w}, igual que {p} × {d}.",
        datos=dict(p=p, d=d, p2=p2))

def g_veces(v):
    r1, r2, modo, ctx = [
        (4, 5, "pct", "La tasa de conversión de una tienda pasó de 4% a 5%. ¿En qué porcentaje aumentó la tasa respecto de su valor anterior?"),
        (2, 3, "veces", "La tasa de respuesta de un mail pasó de 2% a 3%. ¿Cuántas veces es la tasa nueva comparada con la vieja?"),
        (8, 6, "pct", "La tasa de abandono del carrito bajó de 8% a 6%. ¿En qué porcentaje bajó respecto de su valor anterior?"),
        (5, 8, "puntos", "La tasa de recompra subió de 5% a 8%. ¿Cuántos puntos porcentuales subió?"),
    ][v]
    tres = (f"Con los mismos datos hay tres preguntas distintas: cuántas veces ({r2} ÷ {r1}), qué porcentaje "
            f"({r2} ÷ {r1} y {'le quitas el 1' if r2 > r1 else 'se lo quitas a 1'}) y cuántos puntos "
            f"({max(r1, r2)} − {min(r1, r2)}). Cada una da un número distinto.")
    if modo == "pct":
        g = abs(F(r2 - r1, r1))
        sube = r2 > r1
        tr = [(f"{abs(r2 - r1)}%", f"Son los puntos porcentuales ({max(r1, r2)} − {min(r1, r2)}). La pregunta es por el porcentaje."),
              (pct(F(abs(r2 - r1), r2)), f"Divide sobre {r2}, la tasa nueva. La base es la de antes, {r1}.")]
        tr.append((pct(F(r2, r1)), f"Es {r2} ÷ {r1} sin quitarle el 1.") if sube else
                  (pct(F(r2, r1)), f"Es {r2} ÷ {r1}: lo que quedó, no lo que bajó."))
        return P("Veces, porcentaje y puntos", ctx, (g * 100, pct(g)), tr,
            [f"Cambio: {max(r1, r2)} − {min(r1, r2)} = {abs(r2 - r1)} punto{'s' if abs(r2 - r1) != 1 else ''} {'más' if sube else 'menos'}",
             f"Sobre el de antes: {abs(r2 - r1)} ÷ {r1} = {fnum(g)}", f"Por 100: {pct(g)}"],
            tres, f"Atajo: {r2} ÷ {r1} = {fnum(F(r2, r1))}, y {'le quitas el 1' if sube else 'se lo quitas a 1'}.",
            datos=dict(r1=r1, r2=r2, modo=modo))
    if modo == "veces":
        x = F(r2, r1)
        return P("Veces, porcentaje y puntos", ctx, (x, f"{fnum(x)} veces"),
            [(f"{fnum(r2 - r1)} vez", f"Resta las tasas ({r2} − {r1}). Eso son puntos, no veces."),
             (f"{fnum(F(r1, r2))} veces", f"Divide al revés: {r1} ÷ {r2}."),
             (f"{fnum(x - 1)} veces", f"Le quita el 1 a {fnum(x)}. Eso da el porcentaje de aumento (50%), no las veces.")],
            [f"Cuántas veces es dividir: {r2} ÷ {r1} = {fnum(x)}",
             f"Comprobación: {r1}% × {fnum(x)} = {r2}%"],
            tres, "Cuántas veces es la pregunta por cuánto multiplicas lo viejo para llegar a lo nuevo.",
            datos=dict(r1=r1, r2=r2, modo=modo))
    d = r2 - r1
    return P("Veces, porcentaje y puntos", ctx, (F(d), f"{d} puntos"),
        [(f"{fnum(F(d, r1) * 100)} puntos", f"Es el aumento porcentual ({pct(F(d, r1))}) escrito como puntos."),
         (f"{fnum(F(r2, r1))} puntos", f"Es {r2} ÷ {r1}: las veces, no los puntos."),
         (f"{r1 + r2} puntos", "Suma las dos tasas.")],
        [f"Puntos porcentuales es restar: {r2} − {r1} = {d}"],
        tres, "Si la pregunta dice puntos, es una resta y nada más.",
        datos=dict(r1=r1, r2=r2, modo=modo))

def g_embudo_total(v):
    etapas, modo, preg = [
        ([("Visitas", 2000), ("Carrito", 1500), ("Checkout", 1000), ("Compra", 500)], "total",
         "¿Qué porcentaje de las visitas terminó en compra?"),
        ([("Descargas", 5000), ("Registro", 3000), ("Identidad validada", 2000), ("Primer pago", 1000)], "total",
         "¿Qué porcentaje de las descargas llegó al primer pago?"),
        ([("Solicitudes", 4000), ("Registro completo", 3000), ("Aprobadas", 1800), ("Primer uso", 1200)], "no2",
         "¿Qué porcentaje de los que completaron el registro NO llegó al primer uso?"),
        ([("Leads", 2500), ("Demo", 2000), ("Propuesta", 1500), ("Cierre", 900)], "escala",
         "Si el mes que viene entran 20% más leads y todas las tasas de conversión se mantienen, ¿cuántos cierres habrá?"),
    ][v]
    enun = tabla(["Etapa", "Cantidad"], [(n, fnum(x)) for n, x in etapas]) + preg
    (n1, e1), (n2, e2), (n3, e3), (n4, e4) = etapas
    if modo == "total":
        r = F(e4, e1)
        return P("Embudo: conversión total", enun, (r * 100, pct(r)),
            [(pct(F(e4, e3)), f"Es solo el último paso ({fnum(e4)} ÷ {fnum(e3)}), no el embudo completo."),
             (pct(1 - r), f"Son los que se quedaron en el camino. La pregunta es por los que llegaron."),
             (pct(F(e4, e2)), f"Divide sobre {n2} ({fnum(e2)}). La base es la primera etapa.")],
            [f"La parte: los que llegaron al final, {fnum(e4)}",
             f"La base: los que entraron, {fnum(e1)}",
             f"{fnum(e4)} ÷ {fnum(e1)} = {fnum(r)}, o sea {pct(r)}"],
            "La conversión total es la última etapa sobre la primera. Las del medio no hacen falta.",
            f"Estima: {fnum(e4)} es {'la cuarta parte' if r == F(1, 4) else 'la quinta parte'} de {fnum(e1)}.",
            datos=dict(etapas=etapas, modo=modo))
    if modo == "no2":
        si = F(e4, e2)
        r = 1 - si
        return P("Embudo: conversión total", enun, (r * 100, pct(r)),
            [(pct(si), "Son los que sí llegaron. La pregunta tenía un NO."),
             (pct(1 - F(e4, e1)), f"Usa como base las {n1.lower()} ({fnum(e1)}). La pregunta dice los que completaron el registro."),
             (pct(1 - F(e4, e3)), f"Son los que se pierden solo en el último paso ({n3} a {n4}).")],
            [f"La base: los que completaron el registro, {fnum(e2)}",
             f"De esos llegaron {fnum(e4)}, así que no llegaron {fnum(e2)} − {fnum(e4)} = {fnum(e2 - e4)}",
             f"{fnum(e2 - e4)} ÷ {fnum(e2)} = {fnum(r)}, o sea {pct(r)}"],
            "Primero se fija la base que nombra la pregunta. Después, como hay un NO, se cuentan los que no llegaron.",
            "Repite la pregunta con la base adelante: de 3.000, ¿cuántos NO?",
            datos=dict(etapas=etapas, modo=modo))
    r = e4 * F(6, 5)
    return P("Embudo: conversión total", enun, (r, fnum(r)),
        [(fnum(e4 + 20), "Le suma 20 unidades a los cierres, como si 20% fueran 20."),
         (fnum(e4 + e1 // 5), f"Le suma a los cierres los {fnum(e1 // 5)} leads nuevos, como si todos cerraran."),
         (fnum(e4 * F(4, 5)), "Aplica el 20% para abajo en vez de para arriba.")],
        [f"Si todas las tasas se mantienen, todo el embudo crece en la misma proporción que la entrada",
         f"Cierres: {fnum(e4)} × 1,2 = {fnum(r)}"],
        "Con las tasas fijas, cada etapa es una fracción fija de la anterior. Si la entrada crece 20%, cada etapa crece 20%.",
        f"No rehagas el embudo etapa por etapa. El 20% de {fnum(e4)} es {fnum(e4 // 5)}, y {fnum(e4)} + {fnum(e4 // 5)} = {fnum(r)}.",
        datos=dict(etapas=etapas, modo=modo))

def g_embudo_perdida(v):
    etapas = [
        [("Visitas", 5000), ("Registro", 3000), ("Prueba gratis", 2400), ("Pago", 1200)],
        [("Solicitudes", 1600), ("Entrevista", 1200), ("Prueba técnica", 900), ("Oferta", 675)],
        [("Impresiones", 10000), ("Clics", 5000), ("Formulario", 2000), ("Venta", 1600)],
        [("Visitas", 2000), ("Producto", 1000), ("Carrito", 700), ("Compra", 420)],
    ][v]
    pasos = [(f"De {etapas[i][0]} a {etapas[i + 1][0]}", etapas[i][1], etapas[i + 1][1]) for i in range(3)]
    igual = "Todos los pasos pierden la misma proporción"
    perdidas = [F(a - b, a) for _, a, b in pasos]
    enun = (tabla(["Etapa", "Cantidad"], [(n, fnum(x)) for n, x in etapas])
            + "¿En qué paso se pierde la mayor proporción respecto de la etapa anterior?")
    if len(set(perdidas)) == 1:
        correcta = igual
    else:
        mx = max(perdidas)
        assert perdidas.count(mx) == 1
        correcta = pasos[perdidas.index(mx)][0]
    abs_i = max(range(3), key=lambda i: pasos[i][1] - pasos[i][2])
    tr = []
    for i, (lab, a, b) in enumerate(pasos):
        if lab == correcta:
            continue
        txt = f"Ahí se pierde {pct(perdidas[i])} ({fnum(a - b)} de {fnum(a)})"
        if correcta == igual:
            txt += ", la misma proporción que en los otros pasos"
            if i == abs_i:
                txt += ". Es la resta más grande, pero en proporción pierde lo mismo"
        elif i == abs_i:
            txt += ". Es la resta más grande, pero la pregunta es por proporción"
        tr.append((lab, txt + "."))
    if correcta != igual:
        tr.append((igual, "Las proporciones no son iguales: " + ", ".join(pct(x) for x in perdidas) + "."))
    return P("Embudo: mayor pérdida", enun, (correcta, correcta), tr,
        [f"{lab}: {fnum(b)} ÷ {fnum(a)} = {fnum(F(b, a))}, se pierde {pct(F(a - b, a))}" for lab, a, b in pasos],
        "Proporción respecto de la etapa anterior quiere decir dividir sobre la etapa de arriba, de donde viene la gente.",
        "No te guíes por la resta más grande. El primer paso casi siempre la tiene, solo porque es la etapa con más gente.",
        datos=dict(etapas=etapas), fijas=[p[0] for p in pasos] + [igual])

def g_tipo_cambio(v):
    if v == 0:
        tc, monto = 20, 3600
        r = F(monto, tc)
        return P("Tipo de cambio", f"El tipo de cambio es 1 USD = {tc} pesos. Un proveedor factura {fnum(monto)} pesos. ¿Cuántos dólares son?",
            (r, f"USD {fnum(r)}"),
            [(f"USD {fnum(monto * tc)}", "Multiplica en vez de dividir. Un dólar son muchos pesos, así que en dólares el número tiene que quedar más chico."),
             (f"USD {fnum(r * 10)}", "La coma quedó corrida un lugar: es diez veces la respuesta."),
             (f"USD {fnum(r / 10)}", "La coma quedó corrida un lugar para el otro lado.")],
            [f"De pesos a dólares se divide por el tipo de cambio: {fnum(monto)} ÷ {tc} = {fnum(r)}"],
            "Si 1 dólar son 20 pesos, cada 20 pesos tienes un dólar. Contar cuántas veces entra 20 en el monto es dividir.",
            f"Divide en dos pasos: {fnum(monto)} ÷ 10 = 360, y 360 ÷ 2 = 180.",
            datos=dict(modo="simple", tc=tc, monto=monto))
    if v == 1:
        tc, monto = F(5, 4), 500
        r = monto / tc
        return P("Tipo de cambio", f"El tipo de cambio es 1 EUR = 1,25 USD. ¿Cuántos euros son USD {monto}?",
            (r, f"EUR {fnum(r)}"),
            [(f"EUR {fnum(monto * tc)}", "Multiplica en vez de dividir. Un euro vale más que un dólar, así que tienen que ser menos euros."),
             (f"EUR {fnum(monto * F(3, 4))}", "Le resta el 25% a los dólares. Dividir por 1,25 no es lo mismo que restar 25%."),
             (f"EUR {fnum(r * 10)}", "La coma quedó corrida un lugar.")],
            [f"De dólares a euros se divide por lo que vale un euro: {monto} ÷ 1,25 = {fnum(r)}",
             f"Comprobación: {fnum(r)} × 1,25 = {monto}"],
            "La moneda que vale más siempre da un número más chico. Por eso se divide.",
            "Dividir por 1,25 es dividir por 5/4, o sea multiplicar por 4/5: 500 × 4 ÷ 5 = 400.",
            datos=dict(modo="simple", tc=tc, monto=monto))
    if v == 2:
        a, tca, b, tcb = 24000, 40, 1500, 5
        ua, ub = F(a, tca), F(b, tcb)
        r = ua - ub
        enun = (f"Tipos de cambio: 1 USD = {tca} pesos y 1 USD = {tcb} reales. El proveedor A factura {fnum(a)} pesos "
                f"y el proveedor B factura {fnum(b)} reales. ¿Cuántos dólares más se le pagan al proveedor A?")
        return P("Tipo de cambio", enun, (r, f"USD {fnum(r)}"),
            [(f"USD {fnum(ua + ub)}", "Suma los dos montos en vez de restarlos."),
             (f"USD {fnum(a - b)}", "Resta los montos sin convertirlos: pesos y reales no se pueden restar entre sí."),
             (f"USD {fnum(ua * 10 - ub)}", "Corre la coma al convertir los pesos: 24.000 ÷ 40 da 600, no 6.000.")],
            [f"A en dólares: {fnum(a)} ÷ {tca} = {fnum(ua)}",
             f"B en dólares: {fnum(b)} ÷ {tcb} = {fnum(ub)}",
             f"Diferencia: {fnum(ua)} − {fnum(ub)} = {fnum(r)}"],
            "Solo se puede comparar lo que está en la misma moneda. Primero se pasa todo a dólares y después se resta.",
            "24.000 ÷ 40 es lo mismo que 2.400 ÷ 4.",
            datos=dict(modo="dos", a=a, tca=tca, b=b, tcb=tcb))
    usd, tc, rec = 200, 1000, 5
    base = usd * tc
    r = base * F(100 + rec, 100)
    enun = (f"Compras USD {usd} con tarjeta. El banco usa 1 USD = {fnum(tc)} pesos y cobra un recargo de {rec}% "
            f"sobre el monto en pesos. ¿Cuántos pesos pagas?")
    return P("Tipo de cambio", enun, (r, pesos(r)),
        [(pesos(base), "Se olvida del recargo."),
         (pesos(base * F(100 - rec, 100)), "Resta el recargo en vez de sumarlo."),
         (pesos(base + usd * F(rec, 100)), "Calcula el recargo en dólares (USD 10) y lo suma a los pesos sin convertir.")],
        [f"En pesos: {usd} × {fnum(tc)} = {pesos(base)}",
         f"Recargo: {rec}% de {pesos(base)} = {pesos(base * F(rec, 100))}",
         f"Total: {pesos(base)} + {pesos(base * F(rec, 100))} = {pesos(r)}"],
        "De dólares a pesos se multiplica, porque cada dólar son muchos pesos. Y el recargo va sobre el monto ya convertido.",
        "El 5% es la mitad del 10%: 10% de 200.000 es 20.000, y la mitad es 10.000.",
        datos=dict(modo="recargo", usd=usd, tc=tc, rec=rec))

def g_comision(v):
    n, m, p, f, modo = [(40, 500, F(3, 2), 2, "total"), (25, 800, F(2), 4, "total"),
                        (50, 1200, F(3), 5, "total"), (30, 250, F(4), 10, "neto")][v]
    monto = n * m
    porc = monto * p / 100
    fijo = n * f
    com = porc + fijo
    if modo == "total":
        enun = (f"Una empresa hace {n} pagos de {pesos(m)} cada uno. La comisión es {fnum(p)}% del monto más "
                f"{pesos(f)} fijos por pago. ¿Cuánto paga de comisiones en total?")
        return P("Comisión: porcentaje más fijo", enun, (com, pesos(com)),
            [(pesos(m * p / 100 + fijo), f"Calcula el {fnum(p)}% de un solo pago ({pesos(m * p / 100)}) y no lo multiplica por los {n} pagos."),
             (pesos(porc), "Se olvida del cargo fijo."),
             (pesos(porc + f), f"Cobra el fijo una sola vez, cuando es uno por cada pago.")],
            [f"Monto total: {n} × {pesos(m)} = {pesos(monto)}",
             f"Parte porcentual: {fnum(p)}% de {pesos(monto)} = {pesos(porc)}",
             f"Parte fija: {n} × {pesos(f)} = {pesos(fijo)}",
             f"Total: {pesos(porc)} + {pesos(fijo)} = {pesos(com)}"],
            "La comisión tiene dos pedazos que se calculan por separado: el porcentaje va sobre todo el monto y el fijo se cobra una vez por pago.",
            f"El 1% es correr la coma dos lugares: 1% de {pesos(monto)} = {pesos(F(monto, 100))}. De ahí armas el {fnum(p)}%.",
            datos=dict(n=n, m=m, p=p, f=f, modo=modo))
    neto = monto - com
    enun = (f"Una plataforma cobra {fnum(p)}% más {pesos(f)} por cada venta. Vendes {n} productos de {pesos(m)}. "
            f"¿Cuánto te queda después de comisiones?")
    return P("Comisión: porcentaje más fijo", enun, (neto, pesos(neto)),
        [(pesos(com), "Es la comisión, no lo que te queda."),
         (pesos(monto - porc - f), "Descuenta el fijo una sola vez, cuando es uno por venta."),
         (pesos(monto - porc), "Se olvida del cargo fijo.")],
        [f"Ventas: {n} × {pesos(m)} = {pesos(monto)}",
         f"Porcentaje: {fnum(p)}% de {pesos(monto)} = {pesos(porc)}",
         f"Fijo: {n} × {pesos(f)} = {pesos(fijo)}",
         f"Te queda: {pesos(monto)} − {pesos(porc)} − {pesos(fijo)} = {pesos(neto)}"],
        "Primero se arma la comisión completa, con sus dos pedazos, y después se resta de lo vendido.",
        "Relee qué te preguntan: lo que pagas o lo que te queda. Las dos cuentas comparten todos los pasos menos el último.",
        datos=dict(n=n, m=m, p=p, f=f, modo=modo))

def g_runway(v):
    c, b, b2, modo, ctx = [
        (600000, 50000, 40000, "mas", "Una empresa tiene {c} en caja y gasta {b} por mes. Si baja el gasto a {b2} por mes, ¿cuántos meses más que antes le dura la caja?"),
        (1200000, 100000, 75000, "mas", "Una startup tiene {c} en caja y gasta {b} por mes. Si baja su gasto 25%, ¿cuántos meses más que antes le dura la caja?"),
        (900000, 60000, 90000, "menos", "Una empresa tiene {c} en caja y gasta {b} por mes. Si su gasto sube 50%, ¿cuántos meses menos le dura la caja?"),
        (720000, 60000, 40000, "ingreso", "Una empresa tiene {c} en caja y gasta {b} por mes. Si empieza a ingresar $20.000 por mes, ¿cuántos meses más que antes le dura la caja?"),
    ][v]
    antes, despues = F(c, b), F(c, b2)
    r = abs(despues - antes)
    enun = ctx.format(c=pesos(c), b=pesos(b), b2=pesos(b2))
    cuenta = [f"Antes: {pesos(c)} ÷ {pesos(b)} = {fnum(antes)} meses"]
    if modo == "ingreso":
        cuenta.append(f"Gasto neto: {pesos(b)} − $20.000 = {pesos(b2)}")
    elif b2 != 40000:
        cuenta.append(f"Gasto nuevo: {pesos(b2)}")
    cuenta += [f"Después: {pesos(c)} ÷ {pesos(b2)} = {fnum(despues)} meses",
               f"Diferencia: {fnum(max(antes, despues))} − {fnum(min(antes, despues))} = {fnum(r)}"]
    cambio_pct = abs(F(b2 - b, b))
    tr = [(fnum(despues), "Es cuánto dura la caja después, sin restarle lo de antes."),
          (fnum(antes * cambio_pct, 1),
           (f"El ingreso es {pct(cambio_pct)} del gasto, y le suma ese mismo {pct(cambio_pct)} a los {fnum(antes)} meses. Pero al bajar el gasto neto, la caja se estira más que eso."
            if modo == "ingreso" else
            f"Es el {pct(cambio_pct)} de {fnum(antes)} meses. Suena lógico, pero la duración no cambia en el mismo porcentaje que el gasto.")),
          (fnum(antes), "Es cuánto dura la caja antes del cambio.")]
    if modo == "menos":
        tr.insert(1, (fnum(antes * F(3, 2), 1), "Multiplica los meses por 1,5 como si el gasto más alto alargara la caja."))
    return P("Caja: cuántos meses más", enun, (r, fnum(r)), tr, cuenta,
        "La pregunta es por la diferencia: siempre son dos divisiones y una resta. Y como el gasto está abajo en la división, "
        "cambiar el gasto un porcentaje mueve la duración en otro porcentaje distinto.",
        "Ojo con la palabra más o menos: la respuesta es la resta, no la duración nueva.",
        datos=dict(c=c, b=b, b2=b2, modo=modo))

def g_velocidad(v):
    if v == 0:
        km, h, km2 = 240, 3, 400
        vel = F(km, h)
        r = F(km2, vel)
        return P("Velocidad, distancia y tiempo", f"Un camión recorre {km} km en {h} horas. A la misma velocidad, ¿cuántas horas tarda en recorrer {km2} km?",
            (r, f"{fnum(r)} horas"),
            [(f"{fnum(F(h * km, km2), 1)} horas", f"Regla de tres al revés: {h} × {km} ÷ {km2}. Más distancia tiene que llevar más tiempo."),
             (f"{h + 1} horas", "Suma una hora a ojo porque la distancia creció, sin sacar la velocidad."),
             (f"{fnum(vel)} horas", "Es la velocidad (80 km por hora), no el tiempo.")],
            [f"Velocidad: {km} ÷ {h} = {fnum(vel)} km por hora",
             f"Tiempo: {km2} ÷ {fnum(vel)} = {fnum(r)} horas"],
            "Tiempo es distancia dividida por velocidad. Primero sacas cuánto recorre en una hora.",
            "Comprueba: 5 horas × 80 km por hora = 400 km.",
            datos=dict(modo="tiempo", km=km, h=h, km2=km2))
    if v == 1:
        km, mins = 90, 45
        r = F(km * 60, mins)
        return P("Velocidad, distancia y tiempo", f"Un tren recorre {km} km en {mins} minutos. ¿A qué velocidad va, en km por hora?",
            (r, f"{fnum(r)} km/h"),
            [(f"{fnum(F(km, mins))} km/h", f"Divide {km} ÷ {mins}: eso da kilómetros por minuto, no por hora."),
             (f"{fnum(F(km * mins, 60), 1)} km/h", "Convierte al revés: multiplica por los minutos y divide por 60."),
             (f"{km + mins} km/h", "Suma los kilómetros y los minutos.")],
            [f"{mins} minutos son tres cuartos de hora",
             f"En 15 minutos recorre {km} ÷ 3 = {km // 3} km",
             f"En 60 minutos, 4 veces eso: {fnum(r)} km/h"],
            "Una velocidad en km por hora es cuánto recorrería en 60 minutos. Si te dan minutos, primero llevas todo a una hora.",
            "Busca un bloque que entre en 60: 15 minutos entra 3 veces en 45 y 4 veces en 60.",
            datos=dict(modo="kmh", km=km, mins=mins))
    if v == 2:
        km, horas = 150, F(5, 2)
        r = km / horas
        return P("Velocidad, distancia y tiempo", f"Tienes que recorrer {km} km en 2 horas y 30 minutos. ¿A qué velocidad promedio tienes que ir?",
            (r, f"{fnum(r)} km/h"),
            [(f"{fnum(F(km * 10, 23), 1)} km/h", "Toma 2 horas y 30 minutos como 2,3 horas. Media hora es 0,5."),
             (f"{fnum(F(km, 2))} km/h", "Ignora los 30 minutos."),
             (f"{fnum(F(km, 3))} km/h", "Redondea el tiempo a 3 horas.")],
            ["2 horas y 30 minutos son 2,5 horas",
             f"{km} ÷ 2,5 = {fnum(r)} km/h"],
            "Los minutos se pasan a fracción de hora antes de dividir: 30 minutos es media hora, 0,5, y no 0,3.",
            "Dividir por 2,5 es lo mismo que multiplicar por 2 y dividir por 5: 150 × 2 = 300, y 300 ÷ 5 = 60.",
            datos=dict(modo="vel", km=km, horas=horas))
    d, v1, v2 = 120, 60, 40
    t1, t2 = F(d, v1), F(d, v2)
    r = F(2 * d) / (t1 + t2)
    return P("Velocidad, distancia y tiempo", f"Un auto va a una ciudad que está a {d} km. La ida la hace a {v1} km/h y la vuelta, por el mismo camino, a {v2} km/h. ¿Cuál es su velocidad promedio en todo el viaje?",
        (r, f"{fnum(r)} km/h"),
        [(f"{fnum(F(v1 + v2, 2))} km/h", "Es el promedio simple de las velocidades. Pero a la vuelta, más lenta, pasa más tiempo en la ruta."),
         (f"{v1 + v2} km/h", "Suma las dos velocidades."),
         (f"{fnum(F(v1 * t2 + v2 * t1, t1 + t2))} km/h", "Pondera al revés: le da más peso a la velocidad rápida.")],
        [f"Ida: {d} ÷ {v1} = {fnum(t1)} horas", f"Vuelta: {d} ÷ {v2} = {fnum(t2)} horas",
         f"Todo el viaje: {2 * d} km en {fnum(t1 + t2)} horas", f"{2 * d} ÷ {fnum(t1 + t2)} = {fnum(r)} km/h"],
        "La velocidad promedio es la distancia total sobre el tiempo total. Como el tramo lento dura más, pesa más.",
        "Si las distancias son iguales y las velocidades distintas, el promedio siempre queda por debajo del promedio simple.",
        datos=dict(modo="idavuelta", d=d, v1=v1, v2=v2))

def g_tabla(v):
    cols, filas, modo, preg = [
        (["Producto", "Mes 1", "Mes 2"], [("Cafeteras", 120, 150), ("Tostadoras", 45, 63), ("Licuadoras", 80, 95), ("Batidoras", 200, 240)],
         "crece", "¿Qué producto tuvo el mayor crecimiento porcentual del Mes 1 al Mes 2?"),
        (["Zona", "Trimestre 1", "Trimestre 2"], [("Sur", 150, 180), ("Este", 54, 63), ("Norte", 76, 95), ("Oeste", 40, 46)],
         "crece", "¿Qué zona tuvo el mayor crecimiento porcentual?"),
        (["Plan", "Enero", "Febrero"], [("Básico", 90, 81), ("Estándar", 80, 60), ("Pro", 150, 120), ("Empresa", 50, 35)],
         "baja", "¿Qué plan tuvo la mayor caída porcentual?"),
        (["Canal", "T1", "T2", "T3"], [("Web", 100, 80, 100), ("App", 60, 90, 108), ("Local", 200, 210, 240), ("Mayorista", 50, 60, 66)],
         "t2t3", "¿Qué canal tuvo el mayor crecimiento porcentual entre T2 y T3?"),
    ][v]
    enun = tabla(cols, [(f[0],) + tuple(fnum(x) for x in f[1:]) for f in filas]) + preg
    ant = lambda f: f[-2]
    nue = lambda f: f[-1]
    cambios = [F(nue(f) - ant(f), ant(f)) for f in filas]
    if modo == "baja":
        cambios = [-c for c in cambios]
    mejor = max(cambios)
    assert cambios.count(mejor) == 1
    correcta = filas[cambios.index(mejor)][0]
    abs_i = max(range(4), key=lambda i: abs(nue(filas[i]) - ant(filas[i])))
    tr = []
    for i, f in enumerate(filas):
        if f[0] == correcta:
            continue
        verbo = "cayó" if modo == "baja" else "creció"
        txt = f"{verbo.capitalize()} {pct(cambios[i])} ({fnum(ant(f))} a {fnum(nue(f))})"
        if i == abs_i:
            txt += ". Es el cambio más grande en unidades, pero la pregunta es en porcentaje"
        if modo == "t2t3" and F(f[3], f[1]) - 1 == max(F(g[3], g[1]) - 1 for g in filas):
            txt += ". Además es la que más creció de T1 a T3, pero la pregunta es de T2 a T3"
        tr.append((f[0], txt + "."))
    verbo = "cae" if modo == "baja" else "crece"
    return P("Tablas", enun, (correcta, correcta), tr,
        [f"{f[0]}: {fnum(nue(f))} ÷ {fnum(ant(f))} = {fnum(F(nue(f), ant(f)), 3)}, {verbo} {pct(cambios[i])}" for i, f in enumerate(filas)],
        "Para comparar cambios de cosas de distinto tamaño hay que pasarlos a porcentaje, cada uno sobre su propio número de antes.",
        "No hace falta el porcentaje exacto de cada una: con el cociente (nuevo ÷ viejo) alcanza para ver cuál es más grande."
        + (" Y fíjate bien en qué columnas pide la pregunta." if modo == "t2t3" else ""),
        datos=dict(filas=filas, modo=modo), fijas=[f[0] for f in filas])

def g_sucesivos(v):
    x, y, ctx = [
        (50, -50, "El precio de un producto sube 50% en marzo y baja 50% en abril. Comparado con el precio de febrero, el de abril es:"),
        (10, 10, "Un sueldo sube 10% en marzo y otro 10% en septiembre. Comparado con febrero, el sueldo de septiembre es:"),
        (-20, 20, "Las ventas bajan 20% en un mes y suben 20% al mes siguiente. Comparadas con el principio, las ventas son:"),
        (25, -20, "Un precio sube 25% y después baja 20%. Comparado con el precio original, el precio final es:"),
    ][v]
    fx, fy = 1 + F(x, 100), 1 + F(y, 100)
    neto = fx * fy - 1
    suma = (cambio(F(x + y, 100)), f"Suma los porcentajes ({x:+d}% y {y:+d}%) como si los dos fueran sobre la misma base.".replace("-", "−"))
    signo = (cambio(-neto), "Hace bien la cuenta pero se equivoca de dirección.")
    if x == y:
        tr = [suma, (cambio(F(x * y, 10000)), "Multiplica los porcentajes entre sí (10% × 10% = 1%)."),
              (cambio(F(x, 100)), "Aplica un solo aumento."), signo]
    else:
        tr = [suma, signo, (cambio(F(y, 100)), "Se queda solo con el segundo cambio."),
              (cambio(F(x, 100)), "Se queda solo con el primer cambio.")]
    p1 = 100 * fx
    p2 = p1 * fy
    return P("Porcentajes seguidos", ctx, (neto, cambio(neto)), tr,
        ["Arranca en 100",
         f"{'Sube' if x > 0 else 'Baja'} {abs(x)}%: 100 × {fnum(fx)} = {fnum(p1)}",
         f"{'Sube' if y > 0 else 'Baja'} {abs(y)}% sobre {fnum(p1)}: {fnum(p1)} × {fnum(fy)} = {fnum(p2)}",
         f"Termina en {fnum(p2)} contra 100: {cambio(neto).lower()}"],
        "Cada porcentaje se calcula sobre el valor que había en ese momento. El segundo cambio ya no es sobre 100.",
        f"Multiplica los factores: {fnum(fx)} × {fnum(fy)} = {fnum(fx * fy)}. Si da más de 1 subió, si da menos bajó.",
        datos=dict(x=x, y=y))

def g_volver(v):
    d = [20, 50, 25, 60][v]
    fr = F(d, 100)
    r = 1 / (1 - fr) - 1
    queda = 100 - d
    return P("Volver al precio original", f"Un precio baja {d}%. ¿En qué porcentaje tiene que subir el precio nuevo para volver al original?",
        (r * 100, pct(r)),
        [(f"{d}%", f"Sube lo mismo que bajó. Pero el {d}% de subida se calcula sobre un precio más chico, así que no alcanza."),
         (f"{queda}%", f"Es lo que quedó del precio ({queda}%), no lo que falta subir."),
         (pct(fr / (1 + fr)), f"Divide {d} sobre {100 + d}: usa una base que no aparece en ningún lado."),
         (pct(1 / (1 - fr)), f"Es 100 ÷ {queda} sin quitarle el 1.")],
        [f"Arranca en 100 y baja a {queda}",
         f"Para volver a 100 le faltan {d}",
         f"{d} sobre {queda}, que ahora es el de antes: {fnum(F(d, queda), 3)}, o sea {pct(r)}"],
        "La subida se calcula sobre el precio rebajado, que es más chico. Por eso hay que subir más porcentaje del que se bajó.",
        f"Nuevo sobre viejo: 100 ÷ {queda} = {fnum(1 / (1 - fr), 3)}, y le quitas el 1.",
        datos=dict(d=d))

def g_precio_original(v):
    if v == 3:
        pagado, t = 1210, 21
        r = F(pagado * 100, 100 + t)
        return P("Precio original", f"Pagaste {pesos(pagado)} por un producto, con un impuesto de {t}% incluido. ¿Cuál era el precio sin impuesto?",
            (r, pesos(r)),
            [(pesos(pagado * F(100 - t, 100), 1), f"Le resta el {t}% a lo pagado, pero el {t}% se calculó sobre el precio sin impuesto."),
             (pesos(pagado * F(100 + t, 100), 1), "Le vuelve a sumar el impuesto."),
             (pesos(pagado - t), f"Resta {t} pesos, como si el porcentaje fuera una cantidad.")],
            [f"Con impuesto pagas el {100 + t}% del precio",
             f"{pesos(pagado)} es el {100 + t}% del precio",
             f"Precio: {fnum(pagado)} ÷ 1,21 = {pesos(r)}"],
            "El impuesto se calculó sobre el precio original, que no conoces. Por eso se divide por el factor en vez de restar el porcentaje.",
            "Comprueba con la opción: 1.000 + 21% = 1.210. Probar las opciones es muy rápido en este tipo.",
            datos=dict(modo="impuesto", pagado=pagado, t=t))
    pagado, d = [(240, 20), (450, 10), (600, 25)][v]
    r = F(pagado * 100, 100 - d)
    return P("Precio original", f"Un producto está en oferta a {pesos(pagado)} después de un descuento de {d}%. ¿Cuál era el precio original?",
        (r, pesos(r)),
        [(pesos(pagado * F(100 + d, 100)), f"Le suma el {d}% a {pesos(pagado)}. Pero el {d}% se calculó sobre el precio original, no sobre el de oferta."),
         (pesos(pagado * F(100 - d, 100)), "Le vuelve a aplicar el descuento."),
         (pesos(pagado + d), f"Suma {d} pesos, como si el porcentaje fuera una cantidad.")],
        [f"Con {d}% de descuento pagas el {100 - d}% del precio",
         f"{pesos(pagado)} es el {100 - d}% del original",
         f"Si el {100 - d}% son {pesos(pagado)}, el 1% es {pesos(F(pagado, 100 - d))} y el 100% es {pesos(r)}"],
        f"El descuento se calculó sobre un precio que no conoces. Lo que sí sabes es que {pesos(pagado)} es el {100 - d}% de ese precio, así que se divide.",
        f"Directo: {fnum(pagado)} ÷ {fnum(F(100 - d, 100))} = {fnum(r)}. Y compruebas: {d}% de {fnum(r)} es {fnum(r * d / 100)}, y {fnum(r)} − {fnum(r * d / 100)} = {fnum(pagado)}.",
        datos=dict(modo="descuento", pagado=pagado, d=d))

def _sust(a, b, x):
    ax = fnum(x) if a == 1 else f"{a} × {fnum(x)}"
    return f"({ax} {'+' if b >= 0 else '−'} {abs(b)})"

def _lado(a, b):
    xa = "x" if a == 1 else f"{a}x"
    return f"({xa} {'+' if b >= 0 else '−'} {abs(b)})"

def g_ecuacion(v):
    a, b, c, d, e, f = [(1, 3, 2, 1, 7, 3), (2, 1, 3, 3, -5, 4), (3, -2, 4, 1, 6, 2), (5, 4, 6, 2, 10, 3)][v]
    L, lb, R, rc = f * a, f * b, c * d, c * e
    x = F(rc - lb, L - R)
    assert x.denominator == 1
    val = (a * x + b) / c
    enun = f"Resuelve para x: {_lado(a, b)} / {c} = {_lado(d, e)} / {f}"
    tr = []
    if a != d:
        xi = F(e - b, a - d)
        if xi.denominator == 1:
            tr.append((fnum(xi), f"Ignora los denominadores y resuelve {_lado(a, b)} = {_lado(d, e)}."))
    if c * a != f * d:
        xm = F(f * e - c * b, c * a - f * d)
        if xm.denominator == 1:
            tr.append((fnum(xm), f"Multiplica en cruz al revés: {c} × {_lado(a, b)} = {f} × {_lado(d, e)}. Cada denominador tiene que pasar al otro lado."))
    tr.append((fnum(val), f"Es el valor de cada lado de la igualdad ({fnum(val)}), no el de x."))
    tr.append((fnum(-x), "Se equivoca con un signo al pasar los términos de lado."))
    termino = lambda k, n: ("x" if k == 1 else ("−x" if k == -1 else f"{k}x".replace("-", "−"))) + f" {'+' if n >= 0 else '−'} {abs(n)}"
    coef, const = L - R, rc - lb
    return P("Ecuaciones", enun, (x, fnum(x)), tr,
        [f"Multiplicas en cruz: {f} × {_lado(a, b)} = {c} × {_lado(d, e)}",
         f"{termino(L, lb)} = {termino(R, rc)}",
         f"Pasas las x a un lado y los números al otro: {termino(coef, 0).split(' ')[0]} = {fnum(const)}"]
        + ([f"x = {fnum(x)}"] if coef != 1 else []) + [
         f"Compruebas: {_sust(a, b, x)} ÷ {c} = {fnum(a * x + b)} ÷ {c} = {fnum(val)}, y {_sust(d, e, x)} ÷ {f} = {fnum(d * x + e)} ÷ {f} = {fnum(val)}"],
        "Cada denominador pasa multiplicando al otro lado. Así quedan dos lados sin fracciones y la igualdad sigue siendo la misma.",
        "Si despejar te lleva mucho, prueba las opciones: la que deja los dos lados iguales es la buena.",
        datos=dict(a=a, b=b, c=c, d=d, e=e, f=f))

def g_secuencia(v):
    serie, sig, tipo = [([3, 4, 6, 9, 13], 18, "difs"), ([3, 6, 12, 24], 48, "geom"),
                        ([2, 20, 4, 17, 6, 14], 8, "inter"), ([4, 7, 11, 18, 29], 47, "fibo")][v]
    enun = f"Observa la secuencia {', '.join(str(s) for s in serie)}, … ¿Cuál es el siguiente número?"
    if tipo == "difs":
        difs = [serie[i + 1] - serie[i] for i in range(len(serie) - 1)]
        tr = [(fnum(serie[-1] + difs[-1]), f"Repite la última diferencia (+{difs[-1]}) en vez de seguir el patrón."),
              (fnum(serie[-1] + difs[-1] + 2), "Salta un número en el patrón de diferencias."),
              (fnum(serie[-1] * 2), "Duplica el último número, pero la serie no se duplica.")]
        cuenta = [f"Diferencias: {', '.join('+' + str(d) for d in difs)}",
                  f"Cada diferencia crece de a 1, la que sigue es +{difs[-1] + 1}",
                  f"{serie[-1]} + {difs[-1] + 1} = {sig}"]
        porque = "Cuando la diferencia no es fija, mira cómo cambian las diferencias: acá forman su propia serie."
    elif tipo == "geom":
        tr = [(fnum(serie[-1] + serie[-1] - serie[-2]), "Suma la última diferencia (+12), como si fuera una serie que suma lo mismo."),
              (fnum(serie[-1] + 6), "Suma 6, que es la segunda diferencia."),
              (fnum(serie[-1] + serie[0]), "Suma 3, el primer número.")]
        cuenta = ["Cada número es el doble del anterior: 3 × 2 = 6, 6 × 2 = 12, 12 × 2 = 24", f"24 × 2 = {sig}"]
        porque = "Si las diferencias crecen muy rápido, prueba dividir: cuando cada número sobre el anterior da lo mismo, la serie multiplica."
    elif tipo == "inter":
        tr = [(fnum(serie[-1] - 3), "Sigue la serie de las posiciones pares (20, 17, 14, 11), pero el que toca es de las impares."),
              (fnum(serie[-2] * 2), "Duplica el 6."),
              (fnum(serie[-1] + serie[-2]), "Suma los dos últimos, como si fuera una serie de sumas.")]
        cuenta = ["Hay dos series intercaladas", "Posiciones impares: 2, 4, 6, sube de a 2",
                  "Posiciones pares: 20, 17, 14, baja de a 3",
                  f"El séptimo número es de las impares: 6 + 2 = {sig}"]
        porque = "Cuando la serie sube y baja sin patrón claro, sepárala en dos: los de posición impar y los de posición par."
    else:
        tr = [(fnum(serie[-1] + serie[-1] - serie[-2]), "Suma la última diferencia (+11)."),
              (fnum(serie[-1] + serie[1]), "Suma 7, un número de la serie que no es el anterior."),
              (fnum(serie[-1] * 2), "Duplica el último número.")]
        cuenta = ["Cada número es la suma de los dos anteriores: 4 + 7 = 11, 7 + 11 = 18, 11 + 18 = 29",
                  f"18 + 29 = {sig}"]
        porque = "Si las diferencias repiten números de la propia serie (+3, +4, +7, +11), cada número se arma sumando los dos anteriores."
    return P("Secuencias", enun, (F(sig), fnum(sig)), tr, cuenta, porque,
        "Orden para probar: diferencia fija, diferencias que crecen, multiplicar, sumar los dos anteriores, dos series intercaladas.",
        datos=dict(serie=serie, tipo=tipo))

def g_compuesto(v):
    if v == 3:
        t = 20
        r = (1 + F(t, 100)) ** 2 - 1
        return P("Crecimiento compuesto", f"Un precio sube {t}% un año y otro {t}% el año siguiente. ¿Cuánto subió en total en los dos años?",
            (r * 100, pct(r)),
            [(f"{2 * t}%", "Suma los dos porcentajes, pero el segundo aumento es sobre un precio que ya había subido."),
             (f"{t}%", "Cuenta un solo año."),
             (pct(F(t, 100) ** 2), "Multiplica los porcentajes entre sí.")],
            ["Arranca en 100", f"Primer año: 100 + {t}% = 120", f"Segundo año, sobre 120: 120 + 24 = 144",
             f"144 contra 100: subió {pct(r)}"],
            "El segundo aumento se calcula sobre lo que ya creció. Por eso da más que sumar los dos porcentajes.",
            "Multiplica el factor por sí mismo: 1,2 × 1,2 = 1,44, y le quitas el 1.",
            datos=dict(modo="pct", t=t, n=2))
    cap, t, u, ctx = [
        (1000, 10, "año", "Inviertes {c} al {t}% anual y los intereses se suman al capital. ¿Cuánto tienes después de 2 años?"),
        (2000, 5, "mes", "Un ahorro de {c} rinde {t}% mensual y lo ganado se suma cada mes. ¿Cuánto hay después de 2 meses?"),
        (800, 25, "trimestre", "Una app tiene {c} usuarios y cada trimestre crece {t}% sobre los que tiene en ese momento. ¿Cuántos usuarios tiene después de 2 trimestres?"),
    ][v]
    fmt = (lambda x: fnum(x)) if u == "trimestre" else (lambda x: pesos(x))
    uno = cap * (1 + F(t, 100))
    r = uno * (1 + F(t, 100))
    return P("Crecimiento compuesto", ctx.format(c=fmt(cap), t=t), (r, fmt(r)),
        [(fmt(cap * (1 + F(2 * t, 100))), f"Suma {2 * t}% de una vez, como si el segundo aumento fuera sobre el valor inicial."),
         (fmt(uno), f"Cuenta un solo {u}."),
         (fmt(cap * (1 + F(t * t, 10000))), "Multiplica los porcentajes entre sí.")],
        [f"Primer {u}: {fmt(cap)} + {t}% = {fmt(uno)}",
         f"Segundo {u}, sobre {fmt(uno)}: {fmt(uno)} + {fmt(uno * F(t, 100))} = {fmt(r)}"],
        "El segundo aumento se calcula sobre lo que ya creció, no sobre el valor inicial. Por eso da un poco más que sumar los porcentajes.",
        f"Multiplica el factor por sí mismo: {fnum(1 + F(t, 100))} × {fnum(1 + F(t, 100))} = {fnum((1 + F(t, 100)) ** 2, 4)}.",
        datos=dict(modo="valor", cap=cap, t=t, n=2))


# nivel: 1 fácil, 2 medio, 3 difícil. Dentro de cada tanda se ordena por nivel.
TIPOS = [
    (g_crecimiento, 1), (g_caida, 1), (g_pct_numero, 1), (g_complemento, 1), (g_parte_total, 1),
    (g_promedio, 1), (g_regla3, 1),
    (g_ponderado, 2), (g_razon, 2), (g_reparto, 2), (g_inversa, 2), (g_veces, 2), (g_embudo_total, 2),
    (g_tipo_cambio, 2), (g_comision, 2), (g_velocidad, 2), (g_tabla, 2),
    (g_embudo_perdida, 3), (g_runway, 3), (g_sucesivos, 3), (g_volver, 3), (g_precio_original, 3),
    (g_ecuacion, 3), (g_secuencia, 3), (g_compuesto, 3),
]


# ─────────────────────────── verificador independiente ───────────────────────────
# Resuelve cada pregunta de nuevo desde los datos crudos, por otro camino, sin mirar la clave.

def verificar(q):
    t, d = q.tipo, q.datos
    if t == "Crecimiento porcentual":
        return F(d["b"] * 100, d["a"]) - 100
    if t == "Caída porcentual":
        return 100 - F(d["b"] * 100, d["a"])
    if t == "Porcentaje de un número":
        return F(d["n"]) / 100 * d["p"]
    if t == "El NO":
        if d["modo"] == "doble":
            return next(k for k in range(d["n"] + 1)
                        if k == d["n"] * F(100 - d["p1"], 100) * F(100 - d["p2"], 100))
        return F(d["n"] * (100 - d["p"]), 100)
    if t == "Parte sobre total":
        tot = sum(x for _, x in d["filas"])
        return F(sum(x for n, x in d["filas"] if n in d["pide"]) * 100, tot)
    if t == "Promedio simple":
        if d["modo"] == "agrega":
            return F(d["prom"] * d["n"] + d["nuevo"], d["n"] + 1)
        return F(sum(d["datos"]), len(d["datos"]))
    if t == "Regla de tres directa":
        return F(d["t2"], d["t"]) * d["q"]
    if t == "Promedio ponderado":
        personas = [m for n, m in d["grupos"] for _ in range(n)]
        return F(sum(personas), len(personas))
    if t == "Razones":
        a, b = d["a"], d["b"]
        for k in range(1, 1000):
            if d["modo"] == "dif" and k * (a - b) == d["valor"]:
                return F(k * (a + b))
            if d["modo"] == "grupo" and k * (a if d["conocido"] == "a" else b) == d["valor"]:
                return F(k * (a + b))
    if t == "Reparto proporcional":
        if d["modo"] == "aportes":
            return F(d["total"]) * d["aportes"][d["i"]] / sum(d["aportes"])
        return F(d["total"]) * max(d["partes"]) / sum(d["partes"])
    if t == "Proporción inversa":
        return next(F(k, 10) for k in range(1, 10000) if F(k, 10) * d["p2"] == d["p"] * d["d"])
    if t == "Veces, porcentaje y puntos":
        r1, r2 = d["r1"], d["r2"]
        if d["modo"] == "pct":
            return abs(F((r2 - r1) * 100, r1))
        if d["modo"] == "veces":
            return F(r2, r1)
        return F(r2 - r1)
    if t == "Embudo: conversión total":
        e = [x for _, x in d["etapas"]]
        if d["modo"] == "total":
            return F(e[3] * 100, e[0])
        if d["modo"] == "no2":
            return F((e[1] - e[3]) * 100, e[1])
        tasas = [F(e[i + 1], e[i]) for i in range(3)]
        x = F(e[0]) * F(6, 5)
        for r in tasas:
            x *= r
        return x
    if t == "Embudo: mayor pérdida":
        e = d["etapas"]
        conserva = [F(e[i + 1][1], e[i][1]) for i in range(3)]
        if len(set(conserva)) == 1:
            return "Todos los pasos pierden la misma proporción"
        i = min(range(3), key=lambda k: conserva[k])
        return f"De {e[i][0]} a {e[i + 1][0]}"
    if t == "Tipo de cambio":
        if d["modo"] == "simple":
            return F(d["monto"]) / d["tc"]
        if d["modo"] == "dos":
            return F(d["a"], d["tca"]) - F(d["b"], d["tcb"])
        return F(d["usd"] * d["tc"]) * F(100 + d["rec"], 100)
    if t == "Comisión: porcentaje más fijo":
        pagos = [F(d["m"]) * d["p"] / 100 + d["f"] for _ in range(d["n"])]
        return sum(pagos) if d["modo"] == "total" else d["n"] * d["m"] - sum(pagos)
    if t == "Caja: cuántos meses más":
        return abs(F(d["c"], d["b2"]) - F(d["c"], d["b"]))
    if t == "Velocidad, distancia y tiempo":
        m = d["modo"]
        if m == "tiempo":
            return F(d["km2"] * d["h"], d["km"])
        if m == "kmh":
            return F(d["km"]) / F(d["mins"], 60)
        if m == "vel":
            return F(d["km"]) / d["horas"]
        return F(2 * d["d"]) / (F(d["d"], d["v1"]) + F(d["d"], d["v2"]))
    if t == "Tablas":
        filas, modo = d["filas"], d["modo"]
        clave = (lambda f: F(f[1], f[2])) if modo == "baja" else (lambda f: F(f[-1], f[-2]))
        return max(filas, key=clave)[0]
    if t == "Porcentajes seguidos":
        final = F(100) + d["x"]
        final += final * F(d["y"], 100)
        return (final - 100) / 100
    if t == "Volver al precio original":
        queda = F(100 - d["d"])
        return (F(100) / queda - 1) * 100
    if t == "Precio original":
        if d["modo"] == "impuesto":
            return next(F(k) for k in range(1, 100000) if F(k) * F(100 + d["t"], 100) == d["pagado"])
        return next(F(k) for k in range(1, 100000) if F(k) * F(100 - d["d"], 100) == d["pagado"])
    if t == "Ecuaciones":
        for x in range(-100, 101):
            if F(d["a"] * x + d["b"], d["c"]) == F(d["d"] * x + d["e"], d["f"]):
                return F(x)
    if t == "Secuencias":
        s = d["serie"]
        if all(s[i] == s[i - 1] + s[i - 2] for i in range(2, len(s))):
            return F(s[-1] + s[-2])
        if len({F(s[i + 1], s[i]) for i in range(len(s) - 1)}) == 1:
            return F(s[-1] * s[1], s[0])
        difs = [s[i + 1] - s[i] for i in range(len(s) - 1)]
        dd = {difs[i + 1] - difs[i] for i in range(len(difs) - 1)}
        if len(dd) == 1:
            return F(s[-1] + difs[-1] + dd.pop())
        impares, pares = s[0::2], s[1::2]
        if len({impares[i + 1] - impares[i] for i in range(len(impares) - 1)}) == 1:
            sig = impares if len(impares) == len(pares) else pares
            return F(sig[-1] + sig[-1] - sig[-2])
    if t == "Crecimiento compuesto":
        f = F(100 + d["t"], 100) ** d["n"]
        return (f - 1) * 100 if d["modo"] == "pct" else d["cap"] * f
    raise AssertionError(f"sin verificador: {t}")


# ─────────────────────────────── armado ───────────────────────────────

def armar():
    rng = random.Random(SEMILLA)
    tandas = []
    for v in range(4):
        qs = [(nivel, gen(v)) for gen, nivel in TIPOS]
        ordenadas = []
        for nivel in (1, 2, 3):
            grupo = [q for n, q in qs if n == nivel]
            rng.shuffle(grupo)
            ordenadas += grupo
        tandas.append(ordenadas)
    todas = [q for t in tandas for q in t]
    libres = [q for q in todas if not q.fijas]
    pozo = list(LETRAS) * (len(libres) // 4) + list(LETRAS[: len(libres) % 4])
    fijas = {i: LETRAS[q.fijas.index(q.texto)] for i, q in enumerate(todas) if q.fijas}

    def racha_maxima(orden):
        it = iter(orden)
        seq = [fijas[i] if i in fijas else next(it) for i in range(len(todas))]
        mejor = actual = 1
        for x, y in zip(seq, seq[1:]):
            actual = actual + 1 if x == y else 1
            mejor = max(mejor, actual)
        return mejor

    rng.shuffle(pozo)
    while racha_maxima(pozo) > 2:      # que no salgan tres letras iguales seguidas
        rng.shuffle(pozo)
    letras = iter(pozo)
    for q in todas:
        q.armar(rng, None if q.fijas else next(letras))
    return tandas

def chequear(tandas):
    todas = [q for t in tandas for q in t]
    assert len(todas) == 100, len(todas)
    for i, q in enumerate(todas, 1):
        esperado = verificar(q)
        assert esperado == q.valor, f"Pregunta {i} ({q.tipo}): la clave dice {q.valor}, el verificador {esperado}"
        if isinstance(q.valor, F):
            assert exacto(q.valor, 2) or (q.valor * 3).denominator == 1, f"Pregunta {i}: respuesta con decimales feos {q.valor}"
    return todas


CSS = """@page{size:A4;margin:14mm 14mm 16mm}
*{box-sizing:border-box}
body{font-family:"Helvetica Neue",Arial,sans-serif;font-size:11.5pt;line-height:1.42;color:#111;margin:0;
     -webkit-print-color-adjust:exact;print-color-adjust:exact}
h1{font-size:22pt;margin:0 0 6pt}
h2{font-size:15pt;margin:0 0 10pt;padding-bottom:4pt;border-bottom:2px solid #111}
h3{font-size:12.5pt;margin:12pt 0 4pt}
.portada{break-after:page}
.portada ul{padding-left:18pt}
.portada li{margin:4pt 0}
.tanda{break-before:page}
.q{display:grid;grid-template-columns:1fr 32%;gap:10pt;break-inside:avoid;page-break-inside:avoid;
   border:1px solid #cfcfcf;border-radius:6px;padding:8pt 10pt;margin:0 0 9pt}
.qn{font-weight:700;font-size:12.5pt;margin-bottom:2pt}
.qt{margin:0 0 6pt}
.opts{display:flex;flex-wrap:wrap;gap:3pt 16pt}
.opts span{white-space:nowrap}
.work{border-left:1px dashed #b5b5b5;padding-left:8pt;color:#9a9a9a;font-size:9pt;min-height:78pt}
table.datos{border-collapse:collapse;margin:4pt 0 6pt}
table.datos th,table.datos td{border:1px solid #aaa;padding:1.5pt 8pt;text-align:right}
table.datos th:first-child,table.datos td:first-child{text-align:left}
table.datos th{background:#f0f0f0}
.grilla{break-inside:avoid;border:2px solid #111;border-radius:6px;padding:8pt 12pt;margin-top:12pt}
.grilla table{border-collapse:collapse;width:100%}
.grilla td{border:1px solid #999;padding:5pt 6pt;width:20%;font-size:11pt}
.nota{font-size:11pt;color:#333}
.clave h3{margin:8pt 0 3pt}
.clave table{border-collapse:collapse;margin:0 0 4pt;width:100%;break-inside:avoid;table-layout:fixed}
.clave td{border:1px solid #999;padding:1.5pt 5pt;font-size:11pt;text-align:center;line-height:1.25}
.r{border-top:1px solid #bbb;padding:6pt 0 4pt;orphans:3;widows:3}
.r .rh,.r .rq{break-inside:avoid;break-after:avoid}
.r li,.r p{break-inside:avoid}
.rh{font-size:13pt;font-weight:700}
.tipo{font-weight:400;font-size:11pt;color:#555;margin-left:6pt}
.rq{background:#f4f4f4;border-radius:5px;padding:4pt 8pt;margin:4pt 0;line-height:1.32}
.r p{margin:3pt 0}
.r{line-height:1.33;font-size:11pt}
.r ol,.r ul{margin:1pt 0 3pt;padding-left:18pt}
.r li{margin:1pt 0}
.lbl{font-weight:700}
.trucos .bloque{break-inside:avoid;margin:0 0 10pt}
.trucos table{border-collapse:collapse;margin:4pt 0}
.trucos td,.trucos th{border:1px solid #aaa;padding:2pt 8pt}
"""

def html_doc(titulo, cuerpo):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f"<style>{CSS}</style></head><body>{cuerpo}</body></html>")

def cuadernillo(tandas):
    partes = ["""<section class="portada">
<h1>Práctica de razonamiento numérico</h1>
<p>100 preguntas en 4 tandas de 25. Cada tanda es una sentada.</p>
<h3>Cómo usarlo</h3>
<ul>
<li><b>Sin calculadora.</b> Papel y lápiz, como en los tests de verdad.</li>
<li><b>Entre 60 y 75 segundos por pregunta.</b> Una tanda son unos 30 minutos. Anota la hora de inicio y la de fin.</li>
<li><b>Escribe tu razonamiento</b> en el espacio de la derecha de cada pregunta. Cuando corrijas, eso te dice si fallaste la cuenta o la lectura.</li>
<li>Si una se traba, marca la que te parezca y sigue. En el test real, una sin contestar cuenta como mala.</li>
<li><b>No mires las respuestas hasta terminar la tanda.</b> Anota las letras en la grilla del final y recién ahí abre la hoja de respuestas.</li>
</ul>
<h3>Antes de cada cuenta, dos preguntas</h3>
<ul>
<li><b>¿Qué me están preguntando?</b> Busca la palabra que manda: NO, más, proporción, respecto de, veces, puntos.</li>
<li><b>¿Sobre quién?</b> Casi siempre la base es el número de antes.</li>
</ul>
</section>"""]
    n = 0
    for ti, t in enumerate(tandas, 1):
        partes.append(f'<section class="tanda"><h2>Tanda {ti} · preguntas {n + 1} a {n + len(t)}</h2>')
        for q in t:
            n += 1
            q.numero = n
            opts = "".join(f"<span><b>{LETRAS[i]})</b> {o}</span>" for i, o in enumerate(q.opciones))
            partes.append(f'<div class="q"><div><div class="qn">{n}.</div><div class="qt">{q.enunciado}</div>'
                          f'<div class="opts">{opts}</div></div><div class="work">Tu cuenta</div></div>')
        filas = []
        nums = [q.numero for q in t]
        for i in range(0, len(nums), 5):
            filas.append("<tr>" + "".join(f"<td><b>{k}.</b> ______</td>" for k in nums[i:i + 5]) + "</tr>")
        partes.append(f'<div class="grilla"><h3>Tus respuestas de la tanda {ti}</h3><table>{"".join(filas)}</table>'
                      f'<p class="nota">Inicio ______ · Fin ______ · Buenas ______ de {len(t)}</p></div></section>')
    return html_doc("Práctica de razonamiento numérico", "".join(partes))

TRUCOS = [
    ("base", "¿Sobre quién? El de antes",
     "<p>Todo porcentaje de cambio se divide sobre el número de antes, sea el grande o el chico. En un crecimiento el de antes es el menor; en una caída o en un embudo es el mayor.</p>"),
    ("atajo", "El atajo: nuevo sobre viejo",
     "<p>Divides el número nuevo sobre el viejo. Si creció, le quitas el 1: 520 ÷ 400 = 1,30, creció 30%. Si cayó, se lo quitas a 1: 3.000 ÷ 5.000 = 0,60, cayó 40%.</p>"),
    ("fracciones", "Fracciones que conviene saber de memoria",
     "<table><tr><th>Fracción</th><th>Decimal</th><th>%</th></tr>"
     + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in [
         ("1/2", "0,5", "50%"), ("1/3", "0,33", "33,3%"), ("2/3", "0,67", "66,7%"), ("1/4", "0,25", "25%"),
         ("3/4", "0,75", "75%"), ("1/5", "0,2", "20%"), ("1/8", "0,125", "12,5%"), ("3/8", "0,375", "37,5%"),
         ("1/10", "0,1", "10%")])
     + "</table><p>Para simplificar, divide arriba y abajo por el mismo número: 6/8 = 3/4.</p>"),
    ("diez", "El truco del 10%",
     "<p>El 10% es correr la coma un lugar. De ahí sale casi todo: el 5% es su mitad, el 1% es su décima parte, el 30% son tres veces el 10%, y el 15% es el 10% más el 5%.</p>"),
    ("no", "Las preguntas con NO",
     "<p>Calcula directo el porcentaje de los que no (100% menos el dato) y aplícalo. Antes, repite la pregunta con la base adelante: de tantos, ¿cuántos NO?</p>"),
    ("veces", "Veces, porcentaje y puntos",
     "<table><tr><th>Te preguntan</th><th>De 4% a 5%</th></tr><tr><td>¿Cuántas veces?</td><td>5 ÷ 4 = 1,25 veces</td></tr>"
     "<tr><td>¿Qué porcentaje?</td><td>5 ÷ 4 = 1,25, le quitas el 1: 25%</td></tr><tr><td>¿Cuántos puntos?</td><td>5 − 4 = 1 punto</td></tr></table>"),
    ("seguidos", "Porcentajes seguidos: multiplica los factores",
     "<p>Subir 20% es multiplicar por 1,2 y bajar 20% es multiplicar por 0,8. Dos cambios seguidos se multiplican: 1,2 × 0,8 = 0,96, o sea 4% menos. Nunca se suman.</p>"),
    ("reves", "Descuentos e impuestos al revés",
     "<p>Si pagaste $240 con 20% de descuento, pagaste el 80%: el original es 240 ÷ 0,8 = 300. Para volver de un precio rebajado al original, la subida va sobre el precio rebajado: después de bajar 20% hay que subir 25%.</p>"),
    ("ponderado", "Promedio ponderado",
     "<p>Recuperas el total de cada grupo (cantidad × promedio), sumas todo y divides por la cantidad total. La respuesta siempre queda más cerca del promedio del grupo grande.</p>"),
    ("razones", "Razones y repartos por partes",
     "<p>Una razón 5:4 son 9 partes iguales. Primero averiguas cuánto vale una parte y después multiplicas. El total siempre es múltiplo de la suma de la razón.</p>"),
    ("inversa", "Directa o inversa",
     "<p>Pregúntate si al subir una cantidad la otra sube (directa) o baja (inversa). En la inversa, multiplica para sacar el trabajo total (4 personas × 6 días = 24) y divide por la cantidad nueva.</p>"),
    ("embudos", "Embudos",
     "<p>Conversión total: última etapa sobre la primera. Pérdida de un paso: lo que se pierde sobre la etapa de arriba. La resta más grande casi siempre está en el primer paso, y no por eso es la mayor proporción.</p>"),
    ("moneda", "Tipo de cambio",
     "<p>A la moneda que vale más se pasa dividiendo, a la que vale menos se pasa multiplicando. Chequeo: un dólar son muchos pesos, así que en dólares el número tiene que quedar más chico.</p>"),
    ("caja", "Caja y diferencias",
     "<p>Cuántos meses más es una resta: después menos antes. Son dos divisiones y una resta, y la respuesta nunca es la duración nueva.</p>"),
    ("velocidad", "Velocidad",
     "<p>Tiempo = distancia ÷ velocidad. Los minutos se pasan a fracción de hora: 30 minutos es 0,5 y 45 minutos es 0,75. Ida y vuelta a velocidades distintas: distancia total sobre tiempo total, nunca el promedio de las velocidades.</p>"),
    ("ecuaciones", "Ecuaciones con fracciones",
     "<p>Multiplicas en cruz: cada denominador pasa multiplicando al otro lado. Pasas las x a un lado y los números al otro. Si te traba, prueba las opciones en la ecuación original.</p>"),
    ("secuencias", "Secuencias",
     "<p>Orden para probar: diferencia fija, diferencias que crecen, multiplicar por lo mismo, sumar los dos anteriores, dos series intercaladas (posiciones pares e impares).</p>"),
    ("estimar", "Estima y descarta",
     "<p>Antes de calcular, estima el orden: menos de la mitad, más del doble, más o menos 20. Casi siempre eso descarta dos opciones. Y si lo que te da no está entre las opciones, te faltó un paso o elegiste mal la base.</p>"),
]

REPASA = [
    ("Crecimiento porcentual", "base, atajo"), ("Caída porcentual", "base, atajo"),
    ("Porcentaje de un número", "diez, fracciones"), ("El NO", "no, diez"),
    ("Parte sobre total", "estimar, fracciones"), ("Promedio simple", "ponderado, estimar"),
    ("Regla de tres directa", "inversa"), ("Promedio ponderado", "ponderado"),
    ("Razones", "razones"), ("Reparto proporcional", "razones"), ("Proporción inversa", "inversa"),
    ("Veces, porcentaje y puntos", "veces, base"), ("Embudo: conversión total", "embudos, no"),
    ("Embudo: mayor pérdida", "embudos, base"), ("Tipo de cambio", "moneda"),
    ("Comisión: porcentaje más fijo", "diez"), ("Caja: cuántos meses más", "caja"),
    ("Velocidad, distancia y tiempo", "velocidad"), ("Tablas", "atajo, base"),
    ("Porcentajes seguidos", "seguidos"), ("Volver al precio original", "reves, base"),
    ("Precio original", "reves"), ("Ecuaciones", "ecuaciones"), ("Secuencias", "secuencias"),
    ("Crecimiento compuesto", "seguidos"),
]

def hoja_respuestas(tandas):
    titulos = {k: t for k, t, _ in TRUCOS}
    partes = ["""<section class="portada">
<h1>Hoja de respuestas</h1>
<h3>Cómo corregir</h3>
<ul>
<li>Primero corrige la tanda entera con la <b>clave rápida</b> de abajo y anota cuántas tuviste bien.</li>
<li>Después lee la explicación de <b>las que fallaste</b> y compárala con lo que escribiste al lado de la pregunta: ¿fue la cuenta o fue la lectura?</li>
<li>Cada explicación dice qué error lleva a cada opción incorrecta. Si caíste en una trampa, ahí está el nombre de tu error.</li>
<li>Al final está la <b>hoja de trucos</b> y una tabla que dice qué truco repasar según el tipo de pregunta que fallaste.</li>
</ul>
<div class="clave">"""]
    for ti, t in enumerate(tandas, 1):
        partes.append(f"<h3>Clave rápida · tanda {ti}</h3><table>")
        for i in range(0, len(t), 5):
            partes.append("<tr>" + "".join(f"<td><b>{q.numero}.</b> {q.letra}</td>" for q in t[i:i + 5]) + "</tr>")
        partes.append("</table>")
    partes.append("</div></section>")
    for ti, t in enumerate(tandas, 1):
        partes.append(f'<section class="tanda"><h2>Tanda {ti} · explicaciones</h2>')
        for q in t:
            otras = "".join(f"<li><b>{LETRAS[i]}) {o}</b>: {q.errores[o]}</li>"
                            for i, o in enumerate(q.opciones) if o != q.texto)
            cuenta = "".join(f"<li>{c}</li>" for c in q.cuenta)
            opts = " · ".join(f"{LETRAS[i]}) {o}" for i, o in enumerate(q.opciones))
            truco = f'<p><span class="lbl">Truco:</span> {q.truco}</p>' if q.truco else ""
            partes.append(
                f'<div class="r"><div class="rh">{q.numero}. {q.letra}) {q.texto}<span class="tipo">{q.tipo}</span></div>'
                f'<div class="rq">{q.enunciado}<br>{opts}</div>'
                f'<p class="lbl">La cuenta</p><ol>{cuenta}</ol>'
                f'<p><span class="lbl">Por qué:</span> {q.porque}</p>'
                f'<p class="lbl">Las otras opciones</p><ul>{otras}</ul>{truco}</div>')
        partes.append("</section>")
    partes.append('<section class="tanda trucos"><h2>Hoja de trucos</h2>')
    for _, titulo, cuerpo in TRUCOS:
        partes.append(f'<div class="bloque"><h3>{titulo}</h3>{cuerpo}</div>')
    filas = "".join(f"<tr><td>{tipo}</td><td>{' · '.join(titulos[k.strip()] for k in ks.split(','))}</td></tr>"
                    for tipo, ks in REPASA)
    partes.append(f'<div class="bloque"><h3>Si fallaste este tipo, repasa este truco</h3>'
                  f"<table><tr><th>Tipo de pregunta</th><th>Truco</th></tr>{filas}</table></div></section>")
    return html_doc("Hoja de respuestas", "".join(partes))


def paginas(pdf):
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes())) or "?"

def navegador():
    for n in NAVEGADORES:
        if n and (pathlib.Path(n).exists() or shutil.which(n)):
            return n
    sys.exit("⛔ No encontré Chrome, Chromium, Edge ni Brave. Pásale la ruta: CHROME=/ruta python3 generar.py")

def main():
    tandas = armar()
    todas = chequear(tandas)
    tipos = {q.tipo for q in todas}
    assert len(tipos) == 25, len(tipos)
    docs = {"preguntas": cuadernillo(tandas), "respuestas": hoja_respuestas(tandas)}
    for nombre, h in docs.items():
        texto = re.sub(r"<[^>]+>", " ", h)
        assert "—" not in h and "–" not in h, f"{nombre}: hay raya larga"
        voseo = re.findall(r"\b(vos|tenés|querés|podés|sabés|mirá|hacé|poné|fijate|dale|contame|sumate|escribinos|agregá|usá|calculá|anotá|elegí|revisá)\b", texto, re.I)
        assert not voseo, f"{nombre}: voseo {voseo}"
    chrome = navegador()
    with tempfile.TemporaryDirectory() as tmp:
        for nombre, h in docs.items():
            ruta = pathlib.Path(tmp) / f"{nombre}.html"
            ruta.write_text(h, encoding="utf-8")
            pdf = AQUI / f"{nombre}.pdf"
            pdf.unlink(missing_ok=True)
            subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", ruta.as_uri()], capture_output=True)
            if not pdf.exists():
                sys.exit(f"⛔ El navegador no generó {pdf.name}.")
            print(f"✅ {nombre}: {paginas(pdf)} páginas")
    letras = [q.letra for q in todas]
    print("Letras:", {l: letras.count(l) for l in LETRAS}, "· preguntas:", len(todas), "· tipos:", len(tipos))

if __name__ == "__main__":
    main()
