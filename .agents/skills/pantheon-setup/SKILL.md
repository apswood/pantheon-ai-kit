---
name: pantheon-setup
description: Guided onboarding that sets up a workspace with only the PANTHEON groups, tools, integrations and thresholds the user needs. Use when installing the kit for the first time, enabling or removing kit groups or integrations, or re-tuning governance baselines such as daily pacing minutes or business hours.
---

# Skill: PANTHEON Guided Setup

## Purpose & Scope
Walk the user through setting up a project workspace with the parts of the PANTHEON kit that fit their role, then hand
them a first task to try. The conversation happens here; every change is made by `setup.py`, so a run can be
previewed, repeated and checked.

The kit folder (where `setup.py` lives) stays the full source. The user's **project workspace** receives the selected
agents, skills, mirrors, `.env` keys and a `pantheon.profile.json` that records their choices.

---

## 1. Ground Rules

- **Ask before changing anything.** Show the dry-run plan and wait for a clear yes before applying it.
- **Secrets never in chat.** Never ask for, accept, echo or write passwords, API keys, webhook URLs or tokens. If the
  user pastes one, tell them not to, and do not repeat it. The user fills secret values in `.env` or Windows
  SecretStore themselves; you only tell them which keys to fill.
- **Never read `.env` or `.custom_blocklist.json`.** `setup.py --detect` reports key *names* that are missing or
  empty; that is all you need.
- **Idempotent.** Re-running with the same answers changes nothing. A saved profile means "change my setup", not
  "start again".
- Ask one short question at a time and offer the recommended option first. Use British English.

---

## 2. The Flow

### Step 1 - Detect
Ask which folder is their project workspace if it is not obvious (it must not be the kit folder itself). Find the
kit: if the workspace already has a `.pantheon-installed.json`, its `kit_dir` field says where `setup.py` lives;
otherwise ask. Then run:

```bash
python <kit>/setup.py --detect --json --target-dir <workspace>
```

From the JSON, report in two or three lines: the kit version, whether a `profile` already exists, which tools are
present (`tools_present`), and whether `pwsh` is available. The `catalogue` block lists every group, role,
integration and threshold you may offer; use it rather than memory. If a profile exists, summarise it and ask what
they want to change, then skip to the relevant step.

### Step 2 - Role and groups
Ask what best describes their work, then recommend groups from `catalogue.roles`:

| Role | Recommended groups |
| :--- | :--- |
| Service desk or operations lead | `operational-excellence` |
| Infrastructure or network engineer | `infrastructure-and-resilience` |
| Platform engineer or developer | `build-and-secure` |
| MSP or service delivery manager | `operational-excellence`, `infrastructure-and-resilience` |

Show each recommended group's one-line purpose and members, and let the user add or remove groups. The
`pantheon-setup` skill and the governance rules are always installed.

### Step 3 - Tools
Ask which AI tools they use: `antigravity`, `claude-code`, `codex` (Codex support is untested). Only the matching
folders and entry files are generated.

### Step 4 - Integrations
Ask which systems they will connect, from `catalogue.integrations` (`itsm`, `sharepoint`, `cosmos`, `teams`,
`dashboard`). Skip this if they only want to work from exported files. For each choice, list the `.env` keys it adds
and mark which are secrets they must fill in themselves.

### Step 5 - Thresholds
Only if `operational-excellence` is enabled: show the default baselines from `catalogue.thresholds` (315 min/day,
2 closed tasks/day, 10% proactive, 5-day stagnancy, 09:00-17:30, Europe/London) and ask whether their organisation
uses different values. Overrides go into `.env` and into a generated `local-baselines` rule that tells every agent to
use the local values over the S.A.G.E. defaults.

### Step 6 - Preview
Write the answers to `<workspace>/pantheon.profile.json`:

```json
{"schema": 1, "role": "service-desk-lead", "groups": ["operational-excellence"],
 "tools": ["claude-code"], "integrations": ["itsm", "teams"],
 "thresholds": {"TARGET_DAILY_PACING_MINUTES": 300}}
```

Then show the plan without changing anything:

```bash
python <kit>/setup.py --target-dir <workspace> --profile <workspace>/pantheon.profile.json --dry-run
```

Summarise the files to add, update and remove, and the `.env` keys to add. Call out any **update** or **remove**
lines explicitly. Ask the user to confirm.

### Step 7 - Apply and verify
After a clear yes:

```bash
python <kit>/setup.py --target-dir <workspace> --profile <workspace>/pantheon.profile.json -y
python <kit>/setup.py --target-dir <workspace> --profile <workspace>/pantheon.profile.json --dry-run --json
```

The second command must report `"changes": false`. If it does not, report what is still different; do not retry
blindly. If the user prefers PowerShell, the equivalent is
`pwsh -File <kit>/validate_and_install.ps1 -TargetWorkspaceDir <workspace> -SetupProfile <path>` (it hands over to `setup.py`).

### Step 8 - Try it
Suggest one first task per enabled group, using the synthetic data in `<kit>/examples/`:

| Group | First task |
| :--- | :--- |
| Operational excellence | `/ticket-backlog-governance` on `examples/ticket_backlog_sample.csv` |
| Infrastructure and resilience | `/infrastructure-best-practice-analyser` on `examples/fortigate_sample.conf` |
| Build and secure | Ask SENTINEL to scan the workspace for exposed secrets |

Close with the secret `.env` keys still to fill (`env.secret_keys_to_fill` in the plan) and remind the user to
reopen the workspace in their tool so it loads the new agents and skills.

---

## 3. Changing or Removing a Setup

- **Change**: edit the saved profile (or pass `--groups`, `--tools`, `--integrations`, `--set KEY=VALUE` to
  `setup.py`), then repeat Steps 6-7. Only files a previous setup installed are ever removed.
- **Remove**: `python <kit>/setup.py --uninstall --target-dir <workspace> --dry-run`, then without `--dry-run`
  after the user confirms. `.env` and the profile are kept unless they ask for `--purge-secrets`.
