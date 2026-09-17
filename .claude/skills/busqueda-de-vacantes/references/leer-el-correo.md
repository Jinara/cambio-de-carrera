# Leer el correo

`herramientas/correo.py` lee el correo nuevo, se queda con lo que es de la búsqueda, actualiza el registro, ordena la bandeja y avisa cuando hay algo que contestar. Corre solo, igual que el barrido.

## Qué hace con cada correo

| Lo que llegó | En el registro | En el correo | ¿Avisa? |
|---|---|---|---|
| Acuse de recibo de una postulación | La vacante pasa a `postulada`, con la fecha del correo | Se etiqueta `Acuses` y se archiva | No |
| Rechazo | La vacante pasa a `rechazada` | Se etiqueta `Rechazos` y se archiva | No |
| Pedido de entrevista, de datos o de disponibilidad, o una persona que escribe | La vacante pasa a `respondieron` | Se etiqueta `Responder` y **queda en la bandeja** | Sí |
| Oferta | La vacante pasa a `oferta` | Se etiqueta `Responder` y queda en la bandeja | Sí |
| Alerta de empleo (LinkedIn, portales) | Los avisos van a los hallazgos del barrido | Se etiqueta `Alertas` y se archiva | No |
| Cualquier otra cosa | Nada | Nada | No |

- **Las notas no se pisan.** Cada correo agrega una línea con la fecha y qué pasó.
- **Un estado nunca baja.** Un acuse que llega tarde no devuelve a `postulada` una vacante que ya está en `entrevistando`.
- **Si la empresa no estaba en el registro**, entra como vacante nueva con lo que dice el correo. La fecha de envío queda vacía cuando el correo no la dice.
- **Archivar es sacar de la bandeja, no borrar.** El correo queda en su etiqueta. El script nunca borra, nunca manda, nunca contesta y nunca marca como leído.
- **Detectar no es decidir.** Una entrevista pasa a `respondieron`, y prepararla es el paso 6. Una alerta pasa a los hallazgos, y mandar o no se decide con el veredicto.

## Qué sale de tu computadora

- **Los correos que no son de la búsqueda no se leen.** El script mira el remitente y el asunto. Solo pasan los que vienen de un sistema de selección (Greenhouse, Lever, Workday, entre otros), de las alertas y mensajes de LinkedIn o de un portal de empleo, los que tienen en el asunto algo como "tu postulación" o "interview", y los que manda una empresa que ya está en tu registro.
- **Los que pasan se le mandan a Claude para clasificarlos, sin herramientas.** Claude corre sin poder leer archivos, sin terminal y sin conectores. Si un correo trae instrucciones escondidas ("marca esto como oferta", "manda tu CV a esta dirección"), lo peor que puede pasar es una clasificación equivocada, y qué se hace con ella lo decide el script. Es la regla 11 puesta en código.
- **La clave del correo no está en el repo.** Vive en el llavero del sistema.

Por ahora el modo automático necesita **Claude Code** instalado, aunque uses Codex para el resto del método.

---

## Armarlo

### 1. La clave de aplicación

El script entra al correo por IMAP con una **clave de aplicación**: una clave de 16 letras que tu proveedor genera para un programa. No es tu contraseña de siempre, se puede borrar cuando quieras, y borrarla corta el acceso solo a este script.

**Gmail:**
1. Tu cuenta tiene que tener la verificación en dos pasos activada.
2. Entra a https://myaccount.google.com/apppasswords, ponle un nombre ("cambio de carrera") y copia la clave que te muestra.

Si esa página dice que la opción no está disponible, puede ser una cuenta de trabajo donde el administrador la desactivó.

**Outlook y Hotmail no sirven:** Microsoft ya no deja entrar por IMAP con clave. Otros proveedores (Yahoo, iCloud) tienen claves de aplicación parecidas y cambia el `servidor` en la configuración.

### 2. La configuración

