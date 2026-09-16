# El CV maestro y sus variantes

## Por qué un maestro

Cuando cada CV se escribe desde cero para cada aviso, a la tercera versión ya hay dos fechas distintas para el mismo trabajo y un número que en una variante es 30% y en otra es "casi la mitad". Un reclutador que ve dos versiones, o que compara el CV con LinkedIn, lo nota.

El maestro resuelve eso: todo lo verdadero vive en un solo archivo, y las variantes solo eligen qué mostrar y en qué orden.

## Las secciones del maestro

### Encabezado

Nombre, ubicación (ciudad y país, sin dirección), correo, teléfono, LinkedIn, idiomas con nivel real. El título cambia en cada variante, así que en el maestro va como `[según variante]`.

**Un solo nombre en todos lados.** El mismo en el CV, en LinkedIn, en el correo y en todos los formularios. Si la persona usa un nombre distinto del legal, ese va en todas partes, y el legal solo donde un campo lo pide explícito. Ver `trampas-de-formularios.md`.

### Resumen

Tres partes, en este orden:

1. **Qué busca**, con el título y el tipo de empresa. Una línea.
2. **Por qué**, con lo que salió del paso 3. Dos o tres líneas. Sin frases que cualquiera podría firmar ("apasionada por los desafíos").
3. **Con qué llega**, con los dos o tres números más fuertes de la evidencia. Dos o tres líneas.

Lo que no va: la mala noticia sin que nadie la pida. Si hubo un cierre, un despido o un hueco, se explica cuando lo preguntan, no en el resumen.

### Experiencia

Por trabajo:

```
### Empresa · Puesto
mes-año → mes-año · Ciudad
Una línea de contexto de la empresa, con dato público si lo hay.
- Viñeta con número o verbo de decisión.
- Viñeta con número o verbo de decisión.
```

- **La línea de contexto** describe a la empresa, no a la persona: *"Cadena de 180 farmacias en Chile (memoria anual 2025)"*. Resuelve la credencial achicada sin inflar nada.
- **Dos vínculos con la misma empresa van en dos entradas** (empleo y después freelance, por ejemplo). Sumados en una línea parecen un solapamiento.
- **Un contrato corto se dice**: *"(contrato de cuatro meses)"* convierte una salida rápida en algo esperable.
- **Un ascenso se muestra** con la flecha en el título: *Analista → Analista Senior*.

### Viñetas

Fórmula: **verbo de decisión + qué + resultado con su contra qué**.

| Floja | Fuerte |
|---|---|
| Responsable del seguimiento de stock | Diseñé la alerta de reposición que bajó los quiebres de 9,1% a 6,4% en el piloto de 12 locales |
| Apoyo en proyectos de mejora | Propuse reducir las alertas de todas a las 30 más críticas por local, después de visitar cuatro locales, y la tasa de alertas atendidas pasó de 11% a 58% |
| Manejo de SQL y Looker | Armé el tablero de salud de stock que usan 31 personas por semana |

Verbos que funcionan: definí, diseñé, decidí, propuse (y se aprobó), dirigí, negocié, corté, medí, reemplacé, encontré. Verbos que no dicen nada: apoyé, participé, colaboré, fui parte de, responsable de.

**Un error propio no va en el CV.** Va en la entrevista. Pero la viñeta que nace de corregirlo sí (la segunda de la tabla de arriba es eso).

### Formación, comunidad, habilidades

- **Formación:** título, institución, año de egreso. Sin promedio salvo que lo pidan.
- **Comunidad, charlas, voluntariado:** ordenado por lo que la persona puede defender cinco minutos, no por lo que suena mejor. Lo que dirigió va primero y dicho como dirigido. Lo que fue una vez, se dice que fue una vez, o no va.
- **Habilidades:** agrupadas por tipo, en una línea cada grupo. Solo lo que usó en un trabajo real del CV.

## Cómo se recorta una variante

| | Cambia | No cambia |
|---|---|---|
| Título | ✔ | |
| Resumen | ✔ | |
| Qué viñetas sobreviven y en qué orden | ✔ | |
| Cuánto espacio lleva cada trabajo | ✔ | |
| Qué habilidades abren el bloque | ✔ | |
| Hechos, números, fechas | | ✔ |
| Orden cronológico | | ✔ |
| Formación y contacto | | ✔ |

**El largo:** una página hasta unos cinco años de carrera, dos páginas después. Más de dos no se lee.

**Los trabajos viejos o que no suman al carril** se comprimen a una línea (empresa, puesto, fechas) o se sacan si son pasantías de hace más de diez años. Nunca se sacan si hacerlo abre un hueco.

## La regla de voz

Los detectores de "texto escrito por IA" se equivocan mucho, sobre todo con gente que escribe en su segundo idioma, y los sistemas de selección no los usan para filtrar. La detección real es humana y pasa en la repregunta: alguien lee una línea genérica y pregunta "¿y eso cómo lo hiciste?".

Así que la defensa es la misma regla de siempre: especificidad. Una línea con un número verificado y un verbo de decisión no suena a nadie más.

Y las de `AGENTS.md`: nada de raya larga, nada de ritmo de tres, nada de "no es X, es Y".

## Antes de generar, la lista

- [ ] Todas las fechas coinciden con LinkedIn, al mes.
- [ ] Ningún `[SIN FUENTE]` ni `[POR CONFIRMAR]`.
- [ ] La prueba de los cinco minutos pasó línea por línea.
- [ ] Nada que contradiga a otra variante.
- [ ] `python3 herramientas/generar-cv.py` corrió sin frenos.
- [ ] La persona abrió el PDF y lo leyó entero.
