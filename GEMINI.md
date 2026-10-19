# Project Handover & Session State (GEMINI.md) — PANTHEON AI Agent and Skills Setup Kit for Service Governance

> [!IMPORTANT]
> This file is a living document and MUST be kept updated at critical project milestones,
> architectural decisions, or status changes to maintain persistent context across sessions.
> **Grounding Frameworks**: **ITIL 4 & ITIL 5**, **NIST SP 800-41/800-53/CSF 2.0**, **NCSC & Cyber Essentials Plus**, and **UKFS-01..06**.

## 📂 Project Architecture & Module Layout

The project follows a decoupled, modular architecture that strictly separates analytical calculations
and scoring algorithms from external API network I/O, credential retrieval, and database storage:

### 1. Ingestion & Relay Module (`/IngestionRelay`)
- **Purpose**: Daily ticket backlog extraction, untruncated journal history parsing, and webhook routing.
- **Core Principles**: Pure vs I/O separation. Pure functions for parsing, comment cleaning, staleness calculation,
  and worst-SLA derivation live in reusable modules; network calls and credential handling live in entry runners.
- **Key Components**:
  - `BacklogRelay.py`: Core ingestion engine querying ITSM APIs (ServiceNow/Jira) and SharePoint list backlogs.
  - `TicketSummaryExporter.py`: CLI utility to export comprehensive ticket summaries, quality/closure metrics,
    root-cause details, untruncated journal histories, and associated SLAs to console, JSON, or text files.
  - `src/ticket_utils.py`: Pure utility functions for ticket parsing, journal comment cleaning, role classification,
    SLA extraction, and report formatting (100% testable offline without network access).
  - `src/itsm_api.py`: Resilient HTTP client featuring connection reuse, 60s request timeouts, exponential
    backoff retry for rate limits (429) and server errors (5xx), and fail-fast exceptions (`FetchError`)
    preventing empty backlog misinterpretation.
  - `src/config.py`: Central configuration engine calling `config.require(...)` to validate all mandatory
    environment variables at startup before performing API queries.
  - `Tests/`: Language-neutral JSON test fixtures and Python unit test suites.

### 2. Automation & PowerShell Port (`/AutomationPS`)
- **Purpose**: Native PowerShell 7.2+ implementation of core relays for enterprise environments where
  PowerShell is the primary automation standard.
- **Core Principles**: Replicates Python decision logic byte-for-byte. Pure functions live in `Private/`,
  I/O operations live in `Public/`, and both implementations validate against identical JSON test fixtures.
- **Key Components**:
  - `RelayModule.psd1` / `RelayModule.psm1`: PowerShell module manifest and loader.
  - `Public/`: I/O layer — credential retrieval (Windows SecretStore / vault), API querying, webhook delivery.
  - `Private/`: Pure functions — business hours calculation, staleness scoring, SLA derivation, payload assembly.
  - `Config/StaleTicketQuery.psd1`: Declarative, commented query definition isolated from code logic.
  - `Tests/`: Pester test suite consuming shared JSON fixtures without requiring network access.

### 3. Analytics & Scorecard Server (`/AnalyticsDashboard`)
- **Purpose**: Analytics web dashboard server, productivity pacing calculations, and QA scorecards.
- **Key Components**:
  - `server.py`: FastAPI backend server enforcing strict Basic Authentication and secure database proxying.
  - `WeeklyPacingAuditor.py`: Daily time worked pacing audit and closed task productivity reporter.
  - `src/analytics.py`: Pure calculation functions for 6-month longitudinal trends, utilization, and QA pass rates.
  - `Data/`: Structured capacity/triage CSVs, Excel models, and generated Markdown productivity summaries.

### 4. Governance Framework & Specialist Multi-Agents (`.agents/`)
- **Purpose**: Native Google Antigravity workspace customizations for automated governance and multi-perspective audits.
- **Specialist Advisory Agents** (`.agents/agents/`):
  - `aegis_best_practice`: Infrastructure Best-Practice Analyser auditing Palo Alto (PAN-OS), FortiGate (FortiOS), Juniper (Junos), Windows Server, and Linux Server against NIST, NCSC, vendor hardening, and UKFS-01..06 outcomes.
  - `atlas_architecture`: Systems Architect auditing modularity, dual-stack parity, pure separation, and resilience.
  - `sage_governance`: Service Analytics Lead auditing operational KPI thresholds, pacing, throughput, and QA.
  - `sentinel_security`: Security & Compliance Lead auditing secret isolation, API authentication, and PII protection.
  - `spark_disruptor`: Contrarian Disruptor challenging operational orthodoxies, timesheet gaming, and complexity.
