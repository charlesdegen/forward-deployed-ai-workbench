# Design System Prompt (portfolio consistency)

Use when building or restyling any operator surface so five artifacts read as one product line.

```text
Apply a shared FDE command-console design system:

Visual:
- Dark background (#0b0f14 / #0f1115), elevated cards (#121820 / #171a21)
- Borders #232733 / #243041; text primary #e6edf3; muted #8b949e
- Danger / critical #ff7b72 or #ff8b8b; OK / nominal green muted
- Dense tables, uppercase micro-labels for governance fields

UX:
- Governance panel always visible: data source, last refresh, model usage, test status, assumptions
- Separate advisory AI text from operator actions
- Offline fallback checklist when no API key
- Primary actions: triage → log → export

Surfaces in this repo:
- Mission Console (NiceGUI), Streamlit starter
- Data Fusion NiceGUI
- Fin Crime Streamlit
- Red-Team Streamlit
- Single-file HTML brief

Do not invent a separate brand per artifact. Prefer reuse of spacing, type hierarchy, and governance strip patterns.
```
