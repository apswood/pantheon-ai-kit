# PANTHEON AI Agent and Skills Setup Kit for Service Governance
## A Starter Kit for Building AI Agents and Skills for Multi-Agent AI Service Governance, Operational Excellence & Infrastructure Hardening

> **Description**: A starter kit for building AI agents and skills for multi-agent AI service governance, operational excellence & infrastructure hardening setup kit for Enterprise IT, Service Operations & MSPs. Grounded in **ITIL 4 & ITIL 5**, **NIST SP 800-53/CSF 2.0**, **NCSC & Cyber Essentials Plus** aligned operational resilience (`PAN-OS`, `FortiOS`, `Junos`, `Windows`, `Linux`).  
> **PANTHEON** — *Platform for AI-Native Technical Hygiene, Excellence & Operational Navigation*  
> **Repository**: [`https://github.com/apswood/pantheon-ai-kit.git`](https://github.com/apswood/pantheon-ai-kit.git) (`pantheon-ai-kit`)

---

## 1. Project Overview, Grounding Frameworks & Architecture

### 1.1 Purpose of the PANTHEON AI Agent and Skills Setup Kit
The **PANTHEON AI Agent and Skills Setup Kit for Service Governance** (`pantheon-ai-kit`) is an enterprise-grade, vendor- and product-agnostic starter kit for building and deploying AI agents and operational skills. While its reference workspace customization rules and local documentation portal (`ANTIGRAVITY_DOCS.html`) are pre-configured to drop directly into **Google Antigravity** workspaces, its specialist agent prompts, operational skills, mathematical KPI formulas, and infrastructure hardening standards are completely portable across any agentic AI coding environment.

Named after the classical **Pantheon**—an assembly of specialist guardians working in concert—this kit equips **Enterprise IT Operations, Service Delivery & ITSM Teams, Managed Service Providers (MSPs), Infrastructure Architects, and Technical Delivery Squads** with battle-tested automation, deterministic metric baselines, multi-vendor infrastructure hardening standards, and a 5-agent advisory council.

Modern enterprise IT operations, service delivery teams, and MSPs frequently struggle with three systemic challenges:
1. **Queue Stagnancy & Configuration Drift**: Ticket backlogs and firewall/router/server estates grow unchecked because manual review rituals cannot prioritize hundreds of aging tickets or multi-vendor device configurations effectively.
2. **Subjective Productivity & Performance Management**: Capacity tracking often degenerates into vanity timesheet compliance or uncalibrated micromanagement without objective, data-driven pacing baselines.
3. **Ungrounded AI Generation Risks**: Introducing AI agents into operations without strict structural guardrails, static analysis, and deterministic scoring models leads to hallucinated API parameters, silent error masking, and unverified code changes.

The **PANTHEON AI Agent and Skills Setup Kit for Service Governance** resolves these operational bottlenecks by providing:
- **Five Specialized Multi-Agent Personas** (`AEGIS`, `ATLAS`, `SAGE`, `SENTINEL`, `SPARK`) that conduct continuous multi-perspective infrastructure hardening, architectural, service governance, security, and contrarian reviews.
- **Six Modular Governance & Best-Practice Skills** encapsulating rigorous mathematical models for ticket stagnancy, 5-tier age bucketing, intraday capacity pacing, dual-metric quality auditing, standup digest automation, and multi-platform infrastructure hardening (`PAN-OS`, `FortiOS`, `Junos`, `Windows Server`, `Linux Server`).
- **Two Standalone Master System Prompts (`SAGE_Agent_System_Prompt.md` & `AEGIS_Agent_System_Prompt.md`)**, including a ready-to-use **Copy-Paste Configuration Analysis Prompt** and an architectural blueprint for an **Automated Multi-Vendor API Config Ingestion Pipeline**.
- **A Living Project Handover Ledger (`GEMINI.md`)** that maintains persistent context, architectural boundaries, and metric status across asynchronous agent turns and developer sessions.
- **Software Engineering Hygiene from First Principles**: Strict secret isolation (`.env.template` + `.gitignore` + OS-level vaults), automated linting and static analysis (Ruff / Mypy / Pester), and pure mathematical calculation decoupling for offline fixture testing.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│        PANTHEON AI AGENT AND SKILLS SETUP KIT FOR SERVICE GOVERNANCE (`pantheon-ai-kit`)│
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ THE PANTHEON: 5 SPECIALIST MULTI-AGENT PERSONAS (.agents/agents/) ]                 │
│  ├── AEGIS (Infra Best-Practice: PAN-OS, FortiOS, Junos, Windows, Linux & UKFS-01..06) │
│  ├── ATLAS (Deep Modules, Seams & Parity)     ├── SENTINEL (Secrets, Redaction, GDPR) │
│  └── SAGE (ITIL 4/5 Governance & KPI Metrics) └── SPARK (Design-Tree Grilling & Kaizen)│
│                                                                                        │
│                                           │ Evaluates & Guides                         │
│                                           ▼                                            │
│  [ 6 MODULAR OPERATIONAL & INFRASTRUCTURE SKILLS (.agents/skills/) ]                   │
│  ├── infrastructure-best-practice-analyser  (NIST, NCSC/CE+, UKFS-01..06, Test Lib 1.1)│
│  ├── ticket-backlog-governance              (145-pt Rubric, 5-Tier Age Bands)          │
│  ├── productivity-workload-governance       (315m Pacing, 80% Utilization, Throughput) │
│  ├── quality-audit-governance               (Resolve Pass % + Granular QA Score)       │
│  ├── teams-standup-digest-notifier          (Top 5 Standup Cards, Multi-Day Badges)    │
│  └── support-team-governance-analytics-coaching (3-Step Evidence-Based Coaching)       │
│                                                                                        │
│                                           │ Drives & Governs                           │
│                                           ▼                                            │
│  [ DECOUPLED APPLICATION CORE & HYGIENE ]                                              │
│  ├── Pure Calculation Engines (Deterministic math, offline JSON fixture testing)       │
│  ├── I/O Integration Layer (Resilient ITSM/Vendor APIs, Graph API, fail-fast config)   │
│  └── Secret Isolation Barrier (.env blocked by .gitignore, Windows DPAPI SecretStore)  │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Grounding Frameworks & Standards Catalogue
Every scoring rubric, operational skill, and audit check in the **PANTHEON AI Agent and Skills Setup Kit for Service Governance** is anchored to established international service management, cybersecurity, and operational resilience frameworks:

