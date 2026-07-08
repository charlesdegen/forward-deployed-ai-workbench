# Forward-Deployed AI Systems Workbench (ClaudeBuild)

A local-first, Claude-accelerated toolchain for converting ambiguous operational requirements into tested applications, data workflows, operator dashboards, offline artifacts, and high-trust decision systems.

---

## Forward-Deployed AI Systems Manifesto (ClaudeBuild Doctrine)

I build software at the edge of ambiguity.

The objective is not to produce demos, dashboards, or AI wrappers. The objective is to compress the distance between operational pain and deployed capability.

A forward-deployed AI system begins with a real user, a messy environment, constrained data, brittle processes, unclear ownership, and a mission that cannot wait for a perfect platform roadmap. The work is to enter that environment, identify the binding constraint, delete unnecessary complexity, build the missing tool, instrument the workflow, harden the failure modes, and return evidence to engineering.

The operating philosophy is local-first, high-trust, and field-deployable. Tools must work under imperfect connectivity, constrained security boundaries, limited installation rights, incomplete data, and compressed timelines. A useful system is one that runs, explains itself, fails safely, exports cleanly, and survives contact with real operators.

The stack is intentionally pragmatic. Use Python when the logic is heavy. Use Streamlit when speed matters. Use NiceGUI when operator experience matters. Use single-file HTML when portability matters. Use React/PWA when the prototype needs to behave like a product. Use DuckDB, Polars, Pandas, and JSON contracts to separate computation from presentation. Use tests, fixtures, golden outputs, and evals to prevent LLM-generated software from becoming ungoverned theater.

**Claude is the acceleration layer, not the product.** Claude performs first-principles decomposition, turns ambiguity into architecture, requirements, evals, and implementation briefs. Claude Code scaffolds code, modifies repositories directly, generates and runs tests, analyzes execution feedback, and repairs defects in an agentic loop. The human owns the mission, constraints, judgment, final acceptance, and operational narrative. The Claude Max tier provides the model access (Opus-class reasoning for decomposition, Sonnet-class speed for build loops), extended context, and agentic tool use with sandboxed validation for production-grade artifacts.

Every artifact should leave behind reusable leverage: a cleaner spec, a stronger prompt, a tested component, a better data contract, a sharper eval, a more portable template, a reusable Skill, or a repeatable deployment path.

The standard is not "it looks impressive." The standard is:

- It runs locally.
- It solves a real workflow.
- It exposes assumptions.
- It separates logic from interface.
- It handles bad inputs.
- It can be tested.
- It can be explained.
- It can be handed to an operator.
- It can be improved by engineering.
- It creates a shorter OODA loop.

Forward-deployed AI engineering is not vibe coding. It is mission compression through software.

---

## The Claude Surface Map (which tool, which job)

Claude is not one interface. It is five surfaces with distinct roles in the FDE loop. Route work deliberately.

| Surface | Role in the loop | Use it for | Avoid using it for |
|---|---|---|---|
| **Claude Desktop** | Strategy & decomposition HQ | First-principles reframing, architecture debate, spec drafting, threat modeling, Mermaid generation, MCP-connected context pulls (Figma, GitHub, calendars, data warehouses), long-running Projects that hold mission memory | Repo surgery — hand that to Code |
| **Claude Code** | Repo-native implementation engine | Agentic builds inside the actual repo: scaffolding, multi-file refactors, test generation and execution, lint/typecheck loops, git operations, headless CI runs (`claude -p`), subagents for parallel workstreams, hooks for governance enforcement | Whiteboard-stage ambiguity — decompose first, then hand Code a tight brief |
| **Cowork** | Operational file & artifact automation | Non-code operator workflows: fixture generation, data profiling on real folders, xlsx/docx/pdf close-out packets, screenshot/export packaging, scheduled recurring briefs, plugin/Skill-driven ops tasks in a sandboxed shell against the actual filesystem | Deep multi-file engineering — Code owns the repo |
| **Claude Design** | Operator-grade UI surface generation | Dashboard and console mockups before committing code, extracting a design system from the existing repo or Figma to keep artifacts visually consistent, generating single-file HTML executive briefs, exporting to HTML/PDF/PPTX for zero-install delivery into restricted environments | Business logic — Design produces the surface; logic lives in `/src/core` behind a JSON contract |
| **Claude Mobile** | Field capture & edge review | On-site intake: photograph the whiteboard, the error screen, the paper process; voice-capture operator pain into a Project; review artifacts and answer operator questions away from the workstation; triage while forward-deployed | Anything requiring the repo or the sandbox |

The handoff pattern: **Mobile captures → Desktop decomposes → Design mocks the surface → Code builds and tests → Cowork packages and schedules → Mobile verifies with the operator.** Shared context flows through Projects, CLAUDE.md, and Skills so no surface starts cold.

