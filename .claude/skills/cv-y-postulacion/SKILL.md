---
name: cv-y-postulacion
description: Paso 4 del método. Arma el CV maestro desde la evidencia verificada, lo recorta en una variante por carril, genera PDF y DOCX que los ATS leen bien, y acompaña cada postulación - primero el veredicto por escrito (qué pide el aviso, qué cumple, qué le falta, si conviene), después las respuestas del formulario listas para pegar, y al final la anotación en el registro de vacantes con qué CV se mandó. Nunca aprieta Enviar. Usar cuando /empezar detecta que existe 03-que-trabajo-quiero.md, o cuando la persona dice "armemos el CV", "adapta mi CV a este aviso", "me quiero postular a esto", "pásame las respuestas del formulario", "¿conviene mandar a esta?".
---

# CV y postulación

Cuatro resultados, todos en `mi-cerebro/`:

- `04-cv-maestro.md`, con todo.
- `cv/cv-<carril>.md`, una variante por carril, y sus PDF y DOCX en `cv/build/`.
- `05-postulaciones.md`, con los datos fijos, las respuestas reusables y un veredicto por aviso.
- La vacante en `vacantes.json`, el registro de la skill `busqueda-de-vacantes`, con el estado y el CV que se mandó.

Lee `AGENTS.md` antes de empezar. Las reglas 1, 3 y 10 son las de este paso.

---

## Parte 1 · El CV maestro

**Qué es:** la versión que contiene todo. No se manda nunca. Las variantes son recortes de este archivo, **nunca reescrituras**, y así ninguna versión puede contradecir a otra.

**De dónde sale:** solo de `02-evidencia.md`. Lo `[SIN FUENTE]` no entra.

**Cómo se escribe:** las reglas completas están en `references/cv-maestro-y-variantes.md`. Las que no se negocian:

1. **Cada línea lleva un número o un verbo de decisión.** "Responsable de reportes" no dice nada. "Definí la regla de reposición que se probó en 12 locales" sí.
2. **Fechas idénticas a LinkedIn**, al mes. Si no coinciden, se corrige LinkedIn o el CV, con el documento del paso 2 como árbitro.
3. **Cronológico inverso.** Un CV reordenado por relevancia dispara la pregunta "¿qué esconde?" y los sistemas de selección lo leen peor.
4. **Los números chicos se presentan como criterio, no como magnitud.** "Decidí qué locales entraban al piloto y con qué regla", no "gestioné la operación de la cadena".
5. **La prueba de los cinco minutos.** Por cada línea: ¿la persona puede hablar cinco minutos de eso, con detalle, si se lo preguntan? Si no, se saca. No porque suene mal: porque se cae en la entrevista y arrastra a las demás.

Copia `plantillas/04-cv.md` para arrancar. Muéstrale el maestro completo antes de escribirlo.

## Parte 2 · Las variantes

**Una por carril** de `03-que-trabajo-quiero.md`. Si hay un solo carril, hay una sola variante.

**Lo que cambia:** el título, el resumen, qué viñetas sobreviven y en qué orden, cuánto espacio se lleva cada trabajo, el bloque de habilidades.

**Lo que no cambia:** los hechos, las fechas, los números, el orden cronológico, la formación y los datos de contacto.

Cuando están aprobadas, se generan:

```bash
python3 herramientas/generar-cv.py mi-cerebro/cv/cv-*.md
```

El script revisa antes de generar. Si encuentra un número de `numeros-retirados.txt`, un dato marcado `[SIN FUENTE]` o una raya larga, **no genera ninguno** y dice en qué línea está. Se arregla el markdown, no el PDF.

Formato de salida: una columna, texto seleccionable, sin tablas, sin íconos, sin foto. Es lo que los sistemas de selección leen sin romper.

## Parte 3 · Cada postulación

La persona trae un aviso (link o texto). Siempre en este orden:

### 1. Verificar que la vacante existe

Antes de leer nada: ¿el aviso está abierto en el sitio de empleo de la propia empresa? Los avisos en portales y buscadores siguen publicados semanas después de cerrarse. Cómo se verifica está en `references/trampas-de-formularios.md`.

### 2. El veredicto, por escrito, antes de tocar el formulario

Es la regla 3 de `AGENTS.md` y es la que más protege. La estructura está en `references/veredicto-antes-de-llenar.md`:

- Qué pide, requisito por requisito, contra la evidencia.
- Los huecos, sin maquillar.
- El riesgo real (un requisito duro que no cumple, una condición que choca con sus criterios).
- Qué variante de CV va.
- **Conviene o no conviene**, en una línea, y por qué.

**Se muestra y se espera.** La persona decide. Si dice que no, se anota como descartada con el motivo, y se sigue.

### 3. Las respuestas del formulario

Solo si dijo que sí. Cada campo resuelto y listo para pegar, en `05-postulaciones.md`:

- Los datos que se repiten (nombre, correo, teléfono, LinkedIn) salen de una sola tabla arriba del archivo, para que sean idénticos en todas las postulaciones.
- Las preguntas abiertas se contestan con la evidencia, en el tono de la regla 9 de `AGENTS.md`, y se pasan por `herramientas/chequear.py` antes de dárselas.
- Sueldo: el número que la persona decidió para este formulario, con la unidad que pide el campo.
- Los campos que confunden (autorización de trabajo, patrocinio de visa, nombre legal) tienen su respuesta en `references/trampas-de-formularios.md`.

**Por qué en un documento y no directo en el formulario.** Muchos formularios no guardan borradores: si se cierra la pestaña, se pierde todo. Con las respuestas escritas, postularse son cinco minutos.

### 4. Enviar

**Lo aprieta la persona. Nunca el asistente**, aunque tenga el navegador abierto y el formulario lleno. Es la regla 10.

### 5. El registro

Después de que la persona confirma que envió, la vacante pasa a `postulada` en `mi-cerebro/vacantes.json`, con la variante de CV:

```bash
python3 herramientas/vacantes.py cambiar kil1 estado=postulada cv=cv-a-producto-operaciones
```

Si la vacante todavía no estaba en el registro, primero va el `alta`. Cómo funciona el registro está en la skill `busqueda-de-vacantes`, parte 1.

**Anotar la variante de CV no es opcional.** Sin eso, el experimento del paso 3 no mide nada.

Si decidió no mandarla, queda `descartada` con el motivo y la muestra en las notas. Cuando llega una respuesta, se cambia el estado: el historial guarda la fecha solo.

---

## Lo que esta skill no hace

- No inventa ni redondea hacia arriba. Si la evidencia dice "al menos", el CV dice "al menos".
- No llena formularios en el mismo movimiento en que los lee.
- No aprieta Enviar, ni Submit, ni Postularme.
- No publica nada en LinkedIn. Si el CV cambió una fecha o un título, avisa qué hay que corregir en el perfil y la persona lo hace.
