**Forward-Deployed AI Systems Workbench (GrokBuild)**

A local-first, Grok-accelerated toolchain for converting ambiguous operational requirements into tested applications, data workflows, operator dashboards, offline artifacts, and high-trust decision systems.

**Grok Build (the platform)** is xAI's terminal-native AI coding agent: a full-screen TUI and headless CLI that reads your repository, executes shell commands, edits files with line-precise diffs, searches the web, spawns parallel subagents, and validates changes through sandboxed execution. The default build model is `grok-build` (display name: **Grok Build**). Sessions persist automatically under `~/.grok/sessions/` and can be resumed with `/resume`, `grok -c`, or `grok --resume <id>`. File context is attached with `@` references (e.g., `@src/core/ingestion.py:10-50`, `@specs/`). GrokBuild is the *doctrine and repo template*; Grok Build is the *agent runtime* that executes it.

**Forward-Deployed AI Systems Manifesto (GrokBuild Doctrine)**

I build software at the edge of ambiguity.

The objective is not to produce demos, dashboards, or AI wrappers. The objective is to compress the distance between operational pain and deployed capability.

A forward-deployed AI system begins with a real user, a messy environment, constrained data, brittle processes, unclear ownership, and a mission that cannot wait for a perfect platform roadmap. The work is to enter that environment, identify the binding constraint, delete unnecessary complexity, build the missing tool, instrument the workflow, harden the failure modes, and return evidence to engineering.

The operating philosophy is local-first, high-trust, and field-deployable. Tools must work under imperfect connectivity, constrained security boundaries, limited installation rights, incomplete data, and compressed timelines. A useful system is one that runs, explains itself, fails safely, exports cleanly, and survives contact with real operators.

The stack is intentionally pragmatic. Use Python when the logic is heavy. Use Streamlit when speed matters. Use NiceGUI when operator experience matters. Use single-file HTML when portability matters. Use React/PWA when the prototype needs to behave like a product. Use DuckDB, Polars, Pandas, and JSON contracts to separate computation from presentation. Use tests, fixtures, golden outputs, and evals to prevent LLM-generated software from becoming ungoverned theater.

**Grok is the acceleration layer, not the product.** Grok performs first-principles decomposition, turns ambiguity into architecture, requirements, evals, and implementation briefs. Grok scaffolds code, proposes repository modifications, generates tests, runs analysis via execution feedback, and repairs defects. The human owns the mission, constraints, judgment, final acceptance, and operational narrative. SuperGrok tier provides extended context, persistent tool calling, and sandbox-backed validation for production-grade artifacts.

**Grok Build is how that acceleration layer executes.** It is not a chat wrapper — it is a repo-native agent with built-in tools (`read_file`, `grep`, `search_replace`, `run_terminal_command`, `web_search`, `web_fetch`, `todo_write`, `spawn_subagent`, `memory_search`) plus optional MCP server extensions (GitHub, databases, internal APIs). Grok Build runs in the operator's actual environment: real filesystem, real `pytest`, real Streamlit/NiceGUI processes, real git history. Permission prompts (`Ctrl+O` always-approve toggle, `/always-approve`, `--yolo` for headless) keep the human in the loop for destructive or sensitive operations. Plan mode (`/plan`, `Shift+Tab`) separates architecture from implementation so Grok explores and writes `plan.md` before touching production code paths.

Every artifact should leave behind reusable leverage: a cleaner spec, a stronger prompt, a tested component, a better data contract, a sharper eval, a more portable template, or a repeatable deployment path.

The standard is not “it looks impressive.” The standard is:
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

**External positioning (resume / portfolio / intro)**

Built a local-first Forward-Deployed AI Systems Workbench (GrokBuild) that converts ambiguous operational requirements into tested Streamlit, NiceGUI, React, and single-file HTML tools. Leveraged Grok for requirements decomposition, architecture, code scaffolding, eval design, test generation, and portfolio narrative. The system includes Grok-generated implementation briefs, Mermaid architectures, DuckDB/Polars data pipelines, eval harnesses, golden-output tests, operator dashboards, offline executive artifacts, and governance scorecards for constrained enterprise environments.

