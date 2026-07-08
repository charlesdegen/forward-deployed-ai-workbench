#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "==> pytest"
python -m pytest -q

echo "==> ruff"
python -m ruff check src tests

echo "==> py_compile"
python -m py_compile src/apps/streamlit_app.py src/core/ingestion.py

echo "==> fixture present"
test -f fixtures/sample_telemetry.csv

echo "OK: all verification checks passed"