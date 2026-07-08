# Codex Repair Brief

Use this prompt when ChatGPT, tests, or operator review found a concrete gap.

```text
Goal:
Repair [specific bug/gap] in the Forward-Deployed AI Systems Workbench.

Inspect first:
- README.md
- specs/product_brief.md
- skills/triage-skill/SKILL.md
- src/core/
- src/apps/
- tests/

Constraints:
- Keep the workbench local-first.
- Do not hardcode secrets.
- Keep telemetry scoring and schema logic in src/core.
- Keep operator UI changes in src/apps.
- Preserve prompt export behavior when no API key is configured.
- Add or update focused tests for changed scoring, parsing, logging, or export behavior.

Verification:
- Run python -m pytest when dependencies are installed.
- Run python -m py_compile src/apps/streamlit_app.py src/core/ingestion.py.
- Summarize changed files, commands run, test results, and remaining risks.
```