---

## External positioning (resume / portfolio / intro)

Built a local-first Forward-Deployed AI Systems Workbench (ClaudeBuild) that converts ambiguous operational requirements into tested Streamlit, NiceGUI, React, and single-file HTML tools. Leveraged Claude across five surfaces — Desktop for requirements decomposition and architecture, Claude Code for repo-native agentic implementation and test generation, Claude Design for operator-grade interfaces and offline executive artifacts, Cowork for data workflow automation and artifact packaging, and Mobile for field capture — with implementation briefs, Mermaid architectures, DuckDB/Polars data pipelines, eval harnesses, golden-output tests, operator dashboards, and governance scorecards for constrained enterprise environments.

For Anduril / defense tech FDE roles:
I build field-deployable AI-assisted tools for constrained operating environments with Claude providing real-time reasoning compression: local-first data ingestion, operator dashboards, triage workflows, eval harnesses, failure-mode instrumentation, RCA packets, and fast feedback loops from user pain to engineering action.

---

## Recommended toolchain (layers, not tools)

| Layer | Purpose | Recommended tools | Why |
|---|---|---|---|
| 0. AI Acceleration (ClaudeBuild core) | Convert ambiguity into buildable requirements, code, tests, and narrative at machine speed | Claude Max (Opus/Fable for decomposition, Sonnet for build loops) + Claude Code agentic execution | First-principles reframing, spec generation, code review, adversarial testing, Mermaid, READMEs, portfolio story. Complements every downstream layer. |
| 1. Strategy / architecture | Convert ambiguity into buildable requirements | Claude Desktop (Projects) + Mermaid + Markdown specs | Turns vague business/mission problems into executable design; Projects hold mission memory across sessions |
| 2. Repo-native implementation | Build, modify, test code | Claude Code + Git / VS Code or terminal | Claude Code edits the repo directly, runs tests, and repairs defects in-loop; hooks and permissions enforce governance |
| 3. Python runtime | Local analytical tools | Python 3.11/3.12, venv, uv optional | Controlled local execution |
| 4. Data backbone | Fast local analytics | Pandas, NumPy, DuckDB, Polars, PyArrow, OpenPyXL | Handles CSV/XLSX/Parquet/JSON with minimal infra |
| 5. UI surfaces | Build interactive artifacts | Streamlit, NiceGUI, React/Vite, single-file HTML; Claude Design for mockups and design-system consistency | Different surfaces for speed, polish, product feel, portability |
| 6. Visualization | Dense decision surfaces | Plotly, ECharts, PyDeck, Leaflet, AG Grid/Tabulator | Operator-grade charts, maps, and tables |
| 7. Docs / diagrams | Explain systems | Mermaid (Claude-generated), Markdown, MkDocs optional | Architecture, process, sequence, data lineage |
| 8. Testing / evals | Prevent broken demos | pytest, ruff, black, mypy optional, JSON Schema, golden files; Claude Code runs the loop | Converts LLM output into verifiable software |
| 9. Security / governance | High-trust posture | Bandit, pip-audit, Semgrep optional, threat model templates, audit logs; Claude Code hooks for policy enforcement | Shows deployment risk understanding |
| 10. Packaging | Share artifacts | Zip exports, single-file HTML (Claude Design export), PWA, local app runner, screenshots; Cowork for docx/pptx/pdf close-out packets | Makes demos portable |
| 11. Portfolio layer | Prove capability | GitHub repos, README (Claude-drafted), screenshots, 3-minute Looms, demo scripts | Converts tooling into interview signal |

Claude Code's agent loop enables a distributed build cycle: high-level intent is decomposed in Desktop; Claude Code generates patches and tests and validates them against the real repo; Cowork packages outputs; human signs off. Subagents parallelize independent workstreams (e.g., one agent on ingestion tests while another builds the export layer).

---

## Installation baseline (first stable stack)

```bash
# repo
git init
python -m venv .venv
source .venv/bin/activate

# Claude Code (repo-native agent)
npm install -g @anthropic-ai/claude-code
claude   # then /init to generate CLAUDE.md

# core quality
pip install pytest ruff black

# core analytics
pip install pandas numpy openpyxl pyarrow duckdb polars

# visualization
pip install plotly altair pydeck

# fast app surface
pip install streamlit streamlit-extras

# premium Python app surface
pip install nicegui

# optional API layer
pip install fastapi uvicorn pydantic

# security checks
pip install bandit pip-audit
```

For React/PWA prototypes: standard Vite + Tailwind + lucide-react + recharts.
For single-file artifacts, maintain the no-build template under `single_file_html/` — Claude Design can generate and export these directly.

---

## Recommended repo structure

