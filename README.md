# PANTHEON AI Agent and Skills Setup Kit for Service Governance

> **PANTHEON** — *Platform for AI-Native Technical Hygiene, Excellence & Operational Navigation*  
> An enterprise starter kit of **5 specialist AI advisory agents**, **6 operational & infrastructure hardening skills**, **standalone master prompts**, and **automated zero-leak validation tooling** for Enterprise IT, Service Operations, and Managed Service Providers (MSPs).  
> Grounded in **ITIL 4 & ITIL 5**, **NIST SP 800-41 / 800-53 / CSF 2.0**, **NCSC & Cyber Essentials Plus**, and **UK Financial-Services Operational Resilience (`UKFS-01`–`UKFS-06`)** across `PAN-OS`, `FortiOS`, `Junos`, `Windows Server`, and `Linux Server`.

- **Live HTML Documentation Portal**: [**`https://apswood.github.io/pantheon-ai-kit/`**](https://apswood.github.io/pantheon-ai-kit/)
- **Offline Local Documentation Portal**: Open [`ANTIGRAVITY_DOCS.html`](ANTIGRAVITY_DOCS.html) directly in any browser (`file://` — zero web server or internet connection required)
- **Complete Setup & Engineering Manual**: [`ANTIGRAVITY_SETUP_GUIDE.md`](ANTIGRAVITY_SETUP_GUIDE.md)

---

## 1. Quickstart & Installation

You do **not** need to clone or manually download the repository beforehand. Run a single bootstrap command in your target project directory to download all 24 canonical kit files, initialize `.env` from `.env.template`, optionally configure the custom keyword leak scanner, and run all 4 pre-flight validation checks.

### Option A: Zero-Clone PowerShell One-Liner (Recommended)
Open PowerShell (`pwsh` 7.2+ recommended, or Windows PowerShell 5.1) in your target directory and run:

```powershell
# 1. Create or enter your project workspace directory and run the remote bootstrapper:
mkdir C:\Workspaces\ServiceDeliveryOps; cd C:\Workspaces\ServiceDeliveryOps
irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex

# Alternative: Install into a specific folder via environment variable:
$env:PANTHEON_TARGET_DIR = "C:\Workspaces\ServiceDeliveryOps"; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex
```

### Option B: Cross-Platform Python Bootstrapper (`setup.py`)
If you prefer Python (Windows, macOS, or Linux):

```powershell
# Zero-clone Python bootstrap (fetches all 24 kit files, initializes .env, rebuilds HTML docs, and validates):
irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/setup.py -OutFile setup.py; python setup.py --init-env

# Or from an existing local clone (with optional isolated .venv creation):
python setup.py --init-env --venv
```

### Next Steps After Installation
1. **Populate Local Credentials (`.env`)**: Open the generated `.env` file and add your environment values (ITSM URL, Entra ID / Graph tenant GUID, or Teams webhook URL). `.env` is strictly blocked by `.gitignore` and never committed to Git.
2. **Open Workspace in Google Antigravity**: Open the workspace folder in Google Antigravity. It automatically discovers `GEMINI.md`, all 5 agents in `.agents/agents/`, and all 6 skills in `.agents/skills/`.
3. **Verify or Customize Leak Scanning *(Optional)***:
   ```powershell
   # Run the 4-stage compliance & credential leak validator at any time:
   python validate_kit.py
   pwsh -NoProfile -File .\validate_and_install.ps1 -ValidateOnly

   # Configure or reset custom organization keywords in .custom_blocklist.json (gitignored):
   pwsh -NoProfile -File .\validate_and_install.ps1 -ConfigureCustomScanner
   python setup.py --configure-scanner
   ```

### Uninstallation & Workspace Cleanup
To surgically remove the starter kit from a target workspace (preserving your `.env` secrets and any custom project files by default):

```powershell
# Preview deletion plan (Dry Run / WhatIf — no files deleted):
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -WhatIf
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" --dry-run

# Execute surgical uninstallation:
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -Force
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" -y
```
*(Add `-PurgeSecrets -PurgeVenv` or `--purge-secrets --purge-venv` for a complete teardown. See [Workspace Lifecycle Symmetry & Surgical Uninstallation](https://apswood.github.io/pantheon-ai-kit/#setup-guide-77-workspace-lifecycle-symmetry-surgical-uninstallation) in the HTML docs).*

---

## 2. What's Included at a Glance

### 2.1 Five Specialist Multi-Agent Personas (`.agents/agents/`)
Invoke any specialist agent in isolated subagent context using `@agent_name` or natural language prompts:

| Agent | Persona & Mandate | Example Invocation | Documentation |
| :--- | :--- | :--- | :--- |
| **`aegis_best_practice`** | **AEGIS** — Multi-platform infrastructure hardening & resilience auditor (`PAN-OS`, `FortiOS`, `Junos`, `Windows`, `Linux` against NIST, NCSC, and `UKFS-01..06`). | `"Ask AEGIS to audit this FortiGate / Palo Alto config against NIST 800-41 and UKFS outcomes."` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#agent-aegis) · [Source](.agents/agents/aegis_best_practice/agent.md) |
| **`atlas_architecture`** | **ATLAS** — Systems architecture, deep modules, clean test seams, pure vs. I/O separation, and Python/PowerShell parity. | `"Ask ATLAS to review our API client for retry backoff and pure-function separation."` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#agent-atlas) · [Source](.agents/agents/atlas_architecture/agent.md) |
| **`sage_governance`** | **SAGE** — ITIL 4/5 service delivery governance, SLA staleness, capacity pacing, QA scorecards, and evidence-based coaching. | `"Have SAGE audit this week's engineer time pacing and backlog stagnancy report."` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#agent-sage) · [Source](.agents/agents/sage_governance/agent.md) |
| **`sentinel_security`** | **SENTINEL** — Zero-trust secret isolation (`.env`, Windows DPAPI), `<REDACTED>` scrubbing, API auth, and GDPR PII hygiene. | `"Ask SENTINEL to scan the workspace for exposed secrets or hardcoded tenant IDs."` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#agent-sentinel) · [Source](.agents/agents/sentinel_security/agent.md) |
| **`spark_disruptor`** | **SPARK** — Design-tree frontier interviewing (`/grill-me`), tracer-bullet vertical slicing, and contrarian Kaizen simplification. | `"Ask SPARK to grill our new config collector design and slice it into tracer-bullet tickets."` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#agent-spark) · [Source](.agents/agents/spark_disruptor/agent.md) |

### 2.2 Six On-Demand Operational & Infrastructure Skills (`.agents/skills/`)
Skills use **progressive disclosure**—only their lightweight YAML context pointers load at startup, hydrating full mathematical rubrics and standards catalogues on demand:

| Skill | Core Thresholds, Formulas & Standards | Slash / Prompt Trigger | Documentation |
| :--- | :--- | :--- | :--- |
| **`infrastructure-best-practice-analyser`** | `Test Library 1.1.0` across `PAN-OS`, `FortiOS`, `Junos`, `Windows`, `Linux`; NIST 800-41/800-53/CSF 2.0, NCSC, `UKFS-01..06`, ISO/CIS/PCI/SWIFT placeholders. | `/infrastructure-best-practice-analyser` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-best-practice) · [Source](.agents/skills/infrastructure-best-practice-analyser/SKILL.md) |
| **`ticket-backlog-governance`** | Business-hours staleness (`>= 8.5h` Incident / `>= 17.0h` Request, Mon–Fri 09:00–17:30), 5-tier age bands, 145-point priority rubric. | `/ticket-backlog-governance` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-backlog) · [Source](.agents/skills/ticket-backlog-governance/SKILL.md) |
| **`productivity-workload-governance`** | `315 min/day` (5.25h / 70%) direct logging target, `80%` utilization ceiling, `2 closed tasks/day` organic throughput, `>= 10%` proactive ratio. | `/productivity-workload-governance` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-productivity) · [Source](.agents/skills/productivity-workload-governance/SKILL.md) |
| **`quality-audit-governance`** | Dual-metric QA scorecard: `Resolve Pass % (Granular Score %)`, KB0016486 rubric, future-date `Pending` override (`HEALTHY`). | `/quality-audit-governance` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-quality) · [Source](.agents/skills/quality-audit-governance/SKILL.md) |
| **`teams-standup-digest-notifier`** | Daily standup Adaptive Cards / HTML payloads capped at **Top 5 tickets per squad**, `🔥 Multi-Day` blocker badges (`>= 3d`). | `/teams-standup-digest-notifier` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-digest) · [Source](.agents/skills/teams-standup-digest-notifier/SKILL.md) |
| **`support-team-governance-analytics-coaching`** | Non-accusatory **3-step evidence-based coaching** plans (Objective Observation $\rightarrow$ Operational Impact $\rightarrow$ Constructive Alignment). | `/support-team-governance-analytics-coaching` | [HTML Docs](https://apswood.github.io/pantheon-ai-kit/#skill-coaching) · [Source](.agents/skills/support-team-governance-analytics-coaching/SKILL.md) |

### 2.3 Standalone System Prompts & Copy-Paste Templates (`Governance_Framework/`)
- **[`AEGIS_Agent_System_Prompt.md`](https://apswood.github.io/pantheon-ai-kit/#aegis-master-prompt)** ([Source](Governance_Framework/AEGIS_Agent_System_Prompt.md)): Ready-to-use copy-paste infrastructure configuration audit prompt (`<REDACTED>` pre-paste checklist + `PAN-OS`, `FortiOS`, `Junos`, `Windows`, `Linux` assessment) and an architectural blueprint for an automated multi-vendor read-only API ingestion pipeline.
- **[`SAGE_Agent_System_Prompt.md`](https://apswood.github.io/pantheon-ai-kit/#sage-master-prompt)** ([Source](Governance_Framework/SAGE_Agent_System_Prompt.md)): Standalone master system prompt for ITIL 4 & ITIL 5 service operations governance and coaching.

---

## 3. Repository Layout (24 Canonical Files)

```text
pantheon-ai-kit/
├── .agents/
│   ├── agents/                             # 5 Specialist Subagents (AEGIS, ATLAS, SAGE, SENTINEL, SPARK)
│   ├── skills/                             # 6 Progressive-Disclosure Operational & Hardening Skills
│   └── rules/sage-governance-prompt.md     # Always-on workspace governance rule
├── Governance_Framework/                   # Standalone SAGE & AEGIS master system prompts
├── GEMINI.md                               # Living workspace handover & session state ledger (< 24 KB)
├── ANTIGRAVITY_DOCS.html                   # Offline-ready responsive HTML5 documentation portal
├── ANTIGRAVITY_SETUP_GUIDE.md              # Full architecture, hygiene & KPI customization manual
├── README.md                               # Concise quickstart & navigation index (this file)
├── .env.template                           # Safe environment variable contract (zero secrets)
├── .gitignore                              # Blocks .env, .venv, and .custom_blocklist.json from Git
├── setup.py                                # Python bootstrapper, runtime advisor & uninstaller
├── build_docs.py                           # Zero-dependency compiler regenerating ANTIGRAVITY_DOCS.html
├── validate_kit.py                         # Python 4-stage structural & secret leak validator
└── validate_and_install.ps1                # PowerShell zero-clone bootstrapper, validator & uninstaller
```

---

## 4. Deep-Dive Architecture & Engineering Guides (HTML Documentation Portal)

Detailed architectural guidance, first-principles explanations for Systems Engineers, and KPI customization runbooks live in the responsive [**HTML Documentation Portal (`ANTIGRAVITY_DOCS.html`)**](https://apswood.github.io/pantheon-ai-kit/) (compiled from [`ANTIGRAVITY_SETUP_GUIDE.md`](ANTIGRAVITY_SETUP_GUIDE.md)):

| Topic / Engineering Guide | What You Will Learn | Portal Link |
| :--- | :--- | :--- |
| **Grounding Frameworks & System Architecture** | How ITIL 4/5, NIST 800-41/800-53/CSF 2.0, NCSC/CE+, and `UKFS-01..06` map to the 5 agents and 6 skills, plus licensed placeholder handling (`ISO 27001`, `CIS`, `PCI DSS`, `SWIFT`). | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-14-grounding-frameworks-standards-catalogue-system-architecture) |
| **Language Selection Strategy (Python vs. PowerShell 7.2+)** | Why Python is primary for KPI math, APIs, and AI accuracy; when to use PowerShell 7.2+ (`pwsh`) for Windows DPAPI SecretStore/AD/OS tasks; and polyglot combination patterns. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-67-language-selection-strategy-systems-scripting-powershell-vs-general-purpose-languages-python) |
| **Skills vs. Agents & Progressive Disclosure** | How Antigravity's 5-tier discovery hierarchy works, when to build a stateless Skill (`SKILL.md`) vs. an isolated Subagent (`agent.md`), and preventing context window degradation. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-2-antigravity-customization-architecture-progressive-disclosure) |
| **Secret Management from First Principles** | Why Git is an append-only DAG, the 3-tier secret isolation defense (`.gitignore` + `.env.template` + `.env` / Windows DPAPI SecretStore), and fail-fast `config.require()` validation. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-3-secret-management-from-first-principles) |
| **Static Analysis (`Ruff` / `Mypy`) & `.venv` Isolation** | Catching probabilistic LLM hallucinations (`TypeError`, bare `except:`, mutable defaults) in milliseconds via AST linting and hermetic Python virtual environments. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-4-code-linting-static-analysis-in-the-ai-era) |
| **Pure vs. I/O Separation & Offline Fixture Testing** | Decoupling mathematical scoring engines (`src/` and `Private/`) from network I/O and verifying cross-runtime parity using shared JSON test fixtures (`Tests/fixtures/*.json`). | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-6-modular-architecture-pure-functions-vs-io-separation-offline-fixture-testing) |
| **Custom Leak Scanner & Validation Severity Guide** | How `.custom_blocklist.json` (`$EncodedRules`) works, understanding **Critical Built-In Secret Matches** vs. **Whole-Word Custom Matches** vs. **Benign Substring False Positives**, and resetting rules. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-76-custom-organization-keyword-leak-scanner-validation-severity-guide) |
| **Customizing KPI Thresholds & Rubrics** | Tailoring business-hours windows (`8.5h`/`17.0h`), the 145-point backlog rubric, 5-tier age bands, `315 min/day` pacing curves, and dual-metric QA weights. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-8-customizing-kpi-frameworks-operational-thresholds) |
| **Agentic Engineering Habits (`mattpocock/skills`)** | Upfront design-tree frontier interviewing (`/grill-me`), tracer-bullet vertical slices, expand–contract refactors, and `< 2s` deterministic feedback loops. | [Open in HTML Docs](https://apswood.github.io/pantheon-ai-kit/#setup-guide-9-ai-assisted-engineering-best-practices-planning-token-efficiency-skills-for-real-engineers) |

> **Tip**: Anytime you edit a Markdown file in this repository, run `python build_docs.py` (or `python setup.py`) to recompile [`ANTIGRAVITY_DOCS.html`](ANTIGRAVITY_DOCS.html) in under 0.5 seconds.

---

## 5. De-Identification Guarantee & Maintenance

This repository contains **zero** proprietary organization identifiers, tenant GUIDs, internal employee names, or live credentials. All configuration is handled via `.env.template` placeholders (`<YOUR_VALUE>`), and every change is verified against `validate_kit.py` and `validate_and_install.ps1` (Exit Code `0`).
