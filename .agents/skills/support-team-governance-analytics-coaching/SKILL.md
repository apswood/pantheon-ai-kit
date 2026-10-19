---
name: support-team-governance-analytics-coaching
description: Synthesise backlog, productivity, and quality metrics into non-accusatory 3-step evidence-based coaching plans. Use when diagnosing time-recording patterns, drafting 1-to-1 coaching notes, or preparing full squad governance packs.
---

# Skill: Support Team Governance Analytics & Evidence-Based Coaching

## Purpose & Scope
This skill translates quantitative operational metrics (time pacing, closed task throughput, quality audit scores, and ticket stagnancy) into constructive, non-accusatory coaching workflows and operational recovery plans.

It provides technical delivery managers, team leads, and governance reviewers with a structured methodology for 1-on-1 performance coaching, standup discussions, and data-driven continuous improvement.

---

## 1. The 3-Step Evidence-Based Coaching Workflow

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      3-STEP EVIDENCE-BASED COACHING WORKFLOW                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   [STEP 1: Direct Dataset Evidence Extraction (Objective Observation)]           │
│   • Ground observations strictly in system-of-record metrics & timestamps        │
│   • Enforce non-accusatory British English ("The visible records show...")        │
│   • Prohibit subjective capability or intent assertions                          │
│                                                                                  │
│                                      ▼                                           │
│                                                                                  │
│   [STEP 2: Operational & Recording Pattern Diagnosis (Systemic Classification)]  │
│   • Classify root causes into systemic archetypes:                               │
│     1. Administrative Under-Recording (real work done, unlogged)                 │
│     2. Tooling / State Misalignment (future date omitted on pending item)        │
│     3. Workflow Boundary Confusion (Request vs Change routing)                   │
│     4. External Dependency Blocker (un-escalated vendor delay)                   │
│                                                                                  │
│                                      ▼                                           │
│                                                                                  │
│   [STEP 3: Actionable Recovery & Calibration Directives (Constructive Resolution)]│
│   • Provide immediate, realistic operational directives for lead and engineer   │
│   • Establish clear next actions, communication templates, and timer habits     │
│   • Document follow-up review dates                                              │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Step 1: Direct Dataset Evidence Extraction

All coaching conversations and written feedback must begin with objective, empirical evidence extracted directly from the dataset.

### Language Protocol
- **Neutral, Verifiable Framing**:
  - *"The visible records show..."*
  - *"Based on recorded timestamps..."*
  - *"Suggests a data-quality validation point..."*
  - *"May reflect an administrative recording pattern..."*
  - *"Based only on the supplied dataset..."*
- **Prohibited Accusatory Phrasing**:
  - ❌ *"Engineer failed to log their hours..."*
  - ❌ *"Technician neglected the ticket..."*
  - ❌ *"Substandard work quality..."*
  - ❌ *"Poor performance / lack of effort..."*

### Concrete Evidence Points
- Exact hours logged vs day-of-week target (e.g. `12.5h actual vs 16.3h target`).
- Timestamp of last customer update (e.g. `Last customer-facing note posted 3.4 days ago`).
- Automated QA rubric score breakdown (e.g. `Overall score 14.0/19.0; deductions in closure notes`).

---

## 3. Step 2: Operational & Recording Pattern Diagnosis

Never assume a metric deficit indicates lack of effort. Systematically evaluate which operational archetype explains the data:

| Archetype | Symptoms in Dataset | Actual Operational Reality |
| :--- | :--- | :--- |
| **1. Administrative Under-Recording** | Low daily pacing ($< 50\%$), sub-minute entries, multiple closed tasks with low logged time. | Real engineering work took place, but engineer delayed booking time until end-of-week. |
| **2. Tooling / State Misalignment** | Ticket marked `PROGRESSION STALLED`, state is `Pending Customer`, but `'Date Required'` is blank or in the past. | Engineer is legitimately awaiting customer feedback, but omitted scheduling a future reminder date. |
| **3. Workflow Boundary Confusion** | Request QA failure due to complex multi-step work undertaken without change record. | Operational work expanded beyond pre-approved request scope into change activity. |
| **4. External Dependency Blocker** | Multi-day stagnancy badge, vendor reference present in journal notes. | Third-party carrier or hardware vendor is delayed, and engineer is waiting passively without formal chasing. |

---

## 4. Step 3: Actionable Recovery & Calibration Directives

Deliver constructive, structured recovery steps tailored to the diagnosed pattern:

### 4.1 Directive for Administrative Under-Recording
- **Immediate Action**: Complete retrospective booking for unlogged working hours within 24 hours.
- **Sustainable Habit**: Adopt real-time time recording using ticket timers or booking 15-minute increments immediately as work concludes.
- **Target**: Maintain $\ge 315 \text{ minutes}$ daily time pacing.

### 4.2 Directive for Tooling / State Misalignment
- **Immediate Action**: Update ticket state to `Pending Customer` and set `'Date Required'` to a realistic future date ($+2$ to $+3$ working days).
- **Template**: Send Chase #2 using standard 3-strike communication template.
- **Result**: Future-date override immediately restores ticket status to `HEALTHY`.

### 4.3 Directive for External Dependency Blocker
- **Immediate Action**: Issue formal escalation to vendor account team referencing vendor ticket reference.
- **Customer Note**: Post holding update to customer summarizing vendor engagement and next update time.

---

## 5. Coaching Deliverables & Output Formats

### 5.1 1-on-1 Engineer Discussion Talking Points
```markdown
### 1-on-1 Coaching Talking Points: [Engineer Name]
- **Operational Context**: Reviewing workload and backlog health for the week ending [Date].
- **Objective Observations**:
  - Recorded 14.5 hours against a cumulative target of 22.3 hours (-7.8h delta).
  - Closed 8 organic tickets (strong throughput, tracking near weekly target).
- **Pattern Exploration**:
  - The high closed task count combined with low logged hours suggests that substantial technical work was delivered but not fully captured in the ticket journal.
- **Collaborative Next Steps**:
  - Identify unrecorded time blocks from calendar/chat and log retrospectives.
  - Review tickets currently in Pending status to ensure future reminder dates are scheduled.
```

### 5.2 Squad Lead Standup Action Item
Summary snippet for the morning standup:
> **Standup Focus**: Squad Alpha has 3 tickets with the `🔥 Multi-Day` badge. Team lead to pair with assignees this morning to confirm third-party vendor escalations and schedule future reminder dates.
