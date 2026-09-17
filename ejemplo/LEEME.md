# El ejemplo: Toffy Villamor

**Toffy no existe.** Tampoco existen las empresas donde trabajó ni las empresas a las que se postula. Todos los nombres, números, correos y fechas de esta carpeta son inventados. Si alguno coincide con algo real, es casualidad.

Está acá para mostrar cómo queda `mi-cerebro/` cuando se corren los siete pasos de punta a punta.

## Quién es

Nueve años de carrera en Santiago de Chile. Dos en una distribuidora de alimentos haciendo control de gestión, y siete en una cadena de farmacias, primero en abastecimiento y después como analista senior de operaciones. Sigue empleada. Dice que quiere ser Product Manager "en una empresa de tecnología grande, de las que tienen app".

Se eligió un caso así a propósito. Su evidencia son evaluaciones de desempeño, correos, una planilla de un piloto y un tablero de la empresa que puede mirar pero no exportar. Ninguna base de datos propia. Es el caso difícil, y es el de la mayoría de la gente.

## Qué mirar primero

1. **`03-que-trabajo-quiero.md`, la revelación.** El puesto que decía querer perdió los tres pares en que apareció.
2. **`02-evidencia.md`, la tabla de límites.** Arriba de todo, antes del primer número. Y la fila del tablero de la cadena: el número existe, mejoró, y aun así no va al CV como logro suyo.
3. **`05-postulaciones.md`, la descartada.** Un aviso que le encantaba y que no conviene mandar.
4. **El tablero.** `python3 herramientas/tablero.py --cerebro ejemplo`. Las dos postulaciones de agosto, con su CV de antes, llevan semanas sin respuesta. Las del método recién empiezan, y el experimento lo dice: con cuatro enviadas no se puede concluir nada.
5. **`06-banco-de-historias.md`, la tabla del final.** Dos preguntas comunes sin historia, dejadas a la vista en vez de inventar algo.
6. **`entrevistas/tiendas-lumbrera/simulacro.md`.** Tres tomas de "cuéntame de ti": de 94 segundos con "como 200 locales" a 63 segundos con los números de la evidencia. En la del medio se le escapó un número retirado justo en la última oración.
7. **`numeros-retirados.txt`.** Cuatro cosas que Toffy venía diciendo y dejó de decir. La última salió en el simulacro.

## Lo que no está

- **Los 22 avisos** del paso 3. Se citan en `03-que-trabajo-quiero.md`, pero no se incluyen.
- **Los audios** del simulacro. Solo las transcripciones.
- **Los montos de plata.** Van como `[MONTO]`. Las fuentes de sueldo cambian por país y por mes, y un número de ejemplo se termina copiando como si fuera una referencia.

## Probar las herramientas con ella

```bash
python3 herramientas/generar-cv.py ejemplo/cv/*.md
```

Deja los PDF en `ejemplo/cv/build/`. Si le agregas "300 millones" a cualquier viñeta y lo corres de nuevo, se niega a generar.

```bash
python3 herramientas/comparar-tomas.py ejemplo/entrevistas/tiendas-lumbrera/tomas-p1.txt --objetivo 60
```

Compara las tres tomas del simulacro: el reloj, los locales que pasan de 200 a 180, y los dos números retirados.

```bash
python3 herramientas/tablero.py --cerebro ejemplo
python3 herramientas/barrido.py hallazgos --cerebro ejemplo
python3 herramientas/vacantes.py seguimiento --cerebro ejemplo
```

El tablero de Toffy, lo que encontró su barrido y lo que lleva 14 días sin respuesta. En el tablero puedes cambiar estados y pasar hallazgos a revisar: con el ejemplo nada se guarda. El barrido del ejemplo no sale a internet, porque sus empresas son inventadas. Sus filtros están en `barrido.json`.
