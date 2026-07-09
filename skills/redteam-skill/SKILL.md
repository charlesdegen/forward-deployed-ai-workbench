# LLM Red-Team Eval Skill

Use when designing, extending, or interpreting red-team suites in this workbench.

## Categories

1. **prompt_injection** — instruction override, system-prompt extraction
2. **jailbreak** — persona / DAN / harmful actionable content
3. **tool_boundary** — destructive shell, SQL, exfil via tools
4. **hallucination** — fabricated citations and unverifiable claims

## Scoring discipline

- Prefer severity-weighted fail cost over raw pass rate alone.
- Document model usage: fixture vs live.
- Never claim production coverage from the starter 8-case suite.

## Adapter notes

Keep heuristics in `redteam/core/`; UI in `redteam/apps/`. Add cases via JSON fixture + tests.
