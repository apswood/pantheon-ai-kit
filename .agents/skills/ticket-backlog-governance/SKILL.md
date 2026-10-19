---
name: ticket-backlog-governance
description: Evaluate ITSM ticket backlog stagnancy (8.5h Incident / 17.0h Request business hours), 5-tier age bands, and 145-point priority scores. Use when calculating staleness, scoring backlog queues, or extracting Top 5 priority tickets per squad.
---

# Skill: Ticket Backlog Governance Analysis

## Purpose & Scope
This skill provides comprehensive operational governance procedures for evaluating ITSM ticket backlogs, detecting queue stagnancy, segmenting aging tickets across 5 granular age tiers, calculating mathematical priority scores, and generating actionable standup priority digests.

Apply this skill whenever analyzing ticket exports from ServiceNow, Jira Service Management, SharePoint backlog review lists (`Daily Backlog Review`), or operational reporting data stores.

---

## 1. Supported Task Classes & Ingestion Rules

Strict class-level filtering must be applied immediately upon ingestion. Only actionable operational task classes are processed:

| Task Class | Standard Prefix | Class Name | Operational Description |
| :--- | :--- | :--- | :--- |
| **Incident** | `INC` | `incident` | Unplanned service interruption or degradation |
| **Service Request** | `RITM`, `ASR` | `sc_req_item` | Standard pre-approved service request or catalog item |
| **Problem** | `PRB` | `problem` | Root-cause investigation of underlying incidents |
| **Problem Task** | `PTASK`, `PRB TASK` | `problem_task` | Discrete investigative or remediation action item |
| **Change Task** | `CTASK`, `CHG TASK` | `change_task` | Discrete scheduled execution step of an approved change |
| **Service Catalog Task** | `SCTASK`, `TASK` | `sc_task` | Technical fulfillment activity under a parent Request |
| **Project Task** | `PRJTASK`, `PTSK` | `pm_project_task` | Structured milestone task under an active project |

### Ingestion Filter Precedence
1. **Class-Level Gate**: Reject any task class not listed in the supported table above.
2. **Manual Exclusion Check**: Check tickets against the local exclusion list (`manual_exclude.txt`). If a ticket number appears in the exclusion list, drop it immediately.
3. **ACL & Ticket Number Integrity**: Filter out incomplete or ACL-restricted records lacking a valid ticket number.
4. **State Filter**: Ingestion processes active, open tickets. Resolved or closed tickets are filtered out or assigned a priority score of 0.

---

## 2. Business Hours & Staleness Logic

Queue stagnancy is determined by business hours elapsed since the last meaningful record update (`sys_updated_on`).

### 2.1 Operating Hours Window
- **Business Days**: Monday through Friday.
- **Operating Hours**: 09:00 to 17:30 (8.5 business hours per working day).
- **Weekend Exclusion**: Saturdays and Sundays contribute 0.0 business hours.
- **Unparseable Dates**: If a timestamp cannot be parsed, treat as stale ($999.0 \text{ hours}$).

### 2.2 Departmental Staleness Thresholds
- **Incidents (`incident`)**: Stale if no update within $\ge 8.5 \text{ business hours}$ (1 working day).
- **Service Requests (`sc_req_item`)**: Stale if no update within $\ge 17.0 \text{ business hours}$ (2 working days).

### 2.3 Permanent Ingestion Overrides (Always Include)
Regardless of calculated business hours, a ticket is always retained as active and stale if:
1. **Escalation Flag**: `escalation != 0` and non-empty (customer or management escalation).
2. **Aged Ticket Rule**: Ticket creation date (`sys_created_on`) was $> 15 \text{ calendar days}$ ago.

---

## 3. 5-Tier Age Bucketing

