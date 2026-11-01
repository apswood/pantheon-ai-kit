"""Guided setup: the catalogue, profile validation, and setup.py --profile planning and applying."""
import json
from pathlib import Path

import pytest

import kit_catalog as kc
import setup as su
import sync_claude as sc
import sync_codex as sx

ROOT = Path(__file__).resolve().parent.parent
PROFILES = Path(__file__).resolve().parent / "fixtures" / "profiles"
SECRETS_FILE = "." + "env"


def load(name):
    return json.loads((PROFILES / f"{name}.json").read_text(encoding="utf-8"))


def files_in(target):
    return {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}


# ---------------- catalogue
def test_groups_cover_every_agent_and_skill_once():
    on_disk = {p.parent.name for p in (ROOT / ".agents/agents").glob("*/agent.md")}
    on_disk |= {p.parent.name for p in (ROOT / ".agents/skills").glob("*/SKILL.md")}
    listed = [n for g in kc.groups().values() for n in g["agents"] + g["skills"]]
    assert sorted(listed) == sorted(on_disk)
    assert "pantheon-setup" in kc.groups()["getting-started"]["skills"]


def test_integration_and_threshold_keys_exist_in_env_template():
    template = kc.template_values((ROOT / ".env.template").read_text(encoding="utf-8"))
    for name, spec in kc.INTEGRATIONS.items():
        assert set(spec["keys"]) <= set(template), name
        assert set(spec["secret"]) <= set(spec["keys"]), name
    for key, (default, _kind, _label) in kc.THRESHOLDS.items():
        assert template[key] == str(default), key


def test_roles_recommend_real_groups():
    for _label, groups in kc.ROLES.values():
        assert set(groups) <= set(kc.groups())


# ---------------- profile validation
@pytest.mark.parametrize("name", ["service_desk", "infrastructure"])
def test_fixture_profiles_are_valid(name):
    assert kc.validate_profile(load(name)) == []


@pytest.mark.parametrize(
    "change, needle",
    [
        ({"groups": ["nope"]}, "unknown group 'nope'"),
        ({"tools": []}, "at least one tool"),
        ({"tools": ["vim"]}, "unknown tool 'vim'"),
        ({"integrations": ["salesforce"]}, "unknown integration"),
        ({"thresholds": {"NOT_A_KEY": 1}}, "unknown threshold"),
        ({"thresholds": {"TARGET_DAILY_PACING_MINUTES": "lots"}}, "not a valid int"),
        ({"thresholds": {"BUSINESS_HOURS_START": "9am"}}, "not a valid time"),
        ({"thresholds": {"TARGET_PROACTIVE_WORK_PCT": 150}}, "not a valid number"),
        ({"role": "astronaut"}, "unknown role"),
        ({"password": "x"}, "unknown profile key"),
    ],
)
def test_invalid_profiles_are_rejected(change, needle):
    errors = kc.validate_profile({**load("service_desk"), **change})
    assert any(needle in e for e in errors), errors


# ---------------- planning and applying
def apply(target, profile, **kw):
    return su.apply_profile(ROOT, target, profile, assume_yes=True, **kw)


def test_dry_run_plans_without_writing(tmp_path, capsys):
    assert apply(tmp_path, load("service_desk"), dry_run=True, as_json=True) == 0
    plan = json.loads(capsys.readouterr().out)
    assert not any(tmp_path.iterdir())
    assert plan["changes"] is True
    assert plan["selection"]["agents"] == ["sage_governance"]
    assert ".claude/skills/ticket-backlog-governance/SKILL.md" in plan["files"]["add"]
    assert not any(f.startswith(".codex/") for f in plan["files"]["add"])
    assert plan["env"]["secret_keys_to_fill"] == ["SN_USERNAME", "SN_PASSWORD", "TEAMS_DIGEST_WEBHOOK", "POWER_AUTOMATE_WEBHOOK"]