| Domain Pillar | Grounding Frameworks & Standards | How PANTHEON AI Applies It |
| :--- | :--- | :--- |
| **Service Management & Operational Excellence** | **ITIL 4 & ITIL 5** *(Service Value System, Continual Improvement, Incident/Problem/Request/Change Management, AI-Native Value Streams & Digital Product/Service Governance)* | Grounds **`SAGE`** and the 5 operational governance skills: business-hours staleness (`8.5h`/`17.0h`), 5-tier age bucketing, 145-point backlog prioritisation, intraday capacity pacing (`315 min/day`), $\ge 10\%$ proactive problem allocation (`PRB`/`PTASK`), and dual-metric quality auditing (`Resolve Pass %` + `Granular Score %`). |
| **Network & Infrastructure Security Baselines** | **NIST SP 800-41 Rev. 1** *(Firewall Policy)*, **NIST SP 800-53 Rev. 5 Update 1** *(21 Controls: SC-7, AC-4, AC-6, AU-2, CM-2, CM-6, SI-2, etc.)*, **NIST CSF 2.0** *(Feb 2024)*, **NCSC Guidance & Cyber Essentials Plus Alignment** *(Boundary Firewalls, Secure Configuration, Access Control, Malware Protection, Security Update Management, 10 Steps)* | Grounds **`AEGIS`** and `infrastructure-best-practice-analyser` (`Test Library 1.1.0`) across **Palo Alto (`PAN-OS`)**, **FortiGate (`FortiOS`)**, **Juniper (`Junos`)**, **Windows Server**, and **Linux Server**. |
| **Operational Resilience & Regulatory Governance** | **UK Financial-Services Outcomes (`UKFS-01` to `UKFS-06`)** drawing on **FCA PS21/3**, **PRA PS6/21 & SS1/21** *(Impact Tolerances)*, and **PRA SS2/21** *(Third-Party Risk)*; optional **NCSC CAF (`B2`, `B4`, `C1`)** | Evaluates technology risk, change governance, third-party assurance, and impact tolerances for Important Business Services (`IBS`) without falsely claiming regulators prescribe specific firewall rules. |
| **Licensed Standards (Reference-ID Placeholders Only)** | **ISO/IEC 27001:2022 & 27002:2022** *(16 Annex A IDs)*, **CIS Benchmarks** *(3 topic placeholders)*, **PCI DSS 4.0.1 Req 1** *(1.2.2–1.4.2)*, **SWIFT CSCF** *(1.1, 2.3, 4.2, 6.4)* | Recorded strictly as reference numbers or topic placeholders until licensed copies are supplied and verified by an authorised engineer (zero copyrighted text reproduced). |
| **Agentic Software Engineering & Security Hygiene** | **Deep Modules & Clean Seams**, **Two-Axis Code Review**, **Tracer-Bullet Slicing**, **Zero-Trust Secret Isolation (DPAPI / `.env.template`)** | Grounds **`ATLAS`**, **`SENTINEL`**, and **`SPARK`** to enforce pure-function vs. I/O separation, offline JSON fixture parity (`Python` + `PowerShell 7.2+`), and mandatory `<REDACTED>` secret scrubbing. |

### 1.3 Target Audience: Enterprise IT, Service Operations, MSPs & Systems Engineers
This kit is tailored for **Enterprise IT Operations Teams, Service Delivery Leads, Managed Service Providers (MSPs), Senior Systems Engineers, and Infrastructure Architects**.

These professionals understand infrastructure, networking, firewalls, hypervisors, directory services (Entra ID / Active Directory), OAuth 2.0 authentication, REST APIs, and **ITIL 4 / ITIL 5** service management deeply, but may not be native full-time software programmers. Therefore, this kit explains software engineering conventions—such as virtual environments (`.venv`), code linters (Ruff), static typing (Mypy), and pure-function decoupling—from **first principles** using familiar infrastructure concepts (sandboxes, pre-flight validators, and idempotent automation).

### 1.4 Architectural Decision #1: Language Selection & Structure Before Prompting AI

