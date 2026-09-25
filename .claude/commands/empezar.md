---
description: La única puerta del método. Mira qué hay en mi-cerebro/ y lleva a la persona al paso que le toca.
---

# /empezar

Lee `AGENTS.md` primero. Después haz esto, en orden.

## 1. Chequeo de privacidad (solo la primera vez)

Si `mi-cerebro/` no tiene ningún archivo además de `LEEME.md`:

1. Si la carpeta es un repositorio de git, confirma que `mi-cerebro/` está ignorada:
   ```bash
   git check-ignore -q mi-cerebro/prueba.md && echo ignorada
   ```
   Si no dice `ignorada`, **para** y dile a la persona que revise `.gitignore` antes de escribir nada.
2. **La bienvenida de Nath, en tres partes.** `BIENVENIDA.md` tiene tres partes separadas por `---`. Muestra la primera tal cual, completa, sin resumirla ni cambiarle una palabra, y agrega al final una sola línea: *Escribe **siguiente** para seguir.* Termina tu mensaje ahí y espera. Cuando la persona conteste, muestra la segunda parte igual, con la misma línea al final, y espera otra vez. Después, la tercera. Si en vez de seguir la persona pregunta algo, contéstalo corto y vuelve a ofrecer *siguiente*.
3. Después de la tercera parte, lo práctico en tres o cuatro líneas: son siete pasos, cuatro para llegar a mandar el CV y tres para preparar entrevistas; todo queda en `mi-cerebro/` y no se sube a ningún lado; el primero es el más largo y conviene hacerlo en varias sesiones.
4. Pregúntale si ya tiene a mano lo de la lista de `EMPEZAR.md` (CV, LinkedIn en PDF, certificados, evaluaciones). No hace falta todo para arrancar: el paso 1 funciona solo con conversación.

## 2. Qué paso toca

Mira `mi-cerebro/` y decide:

| Si... | Toca |
|---|---|
| No existe `01-descubrimiento.md` | Paso 1, skill `descubrimiento` |
| Existe `01-descubrimiento.md` y su sección "Dónde retomamos" dice que falta algo | Paso 1, retomando desde ahí |
| `01-descubrimiento.md` está cerrado y no existe `01-mi-voz.md` | Skill `mi-voz`, que cierra el paso 1. Son 15 minutos y no hay preguntas nuevas. **Si además ya hay CV en `cv/`**, dile que después van a repasarlo con la voz al lado, y córrele el freno (`chequear.py --cv`) para mostrarle qué sale |
| No existe `02-evidencia.md` | Paso 2, skill `inventario-de-evidencia` |
| `02-evidencia.md` no tiene la tabla de límites completa | Paso 2, retomando |
| No existe `03-que-trabajo-quiero.md`, o no tiene la sección de carriles | Paso 3, skill `ejercicio-de-preferencias` |
| No existe `04-cv-maestro.md`, o no hay ninguna variante en `cv/` | Paso 4, skill `cv-y-postulacion`, partes 1 y 2 |
| Hay variantes en `cv/` y no existe `vacantes.json` | Ofrécele la búsqueda, skill `busqueda-de-vacantes`: el registro, el barrido y el tablero. Si prefiere seguir sin eso, sigue la fila de abajo |
| No existe `06-banco-de-historias.md` o `07-narrativa.md` | Paso 5, skill `banco-de-historias`. Si todavía no mandó ninguna postulación, ofrécele primero la parte 3 del paso 4 |
| Hay una carpeta en `entrevistas/` con `brief.md` y sin `simulacro.md`, o con preguntas sin cortar | Paso 7, skill `simulacro`, para esa empresa |
| Está todo | Pregúntale qué necesita: el link de un aviso nuevo (paso 4, parte 3), el correo de una empresa que le escribió (paso 6, skill `brief-de-entrevista`), o cómo va la búsqueda (skill `busqueda-de-vacantes`) |

**Antes de decirle qué sigue, si existe `barrido/hallazgos.json`:** cuéntale en una línea cuántos hallazgos nuevos hay sin decidir, y si el último barrido fue hace más de tres días o no pudo mirar nada. Y si `vacantes.py seguimiento` muestra postuladas con 14 días o más sin respuesta, díselo también. Son dos líneas, no una sesión aparte.

## 3. Decirlo y arrancar

Dile en una línea dónde está y qué sigue. Por ejemplo: *"Ya tienes el descubrimiento y la evidencia. Sigue qué trabajo quieres: para eso necesito entre 15 y 30 avisos reales."*

Y arranca la skill que toca. No le preguntes si quiere empezar: escribió `/empezar`.

**Si la persona pega el correo de una empresa que le escribió para entrevistar**, eso manda sobre la tabla: va el paso 6 para esa empresa, aunque le falten pasos anteriores. Avísale qué le falta (sin el paso 5 no hay historias para asignar a las preguntas) y arranca igual.

## Si la persona quiere saltar a un paso

**Se frena y se le dice qué se rompe.** Es la regla 13, y la tabla de qué se rompe en cada salto está ahí. En corto:

- **Sin el paso 2**, el CV sale sin números o con números que no va a poder defender.
- **Sin el paso 3**, y este es el que más duele: sale un CV genérico y **sin saber a qué postularse**. Sin carriles no hay variantes de CV, el barrido no tiene con qué filtrar y el experimento no mide nada. Dilo así de claro: *"El CV lo armamos igual si quieres, pero vas a terminar con uno solo y parejo para todo, y sin la lista de a qué puestos apuntar, que es lo que viniste a buscar."*
- **Sin `mi-voz`**, el CV sale con las palabras del molde.

**Y ofrece el camino corto antes de que decida.** Casi siempre la persona se salta el paso 3 porque cree que son horas de juntar avisos a mano, y ya no lo es: el barrido en modo exploración le trae 25 avisos reales en minutos (skill `busqueda-de-vacantes`, parte del barrido). Díselo con ese número.

Se espera la respuesta. Si igual quiere adelantarse, se hace, y queda anotado en el archivo que ese paso se saltó. No se insiste dos veces.
