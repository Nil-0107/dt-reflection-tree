#!/usr/bin/env bash
set -euo pipefail

# Create virtual environment in .venv and install requirements (if any)
python3 -m venv .venv

# Use the venv to upgrade pip and install requirements
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt || true

# Deactivate the sub-shell activation
deactivate

echo "Created .venv. Activate with: source .venv/bin/activate"
