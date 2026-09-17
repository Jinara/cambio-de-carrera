# Correr el barrido solo

Lo mismo sirve para el correo: donde dice `barrido.py` va `correo.py`, con otro nombre de tarea y unos minutos después (por ejemplo 9:15, 13:15 y 19:15), así el correo encuentra en el registro lo que el barrido acaba de sumar. El correo necesita que el comando `claude` esté en el `PATH` de la tarea: en launchd y en cron conviene poner la ruta completa, que sale de `which claude`, en una variable `PATH`.

Se programa **después** de la primera corrida a mano, cuando los filtros ya dejan pasar lo que sirve. La primera corrida además crea `mi-cerebro/barrido/`, donde van los registros de las corridas programadas.

## Cada cuánto

Dos o tres veces por día alcanza. Los boards no cambian cada hora, y consultarlos más seguido es mandarles tráfico sin ninguna ganancia.

## Por qué en tu computadora

Los agentes programados en la nube (los de Claude, y en general los de cualquier asistente) corren en un entorno que no tiene salida a los boards de empleo. Se probó 26 veces y las 26 fallaron con la conexión rechazada. Y buscar vacantes por web no lo reemplaza: devuelve avisos que cerraron hace semanas.

La contracara: **si la computadora está apagada o dormida, no corre.** Si recién se despierta, puede correr antes de tener red, y esa corrida queda anotada como "no se pudo mirar nada". No quiere decir que no haya vacantes. El tablero muestra cuándo fue la última corrida y avisa si pasaron tres días.

---

## Mac

Con launchd, que es lo que usa macOS para tareas programadas.

1. Averigua la ruta de Python y la del repo:
   ```bash
   which python3
   cd cambio-de-carrera && pwd
   ```
2. Crea `~/Library/LaunchAgents/cambio-de-carrera.barrido.plist` con esto. Cambia `/usr/bin/python3` por lo que dio `which python3`, y `/Users/TU_USUARIO/cambio-de-carrera` por la ruta del repo (aparece tres veces):
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key>
     <string>cambio-de-carrera.barrido</string>
     <key>ProgramArguments</key>
     <array>
       <string>/usr/bin/python3</string>
       <string>/Users/TU_USUARIO/cambio-de-carrera/herramientas/barrido.py</string>
     </array>
     <key>StartCalendarInterval</key>
     <array>
       <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
       <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>0</integer></dict>
       <dict><key>Hour</key><integer>19</integer><key>Minute</key><integer>0</integer></dict>
     </array>
     <key>StandardOutPath</key>
     <string>/Users/TU_USUARIO/cambio-de-carrera/mi-cerebro/barrido/launchd.log</string>
     <key>StandardErrorPath</key>
     <string>/Users/TU_USUARIO/cambio-de-carrera/mi-cerebro/barrido/launchd.log</string>
   </dict>
   </plist>
   ```
3. Revisa que esté bien escrito y actívalo:
   ```bash
   plutil -lint ~/Library/LaunchAgents/cambio-de-carrera.barrido.plist
   launchctl load -w ~/Library/LaunchAgents/cambio-de-carrera.barrido.plist
   ```
4. Pruébalo sin esperar a la hora:
   ```bash
   launchctl start cambio-de-carrera.barrido
   tail mi-cerebro/barrido/launchd.log
   ```

Si la Mac estaba dormida a la hora programada, macOS lo corre una vez al despertar.

⚠️ **Si el repo está en Documentos, Escritorio o Descargas**, macOS puede bloquearle el acceso a una tarea programada, y el log dice `Operation not permitted`. Lo más simple es tener el repo en otra carpeta, por ejemplo directo en tu carpeta de usuario.

**Para apagarlo:**
```bash
launchctl unload -w ~/Library/LaunchAgents/cambio-de-carrera.barrido.plist
```

---

## Linux

Con cron. Abre la tabla con `crontab -e` y agrega una línea, cambiando la ruta:

```
0 9,13,19 * * * /usr/bin/python3 /home/TU_USUARIO/cambio-de-carrera/herramientas/barrido.py >> /home/TU_USUARIO/cambio-de-carrera/mi-cerebro/barrido/cron.log 2>&1
```

Desde cron, la notificación de escritorio muchas veces no aparece, porque cron no tiene acceso a la sesión gráfica. El reporte y el tablero funcionan igual.

**Para apagarlo:** `crontab -e` y se borra la línea.

---

## Windows

Con el Programador de tareas. En una terminal (PowerShell o Símbolo del sistema), una tarea por horario, cambiando la ruta:

```
schtasks /Create /SC DAILY /ST 09:00 /TN "Barrido de vacantes 09" /TR "py C:\Users\TU_USUARIO\cambio-de-carrera\herramientas\barrido.py"
schtasks /Create /SC DAILY /ST 13:00 /TN "Barrido de vacantes 13" /TR "py C:\Users\TU_USUARIO\cambio-de-carrera\herramientas\barrido.py"
schtasks /Create /SC DAILY /ST 19:00 /TN "Barrido de vacantes 19" /TR "py C:\Users\TU_USUARIO\cambio-de-carrera\herramientas\barrido.py"
```

Si `py` no existe en tu computadora, usa `python` en su lugar. En Windows el barrido no manda notificación. Lo nuevo se ve en el tablero y en `mi-cerebro\barrido\ultimo.md`.

**Para apagarlo:** `schtasks /Delete /TN "Barrido de vacantes 09"`, y lo mismo con las otras dos.

---

## Cómo saber que sigue corriendo

- **El tablero** dice cuándo fue el último barrido y cuántas empresas pudo mirar. Si pasaron tres días, lo avisa en rojo.
- **`mi-cerebro/barrido/ultimo.md`** tiene el reporte de la última corrida, con la fecha y la hora arriba.
- **`mi-cerebro/barrido/hallazgos.json`** guarda las últimas 60 corridas: cuántas empresas miró, cuántas fallaron y por qué.

Un barrido que se apagó sin avisar es peor que no tener barrido, porque da la sensación de que no aparece nada. Conviene mirar la fecha del último cada vez que se abre el tablero.
