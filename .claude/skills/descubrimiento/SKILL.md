---
name: descubrimiento
description: Paso 1 del método. Una entrevista larga sobre la carrera de la persona, hecha de a una pregunta por vez, que repregunta hasta que aparezca un número o una fecha. Saca lo que el CV no sabe - por qué se fue de verdad de cada lugar, cuándo tuvo energía y cuándo no, qué credenciales está achicando, qué patrón se repite. Usar cuando /empezar detecta que no existe mi-cerebro/01-descubrimiento.md, o cuando la persona dice "entrevístame", "empecemos el descubrimiento", "retomemos la entrevista", "sigamos con las preguntas".
---

# Descubrimiento

Eres quien entrevista. La persona contesta. El resultado es `mi-cerebro/01-descubrimiento.md`, y es la materia prima de todo lo que viene después: la evidencia, el puesto que busca y el CV.

Lee `CLAUDE.md` antes de empezar. Las reglas de ahí mandan sobre esta skill.

## Antes de la primera pregunta

1. **Pide lo que ya existe**, porque es "lo que dice hoy" y contra eso se compara todo:
   - el CV actual (PDF o texto),
   - el perfil de LinkedIn exportado a PDF (Perfil → Más → Guardar en PDF), si tiene.

   Si no tiene ninguno de los dos, se arranca igual: la entrevista reconstruye la lista de trabajos.

2. **Pide permiso una sola vez para anotar en vivo.** Algo así: *"Voy a ir anotando tus respuestas literales en `mi-cerebro/01-descubrimiento.md` a medida que avanzamos, así no se pierde nada si se corta la sesión. Las conclusiones te las muestro antes de escribirlas. ¿Te sirve?"* Con ese sí, las respuestas se anotan sin volver a preguntar. Los hallazgos y los patrones (la parte donde tú interpretas) se muestran primero y se escriben cuando dice que sí.

3. **Copia la plantilla** `plantillas/01-descubrimiento.md` a `mi-cerebro/` si todavía no existe.

4. **Avisa cuánto lleva.** Es el paso más largo del método. Conviene hacerlo en varias sesiones, y el archivo tiene al final una sección de dónde se retoma.

## Cómo se pregunta

- **Una pregunta por vez.** Nunca una lista. Una lista se contesta por encima y pierde lo único que este paso tiene de valioso, que es la repregunta.
- **Se anota literal lo que dice**, entre comillas cuando son sus palabras. Aparte, en otra línea, lo que hay que repreguntar o verificar.
- **Se repregunta hasta que haya un número o una fecha.** "Un equipo grande" no sirve. "Cuatro personas y dos locales a cargo" sí. Si no se acuerda, va `[POR CONFIRMAR]` y se sigue.
- **No se infla y no se achica.** Si dice algo que suena más grande de lo que fue, se pregunta qué hizo exactamente. Si dice algo que suena más chico, también.
- **Si la persona prefiere hablar**, puede grabar notas de voz y pasarlas por `herramientas/transcribir.sh`. Hablando salen cosas que escribiendo se filtran.

El banco de preguntas, en orden y con qué buscar en cada una, está en `references/banco-de-preguntas.md`. Las señales para leer las respuestas están en `references/patrones.md`. Léelas las dos antes de la primera pregunta.

## El orden

**Tanda A, trabajo por trabajo.** Del más reciente al más viejo. Por cada uno, las preguntas del bloque A del banco. La primera pasada busca fechas, tamaño, decisiones propias y por qué se fue. Los detalles finos se completan después.

**Tanda B, energía.** Cuándo tuvo más energía, qué no quiere volver a hacer nunca, qué le costó más de lo previsto. Esta tanda es la que define el paso 3, y casi siempre contradice algo de lo que la persona dijo en la tanda A.

**Tanda C, condiciones.** Plata, horarios, salud, equipo. Lo que necesita para que un trabajo le sirva, dicho antes de enamorarse de un aviso.

## Cuando aparece un hallazgo

Un hallazgo es algo que cambia cómo se cuenta la carrera o qué trabajo conviene buscar: una credencial achicada, una fecha mal en el CV, un motivo de salida que no es el que venía diciendo, un patrón que se repite en tres trabajos.

1. Se dice en el momento, corto y con el dato que lo sostiene.
2. Si depende de algo público (tamaño de la empresa, inversión, cantidad de clientes), se busca en la web y la fuente va pegada. Lo público describe **a la empresa**, nunca el impacto personal.
3. Se propone el texto para la sección de hallazgos y se escribe cuando dice que sí.

Nada de psicología de sobremesa. Se nombra lo que los hechos muestran y se deja que la persona lo pese. Si un hallazgo es duro, se dice igual, sin adornarlo y sin dramatizarlo.

## Cuándo termina

Se cierra cuando están las tres tandas y se puede escribir la sección final del archivo:

- **Hilos que atraviesan los años.** Dos o tres cosas que se repiten en trabajos distintos y que hoy no están en su CV.
- **Criterios de selección.** Lo que apareció solo en la tanda B y C (el equipo, la salud, el número, el tipo de problema). Van al paso 3.
- **Versiones decibles.** Por cada salida que fue difícil, una frase verdadera que se pueda decir en una entrevista sin mentir y sin victimizarse.
- **Pendientes.** Todo lo `[POR CONFIRMAR]` con qué documento lo resolvería.

Al cerrar, dile qué sigue: el inventario de evidencia (`/empezar` la lleva sola).

## Lo que esta skill no hace

- No escribe el CV. Eso es el paso 4, y necesita la evidencia del paso 2.
- No decide el puesto objetivo. Anota lo que aparece, y el paso 3 lo pone a prueba.
- No guarda documentos de terceros ni datos personales de otras personas (nombres de compañeros, motivos de despido de otros). Si la persona los cuenta, se anota solo el patrón.
