# PANTHEON AI Agent and Skills Setup Kit for Service Governance — Antigravity Setup & Systems Engineering Hygiene Guide
## A Starter Kit for Building AI Agents and Skills for Multi-Agent AI Service Governance, Operational Excellence & Infrastructure Hardening

> **Project**: **PANTHEON AI Agent and Skills Setup Kit for Service Governance** ([`https://github.com/apswood/pantheon-ai-kit.git`](https://github.com/apswood/pantheon-ai-kit.git) — *Platform for AI-Native Technical Hygiene, Excellence & Operational Navigation*)  
> **Grounding Frameworks**: **ITIL 4 & ITIL 5**, **NIST SP 800-41 Rev. 1**, **NIST SP 800-53 Rev. 5**, **NIST CSF 2.0**, **NCSC Guidance & Cyber Essentials Plus Alignment**, and **UK Financial-Services Operational Resilience (`UKFS-01`–`UKFS-06`)**  
> **Target Audience**: Enterprise IT Operations, Service Delivery Teams, Managed Service Providers (MSPs), Senior Systems Engineers, and Infrastructure Architects.  
> **Runtime Environment**: Google Antigravity Workspaces (Python 3.10+ / PowerShell 7.2+).

---

## 1. Introduction & Persona Alignment

### 1.1 The Systems Engineer's Bridge to AI-Augmented Governance

In enterprise IT operations, service delivery teams, and Managed Service Providers (MSPs), modern IT service management (ITSM) does not suffer from a lack of data; it suffers from a lack of **continuous, automated synthesis**. Technical leadership teams manage hundreds of active incidents, problem tasks, service requests, device configurations, and customer communications across distributed ticketing systems, cloud tenants, and collaboration platforms. 

The **PANTHEON AI Agent and Skills Setup Kit for Service Governance** (`pantheon-ai-kit`) provides a battle-tested, modular setup kit that bridges enterprise systems engineering, multi-vendor infrastructure hardening, and **ITIL 4 & ITIL 5** service governance with **Google Antigravity's multi-agent runtime**. 

This guide is written specifically for **Senior Systems Engineers, Service Operations Leaders, and Technical Architects**. You already possess deep domain expertise in:
- Cloud, virtualization, and hybrid enterprise infrastructure (networking, firewalls, routing, DNS, directory services, compute, storage).
- Identity and access management (OAuth 2.0 Client Credentials, service principals, modern authentication, Windows DPAPI).
- **ITIL 4 & ITIL 5** operational frameworks (Service Value System, Incident, Problem, Change, Request fulfilment, SLAs/OLAs, CMDB hierarchies, AI-enabled value streams, and continual improvement).
- Enterprise scripting and automation (PowerShell, Bash, REST APIs, Microsoft Graph API, JSON payloads, CI/CD runners).

However, you may not be a full-time, native software developer who spends 40 hours a week immersed in software repository ergonomics. Conventions that software engineering teams take for granted—such as hermetic virtual environments (`.venv`), strict Git secret isolation (`.gitignore` + `.env.template`), static Abstract Syntax Tree (AST) linting, and pure-function decoupling—can appear pedantic or esoteric until their operational necessity is demonstrated.

### 1.2 Our Architectural Perspective: Infrastructure Metaphors

To eliminate unnecessary jargon, this guide maps core software development practices directly to familiar systems engineering concepts:

| Software Engineering Practice | Systems / Infrastructure Equivalent | Why It Matters Operationally |
| :--- | :--- | :--- |
| **Python Virtual Environment (`.venv`)** | Lightweight container namespace or `chroot` jail. | Isolates project package dependencies from the host OS; eliminates "dependency hell" and prevents OS package corruption. |
| **`.env.template` + `.gitignore`** | Infrastructure-as-Code parameter contract & secret exclusion policy. | Provides a public schema of required environment variables while mathematically preventing passwords and API keys from leaking into version control history. |
| **Fail-Fast Startup (`config.require()`)** | Pre-flight validation / bootstrap readiness probe. | Inspects environment prerequisites in under 5 milliseconds; halts execution before initiating network sockets or API transactions. |
| **OS Credential Vault (SecretStore)** | Windows DPAPI / Enterprise Key Management Service. | Encrypts secrets at rest on the local workstation, passing in-memory secure credentials without writing plaintext strings to disk. |
| **Static Code Linting (Ruff / Mypy)** | `terraform validate` / ARM-TTK / PSScriptAnalyzer. | Mathematically parses code syntax and variable scoping *without execution*; catches hallucinated LLM variables and syntax errors before they hit production APIs. |
| **Pure Functions vs. I/O Separation** | Idempotent, stateless scripts decoupled from transport agents. | Separates mathematical formulas (SLA calculation, priority scoring) from unreliable network calls (REST endpoints), enabling 100% offline unit testing. |

### 1.3 Architectural Decision #1: Language Selection & Structure Before Prompting AI

> [!IMPORTANT]
> **Establish Your Language & Folder Boundaries Before Writing Code**
> AI coding assistants generate dramatically higher-quality code when your runtime language, directory structure (`src/` vs. `Tests/fixtures/`), and pure-function vs. I/O seams are decided *before* your first implementation prompt. Use the quick matrix below at project kickoff, and see **[Section 6.7: Language Selection Strategy (PowerShell vs. Python)](#67-language-selection-strategy-systems-scripting-powershell-vs-general-purpose-languages-python)** for the full architectural deep dive.

| Operational Workload / Task | Recommended Language | Why This Choice Maximizes AI Accuracy & Reliability |
| :--- | :--- | :--- |
| **Data Analysis, KPI Math & Scoring Rubrics** | **Python (Primary)** | Highest LLM first-pass code accuracy; clean `datetime`/float math; sub-second AST linting (`Ruff`/`Mypy`). |
| **REST API Ingestion (ITSM, Graph, Firewalls)** | **Python (Primary)** | Persistent TCP connection pooling (`requests.Session`), explicit retry/backoff control, strict JSON typing. |
| **Web Dashboards, API Proxies & Containers** | **Python (`FastAPI`)** | Native async web servers, strict Basic Auth middleware, and Linux Docker container portability. |
| **Portable Zero-Install CLI Utilities (`.exe`)** | **Python (`PyInstaller`)** | Compiles script + Python interpreter + libraries into a single standalone `.exe` for colleagues. |
| **Windows DPAPI SecretStore, AD & M365 Cmdlets** | **PowerShell 7.2+ (`pwsh`)** | Direct access to Windows DPAPI vaults (`Get-Secret`), Active Directory, WinRM, and M365 modules. |
| **Host Bootstrap & Task Scheduler Wrappers** | **PowerShell 7.2+ (`pwsh`)** | Native Windows OS service control, Task Scheduler registration, and WMI/CIM inspection. |

*Polyglot Golden Rule*: Default to **Python** for analytical engines, API collectors, and cross-platform tools; use **PowerShell 7.2+** (never legacy Windows PowerShell 5.1) as a thin OS/credential/WinRM wrapper, exchanging data strictly via structured JSON files or environment variables.

### 1.4 Grounding Frameworks, Standards Catalogue & System Architecture

Every scoring rubric, operational skill, and audit check in the **PANTHEON AI Agent and Skills Setup Kit for Service Governance** is anchored to established international service management, cybersecurity, and operational resilience frameworks:

| Domain Pillar | Grounding Frameworks & Standards | How PANTHEON AI Applies It |
| :--- | :--- | :--- |
| **Service Management & Operational Excellence** | **ITIL 4 & ITIL 5** *(Service Value System, Continual Improvement, Incident/Problem/Request/Change Management, AI-Native Value Streams & Digital Product/Service Governance)* | Grounds **`SAGE`** and the 5 operational governance skills: business-hours staleness (`8.5h`/`17.0h`), 5-tier age bucketing, 145-point backlog prioritisation, intraday capacity pacing (`315 min/day`), $\ge 10\%$ proactive problem allocation (`PRB`/`PTASK`), and dual-metric quality auditing (`Resolve Pass %` + `Granular Score %`). |
| **Network & Infrastructure Security Baselines** | **NIST SP 800-41 Rev. 1** *(Firewall Policy)*, **NIST SP 800-53 Rev. 5 Update 1** *(21 Controls: SC-7, AC-4, AC-6, AU-2, CM-2, CM-6, SI-2, etc.)*, **NIST CSF 2.0** *(Feb 2024)*, **NCSC Guidance & Cyber Essentials Plus Alignment** *(Boundary Firewalls, Secure Configuration, Access Control, Malware Protection, Security Update Management, 10 Steps)* | Grounds **`AEGIS`** and `infrastructure-best-practice-analyser` (`Test Library 1.1.0`) across **Palo Alto (`PAN-OS`)**, **FortiGate (`FortiOS`)**, **Juniper (`Junos`)**, **Windows Server**, and **Linux Server**. |
| **Operational Resilience & Regulatory Governance** | **UK Financial-Services Outcomes (`UKFS-01` to `UKFS-06`)** drawing on **FCA PS21/3**, **PRA PS6/21 & SS1/21** *(Impact Tolerances)*, and **PRA SS2/21** *(Third-Party Risk)*; optional **NCSC CAF (`B2`, `B4`, `C1`)** | Evaluates technology risk, change governance, third-party assurance, and impact tolerances for Important Business Services (`IBS`) without falsely claiming regulators prescribe specific firewall rules. |
| **Licensed Standards (Reference-ID Placeholders Only)** | **ISO/IEC 27001:2022 & 27002:2022** *(16 Annex A IDs)*, **CIS Benchmarks** *(3 topic placeholders)*, **PCI DSS 4.0.1 Req 1** *(1.2.2–1.4.2)*, **SWIFT CSCF** *(1.1, 2.3, 4.2, 6.4)* | Recorded strictly as reference numbers or topic placeholders until licensed copies are supplied and verified by an authorised engineer (zero copyrighted text reproduced). |
| **Agentic Software Engineering & Security Hygiene** | **Deep Modules & Clean Seams**, **Two-Axis Code Review**, **Tracer-Bullet Slicing**, **Zero-Trust Secret Isolation (DPAPI / `.env.template`)** | Grounds **`ATLAS`**, **`SENTINEL`**, and **`SPARK`** to enforce pure-function vs. I/O separation, offline JSON fixture parity (`Python` + `PowerShell 7.2+`), and mandatory `<REDACTED>` secret scrubbing. |

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

---

## 2. Antigravity Customization Architecture & Progressive Disclosure

Google Antigravity is an AI-assisted development environment designed to pair human engineers with autonomous and semi-autonomous AI agents. Rather than treating an AI model as an external chatbot, Antigravity embeds AI agents directly into the workspace filesystem, granting them governed tool access to terminal commands, file manipulation, and project-specific instructions.

### 2.1 Workspace Customization Discovery Hierarchy

Antigravity uses a deterministic file-system discovery hierarchy to load workspace instructions, advisory personas, and operational skills. It automatically traverses the project root looking for standard directory markers:

```
<Workspace Root>/
├── .agents/
│   ├── agents/                                  # Specialist Advisory Personas (Isolated Subagents)
│   │   ├── aegis_best_practice/agent.md         # Multi-Platform Infra Best-Practice & Resilience Auditor
│   │   ├── atlas_architecture/agent.md          # Technical Architecture, Deep Modules & Scalability Advisor
│   │   ├── sage_governance/agent.md             # ITIL v4 & Service Excellence Auditor
│   │   ├── sentinel_security/agent.md           # Zero-Trust, Secrets, Redaction & Least-Privilege Auditor
│   │   └── spark_disruptor/agent.md             # Design-Tree Interviewer & Contrarian Innovator
│   ├── skills/                                  # On-Demand Procedural Runbooks & Standards Catalogues
│   │   ├── infrastructure-best-practice-analyser/SKILL.md # PAN-OS, FortiOS, Junos, Win/Linux Catalogue
│   │   ├── ticket-backlog-governance/SKILL.md   # Backlog scoring & SLA staleness engine
│   │   ├── productivity-workload-governance/    # Utilization pacing & time audit
│   │   ├── quality-audit-governance/            # Dual Resolve Pass & audit scoring
│   │   ├── teams-standup-digest-notifier/       # Webhook payload & card generation
│   │   └── support-team-governance-analytics... # Evidence-based coaching framework
│   └── rules/                                   # Always-on workspace rules
├── Governance_Framework/                        # Standalone System Prompts & Copy-Paste Templates
│   ├── SAGE_Agent_System_Prompt.md              # Master ITSM Governance System Prompt
│   └── AEGIS_Agent_System_Prompt.md             # Copy-Paste Infra Config Analyser & API Pipeline Blueprint
├── GEMINI.md                                    # Living project state & continuous context (< 24 KB)
├── .env.template                                # Committed environment variable schema
├── .gitignore                                   # Version control gatekeeper
└── pyproject.toml                               # Static analysis & linter configuration
```

### 2.2 The Mechanics of Customization Types

Antigravity distinguishes between three primary customization mechanisms:

#### 1. Rules (`GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`)
- **Nature**: Persistent, contextual guidelines that govern agent behavior across directories.
- **Scope & Hierarchy**: Directory-scoped. When an agent opens or modifies a file, it traverses from that file's folder up to the repository root, inheriting all rules discovered along the path.
- **Constraints**:
  - Standalone `GEMINI.md` files do not require YAML frontmatter and are **always active** for their directory scope.
  - **Per-File Cap**: Standard rule files are capped at **24 KB (24,000 bytes)**. Files exceeding this cap are truncated at line boundaries.
  - **Aggregate Rules Budget**: All always-on and global rules share a dedicated **20,000-token rules budget**. If the total token footprint of discovered rules exceeds this budget, Antigravity demotes the lowest-priority rules from full in-memory prompt text to file-path pointers that the agent must explicitly read on demand.

#### 2. Skills (`.agents/skills/<skill_name>/SKILL.md`)
- **Nature**: Modular, procedural runbooks, standards catalogues, and analytical recipes (e.g., how to calculate SLA business hours, how to score ticket priority, or how to audit FortiGate/Palo Alto/Junos/Windows/Linux configurations against NIST and UKFS standards).
- **Format**: Every skill must reside in its own folder and begin with a YAML frontmatter block containing `name` and `description` (written as a sharp **context pointer** that front-loads the capability and explicitly states `"Use when..."` trigger branches):
  ```yaml
  ---
  name: ticket-backlog-governance
  description: Evaluate ITSM ticket backlog stagnancy (8.5h Incident / 17.0h Request business hours), 5-tier age bands, and 145-point priority scores. Use when calculating staleness, scoring backlog queues, or extracting Top 5 priority tickets per squad.
  ---
  ```
- **Scope**: Loaded dynamically on demand when relevant to the task.

#### 3. Specialist Agents (`.agents/agents/<agent_name>/agent.md`)
- **Nature**: Autonomous advisory personas with distinct perspectives, isolated context windows, scoped tool permissions, and dedicated system prompts.
- **The 5 Specialist Advisory Personas**:
  - `AEGIS`: Audits Palo Alto (`PAN-OS`), FortiGate (`FortiOS`), Juniper (`Junos`), Windows Server, and Linux Server configurations against public NIST, NCSC, vendor hardening guides, and UK financial-services resilience outcomes (`UKFS-01` to `UKFS-06`).
  - `ATLAS`: Focuses on deep modules, clean test seams, data normalization, two-axis code reviews, and Python/PowerShell parity.
  - `SAGE`: Enforces ITIL v4 service governance, SLA adherence, and objective 3-step evidence-based coaching.
  - `SENTINEL`: Enforces zero-trust credential hygiene, `<REDACTED>` diagnostic scrubbing, DPAPI encryption, least privilege, and deterministic security checks.
  - `SPARK`: Interviews ("grills") plans across the design-tree frontier, slices specs into tracer-bullet tickets, and eliminates operational toil.

### 2.3 Loading Priority and Precedence Order

When customizations have conflicting instructions or identical names, Antigravity resolves them using a strict, five-tier precedence hierarchy:

```
[ HIGHEST PRIORITY ]
   │
   ├── 1. Workspace Project Customizations (Walking up from CWD to Repository Root .agents/)
   │
   ├── 2. Declared Workspace Configurations (Explicitly registered in skills.json / plugins.json)
   │
   ├── 3. Global User Discovery (~/.gemini/config/ on the local machine)
   │
   ├── 4. Built-in Customizations (Default system skills bundled with Antigravity)
   │
   └── 5. Global Declared Configurations (Global machine-level JSON configurations)
   │
[ LOWEST PRIORITY ]
```

This ensures that workspace-level governance rules committed by your team always supersede global defaults or built-in system behaviors.

### 2.4 Deep Dive: Progressive Disclosure vs. Context Window Degradation

A fundamental pitfall in AI-assisted engineering is **prompt bloating**. Large Language Models (LLMs) operate on a finite context window measured in tokens. While modern models accept large context windows, placing thousands of lines of documentation, runbooks, and scripts into the prompt on every turn leads to two severe operational failure modes:

1. **Context Window Exhaustion & Cost Escalation**: Every token injected into the prompt is re-processed on every single interaction, driving up latency and API compute cost.
2. **Attention Degradation (The "Lost in the Middle" Phenomenon)**: LLMs attend most strongly to the beginning and the very end of their context window. When hundreds of pages of instructions are injected simultaneously, the model suffers from instruction dilution—it hallucinates, overlooks critical safety constraints, and produces generic code.

#### How Progressive Disclosure Resolves Context Degradation

Antigravity solves this problem through **Progressive Disclosure**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        INITIAL AGENT PROMPT                            │
│  - System Core Instructions                                            │
│  - Workspace Living Context (GEMINI.md)                                │
│  - Available Skills Catalog (Context Pointers Only):                   │
│      * infrastructure-best-practice-analyser: "PAN-OS/FortiOS/Junos.." │
│      * ticket-backlog-governance: "Calculates SLA staleness & score"   │
│      * productivity-workload-gov: "Audits logged hours vs 70% target"  │
│      * quality-audit-governance:  "Evaluates binary Resolve Pass %"    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ User asks: "Prioritize the backlog"
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        PROGRESSIVE ACTIVATION                          │
│  1. Agent evaluates the available skills catalog.                      │
│  2. Agent matches prompt intent to 'ticket-backlog-governance'.        │
│  3. Antigravity dynamically loads ONLY that specific SKILL.md into     │
│     the working context for the duration of the task.                  │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Index-Only Registration**: At session startup, Antigravity does **not** read the full text of files in `.agents/skills/`. It reads *only* the YAML frontmatter (`name` and `description`).
2. **On-Demand Hydration**: Only when the engineer's prompt or the current task requires that skill does the agent hydrate the full instruction body into memory.
3. **Subdirectory Encapsulation**: Bulky reference manuals, schema tables, and helper scripts reside in subdirectories (`references/`, `scripts/`). The agent navigates to them only when explicitly required, preserving precious context tokens.

### 2.5 Skills vs. Agents: Packaged Expertise & Guidance vs. Autonomous Execution

A common question when designing an Antigravity workspace is: *"Should I package this capability as a **Skill (`SKILL.md`)** or as a **Specialist Agent (`agent.md`)**?"*

Understanding the architectural boundary between **Packaged Expertise (Skills)** and **Autonomous Execution (Agents)** is critical for both accuracy and token efficiency:

| Architectural Dimension | **Skill (`.agents/skills/<name>/SKILL.md`)** | **Specialist Agent (`.agents/agents/<name>/agent.md`)** | **System Prompt (`Governance_Framework/*.md`)** |
| :--- | :--- | :--- | :--- |
| **Core Purpose** | **Packaged Expertise & Guidance**: Standard operating procedures, mathematical formulas, and reference catalogues (*"How to perform a task"*). | **Autonomous Execution & Persona**: An independent specialist worker with its own role, perspective, and toolset (*"Who performs the work"*). | **Portable Drop-In Prompt**: Self-contained master prompt and copy-paste template for interactive chat or external LLM sessions. |
| **Execution Thread & Context Window** | **Shared Context**: Injected on demand into the *current* agent's conversation window. Has no independent thread or memory. | **Isolated Context (`invoke_subagent`)**: Runs in its own separate conversation thread. Intermediate file reads and searches never bloat the parent session. | **Manual / Root Context**: Pasted by the engineer into a fresh chat session along with raw input data (e.g., a firewall config). |
| **Tool Scope & Permissions** | Inherits whatever tools the calling agent already possesses. Cannot restrict or grant tools. | **Explicitly Scoped Tools**: Declares an exact allowlist of tools in YAML frontmatter (e.g., read-only audit tools with write/delete tools stripped). | N/A (Text prompt governing reasoning and output structure). |
| **Concurrency** | Sequential within the current agent's turn. | **Parallel Execution**: Multiple agents (`ATLAS` + `SENTINEL` + `AEGIS`) can be spawned concurrently via a single `invoke_subagent` call. | Single interactive chat session. |
| **When to Choose** | You want *any* agent (including the main coding assistant) to follow an exact mathematical rubric, standards table, or output template when a topic arises. | The task requires heavy multi-file exploration, an orthogonal/adversarial viewpoint (`SPARK`), or parallel two-axis code/security review without polluting the main chat. | An engineer wants to quickly paste a device config or CSV extract into chat for an immediate audit without spinning up multi-agent orchestration. |

#### User-Invoked vs. Model-Invoked Skills (`SKILL-MECHANICS`)
Within Skills themselves, there are two invocation patterns that trade **Context Load** (tokens spent on every turn) against **Cognitive Load** (requiring the human to remember and type a command):
1. **Model-Invoked Skills (All 6 Skills in This Kit)**:
   Include a sharp `description` in YAML frontmatter and omit `disable-model-invocation`. The `description` stays loaded as a permanent **context pointer** (~30–50 tokens per skill) so the agent autonomously fires the skill whenever you paste a FortiGate config or ask about ticket staleness—while still allowing you to mention the skill explicitly by name.
2. **User-Invoked Skills / Slash Workflows (`/grill-me`, `/plan`, `/compact`, or `disable-model-invocation: true`)**:
   Triggered *only* when the human engineer explicitly invokes them. Use user-invoked workflows for phase transitions (starting an architecture interview, cutting a spec into tickets, or running a session retrospective) where human agency decides *when* the workflow should run.

#### How Agent + Skill + System Prompt Pair Together (The `AEGIS` Triad)
To see how all three artifacts complement each other, look at how infrastructure best-practice auditing is packaged in this kit:
- **1. The Specialist Agent ([`.agents/agents/aegis_best_practice/agent.md`](.agents/agents/aegis_best_practice/agent.md))**: Defines the autonomous `AEGIS` auditor persona with read-only tools. You can spawn `AEGIS` in the background alongside `ATLAS` and `SENTINEL` to audit an entire directory of configurations without cluttering your main coding session.
- **2. The Companion Skill ([`.agents/skills/infrastructure-best-practice-analyser/SKILL.md`](.agents/skills/infrastructure-best-practice-analyser/SKILL.md))**: Holds the deep 22 KB `Test Library 1.1.0` reference catalogue (PAN-OS, FortiOS, Junos, Windows, Linux checks, NIST/NCSC/UKFS mappings, and ISO/CIS placeholder rules). It stays out of memory until an infrastructure audit is actually requested.
- **3. The Copy-Paste System Prompt & Pipeline Blueprint ([`Governance_Framework/AEGIS_Agent_System_Prompt.md`](Governance_Framework/AEGIS_Agent_System_Prompt.md))**: Gives engineers a ready-to-use copy-paste prompt template where they can drop a redacted config directly into chat, plus an architectural blueprint for building an automated multi-vendor API config ingestion pipeline in the future.

---

## 3. Secret Management from First Principles

### 3.1 The Production Failure Mode: The Append-Only Nature of Git

In traditional scripting, engineers often place configuration parameters and credentials directly at the head of a file:

```python
# FATAL ANTI-PATTERN: Hardcoded credentials
INSTANCE_URL = "https://<my-company>.service-now.com"
API_USERNAME = "svc_governance_automation"
API_PASSWORD = "Winter2026!SecureAuthPassword"
AZURE_TENANT_ID = "00000000-1111-2222-3333-444444444444"
```

#### Why Editing the File Does NOT Remove the Secret
Systems engineers unfamiliar with Git internal storage often believe that if they commit this file, realize the mistake, delete the password in a second commit, and push, the secret is gone. **This is fundamentally incorrect.**

Git is not a filesystem snapshot; it is an **append-only, cryptographic Directed Acyclic Graph (DAG) of content-addressable objects**:
- Every `git commit` creates an immutable tree object referencing immutable blob objects stored in `.git/objects/`.
- Even if a secret is removed in commit `B`, commit `A` still permanently contains the blob with the plain-text password.
- Anyone with read access to the repository (or any developer who clones it) can retrieve the plain-text password instantly using:
  ```bash
  git log -p -S "Winter2026!"
  git checkout <commit-A-hash>
  ```
- Public and private automated scrapers continuously monitor push events. Leaked API tokens and tenant credentials committed to repositories are harvested and compromised within 30 seconds of pushing.
- Purging a committed secret requires destructive history rewrites (`git filter-repo` or BFG Repo-Cleaner), invalidating all branch clones across the entire team, and triggering an emergency credential revocation drill.

### 3.2 The 3-Tier Secret Isolation Architecture

To make code 100% portable, secure, and shareable across teams without risking credential exposure, the starter kit enforces the **3-Tier Secret Isolation Pattern**:

```
[ Git Version Control Boundary ]
       │
       ├── .gitignore            ──> Strictly blocks local secret stores from entering Git
       ├── .env.template         ──> COMMITTED: Public schema defining all required keys
       └── Application Code      ──> COMMITTED: Reads environment variables via os.getenv()
       │
[ Local Workstation Boundary ]
       ├── .env                  ──> NEVER COMMITTED: Local instance with actual secrets
       └── Windows SecretStore   ──> ENCRYPTED: Hardware/OS-backed DPAPI credential vault
```

#### Layer 1: The Gatekeeper (`.gitignore`)
The `.gitignore` file instructs Git to permanently ignore local configuration files, private virtual environments, and temporary test artifacts. 

**Mandatory Rule**: `.gitignore` must be committed to the repository **before** any `.env` file is generated locally:

```gitignore
# ==============================================================================
# SECRETS & LOCAL ENVIRONMENT CONFIGURATION (NEVER COMMIT)
# ==============================================================================
.env
.env.local
.env.*.local
*.credential
*.secret
*.pfx
*.pem

# ==============================================================================
# PYTHON VIRTUAL ENVIRONMENTS & RUNTIME ARTIFACTS
# ==============================================================================
.venv/
venv/
ENV/
__pycache__/
*.py[cod]

# ==============================================================================
# LOCAL DATA & EXTRACT PAYLOADS
# ==============================================================================
Data/*.txt
Data/*.csv
Data/*.xlsx
!Data/.gitkeep
```

#### Layer 2: The Public Schema (`.env.template`)
The `.env.template` file is committed to Git. It contains **every environment variable key** the application expects, annotated with architectural comments and safe, generic placeholders. It must **never** contain live credentials:

```bash
# ==============================================================================
# SERVICENOW ITSM INTEGRATION
# ==============================================================================
# The base URL of the target ServiceNow instance (e.g. https://<your-instance>.service-now.com)
INSTANCE_URL=https://<your-instance>.service-now.com

# Optional production fallback URL for credential resolution in non-prod environments
SN_PROD_INSTANCE_URL=https://<your-prod-instance>.service-now.com

# Department sys_id used to filter backlog tickets
SN_DEPARTMENT_SYS_ID=<32_character_sys_id_here>

# ==============================================================================
# MICROSOFT GRAPH & SHAREPOINT LIST INTEGRATION
# ==============================================================================
# Azure Entra ID Tenant GUID
SHAREPOINT_TENANT_ID=<00000000-0000-0000-0000-000000000000>

# SharePoint site path in Microsoft Graph format: "<domain>.sharepoint.com:/sites/<sitename>"
SHAREPOINT_SITE_PATH=<domain>.sharepoint.com:/sites/<site_name>

# ==============================================================================
# NOTIFICATION WEBHOOKS
# ==============================================================================
# Microsoft Teams Incoming Webhook or Power Automate HTTP trigger URL
TEAMS_WEBHOOK_URL=https://<your-tenant>.webhook.office.com/...
```

#### Layer 3: The Local Instance (`.env`)
When an engineer sets up their local workspace, they run:
```powershell
Copy-Item .env.template .env
```
They populate `.env` with their workstation's development credentials. Because `.env` is listed in `.gitignore`, Git completely ignores it. Running `git status` will show the working tree clean, guaranteeing zero risk of credential leakage.

### 3.3 Fail-Fast Startup Validation (`config.require()`)

A notorious failure mode in enterprise automation scripts is **lazy parameter evaluation**:
1. An automation script starts executing.
2. It queries an ITSM API for 3,000 backlog records.
3. It performs 40 minutes of complex calculations, scoring algorithms, and database updates.
4. On line 450, it attempts to notify Microsoft Teams: `requests.post(os.getenv("TEAMS_WEBHOOK_URL"), json=payload)`.
5. Because the engineer forgot to set `TEAMS_WEBHOOK_URL` in their `.env`, `os.getenv` returns `None`.
6. The script crashes with `TypeError: Invalid URL None` or an unhandled exception.
7. **Result**: The batch run failed halfway through. Data is in a corrupted, partially synced state, and 40 minutes of compute time was wasted.

#### The Fail-Fast Pattern
In enterprise software, applications must **fail fast**: inspect all environmental prerequisites at application initialization (import time), before opening a network socket, touching a file, or consuming compute resources.

The starter kit implements this via a dedicated configuration module:

```python
# src/config.py
import os
import sys
from dotenv import load_dotenv

# Load local .env into process environment variables
load_dotenv(os.path.join(os.getcwd(), ".env"), override=False)

class ConfigError(RuntimeError):
    """Raised when a required environmental prerequisite is missing."""

def require(*env_keys: str) -> None:
    """
    Fail fast at startup if any required environment variable is missing or empty.
    
    Call this at module import time with the keys the calling script strictly requires.
    Terminates execution immediately with an actionable remediation message.
    """
    missing = [key for key in env_keys if not os.getenv(key)]
    if missing:
        raise ConfigError(
            f"\n[FATAL CONFIGURATION ERROR] Missing required environment variable(s):\n"
            f"  - {', '.join(missing)}\n\n"
            f"Remediation:\n"
            f"  1. Ensure a local '.env' file exists in your workspace root.\n"
            f"  2. Copy missing keys from '.env.template' and supply valid values.\n"
        )
```

#### How Scripts Declare Their Dependencies
When an automation script starts, it declares its requirements immediately:

```python
# BacklogIngestionRelay.py
from src.config import require, INSTANCE_URL, SN_DEPARTMENT_SYS_ID

# Halts immediately (<5ms) if either variable is absent
require("INSTANCE_URL", "SN_DEPARTMENT_SYS_ID")

def main():
    print(f"Connecting to ITSM instance: {INSTANCE_URL}")
    # Proceed with safe execution...
```

If an engineer executes this script without configuring `.env`, the script halts in 5 milliseconds with a clear error message, preventing data corruption and saving hours of troubleshooting.

### 3.4 OS-Level Key Vaults (Windows SecretStore & DPAPI)

While `.env` prevents Git leakage, `.env` files still store credentials in plain text on the local hard drive. If an engineer's laptop is compromised, or if a rogue process reads workspace files, those secrets are exposed.

In enterprise Windows environments, credentials should be stored in the **Windows SecretStore** via PowerShell's native `Microsoft.PowerShell.SecretManagement` and `Microsoft.PowerShell.SecretStore` modules.

#### How Windows SecretStore Works
- **DPAPI Encryption**: Secrets stored in the Windows SecretStore are encrypted at rest using the **Windows Data Protection API (DPAPI)**. DPAPI keys are tied to the logged-in Windows user's cryptographic security context (or enterprise TPM chip). No external master password is required, yet no other user account on the machine can decrypt the data.
- **In-Memory Credential Passing**:
  ```powershell
  # Save credential securely into OS-encrypted store
  $cred = Get-Credential
  Set-Secret -Name "itsm_prod_api" -Secret $cred
  ```
- When retrieved in PowerShell:
  ```powershell
  $sec = Get-Secret -Name "itsm_prod_api"
  # $sec is returned as an encrypted [System.Security.SecureString] or [PSCredential]
  # It never materializes as plaintext on disk or in command-line arguments.
  ```

#### Tiered Fallback Architecture in Hybrid Environments
The starter kit uses a **three-tier credential fallback strategy**:
1. **Container / CI Environment**: First inspects the local `.env` or process environment variables (`ITSM_USER`, `ITSM_PASSWORD`). This ensures headless Docker containers or Azure Container Apps authenticate without requiring a Windows GUI.
2. **Interactive Workstation**: If environment variables are absent, queries the local Windows SecretStore using PowerShell's `Get-Secret`.
3. **Dev-to-Prod Fallback**: If an engineer is pointed at a development instance (`INSTANCE_URL=https://<your-dev-instance>.service-now.com`) and dev credentials are not found in the vault, the engine gracefully falls back to production credentials, ensuring engineers can run test queries without duplicate account setup.

---

## 4. Code Linting & Static Analysis in the AI Era

### 4.1 The AI Pair-Programming Paradigm & Its Latent Risks

Large Language Models (including Google Antigravity) are extraordinary accelerators for technical engineering. They can generate complete PowerShell modules, Python data pipelines, and REST API clients in seconds.

However, an AI agent does **not** evaluate code through a compiler or interpreter. It generates code **probabilistically**—predicting the next most likely token based on its training distribution. In complex enterprise automation, this introduces subtle, latent bugs:

| LLM Defect Pattern | Concrete Manifestation | Production Impact |
| :--- | :--- | :--- |
| **Hallucinated Parameters** | `requests.get(url, retry_limit=3)` | Python's `requests` library does not take `retry_limit`. The script crashes at runtime with `TypeError: unexpected keyword argument`. |
| **Silent Exception Swallowing** | `except Exception: pass` or bare `except:` | Silently swallows network drops, DNS errors, and syntax bugs. The script reports "Completed Successfully" while processing zero records. |
| **Variable Scoping Errors** | Assigning a variable inside an `if` block, then referencing it in an `else` branch. | Crashes intermittently depending on data flow with `UnboundLocalError`. |
| **Mutable Default Arguments** | `def parse_tickets(records=[])` | The list object is created *once* at function definition. Calls persist state across multiple executions, cross-contaminating ticket batches. |
| **Type Mismatches** | Assuming an API property is always a string: `item['assigned_to'].lower()` | When an unassigned ticket arrives, `item['assigned_to']` is `None`. The script crashes with `AttributeError: 'NoneType' object has no attribute 'lower'`. |

### 4.2 What Linters, Formatters, and Static Checkers Actually Do

Systems engineers are thoroughly familiar with pre-flight configuration validators:
- `terraform validate` verifies syntax and variable types before provisioning cloud resources.
- `ansible-lint` checks playbooks for deprecated syntax and security risks.
- `Test-NetConnection` validates network routing before initiating data transfers.

**Static code analysis provides that exact pre-flight validation for your codebase.**

```
┌────────────────────────────────────────────────────────────┐
│                    SOURCE CODE (Python)                    │
└─────────────────────────────┬──────────────────────────────┘
                              │ Statically Parsed into
                              ▼
┌────────────────────────────────────────────────────────────┐
│              ABSTRACT SYNTAX TREE (AST Graph)              │
│  - Mathematical map of all variables, imports, and scopes  │
└─────────────────────────────┬──────────────────────────────┘
                              │ Validated by Rules Engines
                              ▼
┌────────────────────────────────────────────────────────────┐
│ 1. RUFF (Linter): Catches bugs, dead code, bare exceptions │
│ 2. RUFF (Formatter): Enforces standard layout & line wrap  │
│ 3. MYPY (Type Checker): Verifies type hint contracts       │
└────────────────────────────────────────────────────────────┘
```

1. **Linter (Ruff)**:
   Written in Rust, Ruff parses the Python Abstract Syntax Tree (AST) at over 100,000 lines of code per second. It checks for hundreds of logical bugs, unused variables, undefined symbols, insecure patterns, and bad practices **without executing the code**.
2. **Formatter (Ruff / Black standard)**:
   Deterministically adjusts spacing, line lengths, and quotation marks. It eliminates stylistic debates and guarantees clean Git diffs.
3. **Static Type Checker (Mypy)**:
   Examines type annotations (`def calculate_staleness(created: datetime) -> float:`) to prove mathematically that functions receive and return compatible data types, preventing `NoneType` runtime exceptions.

### 4.3 Workspace Configuration Blueprint (`pyproject.toml`)

The starter kit includes a production-tuned `pyproject.toml` file at the root. It configures Ruff and Mypy to enforce high software engineering standards without overwhelming the engineer with pedantic warnings:

```toml
[tool.ruff]
# Target modern Python runtime
target-version = "py310"

# Standard enterprise line length
line-length = 88

# Exclude private, virtual environment, and cache directories
exclude = [
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "build",
    "dist"
]

[tool.ruff.lint]
# Select enterprise-grade rule categories
select = [
    "E",   # pycodestyle syntax errors
    "F",   # Pyflakes (catches undefined variables, unused imports)
    "W",   # pycodestyle warnings
    "I",   # isort (automatically sorts and organizes imports)
    "B",   # flake8-bugbear (catches common bugs, mutable defaults, loop variables)
    "UP",  # pyupgrade (modernizes syntax for Python 3.10+)
    "C4",  # flake8-comprehensions (optimizes data transformations)
    "SIM", # flake8-simplify (simplifies nested if-statements and file handling)
    "ARG", # flake8-unused-arguments (flags dead code and accidental parameter omissions)
    "N"    # pep8-naming (enforces consistent naming conventions)
]

# Targeted rule exemptions
ignore = [
    "E501", # Ignore line-length violations (handled automatically by the formatter)
    "W291", # Ignore trailing whitespace in multi-line string templates
    "W293"  # Ignore blank lines containing whitespace in prompt templates
]

[tool.ruff.lint.isort]
combine-as-imports = true
lines-after-imports = 2

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.mypy]
python_version = "3.10"
warn_unused_configs = true
ignore_missing_imports = true
strict_optional = true
```

### 4.4 Operationalizing Linting with Antigravity AI Agents

Engineers do not need to memorize linting rule codes. The starter kit enables two simple workflows:

#### 1. Instant Terminal Commands
From the workspace root, run:
```powershell
# Scan entire project for syntax, logic, and scoping bugs (<50 milliseconds)
ruff check .

# Automatically fix import sorting, unused imports, and common syntax issues
ruff check . --fix

# Reformat all files to standard style
ruff format .
```

#### 2. The Deterministic AI Pair-Programming Loop
When asking Antigravity to write code or modify an analytical script, add this simple prompt instruction:
> *"Implement this function, then run `ruff check . --fix` and ensure all linting checks pass before reporting completion."*

By enforcing this habit, you compel the AI agent to run deterministic compiler-level tooling against its own probabilistic code output. This eliminates 95% of hallucinated arguments, missing imports, and unhandled exception antipatterns before any code is reviewed by a human engineer or executed against production APIs.

---

## 5. Environment Isolation & Python Virtual Environments (`.venv`)

### 5.1 The Production Failure Mode: The "Global Python" Conflict
In Windows Server or enterprise workstation administration, systems engineers frequently encounter DLL conflicts, version pinning issues, or registry collisions when multiple enterprise tools share a single global operating system path. In Python, installing dependencies globally via `pip install <package>` triggers the exact same failure mode:

1. **Dependency Hell**: Tool A (e.g., an automated ticket ingestion daemon) requires `urllib3==1.26` to maintain compatibility with an older on-premises proxy gateway. Tool B (e.g., a modern analytics dashboard exporter) requires `urllib3==2.2` to support modern HTTP connection pooling and strict TLS verification. Installing Tool B globally silently overwrites Tool A's library, breaking the ticket ingestion daemon without warning.
2. **OS Utility Corruption**: On modern Linux platforms and enterprise Windows automation runtimes, system utilities increasingly rely on Python internally. Running unconstrained global `pip install` commands can mutate system-level libraries, prompting package managers to throw `externally-managed-environment` errors or corrupting OS-bundled management scripts.
3. **Ghost Dependencies**: A script developed on a workstation with 80 globally installed packages will appear to function perfectly. However, when deployed to a clean server or container, it crashes immediately with `ModuleNotFoundError` because its true dependencies were never isolated, tracked, or declared in `requirements.txt`.

### 5.2 The Infrastructure Metaphor: Virtual Environments as Lightweight Sandboxes
For an infrastructure or systems engineer, a **Python Virtual Environment (`.venv`)** is conceptually identical to a **lightweight container namespace, chroot jail, or isolated directory mount**:

```
[ Host Operating System / Windows Kernel ]
       │
       ├── Global Python Runtime (e.g., C:\Program Files\Python310\python.exe)
       │     └── Global site-packages (Untouched / Pristine)
       │
       └── [ Workspace Boundary: ./MySupportProject/ ]
             └── .venv/  <-- HERMETIC SANDBOX
                   ├── Scripts/
                   │     ├── python.exe    <-- Pointer to local isolated interpreter
                   │     ├── pip.exe       <-- Local package installer
                   │     └── Activate.ps1  <-- Shell PATH manipulation script
                   └── Lib/site-packages/
                         ├── requests/     <-- Workspace-specific dependencies only
                         ├── pandas/
                         └── ruff/
```

- **Hermetic Boundary**: When you create a `.venv`, Python creates a lightweight directory structure containing a private copy (or symlink) of the Python interpreter, pip package manager, and a dedicated `site-packages` directory.
- **Zero OS Footprint**: Everything installed while the environment is active is stored exclusively inside the local `.venv` directory. If dependencies become corrupted or experimental packages are no longer needed, deleting the `.venv` folder completely removes all traces from your workstation without affecting any other project or system tool.
- **Git Safety**: Because `.venv` contains binary files, compiled C-extensions, and thousands of vendor libraries, it must **never** be committed to Git. The project's `.gitignore` explicitly blocks `.venv/`.

### 5.3 Anatomy of a `.venv`: How Path Precedence Works Under the Hood
Activating a virtual environment does not execute a daemon, modify the Windows Registry, or alter system-wide environment variables. It performs a single, elegant operation: **it temporarily prepends the virtual environment's `Scripts/` directory to your current shell session's `$env:PATH`**.

When you run:
```powershell
.venv\Scripts\Activate.ps1
```
PowerShell updates your session path:
```powershell
$env:PATH = "C:\Projects\SupportGov\.venv\Scripts;" + $env:PATH
```

Because operating systems search `$env:PATH` from left to right:
1. When you type `python`, Windows resolves `C:\Projects\SupportGov\.venv\Scripts\python.exe` instead of the global interpreter in `C:\Program Files\Python310\python.exe`.
2. When you type `pip install requests`, pip installs the library directly into `C:\Projects\SupportGov\.venv\Lib\site-packages\`.
3. When you run `deactivate`, the script restores your previous `$env:PATH`, returning your terminal to the default global environment.

### 5.4 Automating Workspace Provisioning via `setup.ps1`
To eliminate manual setup friction, the Starter Kit includes an automated bootstrap script (`setup.ps1`) that programmatically verifies prerequisites, provisions `.venv`, upgrades tooling, installs locked dependencies, and mirrors template configurations:

```powershell
# setup.ps1 - Automated Workspace Initialization Workflow
# 1. Verify host Python 3.10+ exists in environment PATH
$pythonCmd = "python"
$version = & $pythonCmd --version 2>&1
Write-Host "Found Python: $version" -ForegroundColor Green

# 2. Provision isolated .venv if not already present
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creating hermetic virtual environment in .venv..." -ForegroundColor Yellow
    & $pythonCmd -m venv .venv
}

# 3. Target the virtual environment's private pip executable directly
$pipCmd = ".venv\Scripts\pip.exe"

# 4. Upgrade pip and install locked project dependencies
Write-Host "Upgrading pip and installing dependencies..." -ForegroundColor Yellow
& $pipCmd install --upgrade pip
& $pipCmd install -r requirements.txt

# 5. Mirror .env.template to local .env if missing
if (Test-Path -Path ".env.template") {
    if (-not (Test-Path -Path ".env")) {
        Copy-Item -Path ".env.template" -Destination ".env"
        Write-Host "Created local .env from template (populate required keys)." -ForegroundColor Cyan
    }
}
```

*Key Systems Engineering Principle*: Notice that `setup.ps1` executes `.venv\Scripts\pip.exe` directly rather than relying on the shell's active environment. This guarantees that dependencies are installed into the sandbox even if PowerShell execution policies temporarily block the interactive `Activate.ps1` script.

### 5.5 Virtual Environment Operations Cheatsheet

| Operational Task | Command (PowerShell) | Technical Explanation |
| :--- | :--- | :--- |
| **Create Sandbox** | `python -m venv .venv` | Provisions a clean, private interpreter and library folder inside `.venv/`. |
| **Activate Session** | `.venv\Scripts\Activate.ps1` | Modifies active shell session `$env:PATH` to prioritize `.venv\Scripts`. |
| **Install Packages** | `pip install -r requirements.txt` | Downloads and unpacks required packages strictly inside `.venv\Lib\site-packages`. |
| **Inspect Installed** | `pip list` | Displays only packages installed in the local virtual environment. |
| **Freeze Contract** | `pip freeze > requirements.txt` | Generates a deterministic manifest of exact package versions for version control. |
| **Deactivate** | `deactivate` | Restores original shell session `$env:PATH` prior to virtual environment activation. |
| **Clean Reset** | `Remove-Item -Recurse -Force .venv` | Completely purges the sandbox with zero residual host operating system impact. |

---

## 6. Modular Architecture: Pure Functions vs. I/O Separation & Offline Fixture Testing

### 6.1 The Failure Mode: Monolithic, Impure Automation Scripts
In traditional operational scripting, engineers frequently write monolithic procedures where API authentication, network requests, data transformations, mathematical calculations, and file writes are interwoven in a single continuous script:

```python
# ANTI-PATTERN: Monolithic Impure Function
def process_stale_tickets():
    # 1. Impure I/O: Network call requiring live VPN and valid credentials
    response = requests.get("https://instance.service-now.com/api/now/table/incident", 
                            auth=(os.getenv("USER"), os.getenv("PASS")))
    data = response.json()
    
    # 2. Pure Logic: Business hours arithmetic & priority scoring
    for ticket in data["result"]:
        hours_elapsed = (datetime.now() - parse(ticket["sys_updated_on"])).seconds / 3600.0
        if hours_elapsed > 8.5:
            # 3. Impure I/O: Outbound notification webhook
            requests.post("https://outlook.office.com/webhook/...", json={"alert": ticket["number"]})
```

**Why this architecture fails in enterprise environments**:
1. **Impossible Offline Testing**: You cannot verify whether your business hours calculation handles weekend rollovers without connecting to a live ServiceNow instance with active credentials.
2. **Flaky CI/CD Pipelines**: Automated test suites fail randomly due to network latency, API rate limits (HTTP 429), expired test credentials, or maintenance windows.
3. **High Blast Radius**: A simple modification to a mathematical scoring formula risks accidentally triggering live notification webhooks or mutating production database records.
4. **Zero Cross-Platform Portability**: If the team decides to port the logic to PowerShell or C#, separating the mathematical rules from the network code requires a complete, risky rewrite.

### 6.2 Architectural Decoupling: The Two-Tier System Model
The Starter Kit strictly decouples code into two distinct architectural layers:
- In Python: **`src/` & pure utility modules** vs. **Runner / CLI scripts**.
- In PowerShell: **`Private/` (Pure Functions)** vs. **`Public/` (I/O Layer)**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      I/O LAYER (Impure / External)                     │
│  - Python: Runner scripts, Backlog Relay daemon, sn_utils.py           │
│  - PowerShell: Public/ (Get-SnStaleTicket.ps1, Send-RelayPayload.ps1)  │
│  - Responsibilities: Network sockets, REST APIs, OAuth tokens,         │
│    SharePoint Graph sync, Windows SecretStore credential extraction.   │
│  * Characteristics: High latency, non-deterministic, network dependent.│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Passes Raw Dictionaries / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   COMPUTATION LAYER (Pure Logic Engine)                │
│  - Python: src/ticket_summary_utils.py, calculate_priority_score()     │
│  - PowerShell: Private/ (Get-BusinessHoursElapsed.ps1, etc.)           │
│  - Responsibilities: Working hours arithmetic, ticket staleness tests, │
│    145-pt priority scoring, productivity pacing, quality aggregation.  │
│  * Characteristics: 100% Deterministic, 0 Side Effects, No Network.    │
└────────────────────────────────────────────────────────────────────────┘
```

1. **The I/O Layer (`Public/` or Runner Scripts)**:
   Performs the external "heavy lifting". It queries the ServiceNow REST API, handles HTTP 429 retries with exponential backoff, reads from local disk caches, and delivers payloads to Microsoft Teams webhooks. It performs zero complex mathematical transformations; it simply collects data and delegates analysis to the pure engine.
2. **The Pure Computation Layer (`Private/` or Pure Utility Modules)**:
   Receives plain data structures (strings, numbers, timestamps, dictionaries) and returns computed results (scores, booleans, formatted text cards). It contains **zero side effects**: it never opens a network socket, never reads an environment variable, never queries a database, and never modifies global state.

### 6.3 The Core Computational Engine: Pure Mathematical Functions
A pure function adheres to two mathematical rules:
1. **Identical Input Yields Identical Output**: Given the same arguments, it will return the exact same output 1,000,000 times in a row.
2. **Zero Side Effects**: It does not alter anything outside its own scope.

#### Pure Business Hours Calculation Example
Notice how `get_business_hours_elapsed` accepts both the update timestamp and an explicit `now` parameter:

```python
def get_business_hours_elapsed(last_update_str: str, now: datetime) -> float:
    """
    Pure Function: Calculates business hours between last_update_str and now.
    Window: Monday to Friday, 09:00 to 17:30 (8.5 business hours per day).
    Weekends (Saturday/Sunday) are completely excluded from elapsed time.
    """
    try:
        dt_update = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return 999.0  # Safe deterministic fallback for unparseable data

    if dt_update >= now:
        return 0.0

    total_hours = 0.0
    current = dt_update

    # Step through whole calendar days
    while current.date() < now.date():
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            day_start = datetime.combine(current.date(), datetime.min.time()) + timedelta(hours=9)
            day_end = datetime.combine(current.date(), datetime.min.time()) + timedelta(hours=17, minutes=30)
            if current < day_end:
                work_start = max(current, day_start)
                total_hours += (day_end - work_start).total_seconds() / 3600.0
        current = datetime.combine(current.date() + timedelta(days=1), datetime.min.time()) + timedelta(hours=9)

    # Process remaining hours on the final day
    if current.weekday() < 5:
        day_start = datetime.combine(current.date(), datetime.min.time()) + timedelta(hours=9)
        day_end = datetime.combine(current.date(), datetime.min.time()) + timedelta(hours=17, minutes=30)
        work_start = max(current, day_start)
        work_end = min(now, day_end)
        if work_start < work_end:
            total_hours += (work_end - work_start).total_seconds() / 3600.0

    return round(total_hours, 2)
```

*Why Injecting `now` is Essential*: If a function internally calls `datetime.now()`, it becomes non-deterministic because its return value changes with every second that passes. By accepting `now` as an optional parameter, the function can be frozen to a specific second in time during automated tests, guaranteeing 100% repeatable verification.

### 6.4 The Power of Fixture Testing: 100% Deterministic Offline Verification
Because core governance logic is pure, it can be tested completely offline without ServiceNow access, without internet connectivity, and without live credentials.

The Starter Kit establishes a **Language-Neutral JSON Fixture Contract** located in `Tests/fixtures/`:
- `business_hours.json`: Validates weekend transitions, after-hours updates, and same-day working windows.
- `ticket_stale.json`: Tests staleness thresholds across incidents, requests, escalated tickets, and aged tickets.
- `priority_score.json`: Tests multi-criteria 0–145 point scoring, boundary limits, and resolved-ticket clamping.
- `clean_comment.json`: Tests HTML stripping, URL label preservation, and whitespace collapsing.

#### Sample Fixture Contract (`Tests/fixtures/ticket_stale.json`)
```json
{
  "function": "is_ticket_stale",
  "description": "Language-neutral test cases for ticket staleness evaluation",
  "cases": [
    {
      "name": "Incident updated 4.0 business hours ago (Fresh)",
      "now": "2026-05-18 14:00:00",
      "record": {
        "sys_class_name": "incident",
        "sys_updated_on": "2026-05-18 10:00:00",
        "escalation": "0",
        "sys_created_on": "2026-05-15 10:00:00"
      },
      "expected": false
    },
    {
      "name": "Incident updated 9.0 business hours ago (Stale > 8.5h)",
      "now": "2026-05-19 10:30:00",
      "record": {
        "sys_class_name": "incident",
        "sys_updated_on": "2026-05-18 10:00:00",
        "escalation": "0",
        "sys_created_on": "2026-05-15 10:00:00"
      },
      "expected": true
    },
    {
      "name": "Escalated incident updated 1 hour ago (Always Flagged)",
      "now": "2026-05-18 11:00:00",
      "record": {
        "sys_class_name": "incident",
        "sys_updated_on": "2026-05-18 10:00:00",
        "escalation": "1",
        "sys_created_on": "2026-05-15 10:00:00"
      },
      "expected": true
    }
  ]
}
```

### 6.5 Cross-Runtime Parity: Dual-Language Testing (Python & PowerShell)
A common challenge in IT operations is maintaining parity between rapid automation scripts written by different engineers in Python and PowerShell.

The Starter Kit solves this by sharing the **exact same JSON fixtures across both runtimes**:
1. **Python Runner (`python Tests/run_fixtures.py`)**:
   Reads `Tests/fixtures/*.json`, passes the inputs into Python functions, and asserts exact equality against `expected`.
2. **PowerShell Runner (`pwsh -File FlowRelayPS/Tests/Invoke-FixtureTests.ps1`)**:
   Reads the exact same `Tests/fixtures/*.json` files, dot-sources the PowerShell functions in `Private/`, and asserts equality against `expected`.

```
                      ┌────────────────────────────┐
                      │    Tests/fixtures/*.json   │
                      │  (Single Source of Truth)  │
                      └──────────────┬─────────────┘
                                     │
                   ┌─────────────────┴─────────────────┐
                   ▼                                   ▼
       ┌───────────────────────┐           ┌───────────────────────┐
       │ Python Test Runner    │           │ PowerShell Test Runner│
       │ (Tests/run_fixtures.py)│           │ (Invoke-FixtureTests) │
       └───────────┬───────────┘           └───────────┬───────────┘
                   │                                   │
                   ▼                                   ▼
       ┌───────────────────────┐           ┌───────────────────────┐
       │ Python Implementation │           │ PowerShell Private/   │
       │ (src/pure_modules.py) │           │ (Get-BusinessHours)   │
       └───────────────────────┘           └───────────────────────┘
```

*Zero Third-Party Test Dependencies*: The PowerShell test runner (`Invoke-FixtureTests.ps1`) does not require Pester to be installed. On enterprise Windows machines where Pester 3.4.0 syntax conflicts with Pester 5+, the runner uses native PowerShell 7 language constructs, ensuring any engineer can run tests immediately with zero environment configuration.

### 6.6 The Pinned Quirks Pattern: Preserving Known Boundary Conditions
During enterprise refactoring or cross-language porting, engineers often discover legacy behaviors that appear mathematically imperfect but are relied upon by downstream systems:
- *Quirk 1 (Prose Angle Brackets)*: In comment cleaning, prose like `if x < 5 and y > 3` might be treated as an HTML tag by simple regex parsers.
- *Quirk 2 (Timezone Offset)*: The business hours calculation standardizes on 09:00–17:30 UK local working hours but operates on UTC timestamps from the ITSM database, causing a 1-hour seasonal shift under British Summer Time (BST).

**The Architectural Rule**: Never silently alter a boundary condition in one language without updating both runtimes and the test fixtures simultaneously. By labeling these cases as `QUIRK:` inside the shared JSON fixture files, both implementations are pinned to identical behavior. When the team decides to improve the logic, the fixture is updated first, and both implementations are refactored together.

### 6.7 Language Selection Strategy: Systems Scripting (PowerShell) vs. General-Purpose Languages (Python)
For Systems Engineers and Technical Leaders transitioning into AI-augmented development, a common question is: *"Should we build this tool in PowerShell (which our operations team already knows) or in Python?"*

Rather than treating language selection as an ideological choice, treat it as an **engineering trade-off** based on the workload, target host environment, and how AI models generate code.

#### 1. Why Python is Recommended for the Majority of Data Analysis, Integrations & AI Coding
While PowerShell is an exceptional administrative shell, **Python is strongly recommended as your primary language** for data analysis, KPI scoring engines, complex API integrations, web dashboards, and standalone utilities:
- **Superior AI Code Generation Quality**: Frontier AI models (Gemini, Claude, GPT) have their deepest training volume in Python. When pair-programming with Antigravity agents, models produce cleaner, more idiomatic, and significantly less bug-prone code in Python on the first pass than in PowerShell (where models occasionally trip over pipeline array-unwrapping, `$null` comparison ordering, or PowerShell 5.1 vs. 7.2+ cmdlet differences).
- **Data Analysis & Mathematical Simplicity**: Calculating multi-dimensional KPIs, weekend-aware working-hour gaps, 6-month longitudinal trends, and sentiment heuristics is far simpler and more readable in Python using standard library data structures (`datetime`, `collections`, `statistics`) or analytics libraries (`pandas`, `numpy`).
- **Portability & Single-File Distribution**: Python code runs identically across Windows laptops, Linux CI/CD runners, and cloud containers (Azure Container Apps / Docker). Furthermore, using `PyInstaller`, a Python CLI tool can be compiled into a standalone, zero-dependency Windows executable (`.exe`) that colleagues can run without installing Python or configuring modules.
- **Sub-Second Static Verification**: Python's static analysis ecosystem (`Ruff` + `Mypy`) parses the Abstract Syntax Tree in milliseconds to catch undefined variables, type mismatches, and bare `except:` blocks before a script ever touches a live production API.

#### 2. When to Choose a Systems-Familiar Language (PowerShell 7.2+)
PowerShell remains the right tool when the task is fundamentally **operating-system or Microsoft-ecosystem administration**:
- **Native Windows Security & Credential Vaults**: Interacting directly with Windows DPAPI via `Microsoft.PowerShell.SecretStore` or Windows Credential Manager without spawning subprocesses.
- **Active Directory, Entra ID & M365 Cmdlets**: Tasks relying on official Microsoft administrative modules (`ActiveDirectory`, `ExchangeOnlineManagement`, `MicrosoftTeams`) where official PowerShell cmdlets handle complex token negotiation natively.
- **Windows Host & Task Scheduler Orchestration**: Managing Windows Services, Registry keys, Event Logs, WMI/CIM objects, or registering Scheduled Tasks on locked-down Windows jump boxes where installing Python is restricted by policy.
- **Critical PowerShell Guardrail**: Always target **PowerShell 7.2+ (`pwsh`)** for API and JSON automation. Avoid legacy Windows PowerShell 5.1 (`powershell.exe`), which lacks `-SkipHttpErrorCheck` on `Invoke-RestMethod`, writes UTF-8 files with a Byte Order Mark (BOM), and escapes non-ASCII characters in `ConvertTo-Json`.

#### 3. Task-to-Language Recommendation Matrix

| Operational Workload / Task | Recommended Language | Engineering Rationale |
| :--- | :--- | :--- |
| **KPI Math, SLA Staleness & Scoring Rubrics** | **Python (Primary)** | Deterministic types, clean date/time arithmetic, highest AI first-pass accuracy, fast unit testing. |
| **ITSM / Graph REST API Ingestion & Pagination** | **Python (Primary)** | Connection pooling (`requests.Session`), explicit backoff/retry control, strict JSON schema typing. |
| **Web Dashboards, REST Proxies & Cloud Containers** | **Python (`FastAPI`)** | Native async web servers, strict auth middleware, and Linux Docker container portability. |
| **Portable CLI Tools for Non-Developer Colleagues** | **Python (`PyInstaller`)** | Compiles script, Python interpreter, and libraries into a single `.exe` with zero host setup. |
| **Windows DPAPI SecretStore & M365 Admin Cmdlets** | **PowerShell 7.2+** | Native access to Windows DPAPI vaults, Active Directory, and Microsoft administrative modules. |
| **Host Bootstrap, Task Scheduler & OS Maintenance** | **PowerShell 7.2+** | Native Windows OS management, service control, and scheduled task registration. |

#### 4. When and How to Combine Both Languages (Polyglot Architecture)
In many enterprise environments, the most resilient architecture **combines both languages** along clean boundaries:
1. **Pattern A — Thin OS Wrapper + Python Analytical Core**:
   Use a concise PowerShell script (`setup.ps1` or a Scheduled Task wrapper) to handle host prerequisite checks, execution policy verification, or Windows SecretStore credential retrieval, and then invoke the Python engine for heavy REST API pagination, KPI calculation, and report generation.
2. **Pattern B — Dual-Runtime Port with Shared JSON Fixtures**:
   When an operational relay needs to exist in both Python (for container/cloud execution) and PowerShell (so an infrastructure team can maintain it in their primary language), keep all scoring/staleness math in pure functions (`src/` in Python, `Private/` in PowerShell) and validate both against the **exact same `Tests/fixtures/*.json` files**.
3. **Pattern C — Strict Inter-Process Data Contracts**:
   Whenever PowerShell and Python exchange data, pass structured JSON files or environment variables—never scrape unformatted console text over `stdout`, and never pass plaintext passwords as command-line arguments (which are visible in process command-line logs).

---

## 7. Step-by-Step Installation & Workspace Bootstrap

### 7.1 Kit Directory Placement & Native Antigravity Discovery Hierarchy
Google Antigravity automatically detects workspace customizations by traversing the project directory tree from your current working directory up to the repository root.

To install the kit into an existing or new workspace, place the unzipped `./Antigravity_Governance_Setup_Kit/` contents directly into your project root:

```
<Your_Project_Workspace_Root>/
├── .agents/
│     ├── agents/                         <-- Discovered by Antigravity as Subagent Personas
│     │     ├── aegis_best_practice/agent.md
│     │     ├── atlas_architecture/agent.md
│     │     ├── sage_governance/agent.md
│     │     ├── sentinel_security/agent.md
│     │     └── spark_disruptor/agent.md
│     └── skills/                         <-- Discovered as Progressive On-Demand Skills
│           ├── infrastructure-best-practice-analyser/SKILL.md
│           ├── ticket-backlog-governance/SKILL.md
│           ├── productivity-workload-governance/SKILL.md
│           ├── quality-audit-governance/SKILL.md
│           ├── teams-standup-digest-notifier/SKILL.md
│           └── support-team-governance-analytics-coaching/SKILL.md
├── Governance_Framework/
│     ├── SAGE_Agent_System_Prompt.md     <-- Master ITSM Governance Persona
│     └── AEGIS_Agent_System_Prompt.md    <-- Copy-Paste Config Analyser & API Pipeline Blueprint
├── .env.template                         <-- Committed schema of required environment keys
├── .gitignore                            <-- Strictly blocks .env, .venv, *.log
├── GEMINI.md                             <-- Living workspace session state & rules
├── README.md                             <-- Kit overview & rapid onboarding
├── ANTIGRAVITY_SETUP_GUIDE.md            <-- This authoritative operations manual
├── ANTIGRAVITY_DOCS.html                 <-- Standalone, zero-server offline HTML5 Local Docs
├── setup.py                              <-- Cross-platform Python bootstrapper & runtime advisor
├── build_docs.py                         <-- Zero-dependency compiler for ANTIGRAVITY_DOCS.html
├── validate_kit.py                       <-- Python automated compliance & leak scanner
└── validate_and_install.ps1              <-- Native PowerShell validator & installer
```

*Discovery Precedence*: Workspace customizations in `.agents/` take highest priority over global user preferences and IDE defaults, ensuring every team member working in the repository experiences identical agent behaviors and governance rules.

### 7.2 Automated Zero-Clone Workspace Bootstrap (`irm | iex`), `setup.py`, and Validation
You do **not** need to clone or manually download the GitHub repository before setting up a workspace. Both [`validate_and_install.ps1`](validate_and_install.ps1) and [`setup.py`](setup.py) are self-bootstrapping: if run in a directory where the 24 canonical kit files are not yet present, they automatically download and extract the complete kit from `https://github.com/apswood/pantheon-ai-kit`, initialize `.env` from `.env.template`, offer the optional custom keyword leak scanner builder (`.custom_blocklist.json`, protected by `.gitignore`), and run all 4 validation stages.

#### Option A (Recommended — Zero-Clone PowerShell One-Liner via `irm | iex`)
```powershell
# 1. Zero-clone bootstrap into your current directory (downloads validate_and_install.ps1, setup.py & all 24 components):
mkdir C:\Workspaces\ITSM_Support_Analytics; cd C:\Workspaces\ITSM_Support_Analytics
irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex

# 2. Zero-clone bootstrap into a specific target folder via environment variable:
$env:PANTHEON_TARGET_DIR = "C:\Workspaces\ITSM_Support_Analytics"; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex

# 3. Zero-clone non-interactive bootstrap (skipping optional custom keyword scanner prompt):
$env:PANTHEON_SKIP_SCANNER = "1"; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/validate_and_install.ps1 | iex
```

#### Option B: Cross-Platform Python Bootstrapper (`setup.py`)
```powershell
# 1. Zero-clone Python one-liner (downloads setup.py, which automatically fetches all 24 kit files & runs setup):
irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/setup.py -OutFile setup.py; python setup.py --init-env

# 2. Inspect host runtimes, print the Python vs. PowerShell guide, rebuild the HTML docs, and validate the kit:
python setup.py

# 3. Initialize a local .env from .env.template and provision an isolated .venv virtual environment:
python setup.py --init-env --venv

# 4. Build or append to the local custom $EncodedRules keyword library (.custom_blocklist.json, gitignored):
python setup.py --configure-scanner
python setup.py --add-scanner-keyword "AcmeCorp, acme.internal" --add-scanner-keyword "AcmeDomain::\bacme\.internal\b"
```

#### Option C: Local PowerShell Validator & Installer (`validate_and_install.ps1`)
```powershell
# 1. Validate kit integrity, frontmatter, generic secret patterns, and any local .custom_blocklist.json rules:
pwsh -NoProfile -File ./validate_and_install.ps1 -ValidateOnly

# 2. Configure or add to the local custom $EncodedRules keyword library (.custom_blocklist.json):
pwsh -NoProfile -File ./validate_and_install.ps1 -ConfigureCustomScanner

# 3. Install from a local kit folder into another target workspace:
pwsh -NoProfile -File ./validate_and_install.ps1 -Install -TargetWorkspace "C:\Workspaces\ITSM_Support_Analytics"
```

#### Option D: Standalone Python CLI Validator (`validate_kit.py`)
```bash
# Run comprehensive multi-stage validation
python validate_kit.py --verbose
```

The validation pipeline executes four discrete checks:
- **Stage 1 (Structure Check)**: Confirms presence and non-zero size of all 24 canonical kit files (5 specialist agents, 6 skills, 2 system prompts, rules, templates, and scripts) and verifies `GEMINI.md` is strictly `< 24,000 bytes`.
- **Stage 2 (YAML Frontmatter Check)**: Verifies that every `agent.md` and `SKILL.md` file contains valid opening/closing `---` delimiters and non-empty `name` and `description` context pointers.
- **Stage 3 (De-Identification & Secret Leak Scan)**: Scans all files against 5 built-in generic credential/secret regex rules (`PEM Private Keys`, `GitHub PATs`, `AWS Access Key IDs`, `Slack API Tokens`, `Hardcoded OAuth Client Secrets`) plus any optional local custom `$EncodedRules` stored in `.custom_blocklist.json` (gitignored). Zero reversible organization-specific text is stored in the upstream repository.
- **Stage 4 (Configuration Hygiene Check)**: Proves that `.gitignore` contains strict exclusion rules for `.env`, `.venv`, and `.custom_blocklist.json`, and that `.env.template` contains no plain text passwords.

### 7.3 Activating the 5 Specialist Advisory Agents
The Setup Kit embeds five distinct multi-agent personas configured to advise on infrastructure hardening, enterprise systems architecture, service delivery governance, security compliance, and process optimization.

You can invoke any specialist directly in Antigravity chat using the `@` mention syntax:

```
@aegis_best_practice Audit this FortiGate FortiOS 7.4 configuration against our NIST, NCSC, and UKFS-01..06 standards catalogue.
```

```
@atlas_architecture Please review our proposed database synchronization module. How can we decouple the REST retry logic from the data transformation classes?
```

```
@sage_governance Audit our team's ticket backlog pacing for this week. Why are 4 tickets currently breaching our meaningful update threshold?
```

```
@sentinel_security Inspect our .env.template and PowerShell credentials engine. Are we exposing any plain text secrets across process pipes?
```

```
@spark_disruptor Grill me across the design-tree frontier for our new automated firewall config collector, then break the plan into tracer-bullet vertical slices.
```

#### Specialist Advisory Team Capabilities Matrix

| Agent Specialist | Acronym Meaning | Primary Architectural Responsibility | When to Engage |
| :--- | :--- | :--- | :--- |
| **AEGIS** | Architecture, Estate Governance & Infrastructure Standards Analyser | Audits Palo Alto (`PAN-OS`), FortiGate (`FortiOS`), Juniper (`Junos`), Windows Server, and Linux Server against NIST, NCSC, vendor guides, and `UKFS-01..06`. | Firewall/router rule-base audits, server hardening reviews, operational resilience mapping, API config pipeline design. |
| **ATLAS** | Architecture & Technology Lead for Application Scalability | Deep modules, clean test seams, pure-vs-I/O separation, two-axis code reviews, cross-runtime parity, tight bug feedback loops. | Designing new modules, reviewing PR diffs, refactoring monolithic scripts, diagnosing regressions. |
| **SAGE** | Service Analytics & Governance Expert | ITIL v4 alignment, 145-pt backlog scoring, 315m pacing, dual quality auditing, 3-step evidence-based coaching. | Backlog triage, capacity reviews, quality scorecard analysis, standup reporting. |
| **SENTINEL** | Security Enforcement, Network Trust & Integrity Evaluation | Credential isolation, `<REDACTED>` diagnostic scrubbing, Windows SecretStore, least-privilege ACLs, deterministic security checks. | Pre-deployment security reviews, credential audits, building automated security guardrails. |
| **SPARK** | Strategic Pivot, Assumption-challenging & Radical Kaizen | Design-tree frontier interviewing ("grilling"), tracer-bullet vertical slicing, eliminating operational toil, questioning metric gaming. | Project kickoff interviews, breaking specs into vertical slices, process simplification. |

### 7.4 On-Demand Execution of the 6 Governance & Best-Practice Skills
Antigravity uses **progressive disclosure** for skills: skills are not loaded into context until their YAML `description` context pointer matches your task:

1. **Infrastructure Best-Practice Analyser (`infrastructure-best-practice-analyser`)**:
   - *Triggers*: `audit firewall config`, `assess PAN-OS / FortiOS / Junos / Windows / Linux`, `map to NIST 800-53 / NCSC / UKFS-01..06`, `Test Library 1.1.0`.
   - *Output*: Prioritised multi-platform findings mapped to public NIST/NCSC/vendor controls, UKFS operational resilience outcomes, licensed placeholder IDs (`ISO 27001`, `CIS`, `PCI DSS`, `SWIFT`), and mandatory caveats.
2. **Ticket Backlog Governance (`ticket-backlog-governance`)**:
   - *Triggers*: `evaluate backlog stagnancy`, `calculate priority scores`, `top 5 tickets for standup`, `age band distribution`.
   - *Output*: Backlog health summary table, 5-tier age breakdown, and Top 5 Standup table highlighting multi-day blockers.
3. **Productivity & Workload Governance (`productivity-workload-governance`)**:
   - *Triggers*: `analyze engineer time pacing`, `daily utilization audit`, `closed ticket throughput`, `flag time anomalies`.
   - *Output*: Dual pacing table comparing actual minutes against the 315-minute target, pro-rated intraday curves, and sub-minute logging alerts.
4. **Quality Audit Governance (`quality-audit-governance`)**:
   - *Triggers*: `generate quality scorecard`, `audit resolve pass rate`, `evaluate KB0016486 rubric`, `check future date pending`.
   - *Output*: `Pass Rate % (Granular Score %)` dual tables, root cause taxonomy splits, and customer communication ratings.
5. **Teams Standup Digest Notifier (`teams-standup-digest-notifier`)**:
   - *Triggers*: `format teams digest card`, `generate standup markdown`, `post backlog summary to teams`.
   - *Output*: Theme-safe Adaptive Card or HTML markdown payload highlighting Top 5 critical items per engineering squad.
6. **Support Governance Analytics Coaching (`support-team-governance-analytics-coaching`)**:
   - *Triggers*: `draft engineer coaching note`, `remediate low time capture`, `discuss ticket stagnancy`, `evidence-based 1-on-1`.
   - *Output*: Objective 3-step coaching scripts (Observation -> Impact & Context -> Constructive Alignment) written in a supportive, blameless tone.

### 7.5 Antigravity Workflow Commands: `/plan`, `/teamwork-preview`, `/grill-me`, and `/compact`
Antigravity provides specialized slash commands in the Chat Canvas to orchestrate complex technical work:

- **`/plan` (Structured Planning Mode)**:
  Instructs Antigravity to perform a deep pre-flight analysis before touching code or executing terminal commands. Use `/plan` when implementing complex features (e.g., adding a new ITSM or firewall API data provider) to review architecture, file changes, and test requirements before approving execution.
- **`/teamwork-preview` (Multi-Agent Decomposition Preview)**:
  In multi-agent collaborative workflows, `/teamwork-preview` spawns an orchestrator and specialist subagents (`ATLAS`, `SENTINEL`, `AEGIS`, `SPARK`) in isolated threads with independent reviewer and challenger verification gates.
- **`/grill-me` (Design-Tree Frontier Interview)**:
  Initiates a structured interrogation session where the agent maps your idea as a **design tree** and interviews you across the **ready frontier** (numbered questions with opinionated recommendations) until every architectural ambiguity is resolved before writing code.
- **`/compact` (Context Window Compaction)**:
  Summarizes and compacts a long conversation into a clean state checkpoint, freeing up context window tokens when transitioning from *Discovery/Planning* to *Implementation*.

### 7.6 Custom Organization Keyword Leak Scanner & Validation Severity Guide

To guarantee that **zero reversible organization-specific text** exists in the upstream repository, [`validate_kit.py`](validate_kit.py) and [`validate_and_install.ps1`](validate_and_install.ps1) ship only with **5 built-in generic credential/secret regex rules** (`PEM Private Keys`, `GitHub PATs`, `AWS Access Key IDs`, `Slack API Tokens`, `Hardcoded OAuth Client Secrets`).

During setup (or anytime thereafter), you can optionally build a **local library of custom organization keywords, domains, colleague names, or resource IDs** (`$EncodedRules` stored in `.custom_blocklist.json`):
- **Single or Comma-Separated Input**: Enter a single keyword (`AcmeCorp`) or multiple comma-separated keywords on one line (`AcmeCorp, acme.internal, ProjectX`), or use `Label::Regex` (`AcmeDomain::\bacme\.internal\b`) for custom regexes.
- **Duplicate Prevention & Reset Option**: The interactive builder automatically skips duplicate keywords and allows you to keep or clear existing rules in `.custom_blocklist.json`.
- **Reversed UTF-8 + Base64 Encoding & `.gitignore` Protection**: Each keyword and regex pattern is encoded (`NameB64` and `PatB64`) and saved to `.custom_blocklist.json` (which is automatically added to `.gitignore`) so naive `grep` searches never self-trigger on the rule file and custom rules are never committed upstream.

#### Understanding Validation Match Results & Severity Levels
When Stage 3 (`De-Identification & Secret Leak Scan`) detects a match, the validator prints a detailed **Validation Match Summary & Severity Assessment** at the end of the run, classifying matches into three clear tiers:

| Match Category | Severity Level | What It Means & Why It Matched | Recommended Action |
| :--- | :--- | :--- | :--- |
| **1. Built-In Secret Rule Match** | **CRITICAL** | Matched one of the 5 built-in credential patterns (`PEM Private Key`, `GitHub PAT`, `AWS Access Key ID`, `Slack Token`, or `Hardcoded OAuth Client Secret`). | **Immediate Remediation**: Rotate/revoke the exposed credential immediately and move it to `.env` or Windows DPAPI SecretStore. |
| **2. Custom Rule — Whole-Word / Regex Match** | **MEDIUM (Review Required)** | Matched the full word boundary (`\b<keyword>\b`) or custom regex of a keyword you added to `.custom_blocklist.json`. | **Review**: If the keyword is a real confidential organization, client, or internal domain name, replace it with a generic placeholder (`<ORGANIZATION_NAME>`). |
| **3. Custom Rule — Partial Substring Match** | **LOW (Likely False Positive)** | The characters of a custom keyword appeared *inside* a longer unrelated word (for example, entering test keyword `'bad'` matches inside CSS class `.brand-badge`, or `'good'` matches inside `'Goodhart'`). | **Benign / False Positive**: Avoid short common English words in `.custom_blocklist.json`. Remove or update your custom rules via `-ConfigureCustomScanner` or `--configure-scanner`. |

```powershell
# Reconfigure or clear custom scanner rules interactively:
pwsh -NoProfile -File .\validate_and_install.ps1 -ConfigureCustomScanner
python setup.py --configure-scanner

# Or remove .custom_blocklist.json completely and re-validate:
Remove-Item .\.custom_blocklist.json -Force -ErrorAction SilentlyContinue
pwsh -NoProfile -File .\validate_and_install.ps1 -ValidateOnly
```

### 7.7 Workspace Lifecycle Symmetry & Surgical Uninstallation

Provisioning starter kit files into shared enterprise repositories requires equal rigor when decommissioning or rolling back changes. Both [`setup.py`](setup.py) and [`validate_and_install.ps1`](validate_and_install.ps1) implement non-destructive, surgical uninstallation:

1. **Three-Tier State Decomposition**:
   - **Tier 1 (Canonical Kit Files)**: Agents (`.agents/agents/*`), skills (`.agents/skills/*`), rules, and scripts (`setup.py`, `validate_kit.py`, etc.). Always safely removed during uninstallation.
   - **Tier 2 (Generated Caches & Output)**: `ANTIGRAVITY_DOCS.html`, `.venv/`, `__pycache__/`. Removed when requested (`--purge-venv` / `-PurgeVenv`).
   - **Tier 3 (User Secrets & Keyword Blocklists)**: `.env` (contains live enterprise tokens) and `.custom_blocklist.json`. **Preserved by default** to prevent accidental credential loss; deleted only when explicit flags (`--purge-secrets` / `-PurgeSecrets`) are supplied.
2. **Suicide Deletion Hazard & Source Repo Protection**:
   - Running `python setup.py --uninstall` or `pwsh validate_and_install.ps1 -Uninstall` directly inside the kit source clone aborts immediately (`Exit Code 1`) to prevent accidental repository self-destruction. Uninstallation requires either an external `--target-dir` / `-TargetWorkspaceDir` or an explicit `--force` override.
3. **Surgical Deletion vs. Recursive Purge**:
   - Uninstallation removes only the 24 canonical kit files and generated artifacts. It prunes parent directories (`.agents/agents/`, `.agents/skills/`, `.agents/`) **only if they become completely empty**, preserving any custom agents, skills, or configurations created by your engineers.
4. **Deterministic Dry-Run Verification**:
   - Both `python setup.py --uninstall --dry-run` and `pwsh validate_and_install.ps1 -Uninstall -WhatIf` output a detailed preview of all candidate files and directories without altering disk state.

```powershell
# Preview deletion plan without removing any files (Dry Run / WhatIf)
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" --dry-run
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -WhatIf

# Execute surgical uninstallation (preserves .env and custom user files)
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" -y
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -Force

# Complete purge including .env, .custom_blocklist.json, and .venv
python setup.py --uninstall --target-dir "C:\Workspaces\ServiceDeliveryOps" --purge-secrets --purge-venv -y
pwsh -NoProfile -File .\validate_and_install.ps1 -Uninstall -TargetWorkspaceDir "C:\Workspaces\ServiceDeliveryOps" -PurgeSecrets -PurgeVenv -Force
```

---

## 8. Customizing KPI Frameworks & Operational Thresholds

Every support organization operates under distinct Service Level Agreements (SLAs), customer contracts, and working hours. The Starter Kit's governance rules are entirely modular and can be customized to match your organization's operational reality.

### 8.1 Business Hours & Ticket Staleness Customization

#### Default Operational Parameters
- **Incident Staleness Threshold**: **8.5 business hours** (equivalent to 1 standard business day without an update).
- **Service Request (`sc_req_item`) Threshold**: **17.0 business hours** (equivalent to 2 standard business days).
- **Standard Business Window**: **Monday to Friday, 09:00 to 17:30** (8.5 business hours per day).
- **Fail-Safe Bypasses**:
  - *Escalated Tickets* (`escalation != 0`): Stays in backlog regardless of recent updates.
  - *Aged Tickets* (`sys_created_on` > 15 days ago): Always flagged for standup review to prevent chronic stagnation.

#### Customization Guide
To modify working hours (e.g., expanding to an 08:00–18:00 window, or supporting 24/7 operations) or adjust thresholds:

1. **Python Implementation**:
   Locate `get_business_hours_elapsed()` and `is_ticket_stale()` in your ingestion module:
   ```python
   # To adjust business hours window:
   WORK_START_HOUR = 8   # 08:00
   WORK_END_HOUR = 18    # 18:00
   WORK_END_MINUTE = 0
   DAILY_BUSINESS_HOURS = 10.0

   # To adjust staleness thresholds:
   INCIDENT_STALE_HOURS = 4.0   # Tighter 4-hour SLA for Priority 1/2 incidents
   REQUEST_STALE_HOURS = 20.0   # Relaxed 2-day SLA for standard requests
   ```
2. **PowerShell Implementation**:
   Edit `FlowRelayPS/Private/Test-TicketStale.ps1` and `Get-BusinessHoursElapsed.ps1`:
   ```powershell
   # In Test-TicketStale.ps1:
   if ($ClassName -eq 'incident') {
       return ($businessHours -ge 8.5)
   } elseif ($ClassName -eq 'sc_req_item') {
       return ($businessHours -ge 17.0)
   }
   ```
3. **Update Fixtures**:
   When changing working hours arithmetic, update the test cases in `Tests/fixtures/ticket_stale.json` and `Tests/fixtures/business_hours.json` and run `python Tests/run_fixtures.py` to confirm verification passes.

### 8.2 The 145-Point Backlog Prioritization Rubric Customization

#### Operational Purpose
When an engineering squad maintains 100+ active backlog items, a 15-minute daily standup cannot review every ticket. The prioritization engine scores every ticket from **0 to 145 points** across four objective criteria, sorting the queue and extracting the **Top 5 most urgent tickets per assignment group**.

#### The 4-Criterion Scoring Rubric

| Criterion | Evaluation Metric | Score Points | Operational Rationale |
| :--- | :--- | :--- | :--- |
| **1. Review Status** | `CRITICAL` | **+50 pts** | Active customer escalation, severe blocker, or governance red flag. |
| | `PROGRESSION STALLED` | **+35 pts** | Investigation has ceased; waiting on internal handoff. |
| | `FAILING` | **+30 pts** | Quality or SLA target breached. |
| | `HEALTHY` | **+10 pts** | Actively progressing under normal cadence. |
| | Missing / Unreviewed | **+20 pts** | Unknown risk; requires triage attention. |
| | `ARCHIVED` | **0 pts** | Long-term parked item; suppressed from daily standup. |
| **2. Review Age** | Never reviewed or parse failure | **+40 pts** | High risk; ticket has never undergone governance review. |
| | Last reviewed > 30 days ago | **+40 pts** | Governance visibility lost. |
| | Last reviewed 15 – 30 days ago | **+30 pts** | Significantly overdue for status re-evaluation. |
| | Last reviewed 8 – 14 days ago | **+20 pts** | Moderately overdue. |
| | Last reviewed 4 – 7 days ago | **+10 pts** | Routine review interval. |
| | Last reviewed $\le$ 3 days ago | **0 pts** | Fresh governance review; zero priority penalty. |
| **3. Meaningful Update Stagnancy** | Never updated or negative days | **+35 pts** | Complete lack of technical or customer communication. |
| | Days since update > 30 days | **+30 pts** | Severe communication drought. |
| | Days since update 16 – 30 days | **+20 pts** | High customer dissatisfaction risk. |
| | Days since update 8 – 15 days | **+10 pts** | Approaching staleness boundary. |
| | Days since update $\le$ 7 days | **0 pts** | Active communication verified. |
| **4. Ticket Age Band** | Age > 60 Days | **+20 pts** | Ancient backlog debt. |
| | Age 30 – 60 Days | **+15 pts** | Aged backlog item. |
| | Age 15 – 30 Days | **+10 pts** | Maturing backlog item. |
| | Age 5 – 15 Days | **+5 pts** | Standard operational lifecycle. |
| | Age < 5 Days | **0 pts** | Freshly created item. |
| **Maximum Total Score** | **Worst-case critical, ancient, untouched ticket** | **145 pts** | **Sorted descending to surface Top 5 standup items.** |

*The Resolved Ticket Clamping Rule*: If a ticket's state is `Resolved`, `Closed Complete`, `Closed Incomplete`, or `Closed Skipped`, the total priority score is clamped to **`0`**. The individual metric breakdowns are preserved in the data payload for audit history, but the ticket is removed from standup queues.

#### Customization Guide
To modify scoring weights (for instance, increasing update stagnancy to 50 points for a customer-experience focused campaign), adjust the weighting dictionary inside `calculate_priority_score()` in `src/ticket_summary_utils.py` and `FlowRelayPS/Private/Get-TicketPriorityScore.ps1`. Verify your changes by updating and executing `Tests/fixtures/priority_score.json`.

### 8.3 5-Tier Age Distribution Customization
The framework partitions active tickets into five granular age bands to monitor WIP aging across assignment groups:

```
[ Tier 1: Fresh ]        < 5 Days       --> Normal triage and active investigation
[ Tier 2: Maturing ]     5 – 15 Days    --> Standard investigation lifecycle
[ Tier 3: Review Req ]   15 – 30 Days   --> Potential blocker; requires manager review
[ Tier 4: Aged Backlog ] 30 – 60 Days   --> Chronic technical bottleneck or vendor delay
[ Tier 5: Ancient Debt ] > 60 Days      --> Critical service debt; requires RCA or escalation
```

To adjust age bands (e.g., adopting a 3-tier model: `< 7d`, `7–30d`, `> 30d`), update the regex pattern matching and bucketing logic inside `get_age_tier()`:

```python
def get_age_tier(created_date: datetime, now: datetime) -> str:
    age_days = (now - created_date).days
    if age_days > 60:
        return "Age > 60 Days"
    elif age_days > 30:
        return "Age 30 - 60 Days"
    elif age_days > 15:
        return "Age 15 - 30 Days"
    elif age_days >= 5:
        return "Age 5 - 15 Days"
    return "Age < 5 Days"
```

### 8.4 Productivity Pacing, Workload Throughput & Utilization Caps

#### Operational Targets
1. **Daily Time Pacing Target**: **5 hours 15 minutes (315 minutes / 5.25 hours)** of logged ticket time per engineer per day.
   - *First-Principles Math*: A standard engineering contract is 37.5 hours/week (7.5 hours/day). Targeting 5.25 hours represents **70% direct ticket utilization**, leaving 2.25 hours daily for standups, email, peer reviews, training, and operational handovers.
2. **Standard MSP Capacity Ceiling**: **80% Utilization (30.0 hours/week or 6.0 hours/day)**.
   - Any engineer logging > 6.0 hours daily over multiple weeks is entering the "burnout corridor" where documentation quality drops and cognitive fatigue increases error rates.
3. **Day-of-Week Pacing Curve**:
   To reflect real-world operational rhythms (heavy standups and planning on Monday, handovers on Friday):
   - Monday: **15%** of weekly logged time
   - Tuesday: **23%**
   - Wednesday: **24%**
   - Thursday: **23%**
   - Friday: **15%**
4. **Closed Task Throughput**: **2 tickets/day (~10 closed tasks/week per engineer)**.
   - *Automated Event Isolation*: Bulk system-generated events (such as monitoring heartbeat alarms or mass-resolved event storms) are filtered out to prevent artificial throughput inflation.
5. **Proactive Work Ratio**: **$\ge$ 10% of total recorded time** dedicated to Problem Management, Root Cause Analysis, and continuous service improvement (PRB, PRB TASK, STRY).

#### Customizing Targets in Configuration
Update the threshold constants in your productivity configuration module:

```python
# Configuration parameters for productivity pacing engine
DAILY_PACING_TARGET_MINUTES = 315   # 5h 15m (70% utilization)
PACING_CEILING_MINUTES = 360        # 6h 00m (80% burnout ceiling)
EXPECTED_CLOSED_PER_DAY = 2.0       # Organic tickets closed per day
PROACTIVE_WORK_MIN_PERCENT = 10.0   # Target % on PRB / RCA tasks

# Anomaly detection thresholds
SUB_MINUTE_THRESHOLD_SECONDS = 60   # Flags default rounding or auto-bookings
UNDER_RECORDING_THRESHOLD_PCT = 50  # Flags < 50% of expected pacing
LARGE_BOOKING_HOURS = 4.0           # Flags single entries requiring review
```

### 8.5 Dual Quality Metrics: Binary Resolve Pass vs. Granular Scoring

#### Operational Purpose
Traditional support quality reporting suffers from the "averaging fallacy": an engineer logs exemplary notes across 9 tickets (averaging 98%), but completely omits root-cause details on a critical outage ticket. A standard average scores them at ~90%, obscuring a major operational failure.

The Starter Kit enforces the **Dual Metric Quality Standard**:
`Pass Rate % (Granular Score %)` — e.g. `85.0% (92.3%)`

1. **Primary Metric — Resolve Pass % (Binary Gate)**:
   A strict binary metric (Pass = 100%, Fail = 0%) driven by the automated QA audit engine. If any mandatory field (e.g. Root Cause, Customer Communication, Corrective Action) fails inspection, the entire ticket receives a Resolve Pass score of `0%`.
2. **Secondary Metric — Granular Quality Score % (Execution Nuance)**:
   A multi-criteria 0–100% audit score evaluating documentation depth, diagnostic reasoning, formatting clarity, and customer empathy.
3. **Future Date Pending Override**:
   If a ticket is placed in a `Pending` state (e.g., Pending Customer UAT, Pending Vendor Part) and the `'Date Required'` field is set to a **future date**, the audit engine automatically flags the status as **`HEALTHY`**, eliminating false alarms on legitimately paused tickets.

#### Customizing QA Dimensions
To adapt the quality rubric, modify the scoring criteria in `.agents/skills/quality-audit-governance/SKILL.md` or your QA engine:

```python
# QA Dimension Weightings (100% Total)
QA_WEIGHTS = {
    "root_cause_completeness": 30,    # Detail and technical depth of RFO
    "customer_communication": 25,     # Clarity, tone, absence of jargon
    "actionable_next_steps": 20,      # Clear handover / next milestone
    "accurate_categorization": 15,    # Correct CI, category, and subcategory
    "timely_journal_updates": 10      # Regular updates during active troubleshooting
}
```

### 8.6 The 3-Step Evidence-Based Coaching Framework Customization

#### Operational Purpose
When technical delivery managers address pacing deficits or ticket stagnancy with engineers, conversations must remain objective, collaborative, and blameless. The Starter Kit implements a structured 3-step coaching workflow:

```
┌────────────────────────────────────────────────────────┐
│ STEP 1: OBJECTIVE OBSERVATION (Data Evidence)          │
│ "State raw facts from the API extract without adjectives│
│ or subjective judgment."                                │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ STEP 2: OPERATIONAL IMPACT & CONTEXT (The 'Why')       │
│ "Explain how this pattern impacts squad capacity,       │
│ customer transparency, or standup visibility."         │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ STEP 3: CONSTRUCTIVE ALIGNMENT (Forward Habit)         │
│ "Agree on a concrete operational routine to align       │
│ future recording with team standards."                 │
└────────────────────────────────────────────────────────┘
```

#### Example Coaching Conversation Blueprints

##### Scenario A: Low Time Worked Pacing (< 50% of 315m Target)
- **Step 1 (Observation)**: *"Looking at yesterday's time capture extract, 1 hour 45 minutes was recorded across 3 incidents, against our squad target of 5 hours 15 minutes."*
- **Step 2 (Operational Impact)**: *"When significant troubleshooting time isn't captured as work progresses, our capacity reporting shows artificial availability, leading to more tickets being dispatched to you while you're already handling complex issues."*
- **Step 3 (Constructive Alignment)**: *"Let's make it a habit to log time immediately as work notes are saved. Were there untracked meetings or lab reproductions yesterday that we should account for?"*

##### Scenario B: Stale Ticket with No Customer Update (> 8.5 Business Hours)
- **Step 1 (Observation)**: *"Ticket INC048291 has been in 'Work in Progress' for 14 business hours without an internal or customer work note."*
- **Step 2 (Operational Impact)**: *"Because the ticket breached our 8.5-hour staleness threshold, it appeared on the management exception digest, and the customer service manager had no visibility into what troubleshooting had taken place."*
- **Step 3 (Constructive Alignment)**: *"Even when waiting on external diagnostics, let's post a 1-line update before end-of-day stating current status, so standup digests reflect that the ticket is actively managed."*

---

## 9. AI-Assisted Engineering Best Practices: Planning, Token Efficiency & "Skills for Real Engineers"

When transitioning from traditional script writing to agentic AI pair-programming, the difference between an agent that produces fragile spaghetti code and an agent that ships production-grade automation lies in **how you structure requirements, manage the token context window, and design verification loops**.

This section synthesizes battle-tested agentic engineering patterns—including principles adapted from Matt Pocock's [**Skills For Real Engineers (`github.com/mattpocock/skills`)**](https://github.com/mattpocock/skills)—and explains how they are wired directly into this Setup Kit.

---

### 9.1 Upfront Planning & Requirements Gathering ("Grilling the Design Tree")

The single most expensive mistake in AI-assisted coding is **premature implementation**: giving the agent a one-sentence prompt (*"Build a script to pull FortiGate configs and check compliance"*) and letting it guess 15 unstated architectural decisions at once. When an LLM guesses, errors compound down every branch.

#### 1. Map Requirements as a Design Tree (`/grill-me` & `@spark_disruptor`)
Treat every new feature or automation tool as a **design tree** where root decisions (runtime language, authentication vault, target API endpoints, failure behavior) unlock downstream child decisions:
- **Work the Ready Frontier in Rounds**: Instead of asking 20 disconnected questions or making silent assumptions, instruct the agent (via `/grill-me` or `@spark_disruptor`) to interview you across the **ready frontier**—every decision whose prerequisites are already settled:
  ```markdown
  ❓ **Q1 - Credential Source & Secret Redaction Seam**: Should the FortiOS REST API token be retrieved from Windows DPAPI SecretStore via a thin PowerShell wrapper or injected via `.env`? And where should `<REDACTED>` scrubbing happen before JSON caching?
  ➡️ **Recommended Answer**: Read from `.env` (with `config.require()` fail-fast validation) so the collector runs identically in Linux containers and Windows workstations, and scrub secrets inside the HTTP collector adapter before any disk write.
  ```
- **Sharpen Domain Vocabulary Inline (`domain-modeling`)**: Ensure terms like `Stale Ticket`, `Meaningful Update`, `Organic Throughput`, `Resolve Pass %`, and `UKFS-01` have one exact definition in `GEMINI.md` and your skills. Ambiguous terminology causes subtle bugs across scripts.

#### 2. Tracer-Bullet Vertical Slices vs. Expand–Contract (`to-tickets`)
*"Make the change easy, then make the easy change."* Once the design tree is resolved, never ask the agent to build an entire 2,000-line system in a single turn:
- **Tracer-Bullet Vertical Slices**: Break the plan into narrow, end-to-end slices that cut through *every* architectural layer (1 API field $\rightarrow$ 1 pure calculation function $\rightarrow$ 1 JSON fixture test $\rightarrow$ 1 CLI/HTML output column). Each slice must be verifiable on its own and small enough to complete inside a single fresh context window.
- **Wide Refactors Use Expand–Contract**: If you need to rename a shared data field or change a function signature across 15 files (a wide blast radius where a single edit breaks everything at once), sequence it in three green steps:
  1. **Expand**: Add the new field/function alongside the old one so existing callers still pass tests.
  2. **Migrate**: Update callers file-by-file while keeping tests green after each batch.
  3. **Contract**: Remove the deprecated field/function once zero callers remain.

---

### 9.2 Efficient Token Use & Context Window Hygiene

Every token sitting in your conversation history costs latency, compute budget, and—most critically—**model attention**. As a session grows bloated with raw JSON dumps, 1,000-line file reads, and dead-end debugging attempts, the model's reasoning accuracy degrades.

#### 1. The Two Loads (`writing-for-agents`)
Every piece of documentation or configuration in your workspace spends one of two budgets:
- **Context Load (Agent Cost)**: Material loaded into the LLM on *every single turn* (`GEMINI.md`, always-on rules in `.agents/rules/`, and the YAML `description` lines of model-invoked skills). Every word here must earn its keep.
- **Cognitive Load (Human Cost)**: Slash commands (`/grill-me`, `/plan`, `/compact`) or external reference files that cost **zero tokens** until the human explicitly invokes them.

#### 2. The 3-Rung Information Hierarchy & Context Pointers
To maximize accuracy while minimizing token burn, organize workspace knowledge across three rungs:
1. **Rung 1 — Always-Loaded Core & Context Pointers (`GEMINI.md` < 24 KB & Skill Frontmatter)**:
   Keep `GEMINI.md` strictly under `24,000 bytes`. Store only current project architecture, active workflow commands, and sharp **context pointers** (`description: <Capability>. Use when <branch 1>, <branch 2>, or <branch 3>.`).
2. **Rung 2 — On-Demand Procedural Steps & Rules (`.agents/skills/<name>/SKILL.md`)**:
   Push multi-page scoring rubrics (`145-point backlog model`), `Test Library 1.1.0` standards tables, and coaching templates into `SKILL.md` files. They consume **0 body tokens** until the context pointer fires. Co-locate each concept's definition, mathematical formula, and edge-case caveats under a single heading so the agent never has to hunt across scattered sections.
3. **Rung 3 — Disclosed Deep Reference & Golden Fixtures (`Governance_Framework/`, `Tests/fixtures/*.json`)**:
   Store standalone copy-paste system prompts (`AEGIS_Agent_System_Prompt.md`) and test cases in dedicated files reached only when explicitly needed.

#### 3. Five Daily Habits for Token Efficiency
1. **Delegate Heavy Exploration to Subagents (`invoke_subagent`)**:
   When auditing 15 files or comparing two architectures, spawn `@atlas_architecture`, `@sentinel_security`, or `@aegis_best_practice`. The subagent absorbs the 20,000 tokens of raw file reading in its own isolated context window and returns only a concise 500-word synthesis to your main session.
2. **Verify via `< 2s` CLI Feedback Loops, Not Multi-Turn Code Reading**:
   Instead of asking the agent to re-read a 600-line script three times to "check if the math is right," run `python Tests/run_fixtures.py`, `python validate_kit.py`, or `ruff check .`. A 10-line pass/fail CLI output costs ~100 tokens and gives 100% mathematical certainty.
3. **Compact Between Planning and Implementation (`/compact`)**:
   After a long `/grill-me` or architecture exploration session, update `GEMINI.md` with the final decisions and run `/compact` (or start a fresh task) before writing code. This purges conversational dead-ends so implementation starts with a clean context window.
4. **Slice File Views (`StartLine` / `EndLine`) & Grep First**:
   Use `grep_search` to locate exact line numbers and view only the relevant 50–100 line slice rather than loading entire multi-thousand-line files into memory.
5. **Scrub Verbose Artifacts & Secrets at the Edge (`<REDACTED>`)**:
   Strip certificates, private keys, encrypted blobs, and repetitive log lines before pasting configs or replaying traces.

---

### 9.3 Engineering Best Practices Adopted from "Skills For Real Engineers" (`mattpocock/skills`)

We evaluated Matt Pocock's open-source [**Skills For Real Engineers**](https://github.com/mattpocock/skills) catalogue and embedded its core architectural disciplines directly into this kit's specialist agents (`ATLAS`, `SPARK`, `SENTINEL`, `SAGE`, `AEGIS`) and skill definitions.

#### 1. Core Engineering Patterns Integrated into This Kit

| Pattern from `mattpocock/skills` | Core Engineering Principle | How It Is Built Into This Antigravity Setup Kit |
| :--- | :--- | :--- |
| **`writing-for-agents` & `SKILL-MECHANICS`** | **Context Pointers, Two Loads & Co-location**: Front-load skill descriptions with explicit `"Use when..."` trigger branches; keep always-loaded files lean; co-locate rules and caveats. | All 5 `agent.md` and 6 `SKILL.md` YAML frontmatter `description` fields are written as branch-triggered context pointers; `GEMINI.md` is enforced `< 24,000 bytes` by `validate_kit.py`. |
| **`codebase-design` (Deep Modules & Seams)** | **Deep Modules**: Place a lot of pure business logic behind a small interface at a clean **seam** (Michael Feathers), testable without live I/O adapters. | Embedded in **`ATLAS`**: Enforces strict separation between pure calculation engines (`src/` / `Private/`) and network/OS adapters (`Public/`), verified via offline `Tests/fixtures/*.json`. |
| **`grilling` & `grill-with-docs`** | **Design-Tree Frontier Interviews**: Map unknowns as a dependency tree and interview the user across the ready frontier (`❓ Q1` $\rightarrow$ `➡️ Recommended Answer`) while sharpening glossary terms. | Embedded in **`SPARK`** & `/grill-me`: Stress-tests requirements in structured rounds before any code is written, preventing premature implementation drift. |
| **`to-tickets` & `to-spec`** | **Tracer-Bullet Vertical Slices & Expand–Contract**: Cut end-to-end vertical slices that fit in one context window; use Expand–Contract for wide refactors. | Embedded in **`SPARK`** & the `AEGIS` API Pipeline Blueprint (`Governance_Framework/AEGIS_Agent_System_Prompt.md` Section 4.4). |
| **`diagnosing-bugs` & `tdd`** | **Tight Red-Capable Feedback Loops & `<REDACTED>`**: Never guess at a bug without first building a `< 2s` deterministic loop that goes red on the bug; redact all secrets (`<REDACTED>`) first. | Embedded in **`ATLAS`** (tight feedback loop requirement) and **`SENTINEL`** / **`AEGIS`** (mandatory `<REDACTED>` secret scrubbing before diagnostics or config analysis). |
| **`code-review` (Two-Axis Parallel Review)** | **Orthogonal Review Axes**: Run **Standards/Fowler Smells** and **Spec Fidelity** reviews in parallel subagents so neither pollutes the other's context. | Embedded in **`ATLAS`** (Standards + Fowler smell baseline vs. Spec/Fixture fidelity) paired with **`SENTINEL`** (Security) and **`SAGE`** (Governance) via `invoke_subagent`. |
| **`retro` (Checks Over Prose Rules)** | **"Default to Building the Check Over Writing the Rule"**: Mechanical violations get a deterministic linter/validator check, not another paragraph in docs. | Embedded in **`SENTINEL`**, `validate_kit.py`, `validate_and_install.ps1`, and `pyproject.toml` (`Ruff` + `Mypy`), catching structural, YAML, and leak violations automatically with Exit Code `0`/`1`. |

#### 2. Complete Reference Map: How to Use the `mattpocock/skills` Workflows in Antigravity

For engineers who wish to adopt or adapt additional workflows from [`github.com/mattpocock/skills`](https://github.com/mattpocock/skills), the table below maps each upstream skill to its operational use case in an Antigravity systems engineering workspace:

| Category | Skill Name | Invocation | Operational Purpose & How to Apply It in Antigravity |
| :--- | :--- | :--- | :--- |
| **Engineering** | **`ask-matt`** | User-invoked | **Workflow Router**: Ask which skill or flow fits your current engineering situation (e.g., starting a new API integration vs. debugging a flaky webhook). |
| **Engineering** | **`grill-with-docs`** | User-invoked | **Domain-Aware Grilling**: Interviews you across the design-tree frontier while simultaneously sharpening terminology in `GEMINI.md` / `GLOSSARY.md` and recording Architecture Decision Records (ADRs). |
| **Engineering** | **`to-spec` & `to-tickets`** | User-invoked | **Spec Synthesis & Tracer Bullets**: Turns a resolved design conversation into a clean specification (`to-spec`) and breaks it into vertical tracer-bullet tickets with explicit blocking edges (`to-tickets`). |
| **Engineering** | **`implement` & `implement-spec`** | User-invoked | **Disciplined Execution**: Drives test-first development (`tdd`) across pre-agreed pure-function seams, running parallel subagents across unblocked tickets and closing out with a two-axis `code-review`. |
| **Engineering** | **`wayfinder`** | User-invoked | **Multi-Session Epic Mapping**: Plans large initiatives (such as the 5-platform `AEGIS` API ingestion pipeline) that exceed a single session as a shared map of decision tickets resolved one at a time. |
| **Engineering** | **`improve-codebase-architecture`** | User-invoked | **Deepening Shallow Modules**: Scans a codebase for shallow pass-through functions or leaky I/O seams, presents an HTML report, and grills through refactoring candidates. |
| **Engineering** | **`triage`** | User-invoked | **Issue State Machine**: Moves operational bugs and feature requests through structured triage states (reproduction, root-cause seam identification, sizing). |
| **Engineering** | **`retro`** | User-invoked | **Agent Environment Retrospective**: Reviews a completed coding session to improve navigation pointers, convert repeated LLM mistakes into deterministic `validate_kit.py` / `Ruff` checks, and prune bloated docs. |
| **Engineering** | **`codebase-design`** | Model-invoked | **Deep Module Vocabulary**: Shared discipline for placing rich behaviour behind small interfaces at clean test seams (`Module`, `Interface`, `Implementation`, `Adapter`, `Depth`, `Seam`, `Leverage`, `Locality`). |
| **Engineering** | **`diagnosing-bugs`** | Model-invoked | **Disciplined Bug Loop**: Redact secrets (`<REDACTED>`) $\rightarrow$ Build a tight (< 2s) red-capable feedback loop $\rightarrow$ Minimise $\rightarrow$ Hypothesise $\rightarrow$ Instrument $\rightarrow$ Fix $\rightarrow$ Regression-test. |
| **Engineering** | **`tdd`** | Model-invoked | **Red-Green-Refactor Slice Loop**: Writes a failing fixture case in `Tests/fixtures/*.json` first, implements the pure function to turn it green, and refactors cleanly. |
| **Engineering** | **`code-review`** | Model-invoked | **Two-Axis Diff Review**: Spawns parallel subagents to check **Standards** (repo rules + Fowler code smells) and **Spec** (requirement fidelity) without cross-polluting context. |
| **Engineering** | **`domain-modeling`** | Model-invoked | **Glossary & Edge-Case Stress Testing**: Challenges vague operational terms against real-world edge cases (e.g., BST timezone shifts, ACL-stripped ServiceNow records, resolved ticket clamping). |
| **Engineering** | **`research` & `prototype`** | Model-invoked | **Isolated Investigation & Throwaway UI/State Prototypes**: Runs primary-source vendor API research in a background subagent (`research`) or builds a single-file HTML prototype (`prototype`) to test dashboard layouts. |
| **Engineering** | **`pr` & `wizard`** | Model-invoked | **High-Signal PRs & Human Setup Wizards**: Formats pull requests with visual summaries, before/after evidence, and blast-radius calls (`pr`), or generates interactive CLI wizards (`wizard`) for human-only setup steps (like registering DPAPI secrets or Azure App Registrations). |
| **Productivity** | **`grill-me` & `grilling`** | User / Model | **Relentless Design-Tree Interview**: The core interview primitive that resolves every branch of a plan before implementation begins. |
| **Productivity** | **`handoff`** | User-invoked | **Session Compaction & Handover**: Compacts the current conversation into `GEMINI.md` or a structured handover artifact so the next session starts with zero context bloat. |
| **Productivity** | **`teach` & `wait-what`** | User-invoked | **Guided Learning & Plain-English Clarification**: Multi-session stateful workspace teaching (`teach`), or an instant plain-English re-explanation using your project's glossary whenever a dense technical message doesn't land (`wait-what`). |
| **Productivity** | **`to-questionnaire`** | User-invoked | **Stakeholder Decision Extraction**: Turns an external dependency you cannot answer alone (e.g., confirming licensed CIS/ISO IDs or PRA impact tolerances with a Risk Officer) into a focused async Markdown questionnaire. |
| **Productivity** | **`writing-for-agents`** | Model-invoked | **Agent Document Architecture**: Governs how `GEMINI.md`, `SKILL.md`, and `agent.md` files are structured using context pointers, progressive disclosure, and co-location. |

---

### 9.4 Copy-Paste Config Analysis & Future API Ingestion Blueprint (`AEGIS`)

To support immediate day-one infrastructure auditing while laying the foundation for future automation, this kit includes [`Governance_Framework/AEGIS_Agent_System_Prompt.md`](Governance_Framework/AEGIS_Agent_System_Prompt.md):

1. **Immediate Interactive Use (Drop-In Config Analysis Prompt)**:
   Engineers can copy the structured prompt block from **Section 2 of `AEGIS_Agent_System_Prompt.md`**, run through the 3-item `<REDACTED>` pre-paste checklist (scrubbing PSKs, SNMP/BGP hashes, and private keys), and paste any **Palo Alto (`PAN-OS`)**, **FortiGate (`FortiOS`)**, **Juniper (`Junos`)**, **Windows Server**, or **Linux Server** configuration directly into chat to receive a complete `Test Library 1.1.0` assessment.
2. **Untested Future Project Idea (Automated Multi-Vendor API Config Ingestion Pipeline)**:
   **Section 4 of `AEGIS_Agent_System_Prompt.md`** provides a complete, ready-to-grill architectural blueprint for building a read-only multi-vendor configuration collector (PAN-OS XML/REST API, FortiOS CMDB REST API, Junos NETCONF/PyEZ, Windows WinRM/CIM JSON, and Linux SSH/Ansible) decoupled at a clean seam from pure Python rule evaluators and offline JSON test fixtures (`Tests/fixtures/aegis_*.json`).

