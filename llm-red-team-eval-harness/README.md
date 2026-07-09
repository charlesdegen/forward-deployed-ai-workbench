# LLM Red-Team Eval Harness

Portfolio artifact #4 for the Forward-Deployed AI Systems Workbench.

**Python + pytest + Streamlit** — prompt injection, jailbreak, tool-boundary, and hallucination checks with severity-weighted reports.

## Run

```bash
source ../.venv/bin/activate
streamlit run redteam/apps/streamlit_app.py
```

## Verify

```bash
pytest tests -q
```

## Layout

```
llm-red-team-eval-harness/
  fixtures/redteam_suite.json
  redteam/core/   # suite, runner, scoring, exports
  redteam/apps/streamlit_app.py
  tests/
  artifacts/exports/
```

## Notes

- Default path uses **fixture responses** and offline pattern checks.
- Live model evaluation is intentionally not wired (governance: offline first).
- Umbrella scorecard: `../evals/security_scorecard.md`
- Domain skill: `../skills/redteam-skill/SKILL.md`
