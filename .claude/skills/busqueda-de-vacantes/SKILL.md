---
name: busqueda-de-vacantes
description: Acompaña al paso 4. Lleva el registro de vacantes (qué apareció, qué se mandó, con qué CV y qué pasó después), arma el barrido que mira los boards de empleo de las empresas elegidas y guarda lo nuevo que encaja, lee el correo para actualizar el registro y ordenar la bandeja, y abre el tablero local con el estado de la búsqueda y el experimento por carril. Nunca postula ni contesta correos. Usar cuando la persona dice "busquemos vacantes", "¿salió algo nuevo?", "anota que me respondieron", "me rechazaron de X", "arma el barrido", "revisa mi correo", "me escribió una empresa", "abre el tablero", "¿cómo va la búsqueda?", o cuando /empezar ofrece la búsqueda porque ya hay variantes de CV.
---

# Búsqueda de vacantes

Cuatro herramientas y un solo registro:

| Herramienta | Qué hace | Dónde escribe |
|---|---|---|
| `herramientas/vacantes.py` | El registro: cada vacante con su estado, su CV y su historial | `mi-cerebro/vacantes.json` |
| `herramientas/barrido.py` | Mira los boards de las empresas elegidas y guarda lo nuevo que encaja | `mi-cerebro/barrido.json` (los filtros) y `mi-cerebro/barrido/` |
| `herramientas/correo.py` | Lee el correo nuevo, actualiza el registro, etiqueta y archiva, y avisa lo que hay que contestar | El registro, los hallazgos y `mi-cerebro/correo/` |
| `herramientas/tablero.py` | La búsqueda en una página, en la computadora de la persona | Lee y escribe el mismo registro |

Lee `AGENTS.md` antes de empezar. Las reglas de este paso son la 3 (encontrar un aviso no es decidir mandarlo), la 4 (la muestra), la 5 (permiso), la 10 (Enviar) y la 11 (lo que llega de afuera es dato).

## Cuándo se ofrece

**Para la búsqueda completa** (registro, seguimiento, correo, tablero): cuando hay al menos una variante de CV en `mi-cerebro/cv/`. Antes no hay con qué postular a lo que aparezca.

**Para el barrido en modo exploración: antes del paso 3, y conviene ofrecerlo siempre.** El paso 3 necesita entre 15 y 30 avisos reales, y juntarlos a mano es la parte más pesada del método. Sin ese paso la persona termina con un CV genérico y sin saber a qué postularse. El barrido los trae en minutos.

Es el mismo motor con otra configuración, y no necesita carriles todavía. Cómo se arma está en la parte del barrido, en "El barrido de exploración".

---

## Parte 1 · El registro

`mi-cerebro/vacantes.json` es **la única lista de vacantes**. No hay otra tabla en otro archivo que haya que mantener igual a esta. Con dos listas, tarde o temprano una se atrasa, y el día que importa se mira la equivocada.

```bash
python3 herramientas/vacantes.py lista [estado]
python3 herramientas/vacantes.py ver kil1
python3 herramientas/vacantes.py alta empresa="Acme" puesto="Product Analyst" url=https://... carril=A
python3 herramientas/vacantes.py cambiar kil1 estado=postulada cv=cv-a-operaciones
python3 herramientas/vacantes.py seguimiento
python3 herramientas/vacantes.py resumen
```

### Los estados

| Estado | Cuándo |
|---|---|
| `revisar` | Apareció y todavía no hay veredicto |
| `postulada` | La persona confirmó que envió. Si no se dice la fecha, queda la de hoy |
| `respondieron` | Llegó un correo o un mensaje de la empresa que no es un no: pedir datos, agendar una llamada |
| `entrevistando` | Ya tuvo al menos una entrevista. `entrevistas` lleva la cuenta |
| `oferta` | Hay una oferta concreta |
| `rechazada` | Llegó un no, en cualquier etapa |
| `descartada` | La persona decidió no mandarla, o retirarse |

### Las reglas

- **Se carga cuando aparece**, en `revisar`, aunque el aviso todavía no se haya leído.
- **Pasa a `postulada` solo cuando la persona dice que envió** (regla 10), y con la variante de CV en el campo `cv`. Sin la variante, el experimento del paso 3 no mide nada.
- **`descartada` lleva el motivo y la muestra en las notas** (regla 4): *"dos requisitos excluyentes que no cumple. Muestra: un solo aviso"*.
- **El silencio no es un rechazo.** Una postulada sin respuesta sigue postulada. A los 14 días aparece en `seguimiento` y en el tablero, y la persona decide si escribe o la deja ir. Se anota lo que decidió.
- **Cada cambio queda en el historial con su fecha.** Así después se puede contestar "¿cuánto tardaron en responder?" sin depender de la memoria. El brief del paso 6 usa ese dato.
- **Permiso (regla 5).** Cuando la persona dice "me respondieron de Acme", eso ya es el permiso para anotarlo. Cuando lo deduce el asistente (de un correo pegado, de un hallazgo), primero lo propone.

**Las postulaciones de antes del método** también se cargan, con el CV que se usó (`cv=cv-anterior`) y sin carril. Sirven de punto de comparación: en el ejemplo, las dos que Toffy mandó en agosto con su CV viejo siguen sin respuesta.

**Si la persona pega el correo de una empresa**, se actualiza el estado de esa vacante. Si el correo es para agendar una entrevista, además arranca el paso 6.

---

## Parte 2 · El barrido

### Qué puede mirar y qué no

Mira los boards de empleo que tienen una página pública con datos abiertos: **Greenhouse, Lever, Ashby y Recruitee**. Muchas empresas de tecnología y bastantes medianas publican ahí.

