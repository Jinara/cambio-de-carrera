# De dónde sale la prueba

Por cada fuente: qué prueba, cómo se cita, y la trampa que tiene.

---

## Camino A · Datos propios

Para quien tiene acceso hoy a lo que produjo.

### Repositorios de código

**Prueba:** volumen y continuidad de trabajo, autoría, fechas de cada sistema, qué se construyó.

**Cómo se cita:** el comando al lado del número, para que se pueda reproducir.
```bash
git -C <repo> rev-list --all --count                      # commits totales
git -C <repo> log --author="<correo>" --oneline | wc -l   # commits propios
git -C <repo> log --format=%ad --date=format:%Y-%m | sort | uniq -c   # por mes
```

**Trampa:** los commits miden actividad, no impacto. Un mes con cientos de commits prueba capacidad de ejecución y también puede ser la prueba de que se estaba construyendo lo equivocado. Y si hubo co-autores, se dice: *"autora única"* solo cuando lo es.

### Bases de datos

**Prueba:** ventas, clientes, retención, costos, todo lo que se mide.

**Cómo se cita:** la consulta guardada en un archivo, y el nombre del archivo al lado del número.

**Trampa:** la definición. "Ventas" puede incluir cancelados, duplicados, impagos o pruebas. Antes de dar una cifra de facturación se escribe qué cuenta como venta válida, y se usa siempre esa misma definición. Dos definiciones distintas en dos documentos es la forma más común de que un número "cambie" sin que nadie lo haya tocado.

### Tableros y analytics (GA4, Looker, Metabase, el panel propio)

**Prueba:** tráfico, conversión, uso.

**Cómo se cita:** nombre del tablero, filtro aplicado, rango de fechas y fecha de la consulta.

**Trampa:** los tableros heredan los errores de la definición de arriba, y muchas veces nadie los revisó. Si un número del tablero no coincide con la base, gana la base, y la diferencia en sí es un hallazgo (alguien que encuentra que su propio tablero miente tiene una historia).

### Cuentas de anuncios

**Prueba:** inversión, costo por resultado, retorno.

**Trampa:** los resultados que reporta la plataforma de anuncios no son ventas. Se cruzan con la base antes de decir "la pauta trajo tanto".

### Libros de gastos, facturas, extractos

**Prueba:** costos reales y márgenes.

**Trampa:** suelen arrancar tarde. Si el libro de gastos existe desde un año, todo costo anterior es un piso.

---

## Camino B · Sin acceso a los sistemas

Para quien trabajó en empresas donde ya no tiene acceso, o donde no puede sacar nada. Es más difícil y es el caso de la mayoría. Todas estas fuentes existen más de lo que la persona cree.

### Certificados laborales, contratos, cartas de ascenso, recibos de sueldo

**Prueba:** fechas exactas, cargo formal, ascensos, tipo de vínculo.

**Cómo se cita:** *"Certificado laboral, emitido el 12-mar-2024"*.

**Trampa:** ninguna. Es la fuente más fuerte para fechas, y la que resuelve cuando el CV y LinkedIn se contradicen. Si no lo tiene, casi todas las empresas lo emiten a pedido, incluso años después.

### Evaluaciones de desempeño

**Prueba:** objetivos, resultados que la empresa reconoció por escrito, comentarios del jefe.

**Cómo se cita:** año, sección y página. No se copia la evaluación a `mi-cerebro/`.

**Trampa:** hablan en el idioma de la empresa ("cumplió el objetivo de reducción de quiebres"). Confirman que algo pasó, pero muchas veces no traen la magnitud. Si la evaluación dice "redujo el tiempo de cierre" y el "de tres días a medio día" sale de la memoria, se cita así: el hecho verificado, la magnitud `[SIN FUENTE]`.

### Correos que la persona guardó

**Prueba:** anuncios internos con números, felicitaciones con el resultado, aprobaciones de un proyecto, invitaciones que muestran qué reunión dirigía.

**Cómo se busca:** en la cuenta personal, los que se reenvió a sí misma. En la cuenta de la empresa si sigue ahí. Palabras que suelen encontrar algo: "resultados", "felicitaciones", "piloto", "cierre", "aprobado", el nombre del proyecto.

**Cómo se cita:** remitente por cargo (no por nombre), fecha y asunto.

**Trampa:** reenviarse correos de la empresa puede violar una política de confidencialidad. Se usan los que ya existen. No se recomienda salir a reenviar.

### Presentaciones, informes y documentos propios

**Prueba:** qué analizó, qué recomendó, a quién se lo presentó.

**Trampa:** una presentación prueba que algo se propuso, no que se hizo ni que funcionó. Se anota qué pasó después, y de dónde se sabe.

### Tickets y herramientas de gestión (Jira, Trello, Asana, mesa de ayuda)

**Prueba:** qué pidió, qué resolvió, cuántos requerimientos definió, cuánto tardaba.

**Cómo se cita:** búsqueda usada y fecha. Si ya no tiene acceso, se anota como `[SIN FUENTE]` y se busca otra prueba del mismo hecho.

### Números públicos de la empresa

**Prueba:** tamaño de la empresa, cantidad de clientes o locales, rondas de inversión, facturación. Memorias anuales, notas de prensa, el sitio de la empresa, registros públicos.

**Cómo se cita:** el link y la fecha del dato.

**Trampa:** **describe a la empresa, no a la persona.** "Trabajé en una cadena de 180 locales" es verdad y se puede decir. "Mejoré la operación de 180 locales" no, salvo que haya prueba de eso. Y si el dato es de después de que la persona se fue, se dice.

### Recomendaciones y referencias

**Prueba:** lo que un ex jefe o un cliente dice de su trabajo.

**Cómo se usa:** una recomendación escrita en LinkedIn se puede citar. Una referencia de palabra no, pero se anota quién podría confirmar qué, para cuando una empresa pida referencias.

### Portfolio, charlas, publicaciones, premios

**Prueba:** trabajo visible y fechado.

**Trampa:** la sección de voluntariado y de charlas se infla fácil. "Organizadora" de un evento en el que se fue una vez como asistente es exactamente lo que una repregunta derrumba.

---

## Cuando no hay nada

A veces un trabajo entero no dejó rastro. Pasa, sobre todo con empleos de hace muchos años o en empresas que cerraron.

- Las fechas se sacan igual: certificado, historia laboral de la seguridad social, recibos.
- Lo que hizo se cuenta sin números, con verbos de decisión que la persona pueda defender cinco minutos: *"definí"*, *"dirigí"*, *"propuse y se aprobó"*.
- Se escribe en la tabla de límites que ese período no tiene evidencia de resultados. Decirlo antes es lo que hace creíble todo lo demás.