> [!IMPORTANT]
> **Decide Your Runtime Language & Seam Structure Before Writing Code**
> Establishing your language boundary (`Python` vs. `PowerShell 7.2+`) and directory layout (`src/` pure logic vs. `Tests/fixtures/` offline tests) *before* prompting the AI prevents architectural drift and maximizes first-pass code accuracy. See **[Section 6.7 of `ANTIGRAVITY_SETUP_GUIDE.md`](ANTIGRAVITY_SETUP_GUIDE.md#67-language-selection-strategy-systems-scripting-powershell-vs-general-purpose-languages-python)** for the full deep dive.

| Operational Workload / Task | Recommended Language | Why This Choice Maximizes AI Accuracy & Reliability |
| :--- | :--- | :--- |
| **Data Analysis, KPI Math & Config Evaluators** | **Python (Primary)** | Highest LLM first-pass code accuracy; clean `datetime`/float math; sub-second AST linting (`Ruff`/`Mypy`). |
| **REST / XML / NETCONF API Ingestion** | **Python (Primary)** | Persistent TCP connection pooling (`requests.Session`), explicit retry/backoff control, strict JSON typing. |
| **Web Dashboards, API Proxies & Containers** | **Python (`FastAPI`)** | Native async web servers, strict Basic Auth middleware, and Linux Docker container portability. |
| **Portable Zero-Install CLI Utilities (`.exe`)** | **Python (`PyInstaller`)** | Compiles script + Python interpreter + libraries into a single standalone `.exe` for colleagues. |
| **Windows DPAPI SecretStore, AD & M365 Cmdlets** | **PowerShell 7.2+ (`pwsh`)** | Direct access to Windows DPAPI vaults (`Get-Secret`), Active Directory, WinRM, and M365 modules. |
| **Host Bootstrap & Task Scheduler Wrappers** | **PowerShell 7.2+ (`pwsh`)** | Native Windows OS service control, Task Scheduler registration, and WMI/CIM inspection. |

### 1.5 Skills vs. Agents: Packaged Expertise vs. Autonomous Execution

| Dimension | **Skill (`.agents/skills/<name>/SKILL.md`)** | **Specialist Agent (`.agents/agents/<name>/agent.md`)** | **System Prompt (`Governance_Framework/*.md`)** |
| :--- | :--- | :--- | :--- |
| **What It Is** | **Packaged Expertise & Guidance**: Stateless SOPs, mathematical formulas, and standards catalogues (*"How to do the work"*). | **Autonomous Execution & Persona**: Independent specialist worker with its own role and scoped tools (*"Who does the work"*). | **Portable Drop-In Prompt**: Copy-paste system prompt and template for interactive chat analysis. |
| **Context Window** | Injected on demand into the **active** agent's context window when its YAML `description` pointer triggers. | Runs in an **isolated subagent thread (`invoke_subagent`)** so heavy file reading never pollutes your main session. | Pasted directly into chat alongside raw data (e.g., a redacted firewall or router config). |
| **When to Use** | Encoding repeatable KPI formulas, `Test Library 1.1.0` rules, or output card schemas. | Multi-file codebase exploration, parallel two-axis code/security reviews (`ATLAS` + `SENTINEL`), or design-tree grilling (`SPARK`). | Ad-hoc copy-paste config analysis (`AEGIS_Agent_System_Prompt.md`) or seeding a standalone assistant. |

---

## 2. Complete Directory Layout

The setup kit adheres strictly to Google Antigravity's native workspace customization discovery hierarchy. All 24 canonical files reside within the structure below:

```text
pantheon-ai-kit/
│
├── .agents/                                # Antigravity native customization root
│   ├── agents/                             # Specialist Advisory Subagents (Isolated Context Layer)
│   │   ├── aegis_best_practice/
│   │   │   └── agent.md                    # AEGIS: Multi-platform best-practice & standards analyser
│   │   ├── atlas_architecture/
│   │   │   └── agent.md                    # ATLAS: Deep modules, clean seams, two-axis review & parity
│   │   ├── sage_governance/
│   │   │   └── agent.md                    # SAGE: Service delivery governance & metric baselines
│   │   ├── sentinel_security/
│   │   │   └── agent.md                    # SENTINEL: Secret hygiene, <REDACTED> scrubbing & guardrails
│   │   └── spark_disruptor/
│   │       └── agent.md                    # SPARK: Design-tree grilling, tracer bullets & Kaizen
│   │
│   ├── skills/                             # Modular Governance Workflows (On-Demand Activation)
│   │   ├── infrastructure-best-practice-analyser/
│   │   │   └── SKILL.md                    # PAN-OS, FortiOS, Junos, Windows & Linux standards catalogue
│   │   ├── ticket-backlog-governance/
│   │   │   └── SKILL.md                    # Queue stagnancy, 5-tier age bands, 145-pt priority rubric
│   │   ├── productivity-workload-governance/
│   │   │   └── SKILL.md                    # 315m pacing, 80% utilization ceiling, closed throughput
│   │   ├── quality-audit-governance/
│   │   │   └── SKILL.md                    # Dual-metric quality (Resolve Pass % + Granular QA score)
│   │   ├── teams-standup-digest-notifier/
│   │   │   └── SKILL.md                    # Per-squad Top 5 digest, multi-day badges, theme-safe HTML
│   │   └── support-team-governance-analytics-coaching/
│   │       └── SKILL.md                    # 3-step evidence-based coaching workflow & recovery plans
│   │
│   └── rules/                              # Directory-scoped always-on rules
│       └── sage-governance-prompt.md       # Workspace governance rule enforcing SAGE principles
│
├── Governance_Framework/                   # Standalone governance & infrastructure system prompts
│   ├── SAGE_Agent_System_Prompt.md         # Master system prompt for S.A.G.E. operational assistant
│   └── AEGIS_Agent_System_Prompt.md        # Copy-paste config analysis prompt & API ingestion blueprint
│
├── GEMINI.md                               # Root workspace handover, session state & runbook ledger
├── .env.template                           # Committed configuration schema contract (zero secrets)
├── .gitignore                              # Git exclusion rules isolating secrets, PII, and venvs
├── ANTIGRAVITY_SETUP_GUIDE.md              # First-principles developer hygiene & onboarding guide
├── ANTIGRAVITY_DOCS.html                   # Standalone, zero-server offline HTML5 Local Docs portal
├── README.md                               # Quickstart index, architecture & operational roster (this file)
├── setup.py                                # Cross-platform Python bootstrapper & language selection advisor
├── build_docs.py                           # Zero-dependency compiler regenerating ANTIGRAVITY_DOCS.html
├── validate_kit.py                         # Standalone Python 3.10+ automated kit validator
└── validate_and_install.ps1                # Native PowerShell validator & workspace installer
```

### Component Roles in the Antigravity Discovery Hierarchy:
- **`.agents/agents/<name>/agent.md`**: Custom advisory agents discovered automatically by Antigravity. Configured with `hidden: true` and `inheritCustomizations: false` to ensure focused, unpolluted domain analysis when invoked via inter-agent messaging or orchestrator delegation.
- **`.agents/skills/<name>/SKILL.md`**: Progressive disclosure workflows. The model only loads the YAML frontmatter (`name`, `description`) into its initial prompt index, fetching the full body instructions only when relevant triggers or user slash commands are received.
- **`.agents/rules/` and `GEMINI.md`**: Always-on workspace context. `GEMINI.md` provides persistent handover across turns while staying within Antigravity's **24 KB per-file limit** and **20,000-token rules budget**.
- **`Governance_Framework/SAGE_Agent_System_Prompt.md` & `AEGIS_Agent_System_Prompt.md`**: Master system prompts defining `SAGE` (ITSM governance) and `AEGIS` (copy-paste configuration analysis for Palo Alto, FortiGate, Juniper, Windows, and Linux, plus an untested future project blueprint for automated API configuration ingestion).
- **`ANTIGRAVITY_DOCS.html` & `build_docs.py`**: A self-contained, zero-dependency HTML5 Local Docs portal that compiles all 17 kit documents into an interactive browser portal (with full-text search, dark/light mode, copyable code blocks, and scroll-spy TOC) that opens directly over `file://` without an HTTP server or internet connection. Re-run `python build_docs.py` anytime you edit a Markdown file to recompile the docs.
- **`setup.py`**: Cross-platform Python bootstrapper that checks host runtimes, displays the Systems Scripting (PowerShell) vs. General-Purpose (Python) recommendation matrix, provisions `.venv` / `.env` when requested, rebuilds `ANTIGRAVITY_DOCS.html`, and runs `validate_kit.py`.

---

## 3. Multi-Agent Advisory Roster Table

The kit includes five specialized advisory subagents that evaluate code, infrastructure, workflows, and operational metrics from complementary technical perspectives:

| Agent Identifier | Display Title & Acronym | Core Operational Pillar & Mandate | Tool Permissions | Example Invocations & Activation Prompts |
| :--- | :--- | :--- | :--- | :--- |
| **`aegis_best_practice`** | **AEGIS**<br>*(Architecture, Estate Governance & Infrastructure Standards Analyser)* | **Multi-Platform Best-Practice & Standards Auditing**<br>Evaluates Palo Alto (PAN-OS) & FortiGate (FortiOS) firewalls, Juniper (Junos) routers, and Windows & Linux servers against public NIST (800-41, 800-53, CSF 2.0), NCSC, vendor hardening docs, and UK financial-services outcomes (`UKFS-01` to `UKFS-06`), while preserving strict reference-only placeholders for ISO 27001, CIS Benchmarks, PCI DSS, and SWIFT CSCF. | Read-only inspection tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`, `read_url_content`, `search_web`, `send_message`, `schedule`, `generate_image`). | • `"Ask Aegis to audit this FortiGate / Palo Alto config against NIST 800-41 and UKFS outcomes."`<br>• `"Have Aegis review our Juniper lo0 filter and Linux sshd_config hardening."`<br>• `"Request Aegis run a best-practice assessment with PCI DSS and NCSC CAF overlays switched on."` |
| **`atlas_architecture`** | **ATLAS**<br>*(Architecture & Technology Lead for Application Scalability)* | **Systems Modularity & Technical Debt**<br>Audits codebase modularity, coupling, dual-runtime parity (Python vs. PowerShell), pure vs. I/O separation, API client resilience (retries, backoff, timeouts), and container readiness. | Read-only inspection tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`, `read_url_content`, `search_web`, `send_message`, `schedule`, `generate_image`). Direct write tools disabled. | • `"Ask Atlas to review our ingestion client for timeout handling and connection reuse."`<br>• `"Have Atlas audit our pure calculation functions for side-effect isolation."`<br>• `"Request Atlas evaluate the maintenance overhead of our dual Python/PowerShell scripts."` |
| **`sage_governance`** | **SAGE**<br>*(Service Analytics & Governance Expert)* | **ITILv4 Delivery & Metric Integrity**<br>Audits operational thresholds: 315m daily time pacing, 2 closed tasks/day throughput, 80% capacity ceiling, 10% proactive work allocation, 5-tier age distribution, 145-pt priority scoring, and dual-metric quality scorecards. Enforces non-accusatory, evidence-based reporting in British English. | Read-only inspection tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`, `read_url_content`, `search_web`, `send_message`, `schedule`, `generate_image`). | • `"Have Sage audit the latest weekly engineer time pacing report."`<br>• `"Ask Sage to verify whether our backlog stagnancy calculations align with ITILv4 standards."`<br>• `"Request Sage draft an evidence-based coaching outline for an engineer with low recorded hours."` |
| **`sentinel_security`** | **SENTINEL**<br>*(Security Enforcement, Network Trust & Integrity Evaluation Lead)* | **Zero Trust, Secret Safety & GDPR Compliance**<br>Audits secret isolation (`.env` vs `.gitignore` vs Windows SecretStore), fail-fast configuration checks, API Basic Auth, OAuth 2.0 token acquisition, ITSM table/field-level ACLs, and customer journal PII protection under GDPR. | Read-only inspection tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`, `read_url_content`, `search_web`, `send_message`, `schedule`, `generate_image`). | • `"Ask Sentinel to scan the workspace for exposed secrets or hardcoded tenant IDs."`<br>• `"Have Sentinel audit our API client's credential retrieval and fallback logic."`<br>• `"Request Sentinel review our ticket summary export routines for customer PII hygiene."` |
| **`spark_disruptor`** | **SPARK**<br>*(Strategic Pivot, Assumption-challenging & Radical Kaizen)* | **Contrarian Kaizen & Radical Simplification**<br>Challenges operational dogmas, timesheet gaming under Goodhart's Law, polling loops vs. event-driven webhooks, bureaucratic review overhead, and bloated code. Identifies the 30% of legacy processes that should be eliminated immediately. | Read-only inspection tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`, `read_url_content`, `search_web`, `send_message`, `schedule`, `generate_image`). | • `"Ask Spark to critique our 315-minute daily time pacing metric for perverse incentives."`<br>• `"Have Spark identify legacy scripts or vanity reports we can safely delete."`<br>• `"Request Spark propose an event-driven alternative to our scheduled batch polling scripts."` |

