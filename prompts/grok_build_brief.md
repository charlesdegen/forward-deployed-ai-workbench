# Grok Build Task Brief

Use this prompt in Grok Build (`grok -m grok-build --cwd <repo>`) or attach via `@prompts/grok_build_brief.md`.

```text
You are Grok assisting modification of this Forward-Deployed AI Systems Workbench repository.

Mission: [One-sentence objective]

Operational context: [Who uses this, under what constraints, what decision/workflow it supports]

Files to inspect first:
- AGENTS.md
- specs/product_brief.md
- specs/data_contract.md
- specs/acceptance_criteria.md
- specs/operator_workflow.md
- skills/triage-skill/SKILL.md
- src/core/ingestion.py
- src/apps/streamlit_app.py
- tests/

Grok Build invocation:
- Attach context: @specs/ @src/core/ @src/apps/ @tests/ @fixtures/
- Run verification: ./scripts/verify.sh
- After edits: /check-work [focus area]
- Before handoff: /review --local

Implementation requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Acceptance criteria:
- App runs: streamlit run src/apps/streamlit_app.py
- ./scripts/verify.sh passes
- Core logic in src/core; UI in src/apps
- Fixtures and tests updated for new data paths
- Governance fields populated (data source, last refresh, test status)
- Known limitations documented

Do not:
- Introduce required cloud dependencies
- Hardcode secrets
- Remove existing tests
- Add large frameworks unless justified in specs

Deliver:
- Changed files summary
- Commands run (including ./scripts/verify.sh output)
- Test results
- git diff summary
- Known gaps
- Suggested next leverage point
```