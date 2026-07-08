# Acceptance Criteria: Mission Autonomy Field Support Console (Starter)

**Artifact:** Starter triage console in `src/apps/streamlit_app.py`  
**Specs:** `product_brief.md`, `data_contract.md`, `operator_workflow.md`

## Run & environment

- [ ] `python -m venv .venv && pip install -r requirements.txt` succeeds on Python 3.11+
- [ ] `streamlit run src/apps/streamlit_app.py` launches without API credentials
- [ ] `./scripts/verify.sh` exits 0 on a clean checkout

## Telemetry ingestion

- [ ] **Mock source** generates 50 synthetic records with known anomalies
- [ ] **Fixture source** loads `fixtures/sample_telemetry.csv` and scores alerts
- [ ] **Upload source** accepts a valid CSV and rejects missing columns with a visible error
- [ ] Scoring logic runs in `src/core/ingestion.py`, not in the Streamlit layer

## Operator workflow

- [ ] System state reflects alert count (NOMINAL vs DEGRADED)
- [ ] Telemetry timeline chart renders CPU, temperature, and battery
- [ ] Critical alerts queue shows rows where `risk_score > 0`
- [ ] Operator can append actions to `artifacts/operator_action_log.csv`
- [ ] Empty action submission shows validation error

## Governance

- [ ] Sidebar shows live **data source**, **record count**, and **last refresh**
- [ ] Deployment posture and test status are visible without opening code
- [ ] No hardcoded secrets in repository files

## AI-assisted triage (prompt export mode)

- [ ] Offline fallback checklist renders when `OPENAI_API_KEY` is unset
- [ ] With API key set, ChatGPT diagnostic prompt includes data source and anomalous records
- [ ] Codex repair brief is exportable from the AI tab
- [ ] Live OpenAI API calls are **not** required for starter acceptance

## Testing

- [ ] `pytest` covers: mock generation, anomaly scoring, schema validation, CSV load, fixture load, file-like parse
- [ ] `ruff check src tests` passes
- [ ] `py_compile` succeeds on `streamlit_app.py` and `ingestion.py`

## Agent readiness

- [ ] `AGENTS.md` and `CLAUDE.md` load FDE constraints for agent sessions
- [ ] `skills/triage-skill/SKILL.md` documents ChatGPT, Codex, Grok Build, and Claude Code roles
- [ ] Build briefs exist under `prompts/` for each adapter

## Out of scope (starter)

- Live LLM inference inside Streamlit
- DuckDB/Polars query layer
- RCA packet PDF/HTML export (P2)
- NiceGUI variant (portfolio artifact #1)
- JSON schema files (P2)

## Demo script (3 minutes)

1. Launch app; confirm fixture source selected by default.
2. Show governance panel with live metadata.
3. Open Telemetry tab; point out anomaly at ~index 30 in alerts queue.
4. Append one operator action; confirm log persistence.
5. Open AI tab; show offline checklist or exported prompts.
6. Run `./scripts/verify.sh` and show passing output.