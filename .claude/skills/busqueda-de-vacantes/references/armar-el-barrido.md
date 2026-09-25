# Armar el barrido

Los filtros viven en `mi-cerebro/barrido.json`. El de Toffy está en `ejemplo/barrido.json` y sirve de modelo.

## El barrido de exploración, antes del paso 3

Sirve para juntar los avisos que el paso 3 necesita, cuando todavía no hay carriles. Es el mismo motor: lo único que cambia es qué se pone en `titulos`.

**La clave del carril es un nombre cualquiera**, así que en vez de `A` y `B` van dos grupos:

```json
"titulos": {
  "explorar": ["analista de datos", "data analyst", "salud publica"],
  "contrario": ["docente", "coordinador de laboratorio", "asistente de investigacion"]
}
```

- **`explorar`** son los dos o tres títulos que la persona cree que quiere. Salen de lo que dijo en la tanda B del paso 1, no de un catálogo de puestos.
- **`contrario`** son los puestos que cree que **no** quiere, y no es opcional. Sin ellos el ejercicio de los lunes solo confirma lo que ya pensaba, y el paso 3 deja de servir. Se arman con lo que hace hoy y con el puesto vecino obvio de su rubro.

**Las ubicaciones** salen de dónde puede trabajar, que en esta altura del método ya se sabe por la tanda C del paso 1.

**Las empresas**, entre diez y quince del tipo que le interesa, probadas una por una:

```bash
python3 herramientas/barrido.py probar "Nombre de la empresa"
python3 herramientas/barrido.py probar https://jobs.lever.co/empresa --agregar
```

Después se corre una vez y se miran los hallazgos:

```bash
python3 herramientas/barrido.py barrer
python3 herramientas/barrido.py hallazgos
```

⚠️ **El barrido trae el título, la ubicación y el link. No trae el texto del aviso**, y los lunes del paso 3 se arman con las responsabilidades. Así que de los hallazgos se eligen entre 15 y 30, se abren, y se guardan en `mi-cerebro/avisos/`, uno por archivo, con la fecha y el link arriba. Eso es lo que el paso 3 va a leer.

**Cuando el paso 3 termine y existan los carriles de verdad**, se reemplazan `explorar` y `contrario` por `A` y `B`, con los títulos que salieron. Los hallazgos viejos quedan: los que no encajen en ningún carril se descartan con su motivo.

```json
{
 "empresas": [
  {"nombre": "Kilómetro Cero", "board": "greenhouse", "slug": "kilometrocero"}
 ],
 "titulos": {
  "A": ["product analyst", "analista de producto", "product owner", "product operations"],
  "B": ["e-commerce", "ecommerce", "tienda online", "comercio electronico"]
 },
 "titulos_no": ["senior product manager", "head", "director", "gerente", "lead", "practica", "intern"],
 "ubicacion_si": ["santiago", "chile"],
 "ubicacion_no": ["argentina", "peru", "colombia", "mexico", "brasil", "brazil", "united states", "us", "spain", "espana"],
 "ubicacion_salva": ["chile"]
}
```

---

## Cómo compara

- **Palabras enteras.** `"ar"` encuentra "Remote job AR" y no encuentra "Marketing".
- **Da igual mayúsculas, tildes y signos.** `"comercio electronico"` encuentra "Comercio Electrónico", y `"e-commerce"` encuentra "E-Commerce". Pero `"e-commerce"` no encuentra "Ecommerce": si los avisos lo escriben de las dos formas, van las dos.
- **Un aviso pasa si** su título tiene alguna palabra de algún carril, no tiene ninguna de `titulos_no`, y su ubicación sirve.

---

## Los títulos

**Una lista por carril**, con la letra o el nombre que tiene en `03-que-trabajo-quiero.md`. Así cada hallazgo llega diciendo a qué carril se parece.

- **Se sacan de los avisos reales del paso 3**, no del diccionario. Si los avisos que eligió decían "Product Owner" y "Analista de Producto", van esas.
- **Los dos idiomas**, si las empresas que le interesan publican en los dos.
- **Un título puede caer en dos carriles.** "Product Owner Tienda Online" cae en el A por "product owner" y en el B por "tienda online". Está bien: cuál variante de CV va se decide en el veredicto.

