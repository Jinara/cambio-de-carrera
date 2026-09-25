# Del habla al papel

Lo hablado no se pega tal cual en un CV. Hay una traducción, y tiene reglas, porque es fácil pasarse para los dos lados: dejar el CV lleno de muletillas, o pulirlo hasta que vuelva a ser de nadie.

## La regla que ordena todo

**Se conserva el verbo y el sustantivo. Se cambia el registro.**

El verbo dice quién decidió. El sustantivo de oficio dice que estuvo adentro. Todo lo demás (el orden de la frase, las muletillas, la puntuación del habla) se puede tocar sin perder a la persona.

## Tres traducciones, paso a paso

**Lo que dijo:**

> *"La primera versión la armé desde la oficina. Mandaba todas las alertas de reposición a las seis de la tarde, y en tres semanas casi nadie las miraba. Fui a cuatro locales y entendí por qué: a las seis el jefe está cerrando caja, y le llegaban como noventa alertas. Nadie lee noventa alertas."*

**Lo que el molde habría escrito:**

> Responsable de la optimización del sistema de alertas de reposición.

Todo cierto, y no queda ni una huella de que estuvo ahí.

**Lo que va al CV:**

> Propuse reducir las alertas de todas a las 15 más críticas por local, después de visitar cuatro locales, y la tasa de alertas atendidas pasó de 11% a 58%.

Qué se conservó: el verbo de su decisión (*propuse*), sus sustantivos (*alertas*, *locales*), y el hecho de que fue a mirar. Qué se cambió: el registro y el orden. Qué se agregó: los números, que salen del paso 2 y no del habla.

---

**Lo que dijo:**

> *"Yo solo apoyé el piloto."*

**Lo que va al CV:**

> Diseñé la regla de reposición que se probó en 12 locales.

El "solo apoyé" no se respeta, porque no es voz: es la credencial achicada. Se corrige con los hechos y se anota en la tabla, porque va a volver a aparecer en la entrevista.

---

**Lo que dijo:**

> *"Bajamos los quiebres un montón."*

**Lo que va al CV:**

> Bajé los quiebres de 9,1% a 6,4% en el piloto de 12 locales.

"Un montón" no puede ir. Pero se anota, porque es cómo ella mide cuando no tiene el dato a mano, y eso el simulacro lo tiene que entrenar.

## Lo que se conserva siempre

- **El verbo de la decisión**, corregido si estaba encogido.
- **Las palabras de su oficio**, tal cual las dice.
- **Qué le parece lo importante**, que decide qué viñeta va primera.
- **El grano del detalle.** Si cuenta con detalles concretos, el CV lleva detalles concretos. Si cuenta en grande, no se le inventan detalles finos que después no va a poder sostener.

## Lo que se cambia siempre

- Las muletillas.
- El "nosotros" cuando lo hizo ella. En el CV va en primera persona, y si de verdad fue de todo el equipo, se dice cuál fue su parte.
- Los adjetivos sin dato.
- El orden, cuando hablando arrancó por el final.

## Los formularios

Las preguntas abiertas de un formulario ("¿por qué te interesa este puesto?") son el lugar donde más se nota el molde, porque casi nadie las revisa con cuidado.

Ahí se puede soltar un poco más que en el CV: se permite una frase que suene a cómo habla, sobre todo si tiene un detalle concreto adentro. Lo que no cambia son las reglas 6 y 9 de `AGENTS.md`, o sea nada de spin, nada de raya larga y nada de ritmo de tres.

Antes de entregarlas, pasan por `herramientas/chequear.py`.

## La prueba final

Léelo en voz alta con la persona delante. Dos preguntas:

1. **¿Esto lo podrías decir mañana en una entrevista, con estas palabras?** Si no, no es suya.
2. **¿Esta línea la podría firmar igual quien tuvo tu puesto antes?** Si sí, todavía nombra el puesto y no a ella.

La segunda es la que más se salta. Es la que el freno de `chequear.py --cv` revisa sola, pero solo puede ver el arranque de la frase. El resto lo ven las dos personas leyendo.
