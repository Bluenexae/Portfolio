#!/usr/bin/env bash
set -e

# Create and activate a virtual environment if needed
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Flask app..."
python app.py
