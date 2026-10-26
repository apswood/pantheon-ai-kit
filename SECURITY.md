# Security Policy

## Reporting a vulnerability or a leaked secret

Please do not open a public issue. Use GitHub's private vulnerability reporting for this repository
(Security tab, "Report a vulnerability"). Include the file, what is exposed and how you found it. Expect an
acknowledgement within a few working days.

If you find a credential, tenant ID or internal name that slipped into the repository, report it the same way so
it can be rotated and removed from history.

## What the kit does to protect you

- `validate_kit.py` and `validate_and_install.ps1` scan every kit file for common credential formats and for your
  own organisation keywords (`.custom_blocklist.json`, gitignored, stored reversed and Base64-encoded).
- CI also runs gitleaks as an independent second layer.
- Installers download from a Git ref you choose and verify each file against `kit_manifest.json` (SHA-256).

## Limits you should know about

- The keyword scanner is a safety net, not a guarantee. It finds known patterns and your keywords, not every secret.
  The Base64 and reversal encoding hides keywords from casual reading only; it is not encryption.
- `kit_manifest.json` lives in the same repository as the files it describes. It detects corruption, truncated or
  mixed-ref downloads, but it cannot protect you if the repository itself is compromised. Pin a tag you have
  reviewed (`PANTHEON_REF=vX.Y.Z`) and read `validate_and_install.ps1` before piping it to `iex`.
- If a ref predates the manifest, the installers warn and skip verification.
- Agents are advisory. Review any generated configuration before applying it to production devices.

## Supported versions

Only the latest tagged release and `main` receive fixes.