- **Governance Skills** (`.agents/skills/`):
  - `infrastructure-best-practice-analyser`: Multi-platform standards catalogue (NIST 800-41/800-53/CSF 2.0, NCSC, UKFS-01..06, ISO/CIS/PCI/SWIFT placeholders) for firewalls, routers, and Windows/Linux servers.
  - `ticket-backlog-governance`: 4-criterion 145-point rubric, staleness rules, and top-5 prioritisation.
  - `productivity-workload-governance`: 315-min daily pacing, 2 tasks/day throughput, and 10% proactive allocation.
  - `quality-audit-governance`: Dual-metric scoring (`Resolve Pass %` vs Granular QA score), future-date pending override.
  - `teams-standup-digest-notifier`: Operational standup card formatting and distribution.
  - `support-team-governance-analytics-coaching`: 3-stage evidence-based coaching workflow.
- **Standalone System Prompts & Blueprints** (`Governance_Framework/`):
  - `SAGE_Agent_System_Prompt.md`: Master system prompt for S.A.G.E. operational governance.
  - `AEGIS_Agent_System_Prompt.md`: Copy-paste infrastructure config analysis prompt template (`PAN-OS`, `FortiOS`, `Junos`, `Windows`, `Linux`) + **Untested Future Project Blueprint** for an automated multi-vendor read-only API config ingestion pipeline.

---

## 🧹 Maintenance & Cleanliness Guidelines

### 1. Modular Architecture & Deep Modules (`codebase-design`)
- **Configuration & Constants**: All environment-specific variables must be defined in `.env` and loaded via
  `src/config.py`. Never hardcode instance URLs, tenant GUIDs, usernames, or passwords in source scripts.
- **Deep Modules & Clean Seams**: Place rich, pure calculation logic (`src/` or `Private/`) behind small, well-typed
  interfaces at a clean **seam**, strictly decoupled from I/O adapters (`Public/` or CLI runners).
- **Mandatory Redaction (`<REDACTED>`)**: Scrub all credentials, tokens, PSKs, and hashes (`<REDACTED>`) before
  logging, displaying diagnostic output, or saving test fixtures.
- **Fail-Fast Error Handling**: API integration modules must raise explicit exceptions on failure rather than
  returning empty or partial datasets that could be misinterpreted as a cleared backlog.
- **Shared Test Fixtures**: Pure logic changes must be accompanied by updates to language-neutral JSON test
  fixtures under `Tests/fixtures/` to verify parity across both Python and PowerShell runtimes.

### 2. Deployment & Security Standards
- Maintain `.dockerignore` to exclude local secrets (`.env`), raw customer ticket data (`Data/`), and temporary caches.
- Restrict dashboard endpoints with mandatory authentication (`BasicAuthMiddleware` with fail-fast startup checks).
- Never commit credentials, API keys, or customer journal exports to version control.

---

## ⚡ Primary Workflows & Operational Runbook

### 1. Language Selection & Polyglot Strategy (Read Before Writing Code)
Establish your language boundary and folder seams *before* prompting the AI (see `ANTIGRAVITY_SETUP_GUIDE.md` §1.3 & §6.7):

| Operational Task | Recommended Language | Rationale |
| :--- | :--- | :--- |
| **KPI Math, Pacing & Config Evaluators** | **Python (Primary)** | Deterministic types, clean date/time math, highest AI first-pass accuracy, fast unit testing. |
| **ITSM / Graph / Firewall REST APIs** | **Python (Primary)** | Connection pooling (`requests.Session`), retry/backoff ergonomics, strict JSON schema typing. |
| **Web Dashboards, APIs & DB Proxies** | **Python (`FastAPI`)** | Native async web servers, middleware auth, Linux containerization for cloud hosting. |
| **Portable Distributable CLI Tools** | **Python (`PyInstaller`)** | Bundles runtime + dependencies into a single `.exe` for colleagues without dev setups. |
| **OS Credential Vaults & Host Tasks** | **PowerShell 7.2+ (`pwsh`)** | Native SecretStore/DPAPI cmdlets, Active Directory, WinRM, Task Scheduler registration. |

- **Polyglot Combination Rules**:
  1. **Thin OS Wrapper + Analytical Core**: Use PowerShell 7.2+ (`setup.ps1` / Task Scheduler wrapper / SecretStore) for host/OS seams, and invoke Python for API pagination, data analysis, and reporting.
  2. **Dual-Runtime Parity via Shared JSON Fixtures**: Keep pure logic in `src/` (Python) and `Private/` (PowerShell 7.2+) validated against identical `Tests/fixtures/*.json` files.
  3. **Strict Inter-Process Contracts**: Exchange data via structured JSON files or environment variables—never scrape console `stdout` or pass plaintext secrets on the command line.