---

## 4. Governance Skills Catalog Table

The six governance and best-practice skills encapsulate the analytical formulas, threshold models, infrastructure standards catalogues, and operational runbooks of modern service management. They are automatically discovered by Antigravity and loaded on demand:

| Skill Directory & Name | Operational Scope & Deliverables | Core Mathematical Formulas & Thresholds | Antigravity Activation Triggers |
| :--- | :--- | :--- | :--- |
| **`infrastructure-best-practice-analyser`** | Multi-platform configuration & rule-base assessment across Palo Alto (`PAN-OS`), FortiGate (`FortiOS`), Juniper (`Junos`), Windows Server, and Linux Server (`Test Library 1.1.0`). | • **Public Standards**: NIST SP 800-41 Rev. 1, NIST SP 800-53 Rev. 5 (21 controls), NIST CSF 2.0 (11 subcategories), NCSC Guidance, Vendor Hardening Docs.<br>• **UK Financial Services**: `UKFS-01` to `UKFS-06` (FCA PS21/3, PRA PS6/21, SS1/21, SS2/21).<br>• **Licensed Placeholders**: ISO 27001/27002 (16 Annex A IDs only), CIS Benchmarks (`policy`/`admin`/`system` placeholders), PCI DSS (`1.2.2–1.4.2`), SWIFT (`1.1, 2.3, 4.2, 6.4`). | • `"Run an infrastructure best-practice assessment on this firewall/router/server config."`<br>• `/infrastructure-best-practice-analyser` |
| **`ticket-backlog-governance`** | Evaluates active ITSM ticket backlogs, queue aging, and stagnation. Categorizes actionable task classes (`incident`, `sc_req_item`, `problem`, `problem_task`, `change_task`). | • **Business Hours Staleness**: $\ge 8.5\text{h}$ (Incident), $\ge 17.0\text{h}$ (Request) within Mon–Fri 09:00–17:30.<br>• **5-Tier Age Bucketing**: `<5d`, `5–15d`, `15–30d`, `30–60d`, `>60d`.<br>• **145-Point Priority Score**: Status (max 50) + Review Age (max 40) + Update Stagnancy (max 35) + Age Band (max 20).<br>• **Future Date Override**: `Pending` state with future `'Date Required'` = **`HEALTHY`**. | • `"Analyze the current ticket backlog export for stagnant tickets."`<br>• `"Run backlog prioritization scoring on our queue."`<br>• `/ticket-backlog-governance` |
| **`productivity-workload-governance`** | Analyzes engineer daily time pacing, closed task throughput, capacity utilization, proactive work allocation, and timesheet capture anomalies. | • **Daily Time Worked Target**: 315 minutes (5h 15m / 5.25h), representing 70% direct logging of a 37.5h workweek.<br>• **Intraday Pacing**: $\text{Target} = 315 \times (\text{Elapsed Mins} / 480)$.<br>• **Cumulative Day Weights**: Mon 15%, Tue 38%, Wed 62%, Thu 85%, Fri 100%.<br>• **Operational Capacity Ceiling**: 80% Utilization (30.0h/week).<br>• **Closed Throughput**: 2 closed tasks/day (~10/week organic).<br>• **Proactive Ratio**: $\ge 10\%$ on Problem/Story work. | • `"Audit engineer time worked pacing for this week."`<br>• `"Check timesheet entries for low bookings or bulk end-of-week logging anomalies."`<br>• `/productivity-workload-governance` |
| **`quality-audit-governance`** | Enforces ticket documentation quality, SLA compliance, customer communication depth, and automated rubric scoring. | • **Dual-Metric Standard**: Always reports `Pass Rate % (Granular Score %)`. Example: `95.0% (92.3%)`.<br>• **Primary Metric (`Resolve Pass %`)**: Strict binary compliance (Pass/Fail) driving RAG status.<br>• **Secondary Metric (`Granular Quality %`)**: Multi-point technical rubric (Incident max 19.0 pts, Request max 20.0 pts).<br>• **Status Bandings**: `HEALTHY`, `AT RISK`, `PROGRESSION STALLED`, `FAILING`, `CRITICAL`. | • `"Evaluate ticket QA scorecards against the dual-metric standard."`<br>• `"Audit ticket closure notes and customer communication logs."`<br>• `/quality-audit-governance` |
| **`teams-standup-digest-notifier`** | Formats and delivers daily morning standup digests via Microsoft Teams webhooks or Power Automate flows. | • **Filtering Pipeline**: Records reviewed today with status in `[CRITICAL, FAILING, PROGRESSION STALLED, AT RISK]`.<br>• **Squad Capping**: Strictly capped at **Top 5 tickets maximum per assignment squad**.<br>• **Multi-Day Badge**: Appends `🔥 Multi-Day` if `Days_Since_Meaningful_Update >= 3`.<br>• **Theme-Safe HTML**: High-contrast text over soft color-coded backgrounds legible in both Dark and Light Teams themes. | • `"Generate today's morning standup digest for engineering squads."`<br>• `"Prepare the Teams notification card for our backlog standup."`<br>• `/teams-standup-digest-notifier` |
| **`support-team-governance-analytics-coaching`** | Translates quantitative metrics into non-accusatory, constructive 1-on-1 performance coaching workflows and operational recovery plans. | • **Step 1: Direct Evidence Extraction**: Objective timestamps and system-of-record metrics without blame or adjectives.<br>• **Step 2: Operational Impact & Pattern Diagnosis**: Linking recording habits (e.g., end-of-week batch logging) to team capacity distortions.<br>• **Step 3: Constructive Alignment & Recovery Action**: Actionable forward-looking habits (daily incremental capture, timer tools). | • `"Draft a 1-on-1 coaching talking points outline for an engineer pacing below 50%."`<br>• `"Provide constructive feedback on ticket journal documentation habits."`<br>• `/support-team-governance-analytics-coaching` |

