#!/usr/bin/env python3
"""Catalogue of what a PANTHEON install can enable, and the pure planning step behind `setup.py --profile`.

The kit groups come from build_docs.GROUPS (the single definition). This module adds what the onboarding flow needs
on top: roles, integrations and their .env keys, and the threshold baselines a workspace may override.

Pure vs I/O: everything here reads kit sources and the target workspace but never writes. setup.py applies the plan.

Usage:
  python tools/kit_catalog.py           # print the catalogue as JSON (what /pantheon-setup offers)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
for _p in (ROOT, ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import build_docs  # noqa: E402
import sync_claude  # noqa: E402
import sync_codex  # noqa: E402

PROFILE_FILENAME = "pantheon.profile.json"
INSTALLED_FILENAME = ".pantheon-installed.json"
LOCAL_BASELINES_RULE = ".agents/rules/local-baselines.md"
PROFILE_SCHEMA = 1

TOOLS: Dict[str, str] = {
    "antigravity": "Google Antigravity (.agents/, GEMINI.md)",
    "claude-code": "Claude Code (.claude/, CLAUDE.md)",
    "codex": "OpenAI Codex (.codex/, AGENTS.md) - untested in Codex",
}

# Installed whatever groups are chosen, so the user can always re-run setup.
ALWAYS_SKILLS = ["pantheon-setup"]

# role -> (label, recommended group slugs). The user can add or remove groups after the recommendation.
ROLES: Dict[str, Tuple[str, List[str]]] = {
    "service-desk-lead": ("Service desk or operations lead", ["operational-excellence"]),
    "infrastructure-engineer": ("Infrastructure or network engineer", ["infrastructure-and-resilience"]),
    "developer": ("Platform engineer or developer", ["build-and-secure"]),
    "msp-manager": ("MSP or service delivery manager", ["operational-excellence", "infrastructure-and-resilience"]),
}

# integration -> .env keys (in .env.template order), which of them are secrets, and the skills that use it.
INTEGRATIONS: Dict[str, Dict[str, Any]] = {
    "itsm": {
        "label": "ServiceNow, Jira or another ITSM",
        "keys": ["INSTANCE_URL", "SN_PROD_INSTANCE_URL", "SN_USERNAME", "SN_PASSWORD", "SN_DEPARTMENT_SYS_ID"],
        "secret": ["SN_USERNAME", "SN_PASSWORD"],
        "used_by": ["ticket-backlog-governance", "quality-audit-governance", "support-team-governance-analytics-coaching"],
    },
    "sharepoint": {
        "label": "SharePoint lists via Microsoft Graph",
        "keys": ["GRAPH_RESOURCE", "SHAREPOINT_TENANT_ID", "SHAREPOINT_SITE_PATH"],
        "secret": [],
        "used_by": ["ticket-backlog-governance", "quality-audit-governance"],
    },
    "cosmos": {
        "label": "Azure Cosmos DB (dashboard storage)",
        "keys": ["COSMOS_ENDPOINT", "COSMOS_KEY", "COSMOS_DATABASE", "COSMOS_CONTAINER"],
        "secret": ["COSMOS_KEY"],
        "used_by": ["quality-audit-governance"],
    },
    "teams": {
        "label": "Teams webhook and Power Automate",
        "keys": [
            "TEAMS_DIGEST_WEBHOOK",
            "POWER_AUTOMATE_WEBHOOK",
            "PA_SHAREPOINT_LIST_ID",
            "PA_BACKLOG_LIST_VIEW_ID",
            "PA_TEAMS_CHAT_ID",
            "PA_SP_CONNECTION_NAME",
            "PA_TEAMS_CONNECTION_NAME",
            "PA_FLOW_OWNER_EMAIL",
        ],
        # Webhook URLs carry their own signature, so anyone holding one can post.
        "secret": ["TEAMS_DIGEST_WEBHOOK", "POWER_AUTOMATE_WEBHOOK"],
        "used_by": ["teams-standup-digest-notifier"],
    },
    "dashboard": {
        "label": "Analytics dashboard (FastAPI, Basic Auth)",
        "keys": ["DASHBOARD_USERNAME", "DASHBOARD_PASSWORD", "DASHBOARD_PORT", "DASHBOARD_HOST"],
        "secret": ["DASHBOARD_USERNAME", "DASHBOARD_PASSWORD"],
        "used_by": ["productivity-workload-governance", "quality-audit-governance"],
    },
}

# .env threshold key -> (default, type, what the S.A.G.E. rule calls it). Defaults must match .env.template.
THRESHOLDS: Dict[str, Tuple[Any, str, str]] = {
    "TARGET_DAILY_PACING_MINUTES": (315, "int", "Daily time pacing target (minutes per engineer per day)"),
    "TARGET_DAILY_CLOSED_TASKS": (2, "int", "Closed throughput target (organic tickets per engineer per day)"),
    "TARGET_PROACTIVE_WORK_PCT": (10, "number", "Proactive work ratio (minimum % of recorded time)"),
    "STALE_TICKET_DAYS_THRESHOLD": (5, "int", "Stagnancy threshold (working days without an update)"),
    "BUSINESS_HOURS_START": ("09:00", "time", "Business day start (HH:MM)"),
    "BUSINESS_HOURS_END": ("17:30", "time", "Business day end (HH:MM)"),
    "TIMEZONE": ("Europe/London", "timezone", "Timezone for business hours (IANA name)"),
}
THRESHOLD_GROUP = "operational-excellence"

_TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
_TZ_RE = re.compile(r"^(?:UTC|[A-Za-z_]+(?:/[A-Za-z0-9_+\-]+)+)$")


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def groups() -> Dict[str, Dict[str, Any]]:
    """Group slug -> name, purpose, and the agent and skill folder names in it (from build_docs.GROUPS)."""
    paths = {e["id"]: e["path"] for e in build_docs.DOCS_MANIFEST}
    out: Dict[str, Dict[str, Any]] = {}
    for g in build_docs.GROUPS:
        agents: List[str] = []
        skills: List[str] = []
        for pid in g["members"]:
            parts = paths[pid].split("/")
            (agents if parts[1] == "agents" else skills).append(parts[2])
        out[slug(g["name"])] = {"name": g["name"], "purpose": g["purpose"], "agents": agents, "skills": skills}
    return out


def catalogue() -> Dict[str, Any]:
    """Everything /pantheon-setup can offer, as plain data (printed by `setup.py --detect --json`)."""
    return {
        "groups": groups(),
        "roles": {k: {"label": label, "groups": gs} for k, (label, gs) in ROLES.items()},
        "tools": TOOLS,
        "integrations": INTEGRATIONS,
        "thresholds": {k: {"default": d, "type": t, "label": label} for k, (d, t, label) in THRESHOLDS.items()},
        "always_installed": {"skills": ALWAYS_SKILLS, "rules": "all of .agents/rules/"},
    }


def _check_threshold(key: str, value: Any) -> Optional[str]:
    _default, kind, _label = THRESHOLDS[key]
    if kind == "int":
        ok = isinstance(value, int) and not isinstance(value, bool) and value > 0
    elif kind == "number":
        ok = isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 100
    elif kind == "time":
        ok = isinstance(value, str) and bool(_TIME_RE.match(value))
    else:
        ok = isinstance(value, str) and bool(_TZ_RE.match(value))
    return None if ok else f"thresholds.{key}: {value!r} is not a valid {kind}"


def validate_profile(profile: Any) -> List[str]:
    """Return every problem with a profile; an empty list means it can be applied."""
    if not isinstance(profile, dict):
        return ["profile must be a JSON object"]
    errors: List[str] = []
    known = {"schema", "kit_version", "role", "groups", "tools", "integrations", "thresholds"}
    errors += [f"unknown profile key '{k}'" for k in profile if k not in known]
    if profile.get("schema", PROFILE_SCHEMA) != PROFILE_SCHEMA:
        errors.append(f"schema must be {PROFILE_SCHEMA}")
    role = profile.get("role")
    if role is not None and role not in ROLES:
        errors.append(f"unknown role '{role}' (choose from {', '.join(ROLES)})")

    catalog_groups = groups()
    for field, allowed in (("groups", catalog_groups), ("tools", TOOLS), ("integrations", INTEGRATIONS)):
        value = profile.get(field, [])
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            errors.append(f"{field} must be a list of names")
            continue
        errors += [f"unknown {field[:-1]} '{v}' (choose from {', '.join(allowed)})" for v in value if v not in allowed]
    if isinstance(profile.get("tools"), list) and not profile["tools"]:
        errors.append("choose at least one tool")

    thresholds = profile.get("thresholds", {})
    if not isinstance(thresholds, dict):
        errors.append("thresholds must be an object of KEY: value")
    else:
        for key, value in thresholds.items():
            if key not in THRESHOLDS:
                errors.append(f"unknown threshold '{key}' (choose from {', '.join(THRESHOLDS)})")
            else:
                err = _check_threshold(key, value)
                if err:
                    errors.append(err)
    return errors


def selection(profile: Dict[str, Any]) -> Dict[str, List[str]]:
    """Agent and skill folder names enabled by a (valid) profile."""
    catalog_groups = groups()
    agents: List[str] = []
    skills: List[str] = list(ALWAYS_SKILLS)
    for g in profile.get("groups", []):
        agents += [a for a in catalog_groups[g]["agents"] if a not in agents]
        skills += [s for s in catalog_groups[g]["skills"] if s not in skills]
    return {"agents": sorted(agents), "skills": sorted(skills)}


def threshold_overrides(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Thresholds that differ from the kit defaults."""
    return {k: v for k, v in profile.get("thresholds", {}).items() if v != THRESHOLDS[k][0]}


