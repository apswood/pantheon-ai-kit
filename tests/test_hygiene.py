"""Guards against stray control characters (for example a backslash-v typo turning into a vertical tab)."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CONTROL = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")
CANDIDATES = [
    *ROOT.glob("*.md"),
    *ROOT.glob("*.py"),
    *ROOT.glob("*.ps1"),
    *ROOT.glob("*.yml"),
    *ROOT.glob("docs_template/*"),
    *ROOT.glob("examples/*"),
    *ROOT.glob("tools/*.py"),
    *ROOT.glob(".github/workflows/*.yml"),
]
FILES = [p for p in CANDIDATES if p.is_file() and p.suffix != ".woff2"]


@pytest.mark.parametrize("path", sorted(FILES), ids=lambda p: p.relative_to(ROOT).as_posix())
def test_no_control_characters(path):
    match = CONTROL.search(path.read_text(encoding="utf-8"))
    assert match is None, f"{path.name}: control character {match.group()!r} at offset {match.start()}"
