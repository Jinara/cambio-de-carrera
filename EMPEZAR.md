# Empezar

## Lo que hay que instalar

| Qué | Para qué | Obligatorio |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) | Todo el método | Sí |
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

Graba con la app de notas de voz, deja los audios en `herramientas/audios/` y dile a Claude que los transcriba. Corre `herramientas/transcribir.sh` en tu máquina, sin internet. Los audios están en `.gitignore`.

Si todavía no instalaste Whisper, en el simulacro puedes pegar la transcripción automática de tu teléfono. Se pierde la duración de cada toma, que es una de las cosas que se miran.

En Linux, `whisper-cli` se compila desde [whisper.cpp](https://github.com/ggerganov/whisper.cpp).

## El primer día

```bash
git clone https://github.com/Jinara/cambio-de-carrera
cd cambio-de-carrera
claude
```

```
/empezar
```

Y contesta. Si en algún momento quieres ver cómo queda un archivo terminado, está en `ejemplo/`.