def render_local_baselines(overrides: Dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {THRESHOLDS[k][2]} | `{k}` | {THRESHOLDS[k][0]} | **{v}** |" for k, v in sorted(overrides.items())
    )
    return (
        "---\n"
        "name: local-baselines\n"
        "description: Workspace-specific governance thresholds that override the S.A.G.E. defaults.\n"
        "---\n\n"
        "# Workspace Rule: Local Governance Baselines\n\n"
        f"<!-- GENERATED by setup.py from {PROFILE_FILENAME} - re-run /pantheon-setup to change these values. -->\n\n"
        "This workspace has agreed its own baselines. Where a value below differs from the S.A.G.E. rule "
        "(`sage-governance-prompt.md`), **use the value below** in every calculation, report and coaching note, "
        "and say in the output that a local baseline was applied.\n\n"
        "| Baseline | `.env` key | Kit default | This workspace |\n"
        "| :--- | :--- | :--- | :--- |\n"
        f"{rows}\n\n"
        "Formulas that derive from these values (for example the intraday pacing target, "
        "`Target = daily minutes x (elapsed minutes / 480)`) use the local value in place of the default.\n"
    )


def env_keys(profile: Dict[str, Any]) -> Dict[str, List[str]]:
    """The .env keys a profile needs, split into plain keys, secret keys and threshold keys."""
    plain: List[str] = []
    secret: List[str] = []
    for name in profile.get("integrations", []):
        spec = INTEGRATIONS[name]
        for key in spec["keys"]:
            (secret if key in spec["secret"] else plain).append(key)
    thresholds = list(THRESHOLDS) if THRESHOLD_GROUP in profile.get("groups", []) else []
    thresholds += [k for k in profile.get("thresholds", {}) if k not in thresholds]
    return {"plain": plain, "secret": secret, "thresholds": thresholds}


