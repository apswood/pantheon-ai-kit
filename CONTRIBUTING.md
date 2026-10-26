# Contributing

## Ground rules

- `.agents/` is the source of truth for agents, skills and rules. **Never hand-edit `.claude/`**; it is generated.
- `GEMINI.md` must stay under 24,000 bytes (the validator warns at 19,200).
- No real secrets, tenant IDs, customer names or internal hostnames anywhere. Use `<REDACTED>` or placeholders.
- Never edit `ANTIGRAVITY_DOCS.html` directly. Portal markup, styles and scripts live in `docs_template/`
  (`portal.html`, `portal.css`, `portal.js`; IBM Plex fonts in `docs_template/fonts/` are embedded as base64 so the
  portal works offline). Content rendering lives in `build_docs.py`. The build must stay deterministic: no clocks,
  random values or environment-dependent output.

## Regenerate in this order

After changing `.agents/`, `README.md`, `ANTIGRAVITY_SETUP_GUIDE.md`, `GEMINI.md`, `VERSION` or `build_docs.py`:

```bash
python tools/sync_claude.py       # .agents/ -> .claude/
python build_docs.py              # markdown -> ANTIGRAVITY_DOCS.html
python tools/build_manifest.py    # SHA-256 digests -> kit_manifest.json (must come last)
python validate_kit.py            # must exit 0
pwsh -NoProfile -File validate_and_install.ps1 -ValidateOnly
python -m pytest -q tests
```

CI runs the same steps with `--check` and fails if any generated file is stale. Order matters because the manifest
hashes the generated files.

## Adding or removing a canonical file

Update `EXPECTED_FILES` in `validate_kit.py`, the fallback list in `setup.py`, `$RequiredFiles` in
`validate_and_install.ps1` (and the uninstall prune lists in both installers if it introduces a new folder). Tests in
`tests/test_setup.py` fail when the three lists disagree, and the validator fails when prose states a wrong count.

## Adding an Antigravity tool mapping

If an agent uses a tool not in `TOOL_MAP` (`tools/sync_claude.py`), the sync fails loudly. Map it to the Claude Code
equivalent, or to `None` if there is none.

## Releasing

1. Update `VERSION` and `CHANGELOG.md`, run the regenerate sequence, commit.
2. Tag `vX.Y.Z` and push the tag. Installs pinned to the tag are then immutable.
3. Update README examples if they reference a specific tag.
