---
name: simulacro
description: Paso 7 del método. Entrenamiento para una entrevista, hablado o con cronómetro - Claude hace una pregunta con los segundos objetivo declarados, la persona lee un papel de pocos renglones, graba su respuesta en audio, se transcribe en su máquina, y el feedback compara las tomas contra el reloj, contra su propia evidencia y contra las señales de texto recitado. Se regraba hasta que el arco se sostiene sin el papel. Si viene un test numérico, toma el simulacro de 10 preguntas o una tanda del cuadernillo de 100, corrige separando errores de lectura, de cuenta y de tiempo, y arma más preguntas del tipo que falla. Usar cuando la persona dice "hagamos un simulacro", "practiquemos la entrevista", "te mando un audio", "grabé mi respuesta", "escucha esta toma", "me mandaron un test numérico", "quiero practicar matemáticas", "tómame el simulacro numérico", o cuando el brief de entrevista ya está y falta practicar.
---

# Simulacro

Todo va a `mi-cerebro/entrevistas/<empresa>/`:

- `simulacro.md`: los papeles, la tabla de tomas y el feedback de cada una.
- `tomas-p<N>.txt`: las transcripciones de todas las tomas de la pregunta N, en el orden en que se grabaron.

Los audios van a `herramientas/audios/`, que está en `.gitignore`.

Lee `CLAUDE.md` antes de empezar. La regla 8 (nunca memorizar) es la de este paso.

## Por qué hablado

Escribiendo, una respuesta se puede pulir hasta que suena perfecta, y en la entrevista se cae igual. Hablando aparecen cosas que el papel esconde: el número que cambia de una toma a otra, la historia que se alarga porque todavía no se sabe cuál es, la frase memorizada que se suelta del riel. Y también lo bueno: las mejores frases suelen aparecer en la tercera o cuarta toma, dichas por la persona, y no estaban en ningún documento.

## El bucle

### 1. La pregunta, con su formato

Una por vez, sacada del brief. Antes de grabar se declara:
- **los segundos objetivo** (60, o 90 a 120),
- **el idioma**,
- **si el formato real permite pensar antes** de empezar a contestar.

### 2. El papel

Cómo se escribe está en `references/como-escribir-un-papel.md`. En corto: entre cuatro y seis renglones, oraciones cortas en palabras de la persona, un máximo de tres números escritos, y una frase de cierre que funcione de freno.

**Y arriba del papel, lo que se puede escapar:** los números retirados que tocan esta historia y los errores que aparecieron en tomas anteriores. Dos o tres renglones.

La persona lo lee una vez, lo deja a un costado, y graba.

### 3. Grabar

Con lo que tenga: la app de notas de voz del teléfono o de la computadora. Una toma, de corrido, sin cortar. Si se traba, sigue: el trabón también es información.

Los archivos se nombran por pregunta y toma, y **no se editan ni se sobrescriben**: `lumbrera-p1a.m4a`, `lumbrera-p1b.m4a`, `lumbrera-p1c.m4a`. La toma nueva no corrige a la anterior, la reemplaza.

### 4. Transcribir

```bash
herramientas/transcribir.sh herramientas/audios/lumbrera-p1c.m4a >> mi-cerebro/entrevistas/lumbrera/tomas-p1.txt
```

Corre en la máquina de la persona, sin internet. Si no tiene Whisper instalado (ver `EMPEZAR.md`), puede pegar la transcripción automática de su teléfono, marcando que no tiene duración.

⚠️ **Whisper a veces entra en loop con los audios largos** y repite la misma frase hasta el final, comiéndose lo último que se dijo. Si el final de una transcripción se repite, se recorta el audio desde el minuto 2 o 3 y se transcribe ese tramo aparte. Muchas veces lo más valioso estaba ahí.

### 5. Comparar

```bash
python3 herramientas/comparar-tomas.py mi-cerebro/entrevistas/lumbrera/tomas-p1.txt --objetivo 60
```

Marca lo que se mide solo: duración contra el objetivo, tomas que se alargan, cifras que cambian entre tomas, frases que se repiten dentro de una toma, un comentario sobre la propia toma al final, y números retirados (también dichos en palabras).

### 6. El feedback

Siempre en este orden, y cómo leer cada cosa está en `references/rubrica.md`:

1. **El reloj.**
2. **Los números**, contra `02-evidencia.md`.
3. **El arco.** ¿Contesta la pregunta? ¿Se entiende qué hizo la persona?
4. **Los delatores de recitado.**

**Un solo cambio por toma.** Si se piden tres cosas a la vez, la toma siguiente arregla una y rompe otra. Se elige el cambio que más mueve y se deja el resto para después.

**Las frases buenas de la persona se recuperan.** Si en una toma dijo algo mejor que lo que decía el papel, se le devuelve en el papel siguiente, con sus palabras.

### 7. Regrabar, o cortar

**Se corta cuando el arco se sostiene sin el papel delante**, con el número correcto y dentro del tiempo. No cuando la toma sale perfecta: perfecta no sale nunca, y a partir de cierto punto regrabar empieza a memorizar.

## Preguntas sin papel

Cada tanto, una pregunta del brief que la persona no preparó, sin papel. Es la forma más rápida de encontrar huecos en el banco de historias: si no hay nada para "cuéntame de alguien que no estaba de acuerdo contigo", aparece acá y no en la entrevista. Lo que sale bien se lleva al paso 5.

## El simulacro numérico

Si el brief dice que viene un test numérico, lógico o psicotécnico, ese simulacro no va en audio: va con cronómetro y papel, con el material de `practica/razonamiento-numerico/` (un simulacro de 10 preguntas y un cuadernillo de 100 con cada error explicado). Cómo se toma, cómo se corrige y cómo se arman diez más del tipo que falla está en `references/simulacro-numerico.md`.

## Una sola fuente viva

El papel vive en `simulacro.md` y en ningún otro lado. Nada de copias en PDF o en otro documento "para imprimir": la copia es la que se desactualiza, y es la que tiene el número que ya se corrigió. Si la persona quiere el papel en el teléfono, se le pasa el texto en el momento.

## Lo que esta skill no hace

- No escribe la respuesta completa para leer. Nunca, aunque la persona lo pida: se le explica por qué (regla 8) y se le ofrece el papel.
- No sube los audios a ningún lado.
- No da feedback sobre la voz, el acento o la apariencia. Solo sobre lo que se dijo.