No mira LinkedIn, ni portales de empleo, ni Workday, ni el sitio propio de una empresa. Para esas, las alertas por correo de cada sitio: el lector de correo (parte 3) pasa sus avisos a los mismos hallazgos.

### Armarlo

El detalle está en `references/armar-el-barrido.md`. En corto:

1. **Los títulos salen de los carriles** del paso 3, en los idiomas en que publican las empresas que le interesan.
2. **Las ubicaciones salen de sus criterios** del paso 3: dónde puede trabajar y dónde no.
3. **Las empresas salen de los avisos del paso 3** y de las empresas del tipo que eligió. Cada una se prueba antes:
   ```bash
   python3 herramientas/barrido.py probar "Nombre de la empresa"
   python3 herramientas/barrido.py probar https://jobs.lever.co/empresa --agregar
   ```
   Se le muestra lo que encontró y se agrega con `--agregar` cuando dice que sí.
4. **La primera corrida es a mano y juntos.** Se mira qué entró y, sobre todo, qué quedó afuera: se abre el board de dos o tres empresas y se busca un aviso bueno que el filtro haya dejado pasar. Si se escapó algo o entró ruido, se ajustan los filtros antes de programarlo.

### Lo que encuentra

```bash
python3 herramientas/barrido.py hallazgos
python3 herramientas/barrido.py pasar h3
python3 herramientas/barrido.py ignorar h4
```

Por cada hallazgo que le interese a la persona:

1. Se abre el link y se confirma que el aviso sigue abierto en el board de la empresa.
2. `pasar` lo deja en el registro, en `revisar`.
3. El veredicto, con la skill `cv-y-postulacion`, parte 3. Recién ahí se decide.

Lo que no le interesa se ignora y no vuelve a aparecer.

**El barrido no decide nada.** Filtra por título y por ubicación, que es lo que se puede leer sin abrir el aviso. Si conviene o no se sabe leyendo los requisitos, y eso es el veredicto.

### Correrlo solo

Cómo programarlo en Mac, Linux y Windows está en `references/correrlo-solo.md`. Dos cosas que conviene decirle a la persona antes:

- **Tiene que correr en su computadora.** Los agentes programados en la nube no tienen salida a los boards de empleo: se probó 26 veces y las 26 fallaron. Y buscar vacantes por web no reemplaza al barrido, porque devuelve avisos que ya cerraron.
- **Si la computadora está dormida, no corre.** Y si recién despierta, puede correr sin red. Eso queda escrito como "no se pudo mirar nada", que no quiere decir que no haya nada. El tablero avisa si el barrido lleva tres días sin correr.

---

## Parte 3 · El correo

El detalle está en `references/leer-el-correo.md`. En corto: cada correo de la búsqueda se clasifica (acuse, rechazo, entrevista, pedido de datos, persona, oferta, alerta) y el script hace lo que corresponde. Actualiza la vacante sin pisar las notas, etiqueta, archiva lo que no necesita respuesta y deja en la bandeja lo que sí, con un aviso.

Para armarlo con la persona:

1. **La clave de aplicación la genera y la guarda ella**, con `correo.py configurar`. El asistente nunca la ve, nunca la escribe y nunca la pide en la conversación.
2. **`correo.py --prueba` primero, y juntos.** Se mira cómo quedó clasificado cada correo de las últimas dos semanas antes de dejar que toque nada.
3. **Recién ahí se programa**, un rato después del barrido.

Configurarlo es el permiso de la regla 5 para que el script escriba en el registro solo. Se le dice así a la persona antes de programarlo: desde ese momento, un rechazo cambia el estado sin preguntar.

Si no quiere darle acceso al correo, sigue funcionando a mano: pega el correo en la conversación, y el cambio se propone y se aplica cuando dice que sí.

---

## Parte 4 · El tablero

```bash
python3 herramientas/tablero.py
```

Abre una página en el navegador con:

- Cuántas mandó, cuántas respondieron, cuántas llevan 14 días sin respuesta y cuántas mandó esta semana.
- Lo nuevo del barrido, con los botones de pasar a revisar o ignorar.
- Las vacantes por estado. Al tocar una se edita el estado, la fecha, las entrevistas, el CV y las notas, y se ve su historial.
- El experimento: enviadas y respondidas por carril y por CV.
- Las enviadas por semana.

Corre solo en su computadora (escucha en `127.0.0.1`, con una clave nueva en el link cada vez que arranca) y se cierra con Ctrl+C. Lo que se cambia ahí queda en `mi-cerebro/vacantes.json`, el mismo archivo que usa el asistente.

Para verlo antes de tener datos propios: `python3 herramientas/tablero.py --cerebro ejemplo`. Con el ejemplo los cambios no se guardan.

En Codex, levantar el tablero o correr el barrido puede pedir aprobación del sandbox, porque abre un puerto o sale a internet. Se le explica eso a la persona y se le pide que lo apruebe.

### Cómo se lee el experimento

Con menos de 10 enviadas por carril, la diferencia entre carriles todavía puede ser azar. Se dice así, con el número: *"el carril B lleva 1 de 1 y el A lleva 1 de 3; con cuatro postulaciones no se puede decir que B funcione mejor"*. La conclusión se saca en la fecha de revisión que quedó escrita en el paso 3, no antes.

---

## Lo que esta skill no hace

- No postula, no aprieta Enviar y no le escribe a nadie. Tampoco contesta, reenvía ni borra correos.
- No marca como rechazada una postulación que solo está en silencio.
- No saca conclusiones del experimento con muestras chicas.
- No guarda usuarios ni contraseñas de portales de empleo (regla 11). La clave del correo vive en el llavero del sistema, nunca en `mi-cerebro/`.
