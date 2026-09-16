# Empezar

## Lo que hay que instalar

| Qué | Para qué | Obligatorio |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) o [Codex](https://learn.chatgpt.com/docs/codex/cli) | Todo el método | Uno de los dos |
| Python 3 | Generar el CV y revisar textos | Para el paso 4 |
| Chrome, Chromium, Edge o Brave | Pasar el CV a PDF | Para el paso 4 |
| pandoc | El CV en DOCX (en Mac no hace falta: se usa `textutil`) | No |
| `whisper-cli` y `ffmpeg` | El simulacro hablado, y contestar hablando en el paso 1 | Para el paso 7 |

## Lo que conviene juntar antes

No hace falta tener todo para arrancar. El paso 1 funciona solo con conversación. Pero cuanto más tengas a mano, menos `[SIN FUENTE]` te quedan en el paso 2.

**Para el paso 1:**
- Tu CV actual.
- Tu perfil de LinkedIn en PDF (en tu perfil: Más → Guardar en PDF).

**Para el paso 2**, lo que tengas de esta lista:
- Certificados laborales de cada trabajo. Si no los tienes, casi todas las empresas los emiten a pedido, incluso años después. Pídelos ya, porque tardan.
- Contratos, cartas de ascenso, recibos de sueldo del primer y último mes.
- Evaluaciones de desempeño.
- Correos que hayas guardado con resultados, felicitaciones o aprobaciones de proyectos.
- Presentaciones o informes tuyos.
- Si tuviste un negocio o trabajas por tu cuenta: acceso a tus repositorios, bases de datos, tableros y cuentas de anuncios.

**Para el paso 3:**
- Entre 15 y 30 avisos reales, con link. De puestos que te interesan **y de algunos que crees que no**. Sin esos últimos, el ejercicio solo confirma lo que ya pensabas.

**Para el paso 6:**
- El correo de quien te escribió para entrevistarte, pegado entero, con fecha y hora.

## Cuánto lleva

El paso 1 es el más largo. Es una entrevista de a una pregunta por vez, y conviene hacerla en varias sesiones. El archivo guarda dónde quedaste y `/empezar` retoma desde ahí.

Los pasos 2, 3 y 4 dependen de cuánta evidencia tengas y de cuántos avisos traigas.

El 5 conviene hacerlo apenas mandas las primeras postulaciones, sin esperar a que te llamen. El 6 y el 7 se hacen por cada empresa, entre el correo y la entrevista, así que dependen de cuántos días te den.

## Hablar en vez de escribir

El simulacro del paso 7 va en audio: hablando aparece lo que escribiendo se filtra. Y el descubrimiento también se puede contestar con notas de voz. Para las dos cosas:

```bash
brew install whisper-cpp ffmpeg
mkdir -p ~/.local/share/whisper-models
curl -L -o ~/.local/share/whisper-models/ggml-large-v3-turbo-q5_0.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
```

Graba con la app de notas de voz, deja los audios en `herramientas/audios/` y dile al asistente que los transcriba. Corre `herramientas/transcribir.sh` en tu máquina, sin internet. Los audios están en `.gitignore`.

Si todavía no instalaste Whisper, en el simulacro puedes pegar la transcripción automática de tu teléfono. Se pierde la duración de cada toma, que es una de las cosas que se miran.

En Linux, `whisper-cli` se compila desde [whisper.cpp](https://github.com/ggerganov/whisper.cpp).

## Si usas Codex

Funciona con Codex en la app de escritorio de ChatGPT, en la terminal o en la extensión para el editor, siempre con la carpeta del repo en tu computadora.

**No lo uses con Codex en la nube**, las tareas que corren en chatgpt.com. Ahí tu `mi-cerebro/`, con tu sueldo y lo que salió mal, quedaría en un servidor y no en tu computadora, y tus audios tampoco se transcribirían en tu máquina.

### Con la app de escritorio de ChatGPT

1. **Descarga la app** desde [la página oficial de ChatGPT](https://learn.chatgpt.com/docs/app). Hay versión para Mac, Windows y Linux, y Codex viene adentro. Entras con tu cuenta de ChatGPT.
2. **Baja el repo a tu computadora.** En la terminal:
   ```bash
   git clone https://github.com/Jinara/cambio-de-carrera
   ```
   Si no usas la terminal y estás en Mac, en la página del repo en GitHub le das clic a **Code**, después a **Download ZIP**, y lo descomprimes. En Windows, usa la terminal (más abajo está por qué).
3. **En Codex, crea un proyecto con esa carpeta.** Al crear el proyecto, elige usar una carpeta que ya existe y selecciona `cambio-de-carrera`. Tiene que ser esa carpeta y no la de arriba: si Codex queda en otra, no encuentra las reglas del método.
4. **Escribe `empezar`**, sin la barra.

### Con la terminal

Para instalarlo:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Y para arrancar, adentro de la carpeta del repo:

```bash
codex --search
```

La primera vez te pide entrar con tu cuenta de ChatGPT. `--search` le permite buscar en la web, que hace falta para investigar las empresas en el paso 6. Después escribes `empezar`, sin la barra.

### Si no arranca

Si Codex contesta algo genérico en vez de empezar el método, pégale esto:

```
Lee el archivo AGENTS.md de esta carpeta y después .claude/commands/empezar.md. Sigue las instrucciones de empezar.md paso a paso, empezando por el chequeo de privacidad. Las skills del método están en .agents/skills: cuando un paso diga que uses una skill, lee su SKILL.md y sus references antes de seguir.
```

Si tampoco así, pregúntale en qué carpeta está trabajando. Si no es `cambio-de-carrera`, el proyecto quedó en otra carpeta y hay que crearlo de nuevo.

### Lo que cambia respecto de Claude Code

| En Claude Code | En Codex |
|---|---|
| `/empezar` | `empezar`, sin la barra. Con la barra, Codex lo toma como uno de sus propios comandos |
| Las skills se usan solas o nombrándolas | Igual, o con `$descubrimiento`, `$simulacro`, etc. En la terminal, `/skills` las lista. En la app, con `@` |
| Pide permiso antes de correr un script | Igual. En la terminal, `/permissions` cambia cuándo pregunta |

### En Windows

Codex encuentra las skills a través de un enlace (`.agents/skills`), y git en Windows no siempre crea enlaces. Clona con `git clone -c core.symlinks=true https://github.com/Jinara/cambio-de-carrera`, o usa WSL. Por lo mismo, en Windows no sirve bajar el ZIP.

## El primer día

```bash
git clone https://github.com/Jinara/cambio-de-carrera
cd cambio-de-carrera
claude
```

```
/empezar
```

Con Codex, en vez de `claude` creas un proyecto con la carpeta del repo (o abres `codex --search` en la terminal), y escribes `empezar` sin la barra.

Y contesta. Si en algún momento quieres ver cómo queda un archivo terminado, está en `ejemplo/`.