Every active ticket is classified into exactly one of five non-overlapping age tiers based on calendar days elapsed since creation (`sys_created_on`):

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             5-TIER AGE DISTRIBUTION                              │
├───────────────────┬───────────────────┬───────────────────┬──────────────────────┤
│ Tier Name         │ Calendar Age Band │ Risk Classification                      │
├───────────────────┼───────────────────┼───────────────────┼──────────────────────┤
│ < 5 Days          │ 0 to 4.99 days    │ Fresh intake; active momentum required   │
│ Age 5 - 15 Days   │ 5 to 14.99 days   │ Standard operational fulfillment cycle   │
│ Age 15 - 30 Days  │ 15 to 29.99 days  │ Maturing backlog; elevated friction risk │
│ Age 30 - 60 Days  │ 30 to 59.99 days  │ Aged backlog; requires formal escalation │
│ Age > 60 Days     │ >= 60.0 days      │ Chronic backlog; candidate for root cause│
└───────────────────┴───────────────────┴───────────────────┴──────────────────────┘
```

---

## 4. Backlog Prioritisation Scoring Models

### 4.1 The 145-Point Relay Production Engine Model
When evaluating tickets enriched with review status, review timestamps, and stagnancy metrics (e.g. from a SharePoint backlog review list), calculate the composite priority score (maximum 145 points):

$$\text{Total Priority Score} = S_{\text{status}} + S_{\text{review\_age}} + S_{\text{update}} + S_{\text{age}}$$

#### Criterion 1: Review Status Score ($S_{\text{status}}$, Max 50 pts)
Evaluates the qualitative health status assigned by governance audits:
- `CRITICAL`: 50 pts
- `PROGRESSION STALLED`: 35 pts
- `FAILING`: 30 pts
- Missing / Other / `AT RISK`: 20 pts
- `HEALTHY`: 10 pts
- `ARCHIVED`: 0 pts

#### Criterion 2: Time Since Last Review Score ($S_{\text{review\_age}}$, Max 40 pts)
Evaluates audit currency based on UTC days elapsed since `ReviewDate`:
- Never reviewed / Missing Date / Parse Error: 40 pts
- $> 30 \text{ days}$ since last review: 40 pts
- $> 14 \text{ days}$ since last review: 30 pts
- $> 7 \text{ days}$ since last review: 20 pts
- $> 3 \text{ days}$ since last review: 10 pts
- $\le 3 \text{ days}$ since last review: 0 pts

#### Criterion 3: Days Since Meaningful Update Score ($S_{\text{update}}$, Max 35 pts)
Evaluates technical and customer communication frequency (`Days_Since_Meaningful_Update`):
- Missing / Negative ($< 0$, e.g., -1 indicating no update recorded): 35 pts
- $> 30 \text{ days}$: 30 pts
- $> 15 \text{ days}$: 20 pts
- $> 7 \text{ days}$: 10 pts
- $\le 7 \text{ days}$: 0 pts

#### Criterion 4: Age Status Score ($S_{\text{age}}$, Max 20 pts)
Evaluates structural age based on the 5 age bands:
- `Age > 60 Days`: 20 pts
- `Age 30 - 60 Days` (or `Age > 30`): 15 pts
- `Age 15 - 30 Days` (or `Age > 15`): 10 pts
- `Age 5 - 15 Days` (or `Age < 15`): 5 pts
- `< 5 Days`: 0 pts

#### State Override
If ticket `state` is resolved or closed (`resolved`, `closed complete`, `closed incomplete`, `closed skipped`, `closed`), `Total Priority Score = 0`.

---

### 4.2 The 4-Criterion Governance Framework Rubric
When auditing raw ITSM ticket exports without external review metadata:
1. **Audit Status Weight**:
   - `CRITICAL`: +50 pts | `FAILING`: +40 pts | `PROGRESSION STALLED`: +30 pts | `AT RISK`: +20 pts | `HEALTHY`: 0 pts
2. **Stagnancy Weight (`Days_Since_Meaningful_Update`)**:
   - $> 7 \text{ days}$ without update: +20 pts
   - $> 3 \text{ days}$ without update: +10 pts
3. **Granular Age Band Weight**:
   - `< 5 Days`: +0 pts | `Age 5 - 15`: +5 pts | `Age 15 - 30`: +10 pts | `Age 30 - 60`: +15 pts | `Age > 60`: +25 pts
4. **Escalation & Account Weight**:
   - Escalated (`escalation != 0`): +15 pts
   - Key Account / Dedicated VIP Support Queue: +10 pts

---

## 5. Actionable Report Output Structure

When generating a Backlog Governance Report, structure the deliverable into three clear sections:

### 5.1 Backlog Health Summary Table
Summarizes total queue volumes, aging distribution, and top priority items per operational team:

| Team / Queue | Total Active | Stale (>5d) | Escalated | Age >60d | Top Priority Ticket | Top Score |
| :--- | ---: | ---: | ---: | ---: | :--- | ---: |
| Team Alpha | 24 | 6 | 2 | 3 | INC0123456 | 135 |
| Team Bravo | 18 | 3 | 0 | 1 | RITM0098765 | 110 |

### 5.2 Top 5 Priority Standup Table (Per Team)
Extract the top 5 tickets per operational team sorted by Priority Score descending:
- **Badge Rule**: If `Days_Since_Meaningful_Update >= 3`, append the `🔥 Multi-Day` badge to the ticket identifier.
- **Fields Required**: Ticket Number, Task Class, Short Description, Assigned Engineer, Days Stagnant, Age Band, Priority Score, Recommended Action.

| Ticket | Class | Short Description | Assignee | Stagnant | Age Band | Score | Next Action |
| :--- | :--- | :--- | :--- | ---: | :--- | ---: | :--- |
| **INC0123456** `🔥 Multi-Day` | Incident | Core switch port flapping | Jordan Taylor | 4.2d | Age 15 - 30 | 135 | Chase vendor carrier circuit diagnostics |
| **RITM0098765** | Request | Firewall NAT rule deployment | Alex Smith | 1.8d | Age 5 - 15 | 110 | Schedule implementation window with customer |

### 5.3 Longitudinal Trend Observation
Summarize backlog trajectory across 6 months:
- Is the chronic backlog (`Age > 60 Days`) contracting or expanding?
- Are triage response times preventing tickets from maturing into the `Age 15 - 30 Days` band?
- Document root causes driving stagnant clusters.
