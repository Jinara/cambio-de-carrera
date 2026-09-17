# 05 · Postulaciones

Un veredicto por aviso, antes de tocar el formulario. Y las respuestas listas para pegar, solo si la decisión fue que sí.

Qué se mandó, con qué CV y qué pasó después está en `vacantes.json`. Para verlo en una página: `python3 herramientas/tablero.py --cerebro ejemplo`.

---

## Datos fijos (idénticos en todos los formularios)

| Campo | Qué poner |
|---|---|
| Nombre | Toffy |
| Apellido | Villamor |
| Nombre preferido | Toffy |
| Nombre legal (solo si el campo lo dice explícito) | Toffy Villamor (es el mismo nombre que usa en todos lados) |
| Correo | toffy@example.com |
| Teléfono | +56 9 0000 0000 |
| LinkedIn | linkedin.com/in/ejemplo-toffy |
| Ciudad y país | Santiago, Chile |
| ¿Autorización para trabajar en EE.UU.? | No aplica: todos sus avisos son en Chile. Si aparece en un puesto remoto: No |
| ¿Necesita patrocinio de visa? | Ídem: No |

## Respuestas reusables

### ¿Por qué quieres cambiar de trabajo?

> Lo que más disfruté en siete años en Ruta Norte fue el piloto de alertas de reposición: ir a los locales, entender por qué la primera versión no funcionaba y cambiarla. Quiero que ese sea mi trabajo de todos los días, en un equipo de producto, y no un proyecto cada dos años.

### ¿Cuántos años de experiencia tienes como Product Owner o Product Manager?

> Ninguno con el título. El trabajo sí lo hice en el piloto de 2023: fui a ver a los usuarios, cambié la regla por lo que vi y medí la adopción, que pasó de 11% a 58%.

---

---

## Despachos Cumbre · Product Owner, Herramientas de Bodega · 14-sep-2026

empleos.example.com/cumbre/po-bodega · Híbrido, Santiago · Contrato indefinido · Unas 400 personas (según el aviso) · Lo encontró el barrido

**Veredicto: conviene con un riesgo.** Los tres requisitos de fondo los tiene. El riesgo es con quién trabajaría: el puesto reporta a la gerencia de operaciones y el aviso no nombra a nadie de producto.

**Carril:** A · **Variante de CV:** cv-a-producto-operaciones

### Requisito por requisito

| Lo que pide el aviso | Lo que tiene | Evidencia |
|---|---|---|
| "Experiencia en operaciones de bodega, abastecimiento o distribución" | Sí | Abastecimiento 2019 a 2021 en Ruta Norte, y control de gestión en Quintral |
| "Levantar requerimientos con usuarios de la operación" | Sí | Al menos 64 requerimientos a BI, y las visitas a cuatro locales |
| "Priorizar un backlog de mejoras" | Parcial | Decidió qué entraba al piloto, nunca manejó un backlog |
| "Deseable: SQL" | Sí, en nivel intermedio | Uso semanal para el tablero de salud de stock |

### El riesgo real

"Reporta a la Gerencia de Operaciones" choca con el criterio que salió del par 6: quiere a alguien senior de producto cerca. Puede que exista y el aviso no lo diga. Se pregunta en la primera conversación, y si la respuesta es que no hay nadie, es motivo para retirarse.

### Qué preguntar en la primera conversación

- "¿Con quién trabajaría el día a día, y qué experiencia tiene en producto?"
- "¿Cuánto tarda una idea desde que se propone hasta que se prueba?"

**Enviada por Toffy el 15-sep-2026.**

---

## Rutas Chungará · Product Analyst, Planificación de Rutas · 12-sep-2026

empleos.example.com/chungara/pa-rutas · Híbrido, Santiago · Contrato indefinido · Llegó por una alerta de empleo por correo

**Veredicto: conviene.** Es del carril A y cumple lo requerido. Le falta el deseable de Python y nunca trabajó en transporte, que el aviso no pide como excluyente.

**Carril:** A · **Variante de CV:** cv-a-producto-operaciones

### Requisito por requisito

| Lo que pide el aviso | Lo que tiene | Evidencia |
|---|---|---|
| "SQL (excluyente)" | Sí, en nivel intermedio | Uso semanal para el tablero de salud de stock |
| "Experiencia en logística, transporte u operaciones" | Sí, en operaciones | Siete años en abastecimiento y operaciones. Transporte, no |
| "Trabajo con usuarios internos" | Sí | El piloto de alertas: de 11% a 58% de alertas atendidas |
| "Deseable: Python" | No | · |

**Enviada por Toffy el 13-sep-2026.** El 16-sep llegó un rechazo automático, sin entrevista y sin motivo. Uno solo no dice nada sobre el carril, y queda anotado así en `vacantes.json`.

---

## Tiendas Lumbrera · Product Owner E-commerce · 12-sep-2026

empleos.example.com/lumbrera/po-ecom · Híbrido, Santiago · Contrato indefinido · Rango no publicado

**Veredicto: conviene con un riesgo.** Cumple los dos requisitos de fondo (años en retail y stock) y queda a medias en los dos de forma de trabajo. Le falta lo deseable más visible, que es haber tenido el título, y eso se lo van a preguntar seguro.

**Carril:** B · **Variante de CV:** cv-b-producto-ecommerce

### Requisito por requisito