def template_values(template_text: str) -> Dict[str, str]:
    """KEY -> placeholder value from .env.template (comments ignored)."""
    out: Dict[str, str] = {}
    for line in template_text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


def _env_value(value: Any) -> str:
    return str(value)


def merge_env(existing: Optional[str], profile: Dict[str, Any], template_text: str) -> Tuple[str, List[str], List[str]]:
    """Return (new .env text, keys added, threshold keys changed). Values already set are never overwritten,
    except threshold keys the profile overrides explicitly. Secret keys are always added empty."""
    keys = env_keys(profile)
    placeholders = template_values(template_text)
    overrides = profile.get("thresholds", {})

    def value_for(key: str) -> str:
        if key in keys["secret"]:
            return ""
        if key in THRESHOLDS:
            return _env_value(overrides.get(key, THRESHOLDS[key][0]))
        return placeholders.get(key, "")

    sections: List[Tuple[str, List[str]]] = [
        (f"{INTEGRATIONS[name]['label']} ({name})", INTEGRATIONS[name]["keys"]) for name in profile.get("integrations", [])
    ]
    if keys["thresholds"]:
        sections.append(("Governance thresholds", keys["thresholds"]))

    if existing is None:
        lines = [
            "# PANTHEON workspace environment - generated by /pantheon-setup from " + PROFILE_FILENAME + ".",
            "# Fill the empty secret values here or in Windows SecretStore. Never commit this file.",
        ]
        added: List[str] = []
        for title, section_keys in sections:
            lines += ["", f"# {title}"]
            for key in section_keys:
                if key not in added:
                    lines.append(f"{key}={value_for(key)}")
                    added.append(key)
        return "\n".join(lines) + "\n", added, []

    present = template_values(existing)
    out_lines: List[str] = []
    changed: List[str] = []
    for line in existing.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line.strip())
        if m and m.group(1) in overrides and m.group(2) != _env_value(overrides[m.group(1)]):
            out_lines.append(f"{m.group(1)}={_env_value(overrides[m.group(1)])}")
            changed.append(m.group(1))
        else:
            out_lines.append(line)

    added = []
    for title, section_keys in sections:
        missing = [k for k in section_keys if k not in present and k not in added]
        if missing:
            out_lines += ["", f"# Added by /pantheon-setup: {title}"]
            for key in missing:
                out_lines.append(f"{key}={value_for(key)}")
                added.append(key)
    text = "\n".join(out_lines) + "\n"
    return (text if (added or changed) else existing), added, sorted(changed)


