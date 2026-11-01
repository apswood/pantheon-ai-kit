"""The kit groups (build_docs.GROUPS) are the single definition; README, guide and GEMINI.md must agree with them."""
from pathlib import Path

import pytest

import build_docs as bd

ROOT = Path(__file__).resolve().parent.parent
PATHS = {e["id"]: e["path"] for e in bd.DOCS_MANIFEST}


def _is_member_page(pid):
    return PATHS[pid].startswith((".agents/agents/", ".agents/skills/"))


def test_every_agent_and_skill_is_in_exactly_one_group():
    expected = {pid for pid in PATHS if _is_member_page(pid)}
    listed = [pid for g in bd.GROUPS for pid in g["members"]]
    assert len(listed) == len(set(listed)), "an entry appears in more than one group"
    assert set(listed) == expected


def test_group_members_exist_in_the_manifest_with_matching_category():
    for g in bd.GROUPS:
        for pid in g["members"]:
            assert pid in PATHS
            entry = next(e for e in bd.DOCS_MANIFEST if e["id"] == pid)
            assert entry["category"] == g["name"], pid


def test_goals_point_at_real_pages():
    assert bd.GOALS
    for _goal, pid in bd.GOALS:
        assert pid in PATHS


def test_groups_have_purpose_and_principles():
    for g in bd.GROUPS:
        assert g["purpose"].strip()
        assert len(g["principles"]) >= 3
        for title, text in g["principles"]:
            assert title.strip() and text.strip()


def test_operational_excellence_keeps_the_lean_core_principles():
    group = next(g for g in bd.GROUPS if g["name"] == "Operational excellence")
    titles = {t for t, _ in group["principles"]}
    assert {"Customer value", "Continuous improvement", "Waste reduction", "Employee empowerment"} <= titles


@pytest.mark.parametrize("doc", ["README.md", "ANTIGRAVITY_SETUP_GUIDE.md", "GEMINI.md"])
def test_docs_name_every_group(doc):
    text = (ROOT / doc).read_text(encoding="utf-8")
    for g in bd.GROUPS:
        assert g["name"] in text, f"{doc} does not mention group '{g['name']}'"


def test_readme_lists_every_principle_and_member_under_its_group():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for g in bd.GROUPS:
        start = text.index(f"### 2.{bd.GROUPS.index(g) + 2} {g['name']}")
        nxt = text.find("\n### 2.", start + 1)
        section = text[start:nxt]
        for title, _ in g["principles"]:
            assert f"**{title}**" in section, f"README group '{g['name']}' is missing principle '{title}'"
        for pid in g["members"]:
            assert f"`{PATHS[pid].split('/')[2]}`" in section, f"README group '{g['name']}' is missing {pid}"
