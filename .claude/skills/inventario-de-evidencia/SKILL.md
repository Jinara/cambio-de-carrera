---
name: inventario-de-evidencia
description: Paso 2 del método. Junta la prueba de lo que la persona hizo, cada afirmación con su fuente al lado, y antes de dejar usar un solo número obliga a escribir la tabla de qué NO cubre esa evidencia. Tiene dos caminos - quien tiene datos propios (repos, bases, tableros, cuentas de anuncios) y quien trabajó en sistemas de empresas donde ya no tiene acceso (evaluaciones, correos, certificados, números públicos). Usar cuando /empezar detecta que existe 01-descubrimiento.md pero no 02-evidencia.md, o cuando la persona dice "juntemos la evidencia", "de dónde saco la prueba", "verifiquemos este número", "¿esto lo puedo poner en el CV?".
---

# Inventario de evidencia

El resultado es `mi-cerebro/02-evidencia.md`. Es lo único de donde el CV puede sacar un número o una afirmación. Si algo no está acá con su fuente, no va al CV.

Lee `AGENTS.md` antes de empezar. Las reglas 1, 2 y 4 son las de este paso.

## Punto de partida

Lee `mi-cerebro/01-descubrimiento.md`. Cada afirmación de ahí es una candidata. Las que ya tienen fuente se copian con su fuente. Las marcadas `[SIN FUENTE]` o `[POR CONFIRMAR]` son la lista de trabajo de este paso.

Copia `plantillas/02-evidencia.md` y `plantillas/numeros-retirados.txt` a `mi-cerebro/` si no existen (con permiso, regla 5). La lista de retirados arranca vacía y se llena sola: **cada vez que un número se corrige acá, el viejo se anota ahí** (regla 1), y los scripts la usan de freno.

## La primera pregunta: qué camino

Pregúntale de dónde puede salir la prueba de su trabajo. Casi nunca es un solo camino:

- **Camino A, datos propios.** Tiene acceso hoy a lo que produjo: repositorios, bases de datos, tableros, cuentas de anuncios, su propia tienda, sus planillas. Suele ser quien tuvo un negocio, trabaja por su cuenta o sigue en la empresa.
- **Camino B, sin acceso.** Su trabajo vivió en sistemas de empresas donde ya no está, o donde está pero no puede sacar nada. Es el caso de la mayoría de la gente empleada.

Una persona que sigue empleada suele estar en los dos: acceso de lectura hoy, y nada de sus empleos anteriores. Las fuentes de cada camino, y cómo se cita cada una, están en `references/fuentes-de-evidencia.md`.

## Antes del primer número: la tabla de límites

**No se escribe ni una cifra hasta que esté la tabla.** Es la regla 2 y es la que más cuesta.

Por cada fuente, una fila: desde cuándo tiene datos, hasta cuándo, y qué queda afuera. Cómo se arma y por qué va primero está en `references/tabla-de-limites.md`.

La consecuencia práctica: si los registros de una fuente arrancan en un año, **toda cifra anterior es un piso y no un total**, y se escribe con esa palabra.

## Cómo se anota cada afirmación

Una fila por afirmación, con estas columnas:

| Afirmación | Número | Contra qué y en qué período | Fuente | Estado |
|---|---|---|---|---|

Y un estado de estos cuatro, que decide adónde puede ir:

| Estado | Qué significa | Puede ir al CV |
|---|---|---|
| **Verificado** | Hay un documento, una consulta o un registro que cualquiera podría revisar | Sí |
| **Piso** | Hay fuente, pero la fuente no cubre todo el período | Sí, diciendo "al menos" o "desde tal fecha" |
| **Público** | Sale de una fuente pública sobre la empresa | Sí, pero describe a la empresa, no el impacto personal |
| **`[SIN FUENTE]`** | Solo lo recuerda la persona | No |

Un `[SIN FUENTE]` no se borra. Queda escrito, porque sirve para contar la historia en una conversación ("no tengo el número exacto, pero te cuento qué hice"). Lo que no hace es entrar al CV.

## Cuando un número cambia

Pasa seguido: se busca la fuente y el número real es distinto al que la persona venía diciendo.

1. Se corrige en `02-evidencia.md`, con la fecha de la corrección y el número viejo tachado al lado, para que se vea qué cambió.
2. **El número viejo va a `mi-cerebro/numeros-retirados.txt`**, una línea por número, con el patrón y qué decir en su lugar, separados por un tabulador:
   ```
   300 millones	Sin fuente. Usar la baja de quiebres del piloto: 9,1% a 6,4% en 12 locales.
   ```
   `herramientas/generar-cv.py` se niega a generar un CV que tenga un número de esa lista, y `herramientas/chequear.py` lo encuentra en cualquier texto antes de pegarlo en un formulario.
3. Se busca en los otros archivos de `mi-cerebro/` si el número viejo aparece, y se avisa dónde.

**Por qué importa tanto.** Un número corregido en un archivo y vivo en otros cuatro sigue saliendo en el CV, en LinkedIn y en la respuesta de la entrevista. La lista de retirados es lo que evita que vuelva.

## Las verdades incómodas

La última sección del archivo junta lo que puede explotar en una entrevista: un solapamiento de fechas, una escala chica, un proyecto que no llegó a producción, un número que solo se puede dar como piso. Cada una con la frase honesta que la desactiva.

Van **a propósito**. Lo que puede explotar se desactiva antes, no en la entrevista.

## Confidencialidad

- **No se copian documentos de terceros a `mi-cerebro/`.** Ni evaluaciones completas, ni exportes de sistemas de la empresa, ni correos con datos de otras personas. Se anota el dato y dónde está: *"Evaluación de desempeño 2023, sección objetivos, página 2"*.
- **Los números de una empresa pueden ser confidenciales** aunque la persona los haya producido. Ante la duda, se usa la forma relativa (un porcentaje, una proporción, un antes y después) o el dato público equivalente, y se anota por qué.
- Si la persona sigue trabajando en la empresa, no se sacan exportes. Se anota el número, la fecha de la consulta y cómo se reproduce.

## Cuándo termina

Cuando cada afirmación del descubrimiento tiene estado, la tabla de límites está arriba y la sección de verdades incómodas está escrita. No hace falta que todo quede verificado: hace falta que todo tenga su estado dicho de frente.

Al cerrar, dile qué sigue: qué trabajo quiere de verdad (`/empezar` la lleva sola).