---

## 5. Quickstart Bootstrap Workflow

You do **not** need to clone or manually download the GitHub repository beforehand. A single PowerShell command (`irm ... | iex`) automatically downloads `validate_and_install.ps1`, `setup.py`, and all 24 canonical kit components into your target workspace, initializes `.env`, offers the optional custom keyword leak scanner builder, and validates all compliance checks:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             5-STEP QUICKSTART BOOTSTRAP WORKFLOW                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   STEP 1: Zero-Clone Single-Command Bootstrap (Downloads & Runs Kit Automatically)      │
│           irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex │
│                                           │                                             │
│                                           ▼                                             │
│   STEP 2: Instantiate Local Environment Configuration                                   │
│           Created automatically (.env from .env.template — populate tenant/API keys)    │
│                                           │                                             │
│                                           ▼                                             │
│   STEP 3: Optional Custom Keyword Scanner & Pre-Flight Validation                       │
│           Enter comma-separated keywords (or press Enter to skip/finish) & validate     │
│                                           │                                             │
│                                           ▼                                             │
│   STEP 4: Launch Project Workspace in Google Antigravity                                │
│           Verify discovery of 5 advisory agents, 6 skills, and GEMINI.md                │
│                                           │                                             │
│                                           ▼                                             │
│   STEP 5: Initiate Multi-Agent Collaboration & Governance Auditing                      │
│           Invoke AEGIS, ATLAS, SAGE, SENTINEL, or SPARK via prompt or slash command     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Zero-Clone Single-Command Bootstrap (`irm | iex`)
Open PowerShell (`pwsh` 7.2+ recommended, or Windows PowerShell 5.1) in your target project directory and run a single command—no `git clone` or manual ZIP download required:
```powershell
# Option A (Recommended — Zero-Clone One-Liner): Download all 24 kit files (validate_and_install.ps1, setup.py, agents, skills, docs) into the current directory & run setup:
mkdir C:\Workspaces\ServiceDeliveryOps; cd C:\Workspaces\ServiceDeliveryOps
irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex

# Option B (Zero-Clone One-Liner into a Specific Target Folder):
$env:PANTHEON_TARGET_DIR = "C:\Workspaces\ServiceDeliveryOps"; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex

# Option C (If you already cloned or downloaded the repo locally):
pwsh -NoProfile -File .\validate_and_install.ps1 -Install -TargetWorkspace "C:\Workspaces\ServiceDeliveryOps"
```