```
forward-deployed-ai-workbench/
  README.md
  CLAUDE.md                      # repo-level context Claude Code loads every session
  pyproject.toml
  requirements.txt
  /.claude
    /skills                      # reusable Skills: triage, eval design, RCA packets
    /agents                      # subagent definitions (test-writer, security-reviewer)
    /hooks                       # governance enforcement (block secrets, require tests)
  /specs
    product_brief.md
    operator_workflow.md
    data_contract.md
    acceptance_criteria.md
    threat_model.md
  /prompts
    claude_architect_prompt.md
    claude_build_brief.md
    claude_repair_brief.md
    eval_prompt.md
    design_system_prompt.md
  /src
    /core
      ingestion.py
      transforms.py
      scoring.py
      exports.py
    /apps
      streamlit_app.py
      nicegui_app.py
    /schemas
      input_schema.json
      output_schema.json
  /artifacts
    /html
    /mermaid
    /screenshots
    /exports
  /fixtures
    sample_events.csv
    sample_transactions.xlsx
    sample_incidents.json
    sample_logs.txt
  /tests
    test_ingestion.py
    test_transforms.py
    test_scoring.py
    golden_outputs/
  /evals
    artifact_quality_scorecard.md
    security_scorecard.md
    field_readiness_scorecard.md
  /docs
    architecture.md
    deployment.md
    demo_script.md
```

CLAUDE.md and `/.claude` are the leverage multipliers: every convention, constraint, and governance rule written there is enforced on every future Claude Code session for free. Skills written once (e.g., "generate RCA packet") run identically in Claude Code and Cowork.

---

## The build portfolio (five finished artifacts beat fifty fragments)

1. **Mission Autonomy Field Support Console** (NiceGUI + DuckDB + simulated telemetry) — Anduril FDE / technical operations signal. Shows operator-grade field diagnosis, degraded-mode handling, RCA generation, and engineering feedback packets.
2. **Financial Crime Operations Console** (Streamlit + DuckDB + case workflow) — Palantir / banking domain edge signal. Shows regulated workflow triage, risk scoring, evidence packets, SAR narrative drafts, and audit trails.
3. **Local Data Fusion Workbench** (Polars/DuckDB + entity matching + UI) — FDE data integration skill. Shows upload/profile/join/anomaly detection/export with Mermaid lineage and clean dataset output.
4. **LLM Red-Team Eval Harness** (Python + pytest + Streamlit/NiceGUI) — AI security credibility. Shows prompt injection, jailbreak, tool-call boundary, hallucination checks, golden outputs, severity ratings, and exportable reports. Doubly credible when built with Claude: the harness evaluates the same class of system that built it.
5. **Single-File Executive Command Brief** (HTML + Tailwind + ECharts/Tabulator) — Zero-install artifact delivery. Claude Design generates the surface against the extracted design system and exports standalone HTML. Proves portability into restricted environments.

Each artifact: Desktop decomposes and specs; Claude Design mocks the operator surface; Claude Code scaffolds, tests, and repairs; Cowork packages fixtures, screenshots, and exports; human owns data control, UX judgment, and final integration. Core message across all: **I use Claude inside a disciplined engineering loop to produce working software, not prompts.**

---

## Operating loop (explicit FDE loop)

1. Observe the operational constraint (Mobile: capture on-site — photos, voice, notes into the Project).
2. Identify the binding bottleneck (Desktop: first-principles assist).
3. Convert problem into spec (Desktop: architect prompt → `/specs`).
4. Generate data contract (Desktop/Code: JSON Schema in `/src/schemas`).
5. Build local prototype (Claude Code scaffolds against the repo).
6. Test with fixtures (Claude Code generates and runs pytest; repairs failures in-loop).
7. Add operator workflow (Claude Design mocks the surface; Code implements it).
8. Add eval / audit trail (Desktop designs evals; Code implements; hooks enforce).
9. Package artifact (Cowork: exports, screenshots, close-out packet; Design: offline HTML brief).
10. Feed findings back to engineering (Desktop drafts RCA packet; Mobile delivers and verifies with the operator).

---

## Claude role

Requirement decomposition & reframing, architecture & diagrams, threat modeling, UX critique, eval design, task brief generation, README/demo script/portfolio narrative, code scaffolding, repo modification, test generation and execution, diff analysis, in-loop defect repair, artifact packaging, and design-system-consistent interface generation.

## Human role

Choose mission, define acceptance criteria, control data exposure, judge UX usefulness, decide when to ship, own the operational narrative, review diffs before merge, grant and scope tool permissions, sign off on every artifact that reaches an operator.

---

## Standard Claude Task Brief (use every time)

Drop this into Claude Code (or a Desktop Project) verbatim. Repo-level constants live in CLAUDE.md so the brief stays short.

