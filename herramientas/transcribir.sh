#!/bin/bash
# Transcribe notas de voz del simulacro. Todo local, sin internet.
# Uso: ./transcribir.sh archivo.m4a [mas archivos...]
#      ./transcribir.sh            -> transcribe todo lo que haya en audios/
set -uo pipefail

MODEL="$HOME/.local/share/whisper-models/ggml-large-v3-turbo-q5_0.bin"
DIR="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

files=("$@")
if [ ${#files[@]} -eq 0 ]; then
  while IFS= read -r f; do files+=("$f"); done < <(find "$DIR/audios" -type f \( -iname '*.m4a' -o -iname '*.mp3' -o -iname '*.wav' -o -iname '*.mp4' -o -iname '*.mov' -o -iname '*.aac' -o -iname '*.caf' \) | sort)
fi

[ ${#files[@]} -eq 0 ] && { echo "No hay audios en $DIR/audios"; exit 1; }

for f in "${files[@]}"; do
  [ -f "$f" ] || { echo "No existe: $f"; continue; }
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
  wav="$TMP/$(basename "${f%.*}").wav"
  ffmpeg -nostdin -loglevel error -y -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le "$wav" 2>/dev/null
  echo "=============================================="
  echo "ARCHIVO:  $(basename "$f")"
  echo "DURACION: ${dur:-?} segundos"
  echo "----------------------------------------------"
  whisper-cli -m "$MODEL" -f "$wav" -l auto -nt -np 2>/dev/null | sed 's/^[[:space:]]*//' | grep -v '^$'
  echo ""
done