### Step 2: Configure Environment Secrets (`.env`)
The bootstrapper automatically copies `.env.template` to `.env` if `.env` does not exist yet (or you can run `Copy-Item .env.template .env` manually). Open `.env` in your text editor and configure the necessary parameters:
```ini
# ITSM Configuration
INSTANCE_URL=https://your-instance.service-now.com
SN_DEPARTMENT_SYS_ID=your_department_guid

# Microsoft Graph / SharePoint Integration
SHAREPOINT_TENANT_ID=00000000-0000-0000-0000-000000000000
SHAREPOINT_SITE_PATH=yourtenant.sharepoint.com:/sites/ServiceOperations

# Webhook Notifications
TEAMS_DIGEST_WEBHOOK=https://your-webhook-endpoint-url
```
*(See `.env.template` for the full annotated list of 18 configuration parameters).*

### Step 2.5 (Optional & Skippable): Configure a Custom Organization Keyword Leak Scanner (`$EncodedRules` / `.custom_blocklist.json`)
To guarantee that **zero reversible organization-specific text** exists in the upstream repository, [`validate_kit.py`](validate_kit.py) and [`validate_and_install.ps1`](validate_and_install.ps1) ship only with **generic credential/key regex rules** (`PEM Private Keys`, `GitHub PATs`, `AWS Access Key IDs`, `Slack API Tokens`, `Hardcoded OAuth Client Secrets`).

During setup, you can optionally opt in to build a **local library of custom organization keywords, domains, colleague names, or resource IDs** (`$EncodedRules` stored in `.custom_blocklist.json`):
- **Single or Comma-Separated Input**: Enter a single keyword (`AcmeCorp`) or multiple comma-separated keywords on one line (`AcmeCorp, acme.internal, ProjectX`), or use `Label::Regex` (`AcmeDomain::\bacme\.internal\b`) for custom regexes.
- **Easy Exit with `[Enter]`**: After entering your keyword(s), press **`[Enter]`** at `Add more keywords? [y/N - Press Enter to finish & save]` (or press `[Enter]` on an empty prompt / type `done`) to immediately save `.custom_blocklist.json` and finish.
- **How it works**: Each keyword and regex pattern you enter is **Reversed UTF-8 + Base64 encoded** (`NameB64` and `PatB64`) and saved to `.custom_blocklist.json` so naive `grep` searches never self-trigger on the rule file.
- **Automatic `.gitignore` Protection**: Whenever you opt in, `setup.py` and `validate_and_install.ps1` automatically ensure `.custom_blocklist.json` is listed in `.gitignore` so your organization's custom keywords are **never** committed upstream.
- **Skippable at any time**: Press `Enter` or `N` during interactive setup (or pass `--skip-custom-scanner` / `-SkipCustomScanner`) to skip this step.

```powershell
# Option A: Interactive custom keyword scanner builder via Python setup.py
python setup.py --configure-scanner

# Option B: Append custom keywords non-interactively via CLI (supports comma-separated or Label::CustomRegex)
python setup.py --add-scanner-keyword "AcmeCorp, acme.internal" --add-scanner-keyword "AcmeDomain::\bacme\.internal\b"

# Option C: Interactive custom keyword scanner builder via PowerShell
pwsh -NoProfile -File .\validate_and_install.ps1 -ConfigureCustomScanner
```

### Step 3: Run Automated Pre-Flight Validation
When you run `irm ... | iex`, pre-flight validation runs automatically. You can also re-run validation at any time to verify that all files, YAML frontmatters, generic secret patterns, and any optional local `.custom_blocklist.json` rules are 100% compliant:

```powershell
# Method 1: Using Python 3.10+ (Standard Library only - zero pip dependencies required)
python validate_kit.py

# Method 2: Using native PowerShell (5.1 or 7+)
pwsh -NoProfile -File .\validate_and_install.ps1 -ValidateOnly
```

**Expected Successful Output (Exit Code 0):**
```text
======================================================================
  PANTHEON AI SETUP KIT — AUTOMATED VALIDATOR                        
======================================================================
Target Directory: C:\Workspaces\ServiceDeliveryOps

[STAGE 1/4] Validating directory structure, file existence, and byte limits...
  [PASS] All 24 canonical files exist and GEMINI.md is within 24,000 byte limit.
[STAGE 2/4] Verifying agent and skill YAML frontmatter schemas...
  [PASS] All agent and skill YAML frontmatters and instruction bodies are valid.
[STAGE 3/4] Scanning for live credentials and custom blocklist leaks (5 built-in secret rules + 0 local custom rule(s))...
  [PASS] Zero credential or blocklisted strings detected across all kit files.
[STAGE 4/4] Checking configuration templates and .gitignore hygiene...
  [PASS] Configuration templates and .gitignore filters are fully compliant.

======================================================================
ALL VALIDATION CHECKS PASSED SUCCESSFULLY! (Exit Code 0)
Status: OK — The kit is clean, fully de-identified, and structurally valid.
======================================================================
```

