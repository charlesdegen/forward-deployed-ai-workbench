# Demo Script (≈8 minutes)

## Setup (before audience)

```bash
source .venv/bin/activate
./scripts/verify.sh
```

Leave Mission Console on `:8080` and optionally Fusion on `:8081`.

## 1. Mission Console (2 min) — artifact #1

1. Open http://127.0.0.1:8080
2. Point at governance: data source fixture, DEGRADED state, last refresh.
3. Show critical alerts queue + telemetry charts.
4. Append an operator log action; export RCA packet.

**Line:** “Operator triage with local DuckDB and an engineering handoff packet — no cloud DB.”

## 2. Data Fusion (1.5 min) — artifact #2

1. Open fusion NiceGUI; show profile → join → orphan anomalies (`C999`).
2. Export fused dataset + Mermaid lineage.

**Line:** “FDE data integration: upload, match, explain lineage, export clean data.”

## 3. Financial Crime Console (1.5 min) — artifact #3

1. `streamlit run financial-crime-ops-console/fin_crime/apps/streamlit_app.py`
2. Case queue: highlight TX-1007 CRITICAL.
3. Audit action → export evidence / SAR **draft** (stress training-only).

**Line:** “Regulated workflow signal with audit trail and synthetic-only data.”

## 4. Red-Team Harness (1.5 min) — artifact #4

1. Streamlit red-team app; show 4 categories, mixed pass/fail.
2. Export report; mention `evals/security_scorecard.md`.

**Line:** “Security credibility without pretending the 8-case suite is production coverage.”

## 5. Single-file brief (1 min) — artifact #5

1. Open `single-file-command-briefs/index.html` offline-ish.
2. KPIs + chart + assumptions.

**Line:** “Zero-install packaging for restricted environments.”

## Close (30 s)

- Run `./scripts/verify.sh` live if time.
- Point at `GAP_ANALYSIS.md` for honesty on remaining polish.
