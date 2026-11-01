# Examples: try the kit without real data

Everything here is synthetic. IP addresses come from the documentation ranges (RFC 5737), every secret is
`<REDACTED>`, and names are placeholders. These files are repo-only: they are not part of the 37 canonical kit
files and the installers do not copy them.

| File | Use it with | What to look for |
| :--- | :--- | :--- |
| `fortigate_sample.conf` | `aegis_best_practice`, `infrastructure-best-practice-analyser` | Telnet and HTTP on the WAN, `strong-crypto` off, an any/any accept policy with no logging, IKEv1 with 3DES/MD5, a service account trusted from anywhere, syslog disabled |
| `ticket_backlog_sample.csv` | `ticket-backlog-governance`, `sage_governance` | Staleness by class, the escalation override, the future-dated `Pending` override (`INC0000103`), age bands |
| `qa_scorecard_sample.csv` | `quality-audit-governance` | Pass/fail against the KB0016486 thresholds, dual-metric `Pass % (Granular %)` output, the future-date `Pending` override |

The sample tickets were written as if "today" is **26/10/2026**. Tell the agent that date, otherwise it will
measure staleness against the real clock.

## Antigravity

Open the workspace folder, then in the agent chat:

```text
Ask AEGIS to audit examples/fortigate_sample.conf against NIST 800-41 and UKFS outcomes.
/ticket-backlog-governance Treat today as 26/10/2026 and rank examples/ticket_backlog_sample.csv, Top 5 per squad.
/quality-audit-governance Score examples/qa_scorecard_sample.csv. Today is 26/10/2026.
```

## Claude Code

Run `claude` in the workspace folder (it loads `CLAUDE.md`, `.claude/agents/`, `.claude/skills/`):

```text
@aegis_best_practice audit examples/fortigate_sample.conf against NIST 800-41 and UKFS outcomes
/ticket-backlog-governance Treat today as 26/10/2026 and rank examples/ticket_backlog_sample.csv, Top 5 per squad
/quality-audit-governance Score examples/qa_scorecard_sample.csv. Today is 26/10/2026
```

## OpenAI Codex (untested)

Run `codex` in the workspace folder (it loads `AGENTS.md`, `.codex/agents/` and the skills in `.agents/skills/`):

```text
Spawn aegis_best_practice to audit examples/fortigate_sample.conf against NIST 800-41 and UKFS outcomes.
$ticket-backlog-governance Treat today as 26/10/2026 and rank examples/ticket_backlog_sample.csv, Top 5 per squad.
$quality-audit-governance Score examples/qa_scorecard_sample.csv. Today is 26/10/2026.
```

## Using your own data

Scrub it first: replace credentials, pre-shared keys, SNMP communities, tenant IDs and customer names with
`<REDACTED>`, then run `python validate_kit.py` if the files live inside the kit folder.
