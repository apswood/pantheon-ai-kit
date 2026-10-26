"""Offline link checks: built HTML anchors/relative links and Markdown relative links/anchors."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ANTIGRAVITY_DOCS.html"
MARKDOWN = ["README.md", "ANTIGRAVITY_SETUP_GUIDE.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "examples/README.md"]


def github_slug(heading: str) -> str:
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


def test_html_internal_anchors_resolve():
    html = HTML.read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    broken = sorted({h for h in re.findall(r'href="#([^"]+)"', html) if "${" not in h and h not in ids})
    assert broken == []


def test_html_relative_links_point_at_real_files():
    html = HTML.read_text(encoding="utf-8")
    broken = []
    for target in set(re.findall(r'href="(?!https?:|#|mailto:)([^"]+)"', html)):
        path = target.split("#")[0]
        if path and "${" not in path and not (ROOT / path).exists():
            broken.append(target)
    assert sorted(broken) == []


@pytest.mark.parametrize("rel", MARKDOWN)
def test_markdown_links_resolve(rel):
    src = (ROOT / rel).read_text(encoding="utf-8")
    body = re.sub(r"```.*?```", "", src, flags=re.S)  # ignore fenced code
    slugs = {github_slug(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.+)$", body, re.M)}
    problems = []
    for text, target in re.findall(r"\[([^\]]*)\]\(([^)\s]+)\)", body):
        if re.match(r"(https?:|mailto:)", target):
            continue
        path, _, anchor = target.partition("#")
        base = (ROOT / rel).parent
        if path and not (base / path).exists():
            problems.append(f"{rel}: missing file {target}")
        elif not path and anchor and anchor not in slugs:
            problems.append(f"{rel}: missing anchor #{anchor}")
    assert problems == []