Operated the full loop inside **Grok Build** (xAI's terminal agent): `@`-scoped file context, persistent sessions, subagent delegation for parallel research/implementation/review, sandbox profiles for constrained validation, and headless `grok -p` for scripted verification in CI.

For Anduril / defense tech FDE roles:  
I build field-deployable AI-assisted tools for constrained operating environments with Grok providing real-time reasoning compression: local-first data ingestion, operator dashboards, triage workflows, eval harnesses, failure-mode instrumentation, RCA packets, and fast feedback loops from user pain to engineering action.

**Recommended toolchain (layers, not tools)**

Layer | Purpose | Recommended tools | Why
---|---|---|---
0. AI Acceleration (GrokBuild core) | Convert ambiguity into buildable requirements, code, tests, and narrative at machine speed | Grok Build (`grok-build` model) + SuperGrok tier + sandbox execution for validation | First-principles reframing, spec generation, code review, adversarial testing, Mermaid, READMEs, portfolio story. Complements every downstream layer.
0a. Grok Build runtime | Repo-native agent execution environment | Grok Build TUI (`grok`) or headless (`grok -p`), sessions, `@` file refs, built-in tools | Real shell, real diffs, real test runs — not simulated codegen. Install: `curl -fsSL https://x.ai/cli/install.sh | bash`. Auth via grok.com browser login or `XAI_API_KEY` for CI/headless.
0b. Grok orchestration skills | Multi-step loops with subagent isolation | `/design`, `/execute-plan`, `/review`, `/check-work`, `/create-skill` | Bundled skills run writer→reviewer loops, DAG-based PR stacks in isolated worktrees, and mandatory verification before ship. Maps directly to FDE spec→build→test→feedback cycles.
0c. Grok project memory | Cross-session leverage without re-explaining constraints | `AGENTS.md`, `.grok/rules/*.md`, repo `skills/*/SKILL.md`, optional `--experimental-memory` | Doctrine, conventions, and operator context persist across sessions. Skills auto-invoke when task descriptions match; slash commands force invocation.
0d. Grok sandbox & permissions | High-trust execution in constrained environments | `--sandbox workspace|read-only|strict`, `.grok/sandbox.toml` custom profiles with `deny` globs for secrets | Kernel-enforced FS boundaries (Seatbelt/Landlock). Use `read-only` for adversarial code review; `strict` for untrusted inputs. Deny `**/.env`, `**/*.pem` at profile level.
1. Strategy / architecture | Convert ambiguity into buildable requirements | Grok + `/design` skill + `/plan` mode + Mermaid + Markdown specs | Turns vague business/mission problems into executable design with reviewer consensus and PR-plan DAG output
2. Repo-native implementation | Build, modify, test code | Grok Build code gen + `grok --worktree=<name>` for isolated branches + local Git / VS Code / Cursor ACP | Grok proposes patches; subagents implement in worktree isolation; human or sandbox applies and validates. `grok --cwd <path>` pins workspace context.
3. Python runtime | Local analytical tools | Python 3.11/3.12, venv, uv optional | Controlled local execution
4. Data backbone | Fast local analytics | Pandas, NumPy, DuckDB, Polars, PyArrow, OpenPyXL | Handles CSV/XLSX/Parquet/JSON with minimal infra
5. UI surfaces | Build interactive artifacts | Streamlit, NiceGUI, React/Vite, single-file HTML | Different surfaces for speed, polish, product feel, portability
6. Visualization | Dense decision surfaces | Plotly, ECharts, PyDeck, Leaflet, AG Grid/Tabulator | Operator-grade charts, maps, and tables
7. Docs / diagrams | Explain systems | Mermaid (Grok-generated), Markdown, MkDocs optional | Architecture, process, sequence, data lineage
8. Testing / evals | Prevent broken demos | pytest, ruff, black, mypy optional, JSON Schema, golden files, `/check-work` | Converts LLM output into verifiable software; verifier subagent runs builds/tests against diffs
9. Security / governance | High-trust posture | Bandit, pip-audit, Semgrep optional, threat model templates, audit logs, sandbox deny lists | Shows deployment risk understanding; Grok sandbox blocks credential file reads at kernel level
10. Packaging | Share artifacts | Zip exports, single-file HTML, PWA, local app runner, screenshots | Makes demos portable
11. Portfolio layer | Prove capability | GitHub repos, README (Grok-written), screenshots, 3-minute Looms, demo scripts | Converts tooling into interview signal
12. Automation / CI | Scripted validation without TUI | `grok -p "..." --sandbox workspace --yolo`, `--output-format json`, `--max-turns N`, `--disallowed-tools` | Headless runs for golden-output regression, README lint, or nightly eval harness execution

Grok’s tool-calling and sandbox execution enable a distributed build loop: high-level intent is decomposed in conversation; patches and tests are generated; validation runs reproducibly in sandbox or local environment before human sign-off.

**Grok Build platform primitives (FDE mapping)**

| Primitive | Grok Build capability | FDE use |
|---|---|---|
| Sessions | Auto-saved to `~/.grok/sessions/`; `/resume`, `/fork`, `/rewind`, `/compact` | Long missions survive interruption; fork experiments without losing field context |
| Subagents | `spawn_subagent` with types `general-purpose`, `explore`, `plan`; independent context windows | Parallelize research (explore), planning (plan), and implementation without context exhaustion |
| Plan mode | `/plan`, `enter_plan_mode` → `plan.md` → `exit_plan_mode` approval | Architecture review before code when auth/pipeline/deployment approach is genuinely ambiguous |
| Skills | `SKILL.md` in `skills/`, `.grok/skills/`, or `~/.grok/skills/`; auto-invoke or `/skill-name` | Encode repeatable FDE procedures: triage, RCA packet, eval harness, threat model |
| Project rules | `AGENTS.md`, `.grok/rules/`, `.claude/rules/` (compat) | Bake GrokBuild doctrine into every session without re-prompting |
| MCP servers | `~/.grok/config.toml` `[mcp_servers.*]` | Connect GitHub PRs, internal ticketing, or data catalogs when field connectivity allows |
| Background tasks | `run_terminal_command` with `background: true`; `Ctrl+G` to background foreground cmd | Run Streamlit dev server, long pytest suites, or DuckDB builds while Grok continues coding |
| Memory | `--experimental-memory`, `/remember`, `/flush`, `/dream` | Persist operator conventions, deployment quirks, and prior RCA findings across sessions |
| Headless | `grok -p "..." -m grok-build --cwd <repo>` | CI golden-output checks, scripted eval runs, batch README generation |
| Worktrees | `grok --worktree=feat "..."`, `/execute-plan` worktree-isolated subagents | Safe parallel artifact builds without branch collision |

**Installation baseline (first stable stack)**

```bash
# Grok Build CLI (macOS/Linux)
curl -fsSL https://x.ai/cli/install.sh | bash
grok --version

# authenticate: browser login on first `grok` launch, or for CI/headless:
# export XAI_API_KEY="xai-..."

# launch in workbench with Grok Build model
grok -m grok-build --cwd /path/to/forward-deployed-ai-workbench

# optional: sandbox profile for everyday dev (read everywhere, write CWD + ~/.grok + tmp)
grok --sandbox workspace -m grok-build

# repo
git init
python -m venv .venv
source .venv/bin/activate

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

For single-file artifacts, maintain the no-build template under `single_file_html/`.

**Recommended repo structure**

```
forward-deployed-ai-workbench/
  README.md
  AGENTS.md                    # Grok Build project rules (doctrine, conventions, constraints)
  GROKBUILD_DOCTRINE.md        # This manifesto
  pyproject.toml
  requirements.txt

  /.grok                       # optional per-project Grok Build config
    sandbox.toml               # custom sandbox profiles, deny globs for secrets
    rules/                     # additional project rules (*.md)
    skills/                    # repo-scoped skills (override user skills by name)

  /specs
    product_brief.md
    operator_workflow.md
    data_contract.md
    acceptance_criteria.md
    threat_model.md

  /prompts
    grok_architect_prompt.md
    grok_build_brief.md
    grok_repair_brief.md
    eval_prompt.md
    design_system_prompt.md

  /skills                      # domain skills (Grok auto-discovers; also slash commands)
    triage-skill/SKILL.md
    rca-packet/SKILL.md
    eval-harness/SKILL.md

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

**The build portfolio (five finished artifacts beat fifty fragments)**

1. **Mission Autonomy Field Support Console** (NiceGUI + DuckDB + simulated telemetry) — Anduril FDE / technical operations signal. Shows operator-grade field diagnosis, degraded-mode handling, RCA generation, and engineering feedback packets.

2. **Financial Crime Operations Console** (Streamlit + DuckDB + case workflow) — Palantir / banking domain edge signal. Shows regulated workflow triage, risk scoring, evidence packets, SAR narrative drafts, and audit trails.

3. **Local Data Fusion Workbench** (Polars/DuckDB + entity matching + UI) — FDE data integration skill. Shows upload/profile/join/anomaly detection/export with Mermaid lineage and clean dataset output.

4. **LLM Red-Team Eval Harness** (Python + pytest + Streamlit/NiceGUI) — AI security credibility. Shows prompt injection, jailbreak, tool-call boundary, hallucination checks, golden outputs, severity ratings, and exportable reports.

5. **Single-File Executive Command Brief** (HTML + Tailwind + ECharts/Tabulator) — Zero-install artifact delivery. Proves portability into restricted environments.

Each artifact: Grok generates initial scaffolding, tests, docs, and narrative; human owns data control, UX judgment, and final integration. Core message across all: I use Grok inside a disciplined engineering loop to produce working software, not prompts.

**Bundled Grok Build orchestration skills (use at scale)**

| Skill | Command | What it does in GrokBuild terms |
|---|---|---|
| Design | `/design <description>` | Writer→reviewer subagent loop until design doc + PR-plan DAG reach consensus. Output: architecture spec ready for `/execute-plan`. |
| Execute plan | `/execute-plan <design-doc>` | Topologically sorts PR DAG, implements in worktree-isolated subagents, mandatory orchestrator review, assembles Graphite or plain-git stack. |
| Review | `/review [--local\|--branch\|--pr]` | Read-only reviewer subagent; writes review artifact. Use before operator handoff or engineering feedback. |
| Check work | `/check-work [focus]` | Verifier subagent runs diffs + builds + tests; fix loop until pass. Gate before demo or portfolio screenshot. |
| Create skill | `/create-skill` | Interactive skill authoring — encode a repeatable FDE procedure once, invoke forever. |

For a single artifact (not a multi-PR stack), the lighter loop is: `/plan` or architect prompt → Grok Build implementation → `/check-work` → `/review --local` → package.

**Operating loop (explicit FDE loop)**

1. Observe the operational constraint.
2. Identify the binding bottleneck (Grok first-principles assist).
3. Convert problem into spec (Grok architect prompt or `/design` for multi-component systems).
4. Generate data contract.
5. Build local prototype (Grok scaffolds code; use `grok --worktree=<artifact>` for isolation).
6. Test with fixtures (Grok generates tests; sandbox or local runs them; `/check-work` for verifier gate).
7. Add operator workflow.
8. Add eval / audit trail (Grok designs evals).
9. Package artifact.
10. Feed findings back to engineering (Grok helps craft RCA packet).

**Grok Build command mapping per loop step**

| Step | Grok Build invocation |
|---|---|
| 2–3 | `grok -m grok-build "@[specs/] decompose constraint..."` or `/design <mission>` |
| 4 | `@specs/data_contract.md` + Grok architect prompt; validate with JSON Schema in tests |
| 5 | Standard Grok task brief (below) or `/execute-plan` for multi-PR artifacts |
| 6 | `pytest`; Grok runs via `run_terminal_command`; `/check-work` before sign-off |
| 7–8 | `@src/apps/` + operator workflow spec; Grok edits UI layer only |
| 9 | Export commands in README; Grok generates screenshots narrative |
| 10 | RCA skill or prompt; `/review --local` for engineering-ready diff summary |

**Grok role**  
Requirement decomposition & reframing, architecture & diagrams, threat modeling, UX critique, eval design, Grok task brief generation, README/demo script/portfolio narrative, code scaffolding, test generation, diff analysis, and sandbox validation support.

**Grok Build-specific responsibilities (in addition to above):**
- Spawn `explore` subagents for codebase/architecture reconnaissance without polluting main context
- Spawn `plan` subagents for structured implementation plans on ambiguous missions
- Run `run_terminal_command` with execution feedback (install deps, run apps, capture stderr, repair)
- Manage `todo_write` task lists visible in scrollback for operator transparency
- Attach precise context via `@path:line-range` instead of pasting large blobs
- Compact session (`/compact`) when context fills; flush mission knowledge (`/remember`, `/flush`) before compaction
- Use `--sandbox read-only` when reviewing untrusted operator-supplied scripts or third-party code
- Use headless `grok -p` for reproducible validation scripts checked into `scripts/verify.sh`

**Human role**  
Choose mission, define acceptance criteria, control data exposure, judge UX usefulness, decide when to ship, own the operational narrative, apply patches to local repo, orchestrate sandbox or local execution.

**Human responsibilities specific to Grok Build:**
- Approve or deny plan mode entry (`enter_plan_mode`) and plan completion (`exit_plan_mode`)
- Set permission mode: normal (ask), `/always-approve`, or `/auto` classifier
- Choose sandbox profile for the session (`--sandbox workspace` default; `strict` for untrusted code)
- Select SuperGrok tier / model (`/model grok-build`, `/effort high` for hard architecture problems)
- Own `AGENTS.md` and skill definitions — Grok follows these automatically; garbage rules produce garbage artifacts
- Review subagent summaries before merging into operator-facing narrative (subagents compress; human validates fidelity)
- Decide when to `/fork` session for experimental approach vs. `/rewind` to discard a bad turn

**Standard Grok Task Brief (use every time)**

```
You are Grok assisting modification of this Forward-Deployed AI Systems Workbench repository.

Mission: [One-sentence objective]

Operational context: [Who uses this, under what constraints, what decision/workflow it supports]

Files to inspect first:
- README.md
- AGENTS.md
- GROKBUILD_DOCTRINE.md
- specs/product_brief.md
- src/
- tests/
- skills/

Grok Build invocation hints:
- Attach context: @specs/product_brief.md @src/core/ @tests/
- Run verification: pytest, ruff check, streamlit run (background if long-running)
- After edits: /check-work [focus area]
- Before handoff: /review --local

Implementation requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Acceptance criteria:
- App runs locally with documented command
- Tests pass
- No unnecessary dependencies
- Core logic separated from UI
- Sample fixtures included
- README updated with Grok-generated sections clearly marked
- Known limitations documented
- Governance fields populated (data source, assumptions, model usage, test status)

Do not:
- Introduce cloud dependencies
- Hardcode secrets
- Remove existing tests
- Add large frameworks unless justified

Deliver:
- Changed files summary
- Commands run (or sandbox validation steps)
- Test results
- Known gaps
- Suggested next leverage point
```

**Design doctrine**  
External terms: operator-grade interface, field-deployable tooling, local-first workflow system, high-trust decision surface, constrained-environment deployment, audit-ready AI workflow, offline-capable artifact, human-in-the-loop triage console.

Visual standard: dense, not cluttered; dark mode default; status colors used sparingly; no toy gradients or excessive rounded cards; charts must answer operational questions; every metric needs owner, timestamp, and source. Grok-generated diagrams stay clean and information-dense.

**Governance layer (every artifact exposes)**  
Data source, last refresh time, assumptions, input/output schema, Grok/model usage disclosure, known limitations, test status, export version, user/operator action log. This separates “cool AI app” from “high-trust operational tool.”

**Grok/model usage disclosure fields (recommended):**
- Agent runtime: Grok Build (xAI CLI)
- Model: `grok-build` (or override if noted)
- Session mode: interactive TUI / headless / sandbox profile name
- Skills invoked: list of `SKILL.md` names used in build (e.g., `triage-skill`, `/check-work`)
- Subagents spawned: yes/no + types (`explore`, `plan`, implementer)
- Human approval gates: plan approved Y/N, permission mode, final sign-off owner
- Verification: `/check-work` pass Y/N, pytest count, golden-output hash

**Build sequence (30-day plan, compressible with Grok + sandbox)**

Week 1: Grok generates full repo template, Grok task brief, Streamlit starter, single-file HTML starter, Mermaid generator. Sandbox validates base installs and basic app runs. Initialize `AGENTS.md` with GrokBuild doctrine; create domain skills under `skills/`. Verify Grok Build install and `grok -m grok-build --cwd <repo>` launches cleanly.  
Week 2: Build Local Data Fusion Workbench (Grok scaffolds core + tests + exports). Add pytest fixtures, README, demo script. Run `/check-work` gate before README screenshots.  
Week 3: Build Mission Autonomy Field Support Console and Financial Crime Operations Console. Add screenshots/walkthroughs (Grok assists narrative). Use `grok --worktree=mission-console` and `grok --worktree=fin-crime` for parallel isolation.  
Week 4: Build LLM Red-Team Eval Harness. Add portfolio landing page, refactor shared components, polish GitHub narrative (Grok writes final READMEs and positioning). Optional: `/design` + `/execute-plan` if refactoring into shared library PR stack.

With heavy Grok leverage and sandbox for parallel validation, target compression to 10–14 days for initial five artifacts.

**Accelerated sequence with bundled skills (10–14 day target):**
- Day 1–2: `/design` umbrella architecture → repo template + `AGENTS.md` + core skills
- Day 3–5: Artifact 3 (Data Fusion) — full loop with `/check-work`
- Day 6–8: Artifacts 1 + 2 in parallel worktrees via subagents
- Day 9–10: Artifact 4 (Red-Team Eval)
- Day 11–12: Artifact 5 (single-file HTML) + portfolio landing
- Day 13–14: `/review --local` on each artifact; governance scorecards; headless verify script

**Redline metrics (operating telemetry)**

Idea to spec: <10 minutes  
Spec to working prototype: <45 minutes  
Prototype to polished artifact: <2 hours  
Repair loops: <3  
Manual code written by human: <20%  
Test pass rate before demo: 100%  
Reusable component created per build: >=1  
Offline artifact export: yes  
README quality (Grok-assisted but human-owned): pass  
Demo length: <4 minutes

**Grok Build telemetry (add to redlines):**
- Subagent spawns per artifact: ≤3 (explore + implement + verify)
- `/check-work` passes before demo: required
- Session compactions per build: ≤2 (indicates context discipline)
- Sandbox validation runs before operator handoff: ≥1
- Headless verify script in repo: yes (for CI or air-gapped re-validation)
- Skills created or extended per artifact: ≥1 (reusable leverage)

**What this says to Anduril / Palantir / defense tech**

I can take ambiguous operational problems, build local-first tools quickly, handle constrained environments, instrument failure modes, create operator-grade interfaces, and convert field feedback into engineering-ready artifacts — using Grok as the disciplined acceleration layer inside a first-principles engineering loop (requirements → data contract → implementation → testing → eval → packaging → feedback). The output is working software with governance, not a prompt.

I operate **Grok Build** as the field engineering terminal: real execution, sandboxed validation, subagent parallelism, persistent project rules, and verifiable test gates — not a browser chat session that hallucinates file contents.

Weak alternative narrative to avoid: “I am good at prompting LLMs to make cool dashboards.”

**Final recommendation**

Build this as a named portfolio system with five focused repos under one umbrella:

```
forward-deployed-ai-workbench/
  mission-support-console/
  financial-crime-ops-console/
  local-data-fusion-workbench/
  llm-red-team-eval-harness/
  single-file-command-briefs/
```

Each repo contains: README (Grok-assisted), problem statement, architecture diagram, screenshots, install/run instructions, sample data, tests, demo script, limitations, next build path.

Each repo should also contain: `AGENTS.md` (GrokBuild constraints), at least one domain `skills/*/SKILL.md`, a `scripts/verify.sh` headless Grok or pytest entrypoint, and governance fields in the app footer or export metadata.

This proves the full loop — operator empathy, system design, data handling, code execution, UX judgment, testing, governance, and deployment pragmatism — at the exact signal strength required for FDE AI engineer roles.

**Grok Build quick-reference card**

```bash
# Daily driver
grok -m grok-build --cwd ~/forward-deployed-ai-workbench

# Isolated artifact branch
grok --worktree=data-fusion -m grok-build "implement Local Data Fusion per @specs/"

# Plan before code (ambiguous architecture)
/plan Add degraded-mode telemetry handling with offline queue

# Verify before demo
/check-work scoring and export paths

# Review before engineering handoff
/review --local

# Headless CI verify (check into repo)
grok -p "Run pytest and summarize failures" --cwd . --sandbox workspace --yolo

# Constrained / read-only review of untrusted input
grok --sandbox read-only -m grok-build "Review @fixtures/sample_logs.txt for injection patterns"

# Preserve field context across sessions
/remember operator uses Safari on iPad; Streamlit touch targets must be ≥44px
/flush
```

Ready to execute. I can initialize the umbrella repo structure, generate the Grok task brief template, core prompts, and first artifact scaffolding (e.g., Local Data Fusion Workbench or the single-file HTML base) directly in the sandbox right now. Approve the starting artifact or template and we begin.