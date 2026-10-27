#!/usr/bin/env bash
# One-time install of the print-upscale tools into ~/.local/share/print-upscale
# (override with PRINT_UPSCALE_HOME). Downloads:
#   - realesrgan-ncnn-vulkan macOS build (~52 MB, github.com/xinntao/Real-ESRGAN, BSD-3)
#   - a Python venv with vtracer, numpy, pillow, reportlab (PyPI)
# Ask the user before running it - it downloads files.
set -euo pipefail

HOME_DIR="${PRINT_UPSCALE_HOME:-$HOME/.local/share/print-upscale}"
URL="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip"
mkdir -p "$HOME_DIR"

if [ ! -x "$HOME_DIR/realesrgan/realesrgan-ncnn-vulkan" ]; then
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/r.zip" "$URL"
  unzip -q -o "$tmp/r.zip" -d "$tmp/x"
  mkdir -p "$HOME_DIR/realesrgan"
  cp -R "$tmp/x/realesrgan-ncnn-vulkan" "$tmp/x/models" "$HOME_DIR/realesrgan/"
  chmod +x "$HOME_DIR/realesrgan/realesrgan-ncnn-vulkan"   # zip drops the exec bit
  xattr -dr com.apple.quarantine "$HOME_DIR/realesrgan" 2>/dev/null || true
  rm -rf "$tmp"
fi

# reportlab needs Python >= 3.10; macOS /usr/bin/python3 is 3.9
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$c" >/dev/null && "$c" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || { echo "need Python >= 3.10 (brew install python@3.12)" >&2; exit 1; }

if [ ! -x "$HOME_DIR/venv/bin/python" ] || ! "$HOME_DIR/venv/bin/python" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  rm -rf "$HOME_DIR/venv"
  "$PY" -m venv "$HOME_DIR/venv"
fi
"$HOME_DIR/venv/bin/pip" install -q --disable-pip-version-check vtracer numpy pillow reportlab

"$HOME_DIR/venv/bin/python" -c "import vtracer, numpy, PIL, reportlab" \
  && [ -x "$HOME_DIR/realesrgan/realesrgan-ncnn-vulkan" ] \
  && echo "print-upscale ready: $HOME_DIR"
