# CLAUDE.md - PANTHEON AI Kit (Claude Code entry point)

This workspace works with **Google Antigravity**, **Claude Code** and **OpenAI Codex** (Codex gets a generated `AGENTS.md` that points here).
`GEMINI.md` is the single living handover ledger for both tools; Claude Code loads it here via import so there is
one source of truth.

@GEMINI.md

## Claude Code layout

- `.claude/agents/` - the 6 specialist subagents (AEGIS, ATLAS, HERMES, SAGE, SENTINEL, SPARK). Invoke with `@aegis_best_practice`
  or natural language ("Ask AEGIS to audit this FortiGate config").
- `.claude/skills/` - the 8 skills, invoked as `/pantheon-setup`, `/ticket-backlog-governance` etc.
- `.claude/rules/` - always-on S.A.G.E. governance rule.
- **Do not hand-edit `.claude/`.** It is generated from the canonical `.agents/` sources. After changing anything in
  `.agents/`, run `python tools/sync_claude.py` (CI runs `--check` and fails on drift).

## Working rules

- Treat `.env` and `.custom_blocklist.json` as secrets: never read, print, or commit them.
- Run `python validate_kit.py` before committing; it must exit 0.
- When GEMINI.md and this file disagree, update GEMINI.md (it is size-capped at 24,000 bytes).
