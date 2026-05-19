#!/usr/bin/env bash
set -e

PYTHON=python3
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python
fi

if [ ! -d ".venv" ]; then
  "$PYTHON" -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python -m streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0
