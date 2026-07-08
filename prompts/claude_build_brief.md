# Claude Code Build Brief

Use this prompt in Claude Code (`claude` in repo root) or paste into a Claude Desktop Project with repo context.

```text
You are Claude Code assisting modification of this Forward-Deployed AI Systems Workbench repository.

Mission: [One-sentence objective]

Operational context: [Who uses this, under what constraints, what decision/workflow it supports]

Read first:
- CLAUDE.md
- AGENTS.md
- specs/product_brief.md
- specs/data_contract.md
- specs/acceptance_criteria.md
- specs/operator_workflow.md
- skills/triage-skill/SKILL.md
- src/core/ingestion.py
- src/apps/streamlit_app.py
- tests/

Constraints (from CLAUDE.md):
- Local-first; no required cloud database
- Scoring/ingestion in src/core; UI in src/apps
- Preserve offline fallback when OPENAI_API_KEY is unset
- Do not remove tests; add focused tests for changed behavior
- Never hardcode secrets

Implementation requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Verification (run before claiming done):
./scripts/verify.sh

Acceptance criteria:
- streamlit run src/apps/streamlit_app.py works locally
- All specs acceptance checks relevant to this change pass
- Governance sidebar reflects live data source and refresh time
- git diff is clean and reviewable

Do not:
- Introduce required cloud dependencies
- Bypass schema validation in ingestion
- Move scoring logic into Streamlit callbacks

Deliver:
- Changed files summary
- ./scripts/verify.sh output
- git diff summary
- Known gaps and follow-up risks
- Suggested next build path from GAP_ANALYSIS.md
```