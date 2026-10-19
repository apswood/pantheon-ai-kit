---
name: sage-governance-prompt
description: Always-on Antigravity workspace rule establishing S.A.G.E. (ITIL 4 & ITIL 5) governance frameworks, KPI thresholds, mathematical formulas, and non-accusatory operational standards within the PANTHEON AI Kit for Service Governance.
---

# Workspace Governance Rule: S.A.G.E. Operational Framework (PANTHEON AI Kit)

## 1. Governance Identity & Principles
This workspace operates under the **PANTHEON AI Kit for Service Governance** and its **S.A.G.E.** (**S**ervice **A**nalytics & **G**overnance **E**xpert) framework for Enterprise IT Operations, Service Delivery Teams, and Managed Service Providers (MSPs). All automated analyses, code generation, and team feedback must align with objective, data-driven **ITIL 4 and ITIL 5** service management and non-accusatory governance standards.

---

## 2. Mandatory Mathematical Formulas & Thresholds

### 2.1 Backlog Prioritisation & Staleness
- **Staleness Windows**: Incidents stale after $\ge 8.5 \text{ business hours}$ (Mon–Fri 09:00–17:30); Requests stale after $\ge 17.0 \text{ business hours}$. Weekends excluded.
- **Age Distribution**: 5 tiers: `< 5 Days`, `Age 5 - 15 Days`, `Age 15 - 30 Days`, `Age 30 - 60 Days`, `Age > 60 Days`.
- **Priority Scoring**:
  - 145-Point Relay Engine: Status (max 50) + Review Age (max 40) + Update Stagnancy (max 35) + Age Band (max 20).
  - 4-Criterion Rubric: Status (+50/+40/+30/+20/0) + Stagnancy (+20/+10) + Age (+25/+15/+10/+5/0) + Escalation (+15/+10).
- **Future Date Override**: Any ticket in `Pending` state with a future `'Date Required'` must be classified as **`HEALTHY`**.

### 2.2 Productivity & Capacity Pacing
- **Daily Time Pacing**: **315 minutes** (**5h 15m** / **5.25h**) per engineer per day (70% ticket logging of 37.5h week).
- **Intraday Target**: $\text{Target} = 315 \times (\text{Elapsed Mins} / 480)$.
- **Day-of-Week Cumulative Weights**: Mon 15%, Tue 38%, Wed 62%, Thu 85%, Fri 100%.
- **Capacity Ceiling**: **80% Utilization Pacing** (30.0h/week). Sustainable range: 75% to 115%.
- **Closed Throughput**: **2 closed tickets / day** (10/week) organic throughput, strictly isolating automated event alerts.
- **Proactive Work Ratio**: $\ge 10\%$ of recorded time on Problem (`PRB`/`PTASK`) and Strategic Story (`STRY`) tasks.

### 2.3 Quality Auditing & Coaching
- **Dual-Metric Standard**: Always report `Pass Rate % (Granular Score %)`, e.g. `95.0% (92.3%)`.
- **Auditing Rubric**: KB0016486 automated criteria (Incident 19.0 max, Request 20.0 max).
- **3-Step Coaching Workflow**:
  1. Evidence Extraction (objective timestamps, no blame language).
  2. Recording Pattern Diagnosis (administrative under-recording, tooling gap, external blocker).
  3. Actionable Recovery Directives (concrete next steps, timer habits).

---

## 3. Communication & Language Standards
- Use British English spelling (`analysed`, `prioritised`, `behaviour`).
- Use DD/MM/YYYY dates.
- Frame all findings around system-of-record data (*"the visible records show"*, *"based on recorded timestamps"*).
- Escalate unresolved critical items to `<GOVERNANCE_LEAD_EMAIL>`.
