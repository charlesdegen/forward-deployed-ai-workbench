#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "==> pytest"
python -m pytest -q \
  tests \
  local-data-fusion-workbench/tests \
  financial-crime-ops-console/tests \
  llm-red-team-eval-harness/tests

echo "==> ruff"
python -m ruff check src tests

echo "==> py_compile (mission)"
python -m py_compile src/apps/streamlit_app.py src/apps/nicegui_app.py src/core/ingestion.py src/core/exports.py src/core/duckdb_store.py

echo "==> py_compile (fusion)"
python -m py_compile local-data-fusion-workbench/fusion/apps/nicegui_app.py
for module in ingestion profiling matching fusion anomalies lineage duckdb_store exports; do
  python -m py_compile "local-data-fusion-workbench/fusion/core/${module}.py"
done

echo "==> py_compile (fin crime)"
python -m py_compile financial-crime-ops-console/fin_crime/apps/streamlit_app.py
for module in ingestion scoring duckdb_store exports; do
  python -m py_compile "financial-crime-ops-console/fin_crime/core/${module}.py"
done

echo "==> py_compile (redteam)"
python -m py_compile llm-red-team-eval-harness/redteam/apps/streamlit_app.py
for module in suite runner scoring exports; do
  python -m py_compile "llm-red-team-eval-harness/redteam/core/${module}.py"
done

echo "==> single-file brief present (air-gap vendor assets)"
test -f single-file-command-briefs/index.html
test -f single-file-command-briefs/vendor/echarts.min.js
test -f single-file-command-briefs/vendor/jquery.min.js
test -f single-file-command-briefs/vendor/jquery.dataTables.min.js
test -f single-file-command-briefs/vendor/jquery.dataTables.min.css
# Ensure index does not pull CDN scripts
if grep -E 'https://(cdn\.|code\.jquery)' single-file-command-briefs/index.html; then
  echo "FAIL: single-file brief still references CDN hosts" >&2
  exit 1
fi

echo "==> fixture present"
test -f fixtures/sample_telemetry.csv
test -f fixtures/sample_sensor_log.txt
test -f financial-crime-ops-console/fixtures/sample_transactions.csv
test -f llm-red-team-eval-harness/fixtures/redteam_suite.json

echo "==> schemas present"
test -f src/schemas/input_schema.json
test -f src/schemas/output_schema.json
test -f src/schemas/rca_packet_schema.json

echo "==> golden output present"
test -f tests/golden_outputs/fixture_scoring_summary.json

echo "==> docs present"
test -f docs/architecture.md
test -f docs/deployment.md
test -f docs/demo_script.md

echo "==> portfolio screenshots present"
for shot in \
  mission_console_overview.png \
  mission_console_operator_log.png \
  streamlit_starter_overview.png \
  data_fusion_overview.png \
  fin_crime_overview.png \
  redteam_overview.png \
  single_file_command_brief.png
do
  test -f "artifacts/screenshots/${shot}"
done

echo "==> claude/grok verify hooks present"
test -x .claude/hooks/require-verify.sh || chmod +x .claude/hooks/require-verify.sh
test -f .claude/settings.json
test -f .grok/hooks/require-verify.json

if [[ "${VERIFY_SECURITY:-0}" == "1" ]]; then
  echo "==> bandit (optional)"
  bandit -r src financial-crime-ops-console/fin_crime llm-red-team-eval-harness/redteam local-data-fusion-workbench/fusion -ll || true
  echo "==> pip-audit (optional)"
  pip-audit || true
fi

echo "==> playwright smoke (single-file brief by default; SMOKE_FULL=1 for apps)"
if [[ "${VERIFY_SMOKE:-1}" == "1" ]]; then
  SMOKE_REQUIRED="${SMOKE_REQUIRED:-0}" python scripts/smoke_ui.py
else
  echo "SKIP: VERIFY_SMOKE=0"
fi

# Stamp for PreToolUse commit/push hooks
mkdir -p artifacts
date -u +"%Y-%m-%dT%H:%M:%SZ" > artifacts/.last_verify_ok

echo "OK: all verification checks passed"