### Step 4: Open Workspace in Google Antigravity
Open the workspace directory in Google Antigravity. Antigravity automatically traverses the filesystem from CWD up to the workspace root and discovers:
- The living session state ledger: `GEMINI.md`
- The 5 specialist advisory agents in `.agents/agents/`
- The 6 governance skills in `.agents/skills/`
- The workspace governance rule in `.agents/rules/sage-governance-prompt.md`

### Step 5: Invoke Multi-Agent Collaboration
Interact directly with the multi-agent advisory team using natural language prompts or slash commands in the Antigravity chat window:

```text
# 1. Architectural Review
"Ask ATLAS to analyze our API client module for retry limits and connection pooling."

# 2. Operational Backlog Audit
"Ask SAGE to analyze our active ticket export and extract the Top 5 standup priorities."

# 3. Security & Secret Verification
"Have SENTINEL audit our workspace configuration to verify that no credentials can leak to Git."

# 4. Strategic Kaizen Challenge
"Ask SPARK to challenge our daily 315-minute time worked target and suggest modern alternatives."

# 5. Infrastructure Configuration Assessment
"Ask AEGIS to audit this firewall/router configuration against NIST 800-41 and UKFS-01..06."

# 6. Direct Governance Skill Execution
"/ticket-backlog-governance"
"/productivity-workload-governance"
"/infrastructure-best-practice-analyser"
```

### Step 6: Workspace Decommissioning & Surgical Uninstallation
If you provisioned starter kit files into an existing project workspace and later need to decommission or revert them, both Python and PowerShell provide non-destructive, surgical uninstallation:

```powershell
# Python Uninstallation:
# 1. Preview deletion plan without removing any files (Dry Run)
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" --dry-run

# 2. Execute uninstallation (removes canonical files & empty kit folders; preserves .env and user files)
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" -y

# 3. Complete purge including .env, .custom_blocklist.json, and .venv
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" --purge-secrets --purge-venv -y

# PowerShell Uninstallation:
# 1. Preview deletion plan with -WhatIf or -DryRun
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -WhatIf

# 2. Execute surgical uninstallation
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -Force

# 3. Complete purge including secrets and virtual environment
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -PurgeSecrets -PurgeVenv -Force
```

---

## 6. Developer Hygiene & Verification Summary

For Systems Engineers and Technical Leaders managing automation code, adhering to four core software engineering disciplines ensures stability, prevents security breaches, and protects against AI-generated code regressions:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DEVELOPER HYGIENE & QUALITY GUARDRAILS                          │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  1. SECRET ISOLATION BARRIER                                                           │
│     • Secrets LIVE ONLY in local .env or Windows SecretStore (DPAPI encrypted).        │
│     • .env is PERMANENTLY BLOCKED by .gitignore (never committed to Git).             │
│     • .env.template provides the safe, committed schema (placeholder values only).     │
│     • Fail-fast startup checks (config.require()) terminate immediately on missing keys.│
│                                                                                        │
│  2. STATIC ANALYSIS & LINTING (Ruff / Mypy / Pester)                                  │
│     • Eliminates AI hallucinations: undeclared variables, missing imports, bare except│
│     • Enforces type contracts before code ever executes against enterprise APIs.       │
│     • Commands:  ruff check . --fix  |  ruff format .  |  mypy src/                   │
│                                                                                        │
│  3. VIRTUAL ENVIRONMENT ISOLATION (.venv)                                              │
│     • Hermetic execution sandbox preventing host OS library corruption.                │
│     • Creation:  python -m venv .venv                                                  │
│     • Activation: .\.venv\Scripts\Activate.ps1  or  source .venv/bin/activate          │
│                                                                                        │
│  4. PURE-FUNCTION DECOUPLING & OFFLINE TEST FIXTURES                                   │
│     • Mathematical algorithms strictly decoupled from network/API I/O.                 │
│     • 100% testable offline using language-neutral JSON test fixtures.                 │
│     • Python test runner:  python Tests/run_fixtures.py                                │
│     • PowerShell runner:   pwsh FlowRelayPS/Tests/Invoke-FixtureTests.ps1              │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.1 Secret Management from First Principles
- **The Permanent Danger of Git History**: Git is an append-only object store. The moment a commit containing an API key, password, or tenant ID is made, that secret is baked into `.git` forever. Even deleting the file in a subsequent commit leaves the credential exposed in `git log -p`.
- **The Three-Tier Defense**:
  1. `.gitignore` acts as the firewall, blocking `.env`, `*.credential`, and raw ticket dumps (`Data/*.csv`).
  2. `.env.template` acts as the public blueprint, defining all required keys with dummy placeholders.
  3. `.env` stays strictly on your local disk. In Windows enterprise environments, pair `.env` with **Windows SecretStore** (`Microsoft.PowerShell.SecretStore`), encrypting secrets at rest via Windows DPAPI.
- **Fail-Fast Initialization (`config.require()`)**: Never allow scripts to run for 30 minutes before crashing on a missing webhook URL. Applications must validate all required environment variables at import time and abort within 5 milliseconds if any key is missing.

### 6.2 Static Analysis & Linters in the AI Era
When collaborating with AI agents (LLMs), code is generated probabilistically. AI agents can easily hallucinate non-existent API parameters, introduce mutable default arguments (`def f(x=[])`), or mask critical network failures with silent `except Exception: pass` blocks.
- **Linters (Ruff)** inspect code syntax and logic *without running it*, catching bugs before execution.
- **Type Checkers (Mypy)** prove mathematically that functions receive and return the data types they expect, eliminating `TypeError: 'NoneType' object is not subscriptable` crashes.
- **Quick Reference Commands**:
  ```powershell
  # Check code for syntax, scoping, and logic defects
  ruff check .

  # Automatically fix safe linting errors and reorder imports
  ruff check . --fix

  # Format all code cleanly according to enterprise standards
  ruff format .

  # Run static type checking across core modules
  mypy src/
  ```

