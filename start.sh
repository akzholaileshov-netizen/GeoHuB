#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

pick_python() {
  if command -v python >/dev/null 2>&1 && python -c "import aiogram" 2>/dev/null; then
    echo python
    return
  fi
  if command -v python3 >/dev/null 2>&1 && python3 -c "import aiogram" 2>/dev/null; then
    echo python3
    return
  fi
  echo ""
}

PY="$(pick_python)"
if [ -z "$PY" ]; then
  echo "aiogram not found, installing requirements..."
  if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install -r requirements.txt
  else
    python -m pip install -r requirements.txt
  fi
  PY="$(pick_python)"
fi

if [ -z "$PY" ]; then
  echo "Python with aiogram still not found" >&2
  exit 1
fi

echo "Starting with: $PY -u bot.py"
exec "$PY" -u bot.py
