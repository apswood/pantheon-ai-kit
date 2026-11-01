# Changelog

All notable changes to the PANTHEON AI Kit. The version lives in `VERSION` and in `kit_manifest.json`.

## [1.0.0] - 2026-11-01

First tagged release.

### Added
- Claude Code compatibility: `CLAUDE.md` plus a generated `.claude/` mirror (6 agents, 7 skills, 1 rule) built from
  the canonical `.agents/` sources by `tools/sync_claude.py`.
- Pinned, verified installs: `PANTHEON_REF` / `-Ref` / `--ref`, and SHA-256 verification of every downloaded file
  against `kit_manifest.json`.
- CI: generated-file drift checks, cross-platform validation, pytest, ruff, PSScriptAnalyzer and gitleaks.
- `tests/` pytest suite; `examples/` synthetic inputs; `CONTRIBUTING.md`, `SECURITY.md`.
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