### 6.3 Environment Isolation (`.venv`)
Installing Python packages globally (`pip install ...`) alters the host operating system's system libraries. When two automation tools require conflicting library versions (e.g., `urllib3==1.26` vs `urllib3==2.1`), one tool breaks silently.
- Always create a dedicated project virtual environment: `python -m venv .venv`
- Activate it before installing packages: `.\.venv\Scripts\Activate.ps1`
- Think of `.venv` as a lightweight container sandbox that isolates your project's dependencies completely from the host operating system.

### 6.4 Pure vs. I/O Separation & Offline Fixture Testing
To ensure your governance calculations remain robust without requiring continuous access to live ITSM APIs or network connections:
- **Impure I/O Functions (`Public/` or runner scripts)** handle network requests, authentication tokens, and disk file writes.
- **Pure Functions (`Private/` or utility modules)** handle math, staleness calculations, SLA derivations, and scoring rubrics. Pure functions have **zero side effects** and produce the exact same output for the same input 100% of the time.
- **Shared JSON Fixtures**: By defining test cases in language-neutral JSON files (`business_hours.json`, `priority_score.json`), you can run automated verification offline on an airplane or disconnected laptop:
  ```powershell
  # Validate Python pure functions offline
  python Tests/run_fixtures.py

  # Validate PowerShell pure functions offline
  pwsh FlowRelayPS/Tests/Invoke-FixtureTests.ps1
  ```
  If both runners pass all fixture test cases, you have mathematical proof that your Python and PowerShell implementations will behave identically in production.

### 6.5 Planning, Token Efficiency & "Skills for Real Engineers" (`mattpocock/skills`)
To get the highest code quality and lowest token consumption from Antigravity agents, follow five core agentic engineering habits (adapted from [Matt Pocock's `Skills For Real Engineers`](https://github.com/mattpocock/skills) and detailed in **[Section 9 of `ANTIGRAVITY_SETUP_GUIDE.md`](ANTIGRAVITY_SETUP_GUIDE.md#9-ai-assisted-engineering-best-practices-planning-token-efficiency--skills-for-real-engineers)**):
1. **Grill the Design Tree Before Writing Code (`/grill-me` & `@spark_disruptor`)**: Map requirements as a design tree and resolve the **ready frontier** of prerequisite decisions (language, auth vault, output schema) in structured rounds before generating code.
2. **Cut Tracer-Bullet Vertical Slices (`to-tickets`)**: Implement features as narrow end-to-end slices (1 API field $\rightarrow$ 1 pure function $\rightarrow$ 1 JSON fixture $\rightarrow$ 1 CLI output) that fit in a single context window. Use **Expand–Contract** sequencing for wide refactors.
3. **Protect the Information Hierarchy & Context Load (`writing-for-agents`)**: Keep `GEMINI.md` strictly `< 24,000 bytes` as a high-signal index; push deep rubrics and `Test Library 1.1.0` tables behind sharp `"Use when..."` context pointers inside `.agents/skills/*/SKILL.md`.
4. **Isolate Noisy Exploration & Reviews in Subagents (`code-review` & `invoke_subagent`)**: Spawn `@atlas_architecture` (Standards/Fowler Smells vs. Spec Fidelity) and `@sentinel_security` (`<REDACTED>` scrubbing & least privilege) in parallel subagents so raw file reads never bloat your main chat.
5. **Default to Building the Check Over Writing the Rule (`retro` & `diagnosing-bugs`)**: Verify changes with `< 2s` deterministic CLI loops (`python validate_kit.py`, `python Tests/run_fixtures.py`, `ruff check .`) rather than asking the LLM to re-read files across multiple turns.

### 6.6 Workspace Lifecycle Symmetry & Surgical Decommissioning
Provisioning files into shared enterprise repositories requires equal rigor when decommissioning or rolling back changes:
1. **Three-Tier State Decomposition**:
   - **Tier 1 (Canonical Kit Files)**: Agents (`.agents/agents/*`), skills (`.agents/skills/*`), rules, and scripts (`setup.py`, `validate_kit.py`, etc.). Always safely removed during uninstallation.
   - **Tier 2 (Generated Caches & Output)**: `ANTIGRAVITY_DOCS.html`, `.venv/`, `__pycache__/`. Removed when requested (`--purge-venv` / `-PurgeVenv`).
   - **Tier 3 (User Secrets & Keyword Blocklists)**: `.env` (contains live enterprise tokens) and `.custom_blocklist.json`. **Preserved by default** to prevent accidental credential loss; deleted only when explicit flags (`--purge-secrets` / `-PurgeSecrets`) are supplied.
2. **Suicide Deletion Hazard & Source Repo Protection**:
   - Running `python setup.py --uninstall` or `pwsh validate_and_install.ps1 -Uninstall` directly inside the kit source clone will abort immediately (`Exit Code 1`) with an error message to prevent accidental repository self-destruction. Uninstallation requires either an external `--target-dir` / `-TargetWorkspaceDir` or an explicit `--force` override.
3. **Surgical Deletion vs. Recursive Purge**:
   - Uninstallation removes only the 24 canonical kit files and generated artifacts. It prunes parent directories (`.agents/agents/`, `.agents/skills/`, `.agents/`) **only if they become completely empty**, preserving any custom agents, tools, or configurations created by your engineers.
4. **Deterministic Dry-Run Verification**:
   - Both `python setup.py --uninstall --dry-run` and `pwsh validate_and_install.ps1 -Uninstall -WhatIf` output a detailed preview of all candidate files and directories without altering disk state.

---

## 7. Compliance, De-Identification & Licensing

### De-Identification Guarantee
This setup kit has been rigorously sanitized and generalized. It contains **zero** proprietary organization identifiers, private tenant GUIDs, internal employee names, or environment-specific URLs. All parameters are managed through configurable environment variables (`.env.template`) or generic role placeholders (`<ORGANIZATION_NAME>`, `<TEAM_NAME>`, `<ITSM_INSTANCE_URL>`).

Running `validate_kit.py` or `validate_and_install.ps1` executes an automated regex scan confirming 0 occurrences of blocklisted entities across all files.

### Support & Maintenance
Maintain this repository by keeping `GEMINI.md` updated as operational milestones are completed, adding new test cases to `Tests/fixtures/` whenever governance thresholds are adjusted, and ensuring that all code changes pass `ruff check .` before committing.
