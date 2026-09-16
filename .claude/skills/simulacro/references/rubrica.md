# La rúbrica del simulacro

El feedback mira cuatro cosas, en este orden. Las señales de cada una salieron de transcribir simulacros reales: son las que una transcripción delata y una lectura del papel no.

---

## 1. El reloj

**Qué se mira:** la duración de cada toma contra el objetivo declarado, y la tendencia entre tomas.

**La señal: la toma que se alarga en vez de acortarse.** Si la segunda toma dura bastante más que la primera (de 90 segundos a 150, por ejemplo), la persona todavía no sabe cuál es la historia y la está buscando en voz alta.

**Qué hacer:** antes de pedir que recorte, revisar si la respuesta contesta la pregunta. Muchas veces se alargó porque cambió de tema sin darse cuenta: la pregunta era qué construyó, y la respuesta se convirtió en cuánto costó. El resultado pasó a ser el tema. Se le muestra la pregunta otra vez y se le pide que cuente solo eso.

**Los objetivos de referencia:**

| Pregunta | Segundos |
|---|---|
| Cuéntame de ti, con quien recluta | 60 |
| ¿Por qué este puesto?, ¿por qué te vas? | 30 a 60 |
| Una historia de comportamiento | 90 a 120 |
| Una historia técnica o de caso | 120 a 180 |

## 2. Los números

**Qué se mira:** cada cifra dicha, contra `02-evidencia.md`.

**La señal más fuerte de todo el ejercicio: el número que baila.** La misma respuesta, varias tomas seguidas: *"como 200 locales"*, después *"180 locales"*, después *"casi 190"*. Un número que cambia entre tomas no está anclado a su fuente, y en la entrevista va a salir cualquiera de los tres.

**Se detecta solo**, sin criterio: `comparar-tomas.py` extrae las cifras de todas las tomas de una pregunta y marca las que cambian. Es aritmética.

**Qué hacer:** se busca la cifra en la evidencia. La que tiene fuente va escrita en el papel (los números sí se leen, no se improvisan). Las otras, si se venían diciendo, van a `numeros-retirados.txt`.

**Otra señal: el número inventado del final.** Los números sin fuente aparecen sobre todo en la última oración, cuando la persona busca un remate de escala ("y eso nos ahorró millones"). La defensa es tener el cierre listo en el papel, para que ese hueco ya esté ocupado.

**Y el hecho que se mezcla bajo reloj.** Hablando contra el tiempo, la gente confunde nombres de herramientas, de empresas, de fechas. Esos errores no aparecen escribiendo. Se corrigen en el papel siguiente, en el renglón de lo que se puede escapar.

## 3. El arco

**Qué se mira:** si la respuesta contesta la pregunta, y si quien escucha termina sabiendo qué hizo la persona y qué pasó.

**Las preguntas que se hace quien da el feedback:**
- ¿Cuál era el problema? ¿Se dice en la primera o segunda oración?
- ¿Qué decidió la persona? ¿Se oye "yo" o se oye "se hizo"?
- ¿Está el número del resultado?
- ¿El cierre es sobre lo que hace hoy, o se queda en el pasado?

**La señal: "suena robótico".** Cuando la persona dice que algo suena robótico y no sabe por qué, casi siempre falta un conector de causa: "por eso", "entonces", "y como vi que". Las oraciones están todas, pero no se nota qué llevó a qué. Se busca dónde falta el porqué, y se agrega al papel.

## 4. Los delatores de recitado

**La frase que se repite sin cerrar.** *"Y el tema de la regla, de la regla de reposición de la regla..."* Es texto memorizado que se soltó del riel: la persona recuerda el principio de la oración y no el final, y vuelve a empezar. Se vuelve a las viñetas, con menos texto en el papel.

**La oración que se saltea.** En una respuesta recitada, si se cae una oración, la siguiente queda sin referente: *"Y esa planilla fue la que..."* cuando nunca se mencionó ninguna planilla. Quien escucha se pierde. Improvisando esto casi no pasa.

**El comentario al final.** *"Uf, eso sonó rarísimo."* *"No sé, no me gustó."* La persona se dio cuenta sola de que estaba recitando o de que algo no funcionó. **Es la señal más valiosa de todas y no existe fuera del audio.** Se le pregunta qué notó, y casi siempre tiene razón.

**El papel telegráfico.** Si el papel está escrito con flechas y fragmentos ("piloto → 12 locales → bajó"), la persona tiene que armar la oración mientras lee, y se traba. El arreglo es el papel, no la persona: oraciones cortas y completas, en sus palabras.

---

## Cuándo se corta

Cuando en una toma se cumplen las cuatro a la vez:

1. Dentro del tiempo, o cerca.
2. Los números son los de la evidencia.
3. La respuesta contesta la pregunta y el cierre está en presente.
4. No hay frases que se repiten ni oraciones salteadas.

No hace falta que la toma sea perfecta. Y cuando se corta, se anota cuál es la toma de referencia en `simulacro.md`, por si hay que volver a escucharla antes de la entrevista.
