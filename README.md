# cambio-de-carrera

Este es el método que uso, empaquetado como skills para Claude Code. También funciona con Codex.

No promete trabajo ni es un curso. Es lo que hice para cambiar de carrera, y lo comparto porque me sirvió ordenarlo.

Por qué lo armé, contado por mí, está en [`BIENVENIDA.md`](BIENVENIDA.md). Es lo primero que vas a leer cuando empieces.

La idea de fondo cabe en una línea: **cada cosa que digas sobre ti tiene que tener una prueba detrás.** Un entrevistador senior huele el adorno en una pregunta, y ahí se cae todo lo que digas después. La precisión es lo único que no se puede falsificar.

## Qué necesitas

**Claude Code o Codex, instalado en tu computadora.** No hay versión que se lea sola, y es a propósito.

El método funciona porque algo te repregunta hasta que sueltas el número, y eso un PDF con las mismas preguntas no lo hace. Si no lo vas a instalar, este repo no te va a servir.

```bash
git clone https://github.com/Jinara/cambio-de-carrera
cd cambio-de-carrera
claude
```

Y adentro de Claude Code, una sola cosa:

```
/empezar
```

Con Codex, creas un proyecto con la carpeta del repo y escribes `empezar`, sin la barra. Cómo bajar Codex y crear el proyecto está en [`EMPEZAR.md`](EMPEZAR.md#si-usas-codex).

Para generar el CV en PDF hace falta Python 3 y Chrome (o Chromium, Edge o Brave). Para el simulacro hablado, `whisper-cli` y `ffmpeg`. Qué juntar antes de arrancar y cómo instalar todo está en [`EMPEZAR.md`](EMPEZAR.md).

## Qué pones y qué recibes

Esto es lo que te pide cada paso y lo que te da. **Tres de los pasos no te piden juntar nada nuevo**: trabajan con lo que ya quedó escrito en los anteriores.

| Paso | Lo que pones | Lo que recibes |
|---|---|---|
| **1. Descubrimiento** | Tu tiempo, tu CV actual y tu LinkedIn en PDF | Lo que tu CV no sabe: por qué te fuiste de verdad de cada lugar, qué patrón se repite, qué credencial estás achicando |
| **Tu voz** (cierra el 1) | Nada nuevo | Con qué verbos hablas tú de tu trabajo y qué palabras de tu oficio usas, para que nada de lo que venga después salga del molde |
| **2. Evidencia** | Certificados, contratos, evaluaciones, correos, y acceso a tus datos si los tienes | Cada cosa que puedes afirmar, con su fuente al lado, y escrito qué NO cubre tu evidencia |
| **3. Qué trabajo quiero** | Dos o tres títulos que crees que quieres, y dos o tres que crees que no. Los avisos los trae el barrido | **A qué puestos postularte**, con los títulos exactos para buscarlos, **cuánto paga cada uno**, qué CV le va a cada uno, y qué te falta para el que está más lejos |
| **4. CV y postulación** | Nada nuevo para el CV. Para cada postulación, el aviso | Un CV por cada tipo de puesto, en PDF y DOCX que los sistemas de selección leen bien. Y por aviso, el veredicto antes de llenar nada y las respuestas listas para pegar |
| **5. Banco de historias** | Nada nuevo | Tus historias en 30 segundos y en 2 minutos, y qué historia va con qué pregunta |
| **6. Brief de entrevista** | El correo de quien te escribió | Qué formato te espera, qué venden y cómo están, qué te van a preguntar y con qué contestas |
| **7. Simulacro** | Tu voz, grabada | Qué se te cae cuando lo dices en voz alta, comparando tus tomas contra el reloj y contra tu propia evidencia |
| **La búsqueda** | Las empresas que te interesan | Un registro de cada vacante, los avisos nuevos que aparecen solos, y el tablero de cómo va |

**El paso 3 es el que contesta lo que viniste a buscar.** Es también el que más cuesta empezar, porque el CV se parece a lo que ya conocías y esto no. El método te frena y te dice qué se rompe.

## Los siete pasos

### De saber qué trabajo quieres a mandar el CV

**1. Descubrimiento.** Una entrevista larga sobre tu carrera, hecha por el asistente, que repregunta hasta que haya un número o una fecha. Saca lo que no está en ningún lado, como por qué te fuiste de verdad de cada lugar o en qué momentos de tu carrera tuviste más energía.

**2. Evidencia.** Junta la prueba de lo que hiciste, cada afirmación con su fuente. Sirve si tienes tus propios datos y sirve si no tienes acceso a nada de tus trabajos anteriores: ahí la prueba sale de certificados, evaluaciones, correos y números públicos de las empresas. Y antes de dejarte usar un solo número, te obliga a escribir qué NO cubre tu evidencia. Si tus registros arrancan en 2022, cualquier cifra tuya de antes es un piso, no un total, y hay que decirlo así.

**3. Qué trabajo quiero.** Ocho pares de "lunes" sacados de avisos reales, sin decirte de qué puesto es cada uno. Eliges lunes, no títulos. Es el paso más raro y el que más descoloca, porque casi siempre el resultado no es el puesto que decías querer. Después se cruza con tres cosas más: lo que puedes probar, lo que piden los avisos (contado, no a ojo) y la plata que necesitas.

**Es el paso que contesta lo que viniste a buscar**, y termina leyéndotelo: a qué puestos te postulas, con los títulos exactos para buscarlos, cuánto paga cada uno y dónde cae tu objetivo, qué CV le va a cada uno, y qué te falta para el que está más lejos. Los avisos no los juntas tú: el barrido te los trae.

⚠️ Y es el que más cuesta empezar. Si te lo saltas, el método te frena y te dice qué pasa: terminas con un CV genérico y sin saber a qué postularte.

**4. CV y postulación.** Un CV maestro que sale solo de la evidencia verificada, y una variante por cada tipo de puesto, que nunca contradice al maestro. Un script lo pasa a PDF y se niega a generarlo si encuentra un número que ya corregiste. Y para cada aviso, **primero el veredicto por escrito** (qué pide, qué cumples, qué te falta, si conviene) y recién después las respuestas del formulario. Un formulario lleno empuja a enviar, así que la decisión se toma antes de llenarlo. Al botón de Enviar le das clic tú.

**Y la búsqueda, mientras dure.** Un registro de cada vacante, con qué CV la mandaste y qué pasó después. Un barrido que mira los boards de empleo de las empresas que elegiste (Greenhouse, Lever, Ashby y Recruitee) varias veces por día, filtra por los carriles del paso 3 y te avisa lo nuevo. El mismo barrido corre antes, en modo exploración, para traerte los avisos que el paso 3 necesita. Un lector de correo que entiende lo que te contestan las empresas: actualiza el registro, archiva los acuses, los rechazos y las alertas de LinkedIn, deja en la bandeja lo que hay que contestar y te avisa. No manda ni borra nada, y los correos que no son de la búsqueda no salen de tu computadora. Y un tablero en tu navegador con tus vacantes por estado, las que llevan dos semanas sin respuesta y el experimento: cuántas te respondieron por carril y por CV, con el aviso de que con pocas postulaciones todavía no se puede concluir nada.

```bash
python3 herramientas/tablero.py --cerebro ejemplo
```

Ese comando abre el tablero de Toffy, el ejemplo, para que lo veas antes de tener datos tuyos.

### Cuando te llaman

**5. Banco de historias.** Tu evidencia convertida en historias contables, en versión de 30 segundos y de 2 minutos, con una regla que no se negocia: cada historia lleva un error tuyo dicho de frente. Es lo que hace creíble todo lo bueno que venga después. Y la narrativa: la misma verdad en seis largos, y las preguntas difíciles con la trampa de cada una.

**6. Brief de entrevista.** Le pasas el correo de quien te escribió y arma el brief de esa empresa: qué formato de entrevista te espera, qué venden y cómo están (con fuentes, y separando lo que es un hecho de lo que es una suposición tuya), qué preguntas son probables y qué historia va con cada una.

**7. Simulacro.** Te hace la pregunta, lees un papel de cinco renglones, grabas tu respuesta en audio, se transcribe en tu máquina y te devuelve el feedback. Un script compara tus tomas y encuentra lo que leyendo no se ve, y lo principal es esto: **si el número te cambia entre una toma y la otra, ese número no está anclado a ninguna fuente.** Pasa mucho más de lo que uno cree.

Y si la empresa manda un **test numérico**, en [`practica/razonamiento-numerico/`](practica/razonamiento-numerico/) hay un simulacro de 10 preguntas cronometrado y un cuadernillo de 100 preguntas sin calculadora, en cuatro tandas. Y la hoja de respuestas explica qué error lleva a cada opción incorrecta, así que cuando fallas sabes cómo se llama tu error.

## Qué vas a tener al final

Tus archivos en `mi-cerebro/`:

| | Qué es |
|---|---|
| `01-descubrimiento.md` | Lo que tu CV no sabe, sacado a preguntas |
| `01-mi-voz.md` | Cómo hablas tú de tu trabajo: tus verbos, las palabras de tu oficio y lo que te achicas, para que el CV no salga del molde |
| `02-evidencia.md` | Todo lo que hiciste, con la fuente al lado, y lo que tu evidencia NO cubre declarado arriba |
| `03-que-trabajo-quiero.md` | El puesto objetivo elegido reaccionando al trabajo, tus criterios y lo que no |
| `04-cv-maestro.md` y `cv/` | El CV con todo, sus variantes, y los PDF |
| `05-postulaciones.md` | Tus datos fijos para formularios, las respuestas que reusas y un veredicto por aviso |
| `06-banco-de-historias.md` | Tus historias en dos largos, y qué historia va con qué pregunta |
| `07-narrativa.md` | La misma verdad en seis largos, y las preguntas difíciles con su trampa |
| `entrevistas/<empresa>/` | El brief de cada empresa, los papeles del simulacro y tus tomas |
| `numeros-retirados.txt` | Los números que corregiste, para que no vuelvan a salir |

Y los de la búsqueda, que se llenan solos mientras dure:

| | Qué es |
|---|---|
| `vacantes.json` | Cada vacante: de dónde salió, con qué CV la mandaste y qué pasó después |
| `barrido.json` y `barrido/` | Los filtros y las empresas del barrido, y lo que fue encontrando |
| `correo.json` y `correo/` | Qué cuenta lee el lector de correo, y qué correos ya procesó |

Esa carpeta **está ignorada por git desde el primer commit**. Vas a escribir ahí tu sueldo y las cosas que salieron mal. No se suben ni por accidente.

## El ejemplo

En [`ejemplo/`](ejemplo/) está el cerebro completo de **Toffy**, una persona inventada: nueve años en operaciones en Chile, sin ninguna base de datos propia, que decía querer ser Product Manager en una empresa grande de tecnología. Los siete pasos, de punta a punta: su descubrimiento y su voz, sus dos CV, sus postulaciones con su tablero, el brief de la primera empresa que la llamó y el simulacro de "cuéntame de ti" en tres tomas.

Si quieres ver de una lo que el método contesta, abre [`ejemplo/03-que-trabajo-quiero.md`](ejemplo/03-que-trabajo-quiero.md) y baja hasta "Lo que sale de acá". Ahí está lo que se le leyó a Toffy al cerrar ese paso, incluido que el puesto que decía querer al empezar no quedó en ningún carril.

Si quieres ver cómo termina esto antes de instalar nada, empieza por ahí.

## Privacidad

- `mi-cerebro/` está en `.gitignore`. Es donde va todo lo tuyo.
- El simulacro transcribe con Whisper **en tu máquina**. Tu voz no se sube a ningún lado, y los audios también están en `.gitignore`.
- No hay servidor ni cuenta que crear: es una carpeta con archivos de texto. El tablero corre en tu computadora y solo se puede abrir desde ella.
- Si activas el lector de correo, la clave queda en el llavero de tu sistema, no en el repo. Solo los correos de la búsqueda se mandan a Claude para clasificarlos, y Claude los lee sin herramientas: un correo con instrucciones escondidas no puede hacer que mande, borre ni toque nada.
- Con Codex, úsalo en tu computadora y no en la nube de ChatGPT. En la nube, tu `mi-cerebro/` quedaría en un servidor.

## Por qué el barrido corre en tu computadora

Lo intenté primero en la nube y no funciona: **la búsqueda de vacantes no se puede automatizar con agentes programados en la nube.** Los de Claude corren en un entorno sin salida a internet salvo a los dominios de Anthropic. Probé 26 barridos a boards de empleo y los 26 murieron con `connect_rejected`. Y el reemplazo obvio es peor que el problema: buscar vacantes por web devuelve puestos que ya cerraron. Una que encontré así daba 404 y no estaba en la API del board, o sea que existía solamente en el índice de Google.

Barrer boards funciona, pero en tu propia máquina. Cómo programarlo en Mac, Linux y Windows está en [`correrlo-solo.md`](.claude/skills/busqueda-de-vacantes/references/correrlo-solo.md).

## Licencia

MIT. Puedes usarlo y cambiarlo como te sirva.
