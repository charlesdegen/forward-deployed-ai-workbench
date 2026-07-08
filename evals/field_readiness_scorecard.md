# Field Readiness Scorecard

**Artifact:** Mission Autonomy Field Support Console (starter)  
**Evaluator:** _______________  
**Date:** _______________  
**Deployment target:** _______________

## Scoring (0 = fail, 1 = partial, 2 = pass)

| Criterion | 0 | 1 | 2 | Score | Notes |
|---|---|---|---|---|---|
| Works offline (no API required for core triage) | | | | | |
| Degraded-mode / brittle connectivity assumptions documented | | | | | |
| Operator can complete triage workflow in < 5 min (fixture) | | | | | |
| Governance fields visible without opening code | | | | | |
| RCA packet exportable for engineering handoff | | | | | |
| Operator action log persists locally | | | | | |
| CSV upload + fixture + mock sources available | | | | | |
| Demo script reproducible by non-author | | | | | |

**Total / 16:** _______

## Thresholds

- **Field demo ready:** ≥ 14
- **Bench-only:** 10–13
- **Not deployable:** < 10

## Field demo script (3 min)

1. Launch `streamlit run src/apps/streamlit_app.py`
2. Confirm fixture source; show governance metadata
3. Review alerts queue; explain index-30 anomaly
4. Append one operator action
5. Export RCA packet → `artifacts/exports/`
6. Run `./scripts/verify.sh`

## Operator sign-off

| Role | Name | Accept / Reject | Date |
|---|---|---|---|
| Field operator | | | |
| FDE engineer | | | |