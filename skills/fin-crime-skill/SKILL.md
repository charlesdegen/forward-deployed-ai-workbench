# Financial Crime Triage Skill

Use when triaging synthetic AML / transaction-monitoring cases in the Financial Crime Operations Console.

## Priorities

1. **Customer harm / sanctions exposure** — high-risk jurisdiction flags first.
2. **Materiality** — amount bands and structuring near thresholds.
3. **History** — prior SAR counts on the subject account.
4. **Channel risk** — crypto on-ramp, wire, cash deposit over ACH/card.
5. **Documentation** — evidence packet completeness before close.

## Guardrails

- Never treat fixture data as real persons.
- SAR narrative is a **draft for training** — do not claim regulatory filing.
- Keep scoring deterministic and offline unless human approves live tools.
- Log every operator action to the audit trail.

## Adapter notes

- **Codex / Grok / Claude**: keep logic in `fin_crime/core/`, UI in `fin_crime/apps/`, tests green via `pytest financial-crime-ops-console/tests`.
