# El simulacro numérico

Cuando la empresa manda un test numérico, el simulacro no va en audio: va con cronómetro y papel. El material está en `practica/razonamiento-numerico/`.

## El orden

1. **El simulacro de 10** (`simulacro-10/preguntas.md`) para medir. 75 segundos por pregunta, de una sentada.
2. **Las tandas del cuadernillo de 100** (`cuadernillo-100/preguntas.pdf`), una por sentada, para entrenar.
3. **Diez más del tipo que falla**, armadas por el asistente, cuando un tipo de pregunta falla dos veces.
4. **El simulacro de 10 otra vez** el día antes del test, para ver si el tiempo por pregunta bajó.

## Cómo se toma

- Antes de empezar, la persona anota la hora. Al terminar, la hora y las letras.
- **No se abren las respuestas** hasta terminar. Si la persona pregunta algo en el medio, se le dice que marque la mejor estimación y siga, igual que en el test real.
- Si el test real permite calculadora, se practica con calculadora el simulacro de 10. El cuadernillo va sin calculadora a propósito: estimar es lo que más tiempo ahorra con o sin ella.

## Cómo se corrige

Primero la clave, y después cada error se clasifica en uno de estos tres. Pedirle a la persona lo que escribió al lado de la pregunta ayuda a saber cuál fue.

| Tipo de error | Cómo se reconoce | Qué se entrena |
|---|---|---|
| **De lectura** | La cuenta está bien hecha, pero de otra cosa: la base equivocada, el NO que no vio, puntos en vez de porcentaje, la duración nueva en vez de la diferencia | Releer la pregunta antes de marcar. Buscar la palabra que manda: NO, más, proporción, respecto de, veces, puntos |
| **De cuenta** | El planteo es el correcto y el número no: la coma corrida, una división al revés | Decir la cuenta en voz alta con "sobre" ("lo nuevo sobre lo viejo"). Estimar el orden antes de calcular |
| **De tiempo** | No llegó, o marcó al azar las últimas | Estimar y descartar opciones en vez de calcular exacto |

**La trampa tiene nombre.** En la hoja de respuestas del cuadernillo y en la del simulacro de 10, cada opción incorrecta dice qué error lleva a ella. Se le muestra a la persona el nombre de su error, no solo la respuesta correcta.

## Lo que queda anotado

En `mi-cerebro/entrevistas/<empresa>/simulacro.md`, una sección aparte:

```markdown
## Test numérico

| Fecha | Qué | Buenas | Minutos | Errores de lectura | De cuenta | De tiempo |
|---|---|---|---|---|---|---|

**Los tipos que fallan:**
**Lo que se practica antes del test:**
```

## Las diez más de un tipo

Cuando un tipo de pregunta falla dos veces (en el simulacro o en el cuadernillo), el asistente arma diez preguntas nuevas de ese tipo:

- Mismo estilo: contexto de trabajo, números que se pueden hacer de cabeza, cuatro opciones.
- **Cada opción incorrecta sale de un error concreto**, igual que en el cuadernillo, y la explicación lo nombra.
- **Cada respuesta se verifica con una cuenta de Python antes de dársela a la persona.** Una práctica con una respuesta mal es peor que no practicar.
- Las respuestas van en un archivo aparte, que se abre al terminar.

## Antes del test real

- **Con descanso y de una sola sentada.** El cronómetro por pregunta castiga el cansancio.
- Papel, lápiz y, si se permite, calculadora a mano.
- La hoja de trucos del cuadernillo, leída una vez esa mañana. No más que eso.
