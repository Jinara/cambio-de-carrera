# Práctica de razonamiento numérico

Muchas empresas mandan un test numérico antes o después de la primera entrevista: preguntas de opción múltiple con tablas, porcentajes, proporciones y embudos, cronometradas por pregunta. Es la única parte del proceso que no se puede regrabar, y se entrena.

Acá hay dos cosas, y van en este orden.

## 1. El simulacro de 10 preguntas

`simulacro-10/preguntas.md` · 10 preguntas con tablas, tipo de cambio, comisiones, un embudo y una pregunta de caja. Cinco opciones cada una.

- **75 segundos por pregunta**, 12 minutos y medio en total, de una sentada y con cronómetro.
- Las respuestas están en `simulacro-10/respuestas.md`, con la cuenta y la trampa de cada opción.

**Para qué sirve:** medir dónde estás antes de practicar. Si fallas por tiempo, por la cuenta o por leer mal la pregunta, cada cosa se entrena distinto.

## 2. El cuadernillo de 100 preguntas

`cuadernillo-100/preguntas.pdf` y `cuadernillo-100/respuestas.pdf` · 100 preguntas en 4 tandas de 25, sin calculadora.

- **25 tipos de pregunta**, uno de cada tipo por tanda, de más fácil a más difícil: crecimiento y caída porcentual, el NO, parte sobre total, promedios simple y ponderado, regla de tres, razones y repartos, proporción inversa, veces contra porcentaje contra puntos, embudos, tipo de cambio, comisiones, caja, velocidad, tablas, porcentajes seguidos, volver al precio original, precio sin descuento o sin impuesto, ecuaciones, secuencias y crecimiento compuesto.
- **Cada tanda es una sentada** de unos 30 minutos, entre 60 y 75 segundos por pregunta.
- **La hoja de respuestas explica cada una:** la cuenta paso a paso, por qué, **qué error lleva a cada opción incorrecta** y el truco para hacerla de cabeza. Al final hay una hoja de trucos y una tabla de qué truco repasar según el tipo de pregunta que fallaste.

**Cómo se corrige:** primero la tanda entera con la clave rápida. Después, solo las que fallaste: se compara lo que escribiste al lado de la pregunta con la explicación, y se busca el nombre de tu error entre las opciones incorrectas.

### Regenerarlo

```bash
python3 practica/razonamiento-numerico/cuadernillo-100/generar.py
```

Ningún número está escrito a mano: el script calcula todo con fracciones exactas, y un verificador independiente vuelve a resolver cada pregunta por otro camino antes de generar. Si una respuesta no coincide, no genera nada. La semilla es fija, así que sale siempre igual.

Si quieres un cuadernillo distinto, cambia `SEMILLA` al principio del archivo. Las preguntas son las mismas y cambian el orden y la posición de la respuesta correcta.

## Con Claude o Codex

En la skill `simulacro` hay un modo numérico: el asistente te toma el simulacro o una tanda, anotas las letras y el tiempo, y te corrige separando los errores de cuenta, de lectura y de tiempo. Si un tipo de pregunta te falla dos veces, te arma diez más de ese tipo.
