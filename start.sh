#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ -x ".venv/bin/python" ]; then
  echo "Starting with .venv/bin/python -u bot.py"
  exec .venv/bin/python -u bot.py
fi

echo "No .venv found, creating one..."
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "Starting with .venv/bin/python -u bot.py"
exec .venv/bin/python -u bot.py