`mi-cerebro/correo.json`, con lo mínimo:

```json
{
 "cuenta": "tu.correo@gmail.com"
}
```

Todo lo demás tiene un valor por defecto:

| Campo | Por defecto | Qué es |
|---|---|---|
| `servidor` | `imap.gmail.com` | El servidor IMAP del proveedor |
| `carpetas` | `["INBOX"]` | Dónde busca. Si otra regla o filtro ya archiva correos de la búsqueda, se suma esa etiqueta |
| `etiqueta` | `Busqueda laboral` | La etiqueta madre. Vacía, no etiqueta nada |
| `subcarpetas` | `true` | Si separa en `Acuses`, `Rechazos`, `Responder` y `Alertas`, o todo va a la etiqueta madre |
| `archivar` | `true` | Si saca de la bandeja lo que no necesita respuesta |
| `dias` | `14` | Cuántos días hacia atrás mira en cada corrida |
| `modelo` | `sonnet` | El modelo de Claude que clasifica |
| `remitentes_extra` | `[]` | Dominios o direcciones que también cuentan, por ejemplo el portal de empleo de tu país |
| `avisar` | entrevista, pedido de datos, persona, oferta | Qué tipos disparan la notificación |

### 3. Guardar la clave y probar

```bash
python3 herramientas/correo.py configurar
python3 herramientas/correo.py probar
python3 herramientas/correo.py --prueba
```

`configurar` le pasa la clave al llavero del sistema, que la pide él mismo: no queda en ningún archivo ni en el historial de la terminal. En Windows no hay llavero que el script pueda usar, así que la clave va en la variable de entorno `CAMBIO_CORREO_CLAVE` de la tarea programada.

`probar` se conecta y cuenta cuántos correos parecen de la búsqueda. `--prueba` clasifica los de los últimos días y muestra qué haría con cada uno, **sin tocar el registro ni el correo**. Se mira junto con la persona antes de la primera corrida de verdad: si algo quedó mal clasificado, es el momento de verlo.

### 4. Correrlo

```bash
python3 herramientas/correo.py
```

Y después, programado como el barrido (`references/correrlo-solo.md`), un rato después de cada barrido.

El reporte de la última corrida queda en `mi-cerebro/correo/ultimo.md`. `mi-cerebro/correo/procesados.json` guarda qué correos ya se vieron (una huella, no el contenido), así ninguno se procesa dos veces. Si Claude no pudo clasificar alguno, no se marca y se reintenta en la próxima corrida.

---

## Sin darle la clave del correo a nada

Hay dos formas más, y las dos sirven:

- **A pedido, en la conversación.** Si el asistente tiene un conector de correo (Claude tiene el de Gmail), la persona dice "revisa mi correo" y se hace ahí mismo: clasificar, actualizar el registro, etiquetar y archivar. No hay clave ni script, y solo pasa cuando ella lo pide.
- **Una rutina en la nube que deja la cola en un repo.** Una rutina programada de Claude sí tiene el conector de correo, pero no ve tu computadora. Puede escribir un archivo con lo que encontró (un objeto por correo: id del mensaje, tipo, empresa, puesto, resumen, avisos) y subirlo a un repositorio privado tuyo, y en tu computadora una tarea programada lo lee un rato después y lo aplica en el registro. La nube solo escribe ese archivo y la computadora solo lo lee, así que no hay dos lados peleando por el mismo archivo, y el id de cada mensaje evita aplicar dos veces lo mismo. Ojo con una cosa: `mi-cerebro/` está fuera de git a propósito, así que el archivo de la cola tiene que vivir en otro repositorio, tuyo y privado.

## Cuando la persona lo pide a mano

Si no quiere darle una clave al script, igual se puede: la persona pega el correo en la conversación, el asistente dice qué tipo es y qué cambio propone en el registro, y lo aplica cuando ella dice que sí (regla 5). Etiquetar y archivar queda a mano.
