#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_CMD" -m venv .venv
fi

echo "Installing dependencies..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "Starting app..."
PYTHONPATH="$(pwd)/src" .venv/bin/python -m aws_restart_lab
