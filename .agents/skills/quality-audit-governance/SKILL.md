---
name: quality-audit-governance
description: Audit ticket quality scorecards using dual-metric reporting (Resolve Pass % and Granular Score %), the KB0016486 rubric, and future-date pending overrides. Use when scoring ticket quality, classifying Service Excellence status bands, or publishing QA tracker results.
---

# Skill: Quality & Audit Governance Analysis

## Purpose & Scope
This skill provides auditing standards for evaluating ITSM ticket quality, technical documentation integrity, SLA compliance, and customer communication. It enforces dual-metric quality reporting, automated rubric scoring, and objective status classifications.

Apply this skill when analyzing QA exports from ServiceNow, SharePoint Quality Tracker lists, or scorecard analytics outputs.

---

## 1. Dual Metric Reporting Standard

Every quality scorecard and review MUST report both the primary binary compliance metric and the secondary granular rubric score side by side:

$$\mathbf{\text{Standard Format: }} \quad \text{Pass Rate \% } (\text{Granular Score \%})$$
$$\mathbf{\text{Example: }} \quad 95.0\% \ (92.3\%)$$

- **Primary Metric — `Resolve Pass %`**: The official binary Pass/Fail rate derived from quality evaluations. Target: $\ge 90.0\%$, High Bar: $\ge 95.0\%$. Drives executive RAG status.
- **Secondary Metric — `Granular Quality Score %`**: Arithmetic mean of detailed, multi-point rubric assessments. Provides nuanced insight into technical documentation depth.

---

## 2. Service Excellence Auditor Status Bandings

When assessing ticket lifecycle quality and customer stewardship, assign exactly one of the following operational bandings:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     SERVICE EXCELLENCE AUDITOR STATUS BANDINGS                   │
├─────────────────────┬────────────────────────────────────────────────────────────┤
│ Status Banding      │ Criteria & Trigger Conditions                              │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ HEALTHY             │ Active owner, recent update, clear next steps, SLA on track│
│                     │ *Future Date Override*: Pending + future 'Date Required'   │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ AT RISK             │ Stagnant 3–5 days without update, or SLA breach imminent   │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ PROGRESSION STALLED │ Stagnant > 5 days (or > 7 days with third-party block)     │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ FAILING             │ Failed QA criteria, unassigned > 48h, or holding updates   │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ CRITICAL            │ Stagnant > 15 days, customer escalation, SLA breached      │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ ARCHIVED            │ Ticket in Resolved or Closed state                         │
└─────────────────────┴────────────────────────────────────────────────────────────┘
```

### The Future Date Pending Override Rule
> [!IMPORTANT]
> **Future Date Pending Rule**: If a ticket is in `Pending` state (e.g. `Pending Customer`, `Pending Vendor`, `Pending Change`) AND the `'Date Required'` field is populated with a **future date**, automatically classify the ticket as **`HEALTHY`**.
>
> A ticket deliberately scheduled for future customer or vendor validation is under active control and must not be penalized as stagnant.

---

## 3. Automated QA Scoring Guidance (KB0016486 Rubric)

Automated quality auditing evaluates tickets across Triage and Resolve stages using the standard KB0016486 rubric:

### 3.1 Rubric Scoring Thresholds

| Evaluation Stage | Incident (`incident`) | Service Request (`sc_req_item`) |
| :--- | :---: | :---: |
| **Triage Stage Max Score** | **6.0 points** | **6.0 points** |
| **Triage Pass Threshold** | $\ge \mathbf{5.0 \text{ points}}$ | $\ge \mathbf{5.0 \text{ points}}$ |
| **Resolve Stage Max Score** | **13.0 points** | **14.0 points** |
| **Resolve Pass Threshold** | $\ge \mathbf{10.5 \text{ points}}$ | $\ge \mathbf{13.0 \text{ points}}$ |
| **Overall Total Max Score** | **19.0 points** | **20.0 points** |
| **Overall Pass Threshold** | $\ge \mathbf{15.5 \text{ points}}$ | $\ge \mathbf{18.0 \text{ points}}$ |

### 3.2 Criteria Evaluated

#### Incident Rubric Checks
- **Triage Stage (6.0 pts max)**:
  1. Relevant technical information collected (+1.0)
  2. Routed to correct assignment group (+1.0)
  3. Valid referral notes documented (+1.0)
  4. Valid triage duration (+1.0)
  5. Correct classification as incident vs request (+1.0)
  6. Response SLA achieved (+1.0)
- **Resolve Stage (13.0 pts max)**:
  1. Full understanding of customer ask demonstrated (+1.0)
  2. Meaningful technical work notes documented (+1.0)
  3. Escalated/routed correctly (+1.0)
  4. Valid referral notes if reallocated (+1.0)
  5. Regular customer updates maintained (+1.0)
  6. Engineer demonstrated technical competence (+1.0)
  7. Three-strike contact rule followed (+1.0)
  8. Clear end-to-end ticket ownership (+1.0)
  9. Appropriate use of ticket states (+1.0)
  10. Comprehensive closure notes with root cause & resolution (+2.0)
  11. Fix SLA and Referral SLA achieved (+2.0)

#### Service Request Rubric Checks
- **Triage Stage (6.0 pts max)**:
  1. Relevant requirements captured (+1.0)
  2. Routed to appropriate fulfillment group (+1.0)
  3. Valid referral notes (+1.0)
  4. Prompt triage completion (+1.0)
  5. Correct classification as request vs incident (+1.0)
  6. Response SLA achieved (+1.0)
- **Resolve Stage (14.0 pts max)**:
  1. Clear understanding of service request (+1.0)
  2. Comprehensive technical progress updates (+1.0)
  3. Regular customer update frequency (+1.0)
  4. Three-strike follow-up process applied (+1.0)
  5. Proactive ownership maintained (+1.0)
  6. Correct state transitions (+1.0)
  7. Appropriate distinction between standard request and change (+2.0)
  8. Line manager or financial approval recorded (+1.0)
  9. Scope creep prevented (+1.0)
  10. Completion SLA and Reassign SLA achieved (+2.0)
  11. Thorough handover and completion notes (+2.0)

### 3.3 Hard Override Rules
- If `Triage QA Failure == true` $\rightarrow$ Triage Pass is forced to **"Fail"**.
- If `QA Failure == true` $\rightarrow$ Resolve Pass and Overall Pass are forced to **"Fail"** regardless of numeric score.

---

## 4. Actionable Report Output Structure

### 4.1 Team Quality Scorecard Table

| Team / Squad | Audited Tickets | Resolve Pass % | Granular Score % | Critical Failures | 6-Month Trend |
| :--- | ---: | ---: | ---: | ---: | :--- |
| Squad Alpha | 45 | 93.3% | 91.8% | 1 | 🟢 Stable (+1.2%) |
| Squad Bravo | 38 | 84.2% | 82.5% | 4 | 🔴 Decline (-4.1%) |

### 4.2 Quality Category Failure Breakdown
Identify the top systemic drivers of quality deductions:
1. **Missing Next Steps**: Updates describe past actions without defining the next action date.
2. **Inadequate Closure Notes**: Technical resolution details omitted (`close_notes` blank or trivial).
3. **Ownership Gaps**: Tickets left unassigned or unworked after queue transfer.
4. **Communication Delays**: Gaps $> 48\text{h}$ in customer-facing communication during investigation.

### 4.3 Longitudinal Quality Observation
Compare current month performance against the rolling 6-month historical average to verify whether quality interventions are yielding sustained improvement.