**`titulos_no`** es para lo que de verdad no quiere ver nunca: prácticas, cargos de dirección si no busca eso. Cuidado con palabras sueltas como `"senior"`. Veta "Senior Product Analyst", que a lo mejor sí le sirve. Si lo que no quiere es un cargo en particular, se escribe entero (`"senior product manager"`).

---

## Las ubicaciones

Tres listas, porque los boards escriben la ubicación como quieren:

| Lista | Qué hace | Ejemplo |
|---|---|---|
| `ubicacion_si` | El aviso tiene que nombrar al menos uno | `"chile"`, `"latam"`, `"remote"` |
| `ubicacion_no` | Si nombra uno de estos, no pasa | `"united states"`, `"us"`, `"europe"` |
| `ubicacion_salva` | Si nombra uno de estos, el veto no aplica | `"chile"`, `"latam"` |

**Por qué hace falta `ubicacion_salva`.** Muchos avisos dicen "United States, LATAM" o "Remote: Brazil, Chile, Mexico". Sin la lista que salva, `"united states"` o `"brazil"` los tiraría enteros, y son justo los que sirven.

**La trampa del remoto.** "Remote, US" es remoto dentro de Estados Unidos, y "Remote (Canada)" es remoto dentro de Canadá. Si pone `"remote"` en `ubicacion_si`, tiene que poner en `ubicacion_no` los países donde no puede trabajar, incluido `"us"`. El barrido tampoco usa la marca de "remoto" que tienen algunos boards: muchas empresas la activan para puestos que son remotos solo dentro de su país.

**Un aviso sin ubicación no pasa** si `ubicacion_si` tiene algo. Si `ubicacion_si` está vacía, pasa todo lo que no esté vetado.

**Antes de fijar las listas, se miran las ubicaciones de verdad.** `probar` muestra las de los primeros avisos de cada empresa. Conviene arrancar con filtros anchos, correr una vez, y ajustar mirando qué entró.

---

## Las empresas

Cada empresa necesita tres datos:

| Campo | Qué es |
|---|---|
| `nombre` | Cómo la quiere ver en el registro y en el tablero |
| `board` | `greenhouse`, `lever`, `ashby` o `recruitee` |
| `slug` | El nombre que usa ese board para la empresa, el que aparece en la URL |

No hace falta escribirlos a mano. `probar` los encuentra:

```bash
python3 herramientas/barrido.py probar "Nombre de la empresa"
python3 herramientas/barrido.py probar https://job-boards.greenhouse.io/empresa --agregar
python3 herramientas/barrido.py probar https://empresa.recruitee.com --agregar --nombre "Empresa S.A."
```

**Con el nombre**, prueba variantes en los cuatro boards y puede no encontrarla si el board la llama distinto. **Con la URL es seguro.** La URL sale del botón "Trabaja con nosotros" o "Careers" del sitio de la empresa: si al hacer clic la dirección tiene `greenhouse.io`, `lever.co`, `ashbyhq.com` o `recruitee.com`, se puede barrer.

Si publica en otro lado (Workday, SuccessFactors, su propio sitio, solo LinkedIn), el barrido no la puede mirar. Para esa empresa, la alerta por correo de su sitio.

**`probar` dice cuántos avisos tiene abiertos hoy y cuántos pasan los filtros.** Una empresa con cero avisos que pasen no es un error: puede publicar la semana que viene. Se agrega igual si es del tipo que busca.

---

## Qué no se vuelve a avisar

- **Lo que ya encontró**, aunque la persona lo haya ignorado.
- **Lo que ya está en el registro**, se reconoce por el número del aviso en el link o por la empresa más el título.
- **El mismo puesto publicado una vez por país.** "Product Analyst Chile" y "Product Analyst Perú" de la misma empresa son un solo hallazgo.

Lo que no pasó los filtros no se guarda. Si la empresa corrige el título o la ubicación de un aviso, en la próxima pasada se vuelve a mirar.
