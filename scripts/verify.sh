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
python -m py_compile src/apps/streamlit_app.py src/core/ingestion.py src/core/exports.py

echo "==> fixture present"
test -f fixtures/sample_telemetry.csv

echo "==> schemas present"
test -f src/schemas/input_schema.json
test -f src/schemas/output_schema.json
test -f src/schemas/rca_packet_schema.json

echo "==> golden output present"
test -f tests/golden_outputs/fixture_scoring_summary.json

echo "OK: all verification checks passed"