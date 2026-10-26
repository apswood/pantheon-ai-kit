#!/usr/bin/env python3
"""Build or verify kit_manifest.json: SHA-256 digests of every canonical kit file.

Hashes are taken over LF-normalised content so Windows (CRLF) checkouts and Linux downloads agree.
The installers (setup.py, validate_and_install.ps1) fetch this manifest from the pinned ref and verify
every downloaded file against it before use.

Usage:
  python tools/build_manifest.py            # rewrite kit_manifest.json
  python tools/build_manifest.py --check    # exit 1 if the manifest is stale (CI)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from validate_kit import EXPECTED_FILES  # noqa: E402

MANIFEST = ROOT / "kit_manifest.json"
VERSION_FILE = ROOT / "VERSION"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def build() -> str:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    files = {rel: digest(ROOT / rel) for rel in sorted(EXPECTED_FILES)}
    return json.dumps({"version": version, "algorithm": "sha256", "files": files}, indent=2) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    expected = build()
    current = MANIFEST.read_bytes().decode("utf-8").replace("\r\n", "\n") if MANIFEST.exists() else None
    if args.check:
        if current != expected:
            print("kit_manifest.json is stale. Run: python tools/build_manifest.py")
            return 1
        print(f"OK: kit_manifest.json covers {len(EXPECTED_FILES)} files.")
        return 0
    MANIFEST.write_bytes(expected.encode("utf-8"))
    print(f"Wrote kit_manifest.json ({len(EXPECTED_FILES)} files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
