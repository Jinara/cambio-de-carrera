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
| No existe `02-evidencia.md` | Paso 2, skill `inventario-de-evidencia` |
| `02-evidencia.md` no tiene la tabla de límites completa | Paso 2, retomando |
| No existe `03-que-trabajo-quiero.md`, o no tiene la sección de carriles | Paso 3, skill `ejercicio-de-preferencias` |
| No existe `04-cv-maestro.md`, o no hay ninguna variante en `cv/` | Paso 4, skill `cv-y-postulacion`, partes 1 y 2 |
| No existe `06-banco-de-historias.md` o `07-narrativa.md` | Paso 5, skill `banco-de-historias`. Si todavía no mandó ninguna postulación, ofrécele primero la parte 3 del paso 4 |
| Hay una carpeta en `entrevistas/` con `brief.md` y sin `simulacro.md`, o con preguntas sin cortar | Paso 7, skill `simulacro`, para esa empresa |
| Está todo | Pregúntale qué necesita: el link de un aviso nuevo (paso 4, parte 3), o el correo de una empresa que le escribió (paso 6, skill `brief-de-entrevista`) |

## 3. Decirlo y arrancar

Dile en una línea dónde está y qué sigue. Por ejemplo: *"Ya tienes el descubrimiento y la evidencia. Sigue qué trabajo quieres: para eso necesito entre 15 y 30 avisos reales."*

Y arranca la skill que toca. No le preguntes si quiere empezar: escribió `/empezar`.

**Si la persona pega el correo de una empresa que le escribió para entrevistar**, eso manda sobre la tabla: va el paso 6 para esa empresa, aunque le falten pasos anteriores. Avísale qué le falta (sin el paso 5 no hay historias para asignar a las preguntas) y arranca igual.

## Si la persona quiere saltar a un paso

Puede. Pero si pide el paso 4 sin tener el 2, dile de frente qué pasa: el CV solo puede sacar números de la evidencia, así que sin el paso 2 sale un CV sin números o con números sin fuente. Y que decida.