| Lo que pide el aviso | Lo que tiene | Evidencia |
|---|---|---|
| "3+ años de experiencia en e-commerce, retail u operaciones" | Sí | Siete años en abastecimiento y operaciones de una cadena de retail |
| "Conocimiento de gestión de stock e inventario" | Sí | Abastecimiento 2019 a 2021, alertas de reposición 2023 |
| "Manejo de Jira y metodologías ágiles" | Parcial | Jira como quien pide (al menos 64 requerimientos), nunca dentro de un equipo ágil |
| "Capacidad para priorizar un backlog junto a distintas áreas" | Parcial | Definió qué locales y productos entraban en el stock online, no priorizó un backlog |
| "Deseable: 2 años como Product Owner" | No | · |

### Los huecos, sin maquillar

- **Nunca tuvo el título.** Es deseable, no requerido. Si preguntan, va la respuesta reusable de arriba, sin subir nada.
- **Nunca trabajó dentro de un equipo ágil.** *"Trabajé con Jira del lado de quien pide. Las ceremonias no las hice, y es lo que más rápido se aprende de esta lista."*

### El riesgo real

La empresa tiene unas 1.500 personas (sitio de la empresa, sep-2026), por encima del rango que eligió en el par 4. No alcanza para no mandarla. Queda como pregunta para la primera llamada.

### Qué preguntar en la primera conversación

- "¿Cuánto tarda una idea desde que se propone hasta que se prueba?"
- "¿Con quién trabajaría el día a día, y qué experiencia tiene en producto?"

---

## Canastilla Norte · Senior Product Manager, Marketplace · 12-sep-2026

empleos.example.com/canastilla/spm-marketplace · Remoto en Chile · Contrato indefinido

**Veredicto: no conviene.** Es el aviso que más le gustaba de los 22, y es el que menos conviene mandar. Dos requisitos excluyentes que no cumple, y un puesto de jefatura que su ejercicio de preferencias dijo que no quiere todavía.

**Carril:** ninguno

### Requisito por requisito

| Lo que pide el aviso | Lo que tiene | Evidencia |
|---|---|---|
| "5+ años como Product Manager (excluyente)" | No | Cero años con el título |
| "Inglés avanzado, reportarás a un equipo regional (excluyente)" | No | Intermedio |
| "Experiencia con marketplaces de dos lados" | No | · |
| "Liderarás a dos Product Analysts" | Choca | Pares 2 y 6: no quiere gente a cargo por ahora |
| "Orientación a datos y SQL" | Parcial | SQL intermedio |

### Por qué se anota igual

Para no volver a considerarlo dentro de un mes, cuando el aviso reaparezca y se vea igual de lindo. Y porque si en seis meses Toffy tiene el título de Product Owner, esta empresa vuelve a la lista con otro puesto.

---

## Kilómetro Cero · Product Analyst, Operaciones de Última Milla · 10-sep-2026

empleos.example.com/km0/pa-ops · Híbrido 3x2, Santiago · Contrato indefinido · Unas 350 personas (según el aviso)

**Veredicto: conviene con un riesgo.** Es casi exactamente el carril A. El riesgo es la frase de temporadas altas, que choca con su par 7.

**Carril:** A · **Variante de CV:** cv-a-producto-operaciones

### Requisito por requisito

| Lo que pide el aviso | Lo que tiene | Evidencia |
|---|---|---|
| "Ingeniería Comercial, Industrial o carrera afín" | Sí | Ingeniería Comercial, 2016 |
| "2+ años en análisis de datos u operaciones" | Sí | Nueve años |
| "SQL (excluyente)" | Sí, en nivel intermedio | Uso semanal para el tablero de salud de stock |
| "Experiencia levantando necesidades con usuarios de la operación" | Sí | Visitas a cuatro locales y rediseño de la alerta |
| "Deseable: herramientas de ruteo o TMS" | No | · |
| "Deseable: experiencia en última milla" | No | · |
| "Disponibilidad para apoyar en temporadas altas (Cyber, Navidad)" | A preguntar | Choca con el par 7 |

### Los huecos, sin maquillar

- **Ruteo y última milla:** los dos deseables, ninguno requerido. *"No trabajé con ruteo. Sí con la otra punta de la cadena, el stock que tiene que estar para que el pedido salga."*
- **SQL:** el aviso no pide nivel. No se sube a avanzado.

### El riesgo real

"Apoyar en temporadas altas" puede ser dos semanas al año con horario extendido, o puede ser noviembre y diciembre enteros de noche, que es exactamente lo que no quiere repetir. No se sabe leyendo el aviso. Se pregunta.

### Qué preguntar en la primera conversación

- "¿Qué significa apoyar en temporadas altas: cuántas semanas al año, y en qué horario?"
- "¿Con quién trabajaría el día a día, y qué experiencia tiene en producto?"
- "¿Cuánto tarda una idea desde que se propone hasta que se prueba?"

### Respuestas del formulario

| Campo | Qué poner |
|---|---|
| Datos personales | Tabla de datos fijos |
| CV | `cv-a-producto-operaciones.pdf` |
| ¿Por qué te interesa este puesto? | Ver abajo |
| Nivel de SQL | Intermedio |
| Disponibilidad para temporadas altas | "Sí, con planificación. Me gustaría conocer cómo se organizan." |
| Pretensión de renta líquida mensual | `[MONTO]` (su objetivo, del paso 3) |

**¿Por qué te interesa este puesto?**

> Porque es el tipo de trabajo que más disfruté en nueve años. En Ruta Norte diseñé una alerta de reposición que al principio casi nadie miraba. Fui a cuatro locales a entender por qué y la cambié, y las alertas atendidas pasaron de 11% a 58%. En este puesto los usuarios son los coordinadores de ruta, y quiero hacer ese trabajo con ellos todos los días.

Pasada por `herramientas/chequear.py` el 10-sep-2026: sin números retirados ni rayas.

**Enviada por Toffy el 11-sep-2026.**
