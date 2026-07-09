# LLM Red-Team Eval Harness — Product Brief

**Portfolio artifact #4** — AI security credibility for FDE roles.

## Problem

Teams need a local, repeatable way to score model (or fixture) responses against injection, jailbreak, tool-boundary, and hallucination cases without depending on a cloud eval vendor for the first loop.

## Operator workflow

1. Load suite fixture (`redteam_suite.json`).
2. Run offline heuristic evaluation (fixture responses by default).
3. Review pass/fail by category and severity.
4. Export JSON + markdown report with governance metadata.
5. Optionally wire live model responses later (out of starter scope).

## Constraints

- Offline default — no API key required.
- Severity-weighted security score + SHIP / REPAIR / REJECT band.
- Link to umbrella `evals/security_scorecard.md`.

## Acceptance

- 8 fixture cases across 4 categories.
- Balanced pass/fail for demo honesty.
- pytest covers suite load, scoring, export.
