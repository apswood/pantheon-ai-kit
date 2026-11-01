# Changelog

All notable changes to the PANTHEON AI Kit. The version lives in `VERSION` and in `kit_manifest.json`.

## [Unreleased]

### Added
- OpenAI Codex compatibility (untested in a live Codex session): `tools/sync_codex.py` generates `AGENTS.md` (tells
  Codex to read `GEMINI.md` and the S.A.G.E. rule; it does not copy them, because Antigravity also reads `AGENTS.md`)
  and `.codex/agents/*.toml` (6 custom agents with a read-only note). Codex reads the canonical `.agents/skills/`
  natively. CI checks the files for drift.
- Canonical file list grows from 48 to 55 files.
- Guided setup: the `/pantheon-setup` skill (new "Getting started" group) asks about role, tools, integrations
  and thresholds, then `setup.py --profile` installs only those into a separate workspace. `--detect --json`
  reports the workspace and the catalogue (`tools/kit_catalog.py`); `--dry-run --json` previews the plan;
  re-running is a no-op and only files a previous profile install recorded are removed. Threshold overrides go
  into `.env` and a generated `local-baselines` rule. `validate_and_install.ps1 -SetupProfile` hands over to it.
- `tools/sync_claude.py` and `tools/sync_codex.py` accept `--target-dir` and `--only`.
- Canonical file list grows from 55 to 60 files (setup skill and its mirror, the sync tools and the catalogue).

### Fixed
- `validate_and_install.ps1 -TargetWorkspaceDir` now also copies `.claude/`, `.codex/`, `CLAUDE.md`, `AGENTS.md`,
  `tools/` and `docs_template/`.

## [1.0.1] - 2026-11-01

### Added
- Docs portal home page: the three kit groups are an accessible tabbed interface (arrow keys, Home/End, remembers the
  last tab, stacked panels without scripting).

### Fixed
- README: the "inspect before running" command had a stray control character in `.\validate_and_install.ps1`.
- Pinned-install examples now reference `v1.0.1`.

## [1.0.0] - 2026-11-01

First tagged release.

### Added
- Claude Code compatibility: `CLAUDE.md` plus a generated `.claude/` mirror (6 agents, 7 skills, 1 rule) built from
  the canonical `.agents/` sources by `tools/sync_claude.py`.
- Pinned, verified installs: `PANTHEON_REF` / `-Ref` / `--ref`, and SHA-256 verification of every downloaded file
  against `kit_manifest.json`.
- CI: generated-file drift checks, cross-platform validation, pytest, ruff, PSScriptAnalyzer and gitleaks.
- `tests/` pytest suite; `examples/` synthetic inputs; `CONTRIBUTING.md`, `SECURITY.md`.
- Kit groups: agents and skills are organised into Operational excellence, Infrastructure and resilience, and Build and secure,
  each with a purpose and core principles. The portal sidebar and home view, README section 2, the setup guide and
  `GEMINI.md` all follow the groups, and the portal home adds an "I want to..." shortcut list.
- Validator: prose file-count check, warning at 80% of the `GEMINI.md` size budget.

### Fixed
- `validate_and_install.ps1 -ValidateOnly` now works on Linux and macOS (dotfiles are hidden there and need `-Force`).

### Changed
- Canonical file list grows from 24 to 48 files (Claude Code mirror, CLAUDE.md, docs template and embedded fonts).
- `build_docs.py` stamps the kit version instead of the wall-clock time, so the HTML is reproducible.
- The leak scanner skips tool caches (`.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `node_modules`).

## Earlier work (pre-1.0.0)

Initial release of the setup kit, zero-clone bootstrap, custom keyword leak scanner, uninstall support, and
the GitHub Pages documentation portal.
