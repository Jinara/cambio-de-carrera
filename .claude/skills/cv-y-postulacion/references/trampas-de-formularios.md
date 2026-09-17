# Trampas de formularios y de avisos

Cosas que salieron mal postulando de verdad, y cómo se evitan.

---

## Antes de postular: ¿la vacante existe?

### El aviso que ya cerró

Los portales de empleo, LinkedIn y los buscadores siguen mostrando avisos semanas después de que la empresa los cerró. Buscar vacantes por web es la forma más rápida de encontrar puestos muertos: una vacante encontrada así puede dar error 404 en el sitio de la empresa y existir solamente en el índice del buscador.

**Qué hacer:** se busca el mismo aviso en el sitio de empleo de la propia empresa. Casi todas usan un sistema de selección con una página pública (Greenhouse, Lever, Ashby, Workable, Recruitee, BambooHR, Teamtailor, entre otros). Si el aviso no está ahí, no se postula por el portal.

### El sitio de empleo vacío

Que el sitio de una empresa no muestre vacantes no quiere decir que no tenga.

- **Algunas empresas tienen un sitio por país**, y el que aparece primero es el de otro país.
- **Algunas cambiaron de sistema** y el link viejo devuelve una página vacía.
- **Algunas repueblan rápido.** Un sitio vacío hoy puede tener decenas de avisos la semana que viene.

**Qué hacer:** un sitio vacío es sospechoso, no una respuesta. Se busca otra ruta (el link de "trabaja con nosotros" del sitio principal, el país correcto) antes de darlo por vacío, y se vuelve a mirar en unos días.

### Las alertas

La mayoría de estos sistemas deja suscribirse a avisos nuevos de una empresa. Para las empresas objetivo del paso 3, conviene activarlas. Es lo que evita enterarse de casualidad de un aviso que cerró ayer.

Si la empresa publica en Greenhouse, Lever, Ashby o Recruitee, el barrido de la skill `busqueda-de-vacantes` la mira solo, varias veces por día.

---

## Llenando el formulario

### No guardan borradores

Muchos formularios de postulación no guardan nada hasta que se envía. Si se cierra la pestaña o se vence la sesión, se pierde todo.

**Qué hacer:** las respuestas se escriben primero en `05-postulaciones.md` y se pegan al final.

### Cambian de un día al otro

El mismo formulario puede cambiar de preguntas entre la mañana y la tarde: aparece un campo nuevo, desaparece la pregunta de sueldo, cambia el nivel de idioma que pide.

**Qué hacer:** se relee el formulario justo antes de llenarlo, aunque esté documentado de hace horas.

### Un solo nombre

Si en una plataforma se pone el nombre legal completo, en otra el nombre de uso y en otra un apodo, la persona aparece como tres candidatos distintos, y los correos de respuesta llegan dirigidos a un nombre que no está en el CV.

**Qué hacer:** una tabla de datos fijos arriba de `05-postulaciones.md`, y se usa siempre esa.

| Situación | Qué nombre |
|---|---|
| Nombre y apellido, nombre preferido, nombre completo | El nombre de uso, igual que en el CV y LinkedIn |
| El campo dice explícito "nombre legal" | El legal completo |
| Oferta, contrato, verificación de antecedentes | El legal completo |

El nombre legal importa cuando hay contrato, no cuando hay CV.

### Las dos preguntas de Estados Unidos

Empresas estadounidenses que contratan en Latinoamérica muchas veces dejan en el formulario dos preguntas pensadas para candidatos de allá:

- *"Are you legally authorized to work in the United States?"*
- *"Will you now or in the future require sponsorship for employment visa status?"*

Para un puesto remoto desde otro país, sin mudarse, la respuesta habitual es **No** y **No**, y no se contradicen: la primera pregunta si tiene permiso para trabajar en Estados Unidos (no lo tiene, y el puesto no lo pide), la segunda si le va a pedir a la empresa un trámite de visa (no, porque no se va a mudar).

⚠️ Si el aviso es para trabajar físicamente en Estados Unidos, o si la persona sí tiene permiso de trabajo allá, las respuestas cambian. Se lee el aviso antes.

### El sueldo

- **La unidad del campo.** Mensual o anual, bruto o neto, moneda. Si el campo no lo dice, se aclara en el mismo campo si se puede ("USD, anual, bruto"), o se elige lo que el aviso usa.
- **El número se decide antes**, con el paso 3, no mirando el formulario.
- **Si el campo es obligatorio y el aviso no da rango**, se pone el objetivo, no el piso.

### Las preguntas abiertas

"¿Por qué quieres trabajar aquí?", "¿Qué herramientas de IA usas?", "Cuéntanos un proyecto".

- Se contestan con evidencia de `02-evidencia.md`, no con adjetivos.
- Las respuestas buenas se guardan en `05-postulaciones.md` y se reusan. Una pregunta que aparece en tres formularios no se escribe tres veces.
- Antes de pegar: `python3 herramientas/chequear.py -` con el texto (o sobre el archivo), para cazar números retirados y rayas largas.

---

## Después de enviar

- **Anotar la variante de CV** en `vacantes.json`. Sin eso no hay experimento.
- **El correo de confirmación** confirma que llegó. Si no llega en unos minutos, se revisa spam y después se asume que no se envió.
- **Varias postulaciones a la misma empresa el mismo día** pueden no recibir respuesta en ninguna. Es un solo caso observado, no una regla probada: se anota con qué muestra y se revisa si se repite.
