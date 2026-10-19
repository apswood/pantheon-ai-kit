---
name: teams-standup-digest-notifier
description: Format daily standup digests capped at Top 5 tickets per squad with multi-day blocker badges and theme-safe Adaptive Cards. Use when building Teams webhook payloads, Power Automate digest flows, or morning standup summaries.
---

# Skill: Teams Standup Digest Notifier

## Purpose & Scope
This skill formats and delivers daily standup notification digests for engineering squads via Microsoft Teams webhooks or Power Automate flows. It isolates the most urgent operational blockers, enforces a strict Top 5 cap per assignment group, highlights chronic stagnancy with multi-day badges, and ensures theme-safe visual rendering.

Apply this skill when preparing daily morning standup summaries or generating webhook payloads for Microsoft Teams channels.

---

## 1. Ingestion & Filtering Pipeline

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                       STANDUP DIGEST FILTERING PIPELINE                          │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 1. INGEST DATASET: Daily Backlog Review records / ServiceNow active queue        │
│ 2. DATE FILTER: ReviewDate == TODAY (yyyy-MM-dd)                                 │
│ 3. STATUS FILTER: Review_Status IN [CRITICAL, FAILING, PROGRESSION STALLED,      │
│                   AT RISK]                                                       │
│ 4. SORT ORDER: Priority Score descending                                         │
│ 5. SQUAD GROUPING: Group tickets by assignment squad                             │
│ 6. TOP 5 CAP: Retain maximum 5 highest-priority tickets per assignment squad     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Visual Formatting & Theme-Safe Standards

### 2.1 Multi-Day Stagnancy Badge
- **Condition**: If `Days_Since_Meaningful_Update >= 3.0` days.
- **Rendering**: Append the `🔥 Multi-Day` badge to the ticket identifier.
- **Purpose**: Instantly alerts the team lead that a ticket has been stalled across multiple consecutive morning standups.

### 2.2 Theme-Safe HTML Color Styling
Microsoft Teams users switch between Light and Dark themes. To prevent illegible black-on-black or white-on-white text, notification cards must use **theme-safe color pairs**:
- **Strict Black Foreground**: All status badges, chips, and table cells must specify `#000000` text color.
- **Light Pastel Backgrounds**:
  - `CRITICAL` / `FAILING`: `#ffe8e8` (soft red)
  - `PROGRESSION STALLED`: `#fff5ee` (soft orange/coral)
  - `AT RISK`: `#fffff0` (soft yellow)
  - `HEALTHY`: `#e8f5e9` (soft green)
  - Informational Warnings: `#fff8e0` (soft amber)

---

## 3. Standup Digest Structure

When assembling the Teams digest payload, format the output as follows:

### 3.1 Digest Header Card
- **Title**: 📋 Morning Standup Backlog Digest — DD/MM/YYYY
- **Executive Summary**: Total tickets audited today, count of Critical/Failing items, and total squads represented.

### 3.2 Squad Priority Tables (Top 5 Per Squad)

#### Squad: `<TEAM_NAME>`

| Ticket | Description | Assignee | Stagnant | Age | Score | Action Needed |
| :--- | :--- | :--- | ---: | :--- | ---: | :--- |
| **INC0123456** `🔥 Multi-Day` | Core switch uplink flap | Jordan Taylor | 4.1d | Age 15 - 30 | 135 | Escalate to vendor TAC |
| **RITM0098765** | ExpressRoute BGP peering | Alex Smith | 2.5d | Age 5 - 15 | 105 | Awaiting customer IP confirmation |
| **INC0123999** | VPN gateway tunnel failure | Morgan Chen | 1.9d | < 5 Days | 90 | Review diagnostic logs |

*(Capped at Top 5 maximum)*

---

### 3.3 Chronic Blocker Callout
Directly below the tables, include a dedicated callout block for all tickets exhibiting the `🔥 Multi-Day` badge:
> **🔥 Chronic Blocker Warning**: The following tickets have had no meaningful update for $\ge 3$ working days and require immediate team lead intervention:
> - `INC0123456` (Jordan Taylor) — 4.1 days stagnant. Next step: Confirm carrier dispatch ticket.