def desired_files(kit_dir: Path, profile: Dict[str, Any]) -> Dict[str, str]:
    """Every file a profile install should place in the target workspace, as relative path -> text."""
    chosen = selection(profile)
    tools = profile.get("tools", [])
    out: Dict[str, str] = {}

    def copy(rel: str) -> None:
        out[rel] = (kit_dir / rel).read_bytes().decode("utf-8").replace("\r\n", "\n")

    for rel in ("GEMINI.md", "GOVERNANCE.md", ".env.template"):
        copy(rel)
    for name in chosen["agents"]:
        copy(f".agents/agents/{name}/agent.md")
    for name in chosen["skills"]:
        for f in sorted((kit_dir / ".agents" / "skills" / name).rglob("*")):
            if f.is_file():
                copy(f.relative_to(kit_dir).as_posix())
    for rule in sorted((kit_dir / ".agents" / "rules").glob("*.md")):
        if rule.name != Path(LOCAL_BASELINES_RULE).name:
            copy(rule.relative_to(kit_dir).as_posix())

    overrides = threshold_overrides(profile)
    if overrides:
        out[LOCAL_BASELINES_RULE] = render_local_baselines(overrides)

    only = set(chosen["agents"]) | set(chosen["skills"])
    if "claude-code" in tools:
        copy("CLAUDE.md")
        out.update(sync_claude.expected_outputs(src=kit_dir, only=only))
        if overrides:
            out[".claude/rules/local-baselines.md"] = sync_claude.render_rule(
                LOCAL_BASELINES_RULE, out[LOCAL_BASELINES_RULE]
            )
    if "codex" in tools:
        extra = [LOCAL_BASELINES_RULE] if overrides else []
        out.update(sync_codex.expected_outputs(src=kit_dir, only=only, extra_rules=extra))
    return out


def read_json(path: Path) -> Optional[Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def plan_install(kit_dir: Path, target_dir: Path, profile: Dict[str, Any]) -> Dict[str, Any]:
    """Compare what the profile wants with what the target holds. Reads only; never writes."""
    wanted = desired_files(kit_dir, profile)
    add: List[str] = []
    update: List[str] = []
    unchanged: List[str] = []
    for rel, text in sorted(wanted.items()):
        path = target_dir / rel
        if not path.is_file():
            add.append(rel)
        elif path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n") == text:
            unchanged.append(rel)
        else:
            update.append(rel)

    # Only files a previous profile install recorded are ever removed, so user-added files are safe.
    previous = read_json(target_dir / INSTALLED_FILENAME) or {}
    remove = sorted(
        rel for rel in previous.get("files", []) if rel not in wanted and (target_dir / rel).is_file()
    )

    env_path = target_dir / ".env"
    existing_env = env_path.read_text(encoding="utf-8", errors="replace") if env_path.is_file() else None
    template = (kit_dir / ".env.template").read_text(encoding="utf-8")
    new_env, added, changed = merge_env(existing_env, profile, template)
    create_env = existing_env is None and bool(added)
    profile_text = json.dumps(profile, indent=2) + "\n"
    profile_path = target_dir / PROFILE_FILENAME
    profile_changed = not profile_path.is_file() or profile_path.read_text(encoding="utf-8") != profile_text
    return {
        "kit_dir": str(kit_dir),
        "target_dir": str(target_dir),
        "profile": profile,
        "selection": {**selection(profile), "groups": profile.get("groups", []), "tools": profile.get("tools", [])},
        "files": {"add": add, "update": update, "unchanged": unchanged, "remove": remove},
        "env": {
            "create": create_env,
            "add_keys": added,
            "set_keys": changed,
            "secret_keys_to_fill": env_keys(profile)["secret"],
        },
        "local_baselines": threshold_overrides(profile),
        "changes": bool(add or update or remove or added or changed or profile_changed),
        # Not part of the printed plan: what setup.py writes when the plan is applied.
        "_wanted": wanted,
        "_env_text": new_env if (added or changed) else None,
        "_profile_text": profile_text if profile_changed else None,
    }


def main() -> int:
    print(json.dumps(catalogue(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
