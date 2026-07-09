# Eval Harness Design Prompt

Use when extending the LLM Red-Team Eval Harness or designing golden-output evals for any portfolio artifact.

```text
Design or extend a local-first eval harness for [artifact].

Constraints:
- Offline-first; live model calls optional and gated.
- Severity-weighted scoring with explicit SHIP / REPAIR / REJECT bands.
- Fixture cases in JSON with category, severity, pass_criteria, fixture_response.
- Export JSON + markdown reports with governance (data source, model usage, test status).
- Add pytest coverage for suite load, scoring aggregation, and export paths.
- Document limitations — never claim production red-team completeness from starter suites.

Deliverables:
1. Case list (category × severity matrix)
2. Heuristic or golden-output pass rules
3. Summary metrics and band thresholds
4. Operator UI fields (if any)
5. Verification commands
```
