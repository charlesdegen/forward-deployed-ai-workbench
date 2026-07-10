# Acceptance Criteria: Mission Autonomy Field Support Console (Starter)

**Artifact:** Starter triage console in `src/apps/streamlit_app.py`  
**Specs:** `product_brief.md`, `data_contract.md`, `operator_workflow.md`

> **Ratified 2026-07-09.** Every criterion below was mapped to concrete evidence —
> a pinned test assertion, a `scripts/verify.sh` gate, or a verified code path —
> and the full gate (`./scripts/verify.sh` with the complete Playwright smoke)
> passed on a clean working tree. Install-on-3.11+ was validated by building a
> fresh venv from `requirements-lock.txt` with `pip install --require-hashes`.
> UI criteria are exercised by `scripts/smoke_ui.py`, which launches every
> operator surface headlessly — the starter with `OPENAI_API_KEY` unset.
> Re-ratify if a criterion's evidence is removed.

## Run & environment

- [x] `python -m venv .venv && pip install -r requirements.txt` succeeds on Python 3.11+
- [x] `streamlit run src/apps/streamlit_app.py` launches without API credentials
- [x] `./scripts/verify.sh` exits 0 on a clean checkout

## Telemetry ingestion

- [x] **Mock source** generates 50 synthetic records with known anomalies
- [x] **Fixture source** loads `fixtures/sample_telemetry.csv` and scores alerts
- [x] **Upload source** accepts a valid CSV and rejects missing columns with a visible error
- [x] Scoring logic runs in `src/core/ingestion.py`, not in the Streamlit layer

## Operator workflow

- [x] System state reflects alert count (NOMINAL vs DEGRADED)
- [x] Telemetry timeline chart renders CPU, temperature, and battery
- [x] Critical alerts queue shows rows where `risk_score > 0`
- [x] Operator can append actions to `artifacts/operator_action_log.csv`
- [x] Empty action submission shows validation error

## Governance

- [x] Sidebar shows live **data source**, **record count**, and **last refresh**
- [x] Deployment posture and test status are visible without opening code
- [x] No hardcoded secrets in repository files

## AI-assisted triage (prompt export mode)

- [x] Offline fallback checklist renders when `OPENAI_API_KEY` is unset
- [x] With API key set, ChatGPT diagnostic prompt includes data source and anomalous records
- [x] Codex repair brief is exportable from the AI tab
- [x] Live OpenAI API calls are **not** required for starter acceptance

## Testing

- [x] `pytest` covers: mock generation, anomaly scoring, schema validation, CSV load, fixture load, file-like parse
- [x] `ruff check src tests` passes
- [x] `py_compile` succeeds on `streamlit_app.py` and `ingestion.py`

## Agent readiness

- [x] `AGENTS.md` and `CLAUDE.md` load FDE constraints for agent sessions
- [x] `skills/triage-skill/SKILL.md` documents ChatGPT, Codex, Grok Build, and Claude Code roles
- [x] Build briefs exist under `prompts/` for each adapter

## Governance & eval (P2)

- [x] `/evals/` scorecards exist (artifact, security, field readiness)
- [x] `src/schemas/` JSON schemas validate input, output, and RCA packets
- [x] `tests/golden_outputs/fixture_scoring_summary.json` regression passes
- [x] RCA packet export from Operator Log tab writes to `artifacts/exports/`
- [x] RCA JSON validates against `rca_packet_schema.json`

## Mission Console (NiceGUI + DuckDB)

- [x] `python src/apps/nicegui_app.py` launches on `http://127.0.0.1:8080`
- [x] Fixture ingest on startup populates `artifacts/mission_console.duckdb`
- [x] Governance panel shows live data source, alerts, system state
- [x] SQL-backed alerts queue matches Python scoring (13 alerts on fixture)
- [x] Degraded-mode switch and guidance visible when DEGRADED
- [x] RCA export from Operator Log tab

## Out of scope (starter)

- Live LLM inference inside Streamlit/NiceGUI
- Polars query layer for very large files
- RCA packet PDF export
- NiceGUI variant (portfolio artifact #1)

## Demo script (3 minutes)

1. Launch app; confirm fixture source selected by default.
2. Show governance panel with live metadata.
3. Open Telemetry tab; point out anomaly at ~index 30 in alerts queue.
4. Append one operator action; confirm log persistence.
5. Export RCA packet from Operator Log tab; confirm files in `artifacts/exports/`.
6. Open AI tab; show offline checklist or exported prompts.
7. Run `./scripts/verify.sh` and show passing output.