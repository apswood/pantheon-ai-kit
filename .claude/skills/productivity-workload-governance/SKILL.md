---
name: productivity-workload-governance
description: Calculate engineer daily time pacing (315 min / 5h 15m target), organic closed throughput (2 tickets/day isolating events), proactive work ratio (>=10%), and 80% capacity pacing. Use when auditing time-worked exports, intraday pacing, or weekly productivity reports.
---

# Skill: Productivity & Workload Governance Analysis

## Purpose & Scope
This skill governs engineer capacity, time recording compliance, closed ticket throughput, and proactive work distribution. It enables governance reviewers, technical leads, and managers to monitor operational pacing objectively without administrative micromanagement or subjective bias.

Apply this skill when analyzing time-worked journal exports, timesheet CSV files, closed task dumps, or operational database records.

---

## 1. Standard Governance Targets & Mathematical Models

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         OPERATIONAL GOVERNANCE BENCHMARKS                        │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ Metric                  │ Governance Target       │ Base Workweek Derivation     │
├─────────────────────────┼─────────────────────────┼──────────────────────────────┤
│ Daily Time Pacing       │ 5h 15m (315 mins / 5.25h)│ 70% of 37.5h standard week   │
│ Weekly Ticket Time      │ 26.25 hours             │ 37.5h * 0.70                 │
│ Operational Capacity    │ 80% Utilization (30.0h) │ Standard MSP capacity ceiling│
│ Closed Task Throughput  │ 2 tickets / day (10/wk) │ Organic tasks (excl. events) │
│ Proactive Work Ratio    │ >= 10% of total time    │ Problem, RCA & Initiatives   │
└─────────────────────────┴─────────────────────────┴──────────────────────────────┘
```

### 1.1 Daily Time Worked Pacing (315 Min Target)
- **Target Value**: **5h 15m** = **315 minutes** = **5.25 decimal hours** per working day.
- **Mathematical Derivation**:
  $$\text{Target Weekly Hours} = 37.5 \times 0.70 = 26.25 \text{ hours}$$
  $$\text{Target Daily Hours} = \frac{26.25}{5} = 5.25 \text{ hours} = 315 \text{ minutes}$$
- **Intraday Pro-Rating Formula**:
  When reviewing time logs mid-day during a standard 09:00–17:00 (480-minute) window:
  $$\text{Adjusted Daily Target (mins)} = 315 \times \left( \frac{\text{Elapsed Working Minutes}}{480} \right)$$
- **Pacing Performance Ratio**:
  $$\text{Pacing Target \%} = \left( \frac{\text{Actual Recorded Hours}}{\text{Pacing Target Hours}} \right) \times 100$$

---

### 1.2 Weekly Cumulative Day-of-Week Pacing Weights
Ticket logging naturally varies across weekdays. Time pacing applies an empirical day-of-week weighting model:

| Day of Week | Index | Daily Weight | Cumulative Weight | Target Hours (Cumulative) | Target Tasks (Cumulative) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Monday** | 0 | 15% (0.15) | **15.0%** (0.15) | 3.94h | 1.5 tasks |
| **Tuesday** | 1 | 23% (0.23) | **38.0%** (0.38) | 9.98h | 3.8 tasks |
| **Wednesday** | 2 | 24% (0.24) | **62.0%** (0.62) | 16.28h | 6.2 tasks |
| **Thursday** | 3 | 23% (0.23) | **85.0%** (0.85) | 22.31h | 8.5 tasks |
| **Friday** | 4 | 15% (0.15) | **100.0%** (1.00) | 26.25h | 10.0 tasks |
| **Saturday / Sunday**| 5, 6 | 0% (0.00) | 100.0% (1.00) | 26.25h | 10.0 tasks |

#### Pacing Formulas
$$\text{Pacing Target Hours} = 26.25 \times \text{Cumulative Weight}$$
$$\text{Pacing Delta (Hours)} = \text{Actual Hours Logged} - \text{Pacing Target Hours}$$
$$\text{End-of-Week Projection} = \frac{\text{Actual Hours Logged}}{\text{Cumulative Weight}} \quad (\text{for Cumulative Weight} > 0)$$

#### Performance Status Classification
- **AHEAD** (🟢): $\text{Pacing Delta} \ge +2.0 \text{ hours}$
- **BEHIND** (🔴): $\text{Pacing Delta} < -1.0 \text{ hours}$
- **ON TRACK** (🔵): $-1.0 \text{ hours} \le \text{Pacing Delta} < +2.0 \text{ hours}$

---

### 1.3 80% Utilization Capacity Pacing vs 70% Ticket Logging Target
- **70% Ticket Logging Target (26.25h / 315 min)**: Strict customer-facing ticket booking target. Leaves 30% (11.25h/week) for team standups, training, customer meetings, and administration.
- **80% Utilization Pacing (30.0h / 360 min)**: Standard MSP overall operational utilization ceiling used in capacity forecasting:
  - **Sustainable**: $75\% \le \text{Utilization} \le 115\%$
  - **Over-Utilisation Risk**: $\text{Utilization} > 115\%$ (burnout and error risk)
  - **Under-Utilised**: $\text{Utilization} < 75\%$ (available capacity or recording deficit)

---

### 1.4 Closed Task Throughput & Event Isolation
- **Throughput Benchmark**: **2 closed tickets / day** = **10 closed tickets / week**.
- **Task Delta Formula**:
  $$\text{Target Closed Tasks} = 10.0 \times \text{Cumulative Weight}$$
  $$\text{Task Delta} = \text{Total Organic Closed Tasks} - \text{Target Closed Tasks}$$
- **Status Classification**:
  - **AHEAD** (🟢): $\text{Task Delta} \ge +1.0$
  - **BEHIND** (🔴): $\text{Task Delta} < -1.0$
  - **ON TRACK** (🔵): $-1.0 \le \text{Task Delta} < +1.0$
- **Mandatory Event Isolation**: Automated alert notifications (e.g. synthetic monitoring pings, auto-closing alerts) must be reported separately in an `Events` column and excluded from organic closed task throughput.

---

### 1.5 Proactive Work Allocation
- **Target**: $\ge 10\%$ of total recorded time dedicated to root-cause prevention and structural improvement.
- **Formula**:
  $$\text{Proactive Work \%} = \left( \frac{\text{Hours on PRB} + \text{Hours on PRB TASK} + \text{Hours on STRY}}{\text{Total Recorded Hours}} \right) \times 100$$

---

## 2. Work-Type Prefix Classification

Map every time entry to its operational work category using task number prefixes:

| Task Prefix | Operational Classification | Governance Category | Target Allocation |
| :--- | :--- | :--- | :--- |
| **INC** | Incident Management | Reactive Operational | Core customer support |
| **RITM**, **ASR** | Service Request | Planned Fulfillment | SLA standard delivery |
| **CHG** | Change Request | Planned Maintenance | Scheduled changes |
| **PRB**, **PRB TASK** | Problem / Root Cause Analysis | **Proactive Improvement** | Part of $\ge 10\%$ target |
| **STRY** | Strategic Initiative / Story | **Proactive Improvement** | Part of $\ge 10\%$ target |
| **PRJ**, **PTASK**, **PTSK** | Project Delivery Task | Project Delivery | Billable / capital project |

---

## 3. Time Recording Anomaly Detection

Flag operational entries meeting any of the following data-quality risk triggers:
- **Sub-Minute Bookings**: Single time entry $< 60 \text{ seconds}$. Indicates default button clicking without actual time tracking.
- **Low Daily Capture**: Total daily logged time $< 50\%$ of target ($< 2.62 \text{ hours}$ or $< 157.5 \text{ mins}$). Indicates delayed or batched end-of-week entry habits.
- **Large Single Bookings**:
  - $> 4 \text{ hours}$: Flagged as "Large Booking" requiring worknote detail verification.
  - $> 8 \text{ hours}$: Flagged as "Exceeds Standard Working Day".
  - $> 24 \text{ hours}$: Flagged as "High-Priority Validation Point" (frequently caused by an unstopped timer).

---

## 4. Actionable Report Output Structure

### 4.1 Daily Engineer Pacing & Throughput Table

| Engineer | Squad | Logged (h) | Target (h) | Pacing % | Status | Closed | Target | Task Delta | Proactive % | Anomalies |
| :--- | :--- | ---: | ---: | ---: | :---: | ---: | ---: | ---: | ---: | :--- |
| Alex Smith | Squad Alpha | 17.5 | 16.3 | 107.4% | 🟢 AHEAD | 7 | 6.2 | +0.8 | 14.2% | None |
| Taylor Reed | Squad Beta | 12.0 | 16.3 | 73.6% | 🔴 BEHIND | 4 | 6.2 | -2.2 | 4.5% | Low daily capture |

### 4.2 Work-Type Distribution Split
Summarize team-wide hours across categories:
- Reactive Incidents: X.X hours (XX.X%)
- Service Requests: X.X hours (XX.X%)
- Proactive Problems & Stories: X.X hours (XX.X%) [Target: >= 10%]
- Project Delivery: X.X hours (XX.X%)

### 4.3 Constructive Governance Coaching Snippet
Provide an objective, non-accusatory coaching draft for any engineer showing pacing deficits or recording anomalies, referencing the **3-Step Evidence-Based Coaching Workflow**.