```
You are Claude Code modifying this Forward-Deployed AI Systems Workbench repository.

Mission: [One-sentence objective]
Operational context: [Who uses this, under what constraints, what decision/workflow it supports]

Files to inspect first:
- CLAUDE.md
- README.md
- specs/product_brief.md
- src/
- tests/

Implementation requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Acceptance criteria:
- App runs locally with documented command
- Tests pass (run them; show output)
- No unnecessary dependencies
- Core logic separated from UI
- Sample fixtures included
- README updated with Claude-generated sections clearly marked
- Known limitations documented
- Governance fields populated (data source, assumptions, model usage, test status)

Do not:
- Introduce cloud dependencies
- Hardcode secrets
- Remove existing tests
- Add large frameworks unless justified

Deliver:
- Changed files summary
- Commands run and their output
- Test results
- Known gaps
- Suggested next leverage point
```

Encode the "Do not" list as Claude Code hooks where possible (e.g., a pre-commit hook that blocks secrets and dependency additions without justification) — enforced governance beats requested governance.

---

## Design doctrine

External terms: operator-grade interface, field-deployable tooling, local-first workflow system, high-trust decision surface, constrained-environment deployment, audit-ready AI workflow, offline-capable artifact, human-in-the-loop triage console.

Visual standard: dense, not cluttered; dark mode default; status colors used sparingly; no toy gradients or excessive rounded cards; charts must answer operational questions; every metric needs owner, timestamp, and source. Claude-generated diagrams stay clean and information-dense.

Claude Design enforcement: extract the design system once (from the repo's existing CSS/tokens or a reference Figma file), store it as the project design system, and generate every dashboard, console, and executive brief against it. This makes five separate artifacts read as one product line — a portfolio signal in itself.

---

## Governance layer (every artifact exposes)

Data source, last refresh time, assumptions, input/output schema, Claude/model usage disclosure, known limitations, test status, export version, user/operator action log. This separates "cool AI app" from "high-trust operational tool."

Claude-specific additions: which surface produced each component (Code vs Design vs Cowork), the CLAUDE.md version in effect at build time, and hook-enforced policy checks passed. Anthropic's positioning on safety and auditability is itself part of the high-trust narrative for defense and regulated-finance audiences — use it.

---

## Build sequence (30-day plan, compressible with Claude Code)

**Week 1:** Desktop generates full repo template, task brief, Streamlit starter, single-file HTML starter, Mermaid generator. Claude Code `/init` produces CLAUDE.md; validate base installs and basic app runs in-loop. Write first Skills (RCA packet, eval scorecard).
**Week 2:** Build Local Data Fusion Workbench (Claude Code scaffolds core + tests + exports). Add pytest fixtures, README, demo script. Cowork generates fixture datasets and packages exports.
**Week 3:** Build Mission Autonomy Field Support Console and Financial Crime Operations Console. Claude Design mocks both consoles against the shared design system before implementation. Add screenshots/walkthroughs.
**Week 4:** Build LLM Red-Team Eval Harness. Claude Design generates portfolio landing page; refactor shared components; polish GitHub narrative (Claude drafts final READMEs and positioning; human owns final voice).

With Claude Code subagents running parallel validation and Cowork handling packaging, target compression to 10–14 days for the initial five artifacts.

---

## Redline metrics (operating telemetry)

| Metric | Target |
|---|---|
| Idea to spec | <10 minutes |
| Spec to working prototype | <45 minutes |
| Prototype to polished artifact | <2 hours |
| Repair loops | <3 |
| Manual code written by human | <20% |
| Test pass rate before demo | 100% |
| Reusable component or Skill created per build | ≥1 |
| Offline artifact export | yes |
| README quality (Claude-drafted, human-owned) | pass |
| Demo length | <4 minutes |

---

## What this says to Anduril / Palantir / defense tech

I can take ambiguous operational problems, build local-first tools quickly, handle constrained environments, instrument failure modes, create operator-grade interfaces, and convert field feedback into engineering-ready artifacts — using Claude as the disciplined acceleration layer inside a first-principles engineering loop (requirements → data contract → implementation → testing → eval → packaging → feedback). The output is working software with governance, not a prompt.

Weak alternative narrative to avoid: "I am good at prompting LLMs to make cool dashboards."

---

## Final recommendation

Build this as a named portfolio system with five focused repos under one umbrella:

```
forward-deployed-ai-workbench/
  mission-support-console/
  financial-crime-ops-console/
  local-data-fusion-workbench/
  llm-red-team-eval-harness/
  single-file-command-briefs/
```

Each repo contains: README (Claude-drafted), CLAUDE.md, problem statement, architecture diagram, screenshots, install/run instructions, sample data, tests, demo script, limitations, next build path. Shared Skills and hooks live at the umbrella level and propagate down.

This proves the full loop — operator empathy, system design, data handling, code execution, UX judgment, testing, governance, and deployment pragmatism — at the exact signal strength required for FDE AI engineer roles.