### 2. Skills vs. Agents: Packaged Expertise vs. Autonomous Execution
- **Skill (`.agents/skills/<name>/SKILL.md`) = Packaged Expertise & Guidance**: Stateless SOPs, formulas, and standards catalogues (`Test Library 1.1.0`) injected on demand into the *current* agent's context window when its YAML `description` pointer triggers.
- **Specialist Agent (`.agents/agents/<name>/agent.md`) = Autonomous Execution & Isolated Context**: Independent specialist persona spawned via `invoke_subagent` with its own isolated context window and scoped tools—ideal for multi-file exploration, adversarial grilling (`SPARK`), or parallel two-axis code/security reviews (`ATLAS` + `SENTINEL` + `AEGIS`) without polluting your main session.

### 3. Planning, Requirements Gathering & Token Efficiency (`mattpocock/skills` Baseline)
- **Grill the Design Tree First (`/grill-me` / `@spark_disruptor`)**: Map unknowns as a design tree and resolve the **ready frontier** of prerequisite decisions in structured rounds before writing code.
- **Tracer-Bullet Vertical Slices (`to-tickets`)**: Cut narrow, end-to-end vertical slices (1 API field $\rightarrow$ 1 pure function $\rightarrow$ 1 JSON fixture $\rightarrow$ 1 CLI output) that fit in a single context window. Use **Expand–Contract** sequencing for wide refactors.
- **Context Load & Progressive Disclosure (`writing-for-agents`)**: Keep `GEMINI.md` strictly `< 24,000 bytes` as a high-signal index; push deep reference tables behind sharp `"Use when..."` context pointers in `.agents/skills/`.
- **Tight Feedback Loops & Deterministic Checks (`diagnosing-bugs` & `retro`)**: Build `< 2s` red-capable CLI/fixture loops before debugging, and convert mechanical rules into automated checks (`validate_kit.py`, `ruff check .`, `mypy src/`). Compact long sessions with `/compact` between planning and implementation.

### 4. Workspace Bootstrapping, Linting & Fixture Tests
```powershell
# 1. Bootstrap workspace, print Python vs. PowerShell guide, rebuild HTML docs, and validate kit
python setup.py
pwsh -NoProfile -File .\validate_and_install.ps1 -ValidateOnly

# 2. Static analysis & formatting
ruff check . --fix
ruff format .
mypy src/

# 3. Offline fixture validation (Python & PowerShell)
python Tests/run_fixtures.py
pwsh -File AutomationPS/Tests/Invoke-FixtureTests.ps1
```

---

## 📍 Current Operational Status & Metric Baselines

- **Security Posture**: Strict Basic Auth on analytics endpoints; secrets isolated in `.env` / Windows DPAPI SecretStore; mandatory `<REDACTED>` scrubbing on diagnostic artifacts.
- **Governance & Infrastructure Baselines**:
  - **Daily Time Worked Target**: 315 minutes (5.25h / 70% direct ticket logging); **Capacity Ceiling**: 80% (30.0h/week).
  - **Closed Task Throughput**: 2 organic tasks/day (~10/week, isolating automated events); **Proactive Ratio**: $\ge 10\%$.
  - **Ticket Staleness**: $\ge 8.5\text{h}$ business hours (Incident) and $\ge 17.0\text{h}$ (Request) within Mon–Fri 09:00–17:30.
  - **Backlog Prioritisation**: 4-criterion 145-point model (Status 50, Review Age 40, Stagnancy 35, Age Band 20), capped at Top 5 per squad.
  - **Dual Quality Metric**: `Resolve Pass % (Granular Score %)` with future-date `Pending` override (`HEALTHY`).
  - **Infrastructure Standards (`AEGIS`)**: `Test Library 1.1.0` covering PAN-OS, FortiOS, Junos, Windows Server, and Linux Server against NIST 800-41/800-53/CSF 2.0, NCSC, and `UKFS-01..06`.

---

## ✅ Project Milestones & Living Changelog

- [x] **Repository Initialisation**: Root `.gitignore`, `.env.template`, Ruff, and Mypy configured.
- [x] **Modular Architecture Split**: Segregated ingestion runners, analytics dashboard, and PowerShell port.
- [x] **Pure Function Test Fixtures**: Created language-neutral JSON test fixtures shared across runtimes.
- [x] **Specialist Multi-Agent Team (5 Agents)**: Deployed `AEGIS`, `ATLAS`, `SAGE`, `SENTINEL`, and `SPARK` in `.agents/agents/`.
- [x] **Governance & Infrastructure Skills (6 Skills)**: Configured 6 progressive-disclosure skills in `.agents/skills/`.
- [x] **AEGIS Copy-Paste Prompt & API Pipeline Blueprint**: Added `Governance_Framework/AEGIS_Agent_System_Prompt.md`.
- [ ] **Future Project (Untested)**: Implement tracer-bullet Slice 1 of the `AEGIS` multi-vendor API config ingestion pipeline.

---
*Last Updated: 2026-10-19 (Session 2: Added AEGIS System Prompt, API Pipeline Blueprint, Skill vs. Agent Guide & Skills For Real Engineers Patterns)*
