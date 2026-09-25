# Sacar la voz del paso 1

El descubrimiento ya tiene todo lo que hace falta. Lo que sigue es cómo leerlo para encontrarlo, con el caso de Toffy resuelto entero. Su descubrimiento está en `ejemplo/01-descubrimiento.md` y el resultado en `ejemplo/01-mi-voz.md`.

## La lectura, en un solo pase

Se abre `01-descubrimiento.md` y se marca todo lo que está entre comillas. Eso es la voz. El resto del archivo son hechos, y los hechos ya viven en el paso 2.

Por cada cita se pregunta una sola cosa: **¿con qué verbo se puso ella en la escena?**

## Los cuatro patrones que aparecen siempre

### 1. El verbo encogido

Es el más común y el más caro. La persona usa un verbo que la saca del centro de algo que hizo ella.

> *"Yo solo apoyé el piloto."*

Las señales: *solo*, *un poco*, *ayudé con*, *estuve en*, *fui parte de*, *me tocó*. Cuando aparece un "solo" delante de un verbo, casi siempre hay una decisión propia escondida atrás.

Qué se hace: se busca en el mismo archivo qué dice la repregunta. En Toffy, la repregunta dice que diseñó la regla, armó la planilla de seguimiento y fue a los locales. Entonces a la tabla van los dos verbos, y el CV usa el que los hechos sostienen.

### 2. La escala encogida

Lo mismo pero con el tamaño.

> *"Una cadena de farmacias mediana."* La memoria anual dice 180 locales y 4.200 personas.

Va a la tabla de lo que se achica, con la fuente pegada. En el CV esto no se resuelve inflando a la persona: se resuelve con la línea de contexto de la empresa, que describe a la empresa y no a ella. Así queda *"Cadena de 180 farmacias en Chile (memoria anual 2025)"* y la persona no tuvo que decir nada grandilocuente de sí misma.

### 3. El número de goma

> *"Bajamos los quiebres un montón, y el subgerente dijo que nos ahorramos como 300 millones."*

Dos cosas distintas en la misma frase. Una tiene fuente (9,1% a 6,4%, está en la planilla) y la otra no (los 300 millones los dijo alguien en una reunión).

Acá la voz aporta algo que la evidencia sola no ve: **"un montón" es cómo ella mide.** Si mide en impresiones, en la entrevista va a volver a decir "un montón" y le van a repreguntar. Se anota en la tabla, y el simulacro lo entrena.

### 4. La palabra que se repite sin que se dé cuenta

Se cuentan las palabras de oficio que aparecen en varias respuestas distintas. En Toffy: *quiebres*, *locales*, *reposición*, *alertas*, *jefes de local*. Cinco palabras que aparecen en tres respuestas cada una.

Esas cinco van al CV sí o sí. Son la prueba de que estuvo adentro de una operación de verdad, y ningún molde las habría elegido.

## Lo que no se toma

- **Las muletillas.** *O sea*, *tipo*, *nada*, *la verdad que*. Son registro hablado. No van.
- **Los adjetivos sin dato.** *Increíble*, *tremendo*, *un desastre*. Se anota el hecho que hay debajo, no el adjetivo.
- **Lo que dijo de otras personas.** El jefe, el compañero, quien la despidió. Queda el patrón, sin nombres.
- **Lo que dijo estando enojada o triste**, salvo que ella pida guardarlo. En una entrevista eso no se usa, y tenerlo escrito no ayuda.

## Si el paso 1 quedó corto

Pasa cuando el descubrimiento se hizo rápido o cuando la persona contestó por escrito. Las citas son pocas y suenan a CV.

No se inventa. Se le dice qué falta y se le pide una cosa sola: **que cuente en voz alta un proyecto del que esté orgullosa, tres minutos, grabado.** Se transcribe con `herramientas/transcribir.sh` y de ahí sale más voz que de media hora de preguntas escritas.

La razón es simple: escribiendo, la gente se autocorrige hacia el molde. Hablando, no llega a hacerlo.

## Cómo queda, con Toffy

De su descubrimiento salieron:

- **Verbos que usa:** apoyé, ayudé con, estuve en. Los tres la sacan del centro.
- **Verbos que los hechos sostienen:** diseñé, dirigí, propuse, visité, decidí.
- **Palabras de su oficio:** quiebres, reposición, locales, alertas, jefes de local, inventario confiable.
- **Palabras que nunca dijo:** stakeholders, roadmap, impacto, liderazgo. Ninguna puede aparecer en su CV.
- **Dos cosas que se achica:** el tamaño de la cadena y su papel en el piloto.
- **Dónde se detiene al contar:** en la gente que usa lo que ella hace. Por eso su mejor viñeta es la del cambio de las noventa alertas a quince, y no la del número más grande.

Eso es el archivo. Con eso, el paso 4 ya no puede escribir "Responsable del seguimiento de stock".