def test_apply_installs_only_the_selection_and_is_idempotent(tmp_path, capsys):
    assert apply(tmp_path, load("service_desk")) == 0
    got = files_in(tmp_path)
    assert ".agents/skills/pantheon-setup/SKILL.md" in got
    assert ".claude/rules/local-baselines.md" in got and "CLAUDE.md" in got
    assert not any("aegis" in f or f.startswith(".codex/") or f == "AGENTS.md" for f in got)
    assert "**300**" in (tmp_path / kc.LOCAL_BASELINES_RULE).read_text(encoding="utf-8")

    env = (tmp_path / SECRETS_FILE).read_text(encoding="utf-8")
    assert "SN_PASSWORD=\n" in env and "TEAMS_DIGEST_WEBHOOK=\n" in env
    assert "TARGET_DAILY_PACING_MINUTES=300\n" in env and "COSMOS_KEY" not in env
    assert SECRETS_FILE in (tmp_path / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert json.loads((tmp_path / kc.INSTALLED_FILENAME).read_text())["kit_dir"] == str(ROOT)

    before = {f: (tmp_path / f).read_bytes() for f in files_in(tmp_path)}
    capsys.readouterr()
    assert apply(tmp_path, load("service_desk"), dry_run=True, as_json=True) == 0
    assert json.loads(capsys.readouterr().out)["changes"] is False
    assert apply(tmp_path, load("service_desk")) == 0
    assert {f: (tmp_path / f).read_bytes() for f in files_in(tmp_path)} == before


def test_switching_profile_removes_only_what_setup_installed(tmp_path):
    assert apply(tmp_path, load("service_desk")) == 0
    mine = tmp_path / ".claude/skills/my-own/SKILL.md"
    mine.parent.mkdir(parents=True)
    mine.write_text("mine", encoding="utf-8")

    assert apply(tmp_path, load("infrastructure")) == 0
    got = files_in(tmp_path)
    assert ".claude/skills/my-own/SKILL.md" in got
    assert not any(f.startswith(".claude/skills/ticket") or "sage_governance" in f for f in got)
    assert not (tmp_path / ".claude/skills/ticket-backlog-governance").exists()
    assert {".codex/agents/aegis_best_practice.toml", ".codex/agents/hermes_migration.toml", "AGENTS.md"} <= got
    assert kc.LOCAL_BASELINES_RULE not in got


def test_no_integrations_creates_no_env(tmp_path):
    assert apply(tmp_path, load("infrastructure")) == 0
    assert not (tmp_path / SECRETS_FILE).exists()


def test_existing_env_values_are_kept(tmp_path):
    (tmp_path / SECRETS_FILE).write_text("SN_PASSWORD=keep-me\nTARGET_DAILY_PACING_MINUTES=315\nOTHER=1\n", encoding="utf-8")
    assert apply(tmp_path, load("service_desk")) == 0
    env = (tmp_path / SECRETS_FILE).read_text(encoding="utf-8")
    assert "SN_PASSWORD=keep-me\n" in env and "OTHER=1\n" in env
    assert "TARGET_DAILY_PACING_MINUTES=300\n" in env  # explicit profile override wins
    assert env.count("SN_PASSWORD=") == 1 and "INSTANCE_URL=" in env


def test_defaults_write_no_local_baselines_rule(tmp_path):
    profile = {**load("service_desk"), "thresholds": {"TARGET_DAILY_PACING_MINUTES": 315}}
    assert apply(tmp_path, profile) == 0
    assert not (tmp_path / kc.LOCAL_BASELINES_RULE).exists()


def test_profile_install_refuses_the_kit_folder():
    assert su.apply_profile(ROOT, ROOT, load("service_desk"), dry_run=True) == 1


def test_invalid_profile_returns_error(tmp_path):
    assert apply(tmp_path, {**load("service_desk"), "groups": ["nope"]}) == 2
    assert not any(tmp_path.iterdir())


def test_uninstall_removes_profile_install(tmp_path):
    assert apply(tmp_path, load("service_desk")) == 0
    assert su.execute_uninstallation(tmp_path, ROOT, force=True) == 0
    assert files_in(tmp_path) == {SECRETS_FILE, ".gitignore", kc.PROFILE_FILENAME}


def test_cli_shortcut_flags_build_a_profile(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["setup.py", "--target-dir", str(tmp_path), "--groups", "build-and-secure", "--tools", "codex",
         "--set", "TIMEZONE=UTC", "--dry-run", "--json"],
    )
    assert su.main() == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["profile"]["thresholds"] == {"TIMEZONE": "UTC"}
    assert plan["selection"]["agents"] == ["atlas_architecture", "sentinel_security", "spark_disruptor"]


def test_detect_reports_key_names_only(tmp_path, capsys):
    assert apply(tmp_path, load("service_desk")) == 0
    report = su.detect_workspace(ROOT, tmp_path)
    assert report["profile"]["groups"] == ["operational-excellence"]
    assert report["tools_present"]["claude-code"] is True
    assert report["env"]["empty_secret_keys"] == ["SN_USERNAME", "SN_PASSWORD", "TEAMS_DIGEST_WEBHOOK", "POWER_AUTOMATE_WEBHOOK"]
    assert "catalogue" in report


# ---------------- filtered sync tools
def test_sync_tools_filter_to_a_subset():
    only = {"sage_governance", "ticket-backlog-governance"}
    claude = sc.expected_outputs(only=only)
    assert {k for k in claude if not k.startswith(".claude/rules/")} == {
        ".claude/agents/sage_governance.md",
        ".claude/skills/ticket-backlog-governance/SKILL.md",
    }
    codex = sx.expected_outputs(only=only, extra_rules=[kc.LOCAL_BASELINES_RULE])
    assert set(codex) == {".codex/agents/sage_governance.toml", "AGENTS.md"}
    assert "the 1 governance skills" in codex["AGENTS.md"] and kc.LOCAL_BASELINES_RULE in codex["AGENTS.md"]
    assert sc.expected_outputs() == sc.expected_outputs(src=ROOT)


def test_sync_claude_target_dir_writes_subset(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["sync_claude.py", "--target-dir", str(tmp_path), "--only", "spark_disruptor"])
    assert sc.main() == 0
    assert ".claude/agents/spark_disruptor.md" in files_in(tmp_path)
    assert not any(f.startswith(".claude/skills/") for f in files_in(tmp_path))
