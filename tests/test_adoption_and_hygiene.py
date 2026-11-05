import json
from pathlib import Path
import setup as su
import validate_kit as vk

ROOT = Path(__file__).resolve().parent.parent


def test_scan_and_adopt_custom_agents(tmp_path):
    # Simulate a workspace like DecoFit with pre-existing unmanaged agent folders
    agents_dir = tmp_path / ".agents"
    agents_dir.mkdir(parents=True)
    custom_agent_dir = agents_dir / "chloe_rivera_1"
    custom_agent_dir.mkdir()
    (custom_agent_dir / "agent.md").write_text("---\nname: chloe_rivera_1\ndescription: Test\n---\n# Chloe", encoding="utf-8")

    scan = su.scan_workspace_agents_and_skills(tmp_path)
    assert len(scan["unmanaged"]) == 1
    assert scan["unmanaged"][0]["name"] == "chloe_rivera_1"
    assert scan["unmanaged"][0]["kind"] == "agent"

    # Adopt it
    assert su.adopt_items(tmp_path) == 0

    # Verify manifest recorded adoption
    manifest_file = tmp_path / ".pantheon-installed.json"
    assert manifest_file.is_file()
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert "chloe_rivera_1" in manifest["adopted"]["agents"]

    # Scan again -> unmanaged should now be empty
    scan2 = su.scan_workspace_agents_and_skills(tmp_path)
    assert len(scan2["unmanaged"]) == 0


def test_disable_and_enable_agent(tmp_path):
    agents_dir = tmp_path / ".agents" / "agents" / "aegis_best_practice"
    agents_dir.mkdir(parents=True)
    (agents_dir / "agent.md").write_text("dummy", encoding="utf-8")

    # Disable
    assert su.disable_item(tmp_path, "aegis_best_practice") == 0
    assert not agents_dir.exists()
    disabled_path = tmp_path / ".agents" / ".disabled" / "aegis_best_practice"
    assert disabled_path.is_dir()
    assert (disabled_path / "agent.md").read_text(encoding="utf-8") == "dummy"

    # Enable
    assert su.enable_item(tmp_path, "aegis_best_practice") == 0
    assert agents_dir.is_dir()
    assert not disabled_path.exists()


def test_scaffold_agent_and_skill(tmp_path):
    assert su.scaffold_agent(tmp_path, "security_scanner", "Audits security posture") == 0
    agent_file = tmp_path / ".agents" / "agents" / "security_scanner" / "agent.md"
    assert agent_file.is_file()
    content = agent_file.read_text(encoding="utf-8")
    assert "name: security_scanner" in content
    assert "British English (en-GB)" in content

    assert su.scaffold_skill(tmp_path, "cert-expiry-checker", "Checks TLS certificate expiry") == 0
    skill_file = tmp_path / ".agents" / "skills" / "cert-expiry-checker" / "SKILL.md"
    assert skill_file.is_file()
    skill_content = skill_file.read_text(encoding="utf-8")
    assert "name: cert-expiry-checker" in skill_content


def test_uninstall_single_item(tmp_path):
    agents_dir = tmp_path / ".agents" / "agents" / "temp_agent"
    agents_dir.mkdir(parents=True)
    (agents_dir / "agent.md").write_text("test", encoding="utf-8")

    assert su.uninstall_single_item(tmp_path, "temp_agent", force=True) == 0
    assert not agents_dir.exists()


def test_validator_supports_clutter_free_workspace(tmp_path):
    # Populate a minimal clutter-free workspace (no build_docs.py, no ANTIGRAVITY_DOCS.html)
    for f in ["GEMINI.md", "GOVERNANCE.md", ".env.template", ".gitignore", "setup.py", "validate_kit.py", "validate_and_install.ps1"]:
        src = ROOT / f
        if src.is_file():
            (tmp_path / f).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    agents_dir = tmp_path / ".agents" / "agents" / "sage_governance"
    agents_dir.mkdir(parents=True)
    src_agent = ROOT / ".agents" / "agents" / "sage_governance" / "agent.md"
    (agents_dir / "agent.md").write_text(src_agent.read_text(encoding="utf-8"), encoding="utf-8")

    # In minimal workspace mode, validate_structure should pass!
    errors = vk.validate_structure(tmp_path, workspace_mode=True)
    assert errors == []
