#!/usr/bin/env python3
"""validate_kit.py - Antigravity Governance Setup Kit Automated Validator.

Validates workspace discovery structure, YAML frontmatter compliance,
template configuration integrity, and executes strict de-identification
scans to guarantee zero proprietary data leaks.

Uses Python standard library only (zero pip dependencies).

Exit codes:
  0 = All validation checks passed successfully.
  1 = One or more validation checks failed.
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ANSI Color Codes for Terminal Output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

CUSTOM_BLOCKLIST_FILENAME = ".custom_blocklist.json"

# Expected Kit Files Relative to Kit Root (All 24 canonical files)
EXPECTED_FILES = [
    "README.md",
    "ANTIGRAVITY_SETUP_GUIDE.md",
    "ANTIGRAVITY_DOCS.html",
    "GEMINI.md",
    ".env.template",
    ".gitignore",
    "setup.py",
    "build_docs.py",
    "validate_kit.py",
    "validate_and_install.ps1",
    ".agents/agents/aegis_best_practice/agent.md",
    ".agents/agents/atlas_architecture/agent.md",
    ".agents/agents/sage_governance/agent.md",
    ".agents/agents/sentinel_security/agent.md",
    ".agents/agents/spark_disruptor/agent.md",
    ".agents/skills/infrastructure-best-practice-analyser/SKILL.md",
    ".agents/skills/productivity-workload-governance/SKILL.md",
    ".agents/skills/quality-audit-governance/SKILL.md",
    ".agents/skills/support-team-governance-analytics-coaching/SKILL.md",
    ".agents/skills/teams-standup-digest-notifier/SKILL.md",
    ".agents/skills/ticket-backlog-governance/SKILL.md",
    "Governance_Framework/AEGIS_Agent_System_Prompt.md",
    "Governance_Framework/SAGE_Agent_System_Prompt.md",
    ".agents/rules/sage-governance-prompt.md",
]

# Upstream Generic Credential & Secret Leak Patterns (Zero reversible company/personal text in upstream repo)
GENERIC_SECRET_PATTERNS: List[Tuple[str, str]] = [
    ("PEM Private Key Header", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
    ("GitHub Personal Access Token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b"),
    ("AWS Access Key ID", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("Slack API Token", r"\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*\b"),
    ("Hardcoded OAuth Client Secret", r"(?:client_secret|tenant_secret)\s*[:=]\s*['\"][A-Za-z0-9~._\-]{32,64}['\"]"),
]


def decode_blocklist(kit_dir: Optional[Path] = None) -> Tuple[List[Tuple[str, str, Any, bool]], int]:
    """Compile upstream generic secret patterns and optionally load local .custom_blocklist.json ($EncodedRules).

    Returns (rules_list, custom_rule_count) where each rule is (label, pat_str, compiled_regex, is_custom_token).
    Zero reversible organization-specific strings are stored in the upstream script.
    """
    rules: List[Tuple[str, str, Any, bool]] = []
    for label, pat_str in GENERIC_SECRET_PATTERNS:
        compiled = re.compile(pat_str)
        rules.append((label, pat_str, compiled, False))

    custom_count = 0
    if kit_dir is not None:
        custom_file = kit_dir / CUSTOM_BLOCKLIST_FILENAME
        if custom_file.exists() and custom_file.is_file():
            try:
                raw_items = json.loads(custom_file.read_text(encoding="utf-8"))
                if isinstance(raw_items, list):
                    for item in raw_items:
                        if not isinstance(item, dict):
                            continue
                        name_b64 = str(item.get("NameB64", "")).strip()
                        pat_b64 = str(item.get("PatB64", "")).strip()
                        if not name_b64 or not pat_b64:
                            continue
                        token = base64.b64decode(name_b64.encode("utf-8")).decode("utf-8")[::-1]
                        pat_str = base64.b64decode(pat_b64.encode("utf-8")).decode("utf-8")[::-1]
                        compiled = re.compile(pat_str, re.IGNORECASE)
                        rules.append((token, pat_str, compiled, True))
                        custom_count += 1
            except Exception as exc:
                print(
                    f"  {YELLOW}[WARN] Could not parse local {CUSTOM_BLOCKLIST_FILENAME}: {exc}{RESET}",
                    file=sys.stderr,
                )
    return rules, custom_count


def parse_yaml_frontmatter(content: str) -> Tuple[bool, Dict[str, Any], str, str]:
    """Pure regex/standard-library parser for YAML frontmatter between opening/closing --- lines.

    Returns (is_valid, parsed_metadata_dict, markdown_body, error_message).
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return False, {}, "", "Missing opening '---' delimiter on line 1."

    closing_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_idx = i
            break

    if closing_idx == -1:
        return False, {}, "", "Missing closing '---' frontmatter delimiter."

    yaml_block = "\n".join(lines[1:closing_idx])
    body = "\n".join(lines[closing_idx + 1 :]).strip()

    meta: Dict[str, Any] = {}
    current_key = None
    current_list: List[str] = []

    for raw_line in yaml_block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Check for list item under current key
        if line.startswith("- ") and current_key is not None:
            val = line[2:].strip().strip("'\"")
            current_list.append(val)
            meta[current_key] = current_list
            continue

        if ":" in line:
            current_key = None
            current_list = []
            parts = line.split(":", 1)
            k = parts[0].strip()
            v = parts[1].strip()

            if not v or v in (">", ">-", "|", "|-"):
                current_key = k
                current_list = []
                meta[k] = ""
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                val_list = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
                meta[k] = val_list
            elif v.lower() == "true":
                meta[k] = True
            elif v.lower() == "false":
                meta[k] = False
            elif (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                meta[k] = v[1:-1]
            else:
                meta[k] = v

    return True, meta, body, ""


def validate_structure(kit_dir: Path) -> List[str]:
    """Stage 1: Verify presence and non-empty status of all canonical kit files, and check size boundaries."""
    errors = []
    for rel_path in EXPECTED_FILES:
        full_path = kit_dir / rel_path
        if not full_path.exists():
            errors.append(f"Missing required file: {rel_path}")
        elif not full_path.is_file():
            errors.append(f"Expected regular file but found directory: {rel_path}")
        elif full_path.stat().st_size == 0:
            errors.append(f"File is empty (0 bytes): {rel_path}")

    # Boundary check: GEMINI.md must strictly be under 24,000 bytes
    gemini_path = kit_dir / "GEMINI.md"
    if gemini_path.exists() and gemini_path.is_file():
        gemini_size = gemini_path.stat().st_size
        if gemini_size >= 24000:
            errors.append(f"GEMINI.md exceeds 24,000 byte limit: {gemini_size} bytes (maximum allowed: 23,999)")

    return errors


def validate_frontmatters(kit_dir: Path) -> List[str]:
    """Stage 2: Verify YAML frontmatter syntax, required fields, and body content for agents and skills."""
    errors = []

    # 1. Specialist Agents: .agents/agents/*/*.md
    agent_files = sorted(kit_dir.glob(".agents/agents/*/*.md"))
    if len(agent_files) < 4:
        errors.append(f"Expected at least 4 agent.md files in .agents/agents/, found {len(agent_files)}")

    for agent_file in agent_files:
        rel_path = agent_file.relative_to(kit_dir)
        try:
            content = agent_file.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Could not read {rel_path}: {e}")
            continue

        valid, meta, body, err = parse_yaml_frontmatter(content)
        if not valid:
            errors.append(f"{rel_path}: YAML Frontmatter error: {err}")
            continue

        expected_id = agent_file.parent.name
        name = str(meta.get("name", "")).strip()
        if not name:
            errors.append(f"{rel_path}: Frontmatter missing required 'name' field")
        elif name != expected_id:
            errors.append(f"{rel_path}: 'name' '{name}' does not match folder '{expected_id}'")

        description = str(meta.get("description", "")).strip()
        if not description or len(description) < 10:
            errors.append(f"{rel_path}: 'description' is missing or too short (length: {len(description)})")

        tools = meta.get("tools")
        if not isinstance(tools, list) or len(tools) == 0:
            errors.append(f"{rel_path}: 'tools' must be a non-empty list of tool names")

        hidden = meta.get("hidden")
        if hidden is not True and str(hidden).lower() != "true":
            errors.append(f"{rel_path}: 'hidden' must be set to true")

        inherit_custom = meta.get("inheritCustomizations")
        if inherit_custom is not False and str(inherit_custom).lower() != "false":
            errors.append(f"{rel_path}: 'inheritCustomizations' must be set to false")

        inherit_mcp = meta.get("inheritMcp")
        if inherit_mcp is not False and str(inherit_mcp).lower() != "false":
            errors.append(f"{rel_path}: 'inheritMcp' must be set to false")

        if len(body) < 50:
            errors.append(f"{rel_path}: Agent instruction body is missing or too short ({len(body)} chars)")

    # 2. Governance Skills: .agents/skills/*/*.md
    skill_files = sorted(kit_dir.glob(".agents/skills/*/*.md"))
    if len(skill_files) < 5:
        errors.append(f"Expected at least 5 SKILL.md files in .agents/skills/, found {len(skill_files)}")

    for skill_file in skill_files:
        rel_path = skill_file.relative_to(kit_dir)
        try:
            content = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Could not read {rel_path}: {e}")
            continue

        valid, meta, body, err = parse_yaml_frontmatter(content)
        if not valid:
            errors.append(f"{rel_path}: YAML Frontmatter error: {err}")
            continue

        expected_id = skill_file.parent.name
        name = str(meta.get("name", "")).strip()
        if not name:
            errors.append(f"{rel_path}: Frontmatter missing required 'name' field")
        elif not re.match(r"^[a-z0-9-]+$", name):
            errors.append(f"{rel_path}: Skill name '{name}' must be lowercase alphanumeric and hyphenated")
        elif name != expected_id:
            errors.append(f"{rel_path}: 'name' '{name}' does not match directory '{expected_id}'")

        description = str(meta.get("description", "")).strip()
        if not description or len(description) < 15:
            errors.append(f"{rel_path}: 'description' is missing or too short (length: {len(description)})")

        if len(body) < 100:
            errors.append(f"{rel_path}: Skill instructions body is missing or too short ({len(body)} chars)")

    return errors


def scan_deidentification_detailed(
    kit_dir: Path, blocklist: List[Tuple[str, str, Any, bool]]
) -> Tuple[List[str], Dict[str, Any]]:
    """Stage 3: Recursive credential & custom keyword scan with detailed match & severity breakdown."""
    errors: List[str] = []
    excluded_filenames = {
        "setup.py",
        "validate_kit.py",
        "validate_and_install.ps1",
        CUSTOM_BLOCKLIST_FILENAME,
        ".leak_blocklist.json",
    }

    generic_rules_count = sum(1 for _, _, _, is_cust in blocklist if not is_cust)
    custom_stats: List[Dict[str, Any]] = []
    seen_custom: List[Tuple[str, str, int]] = []
    cust_counter = 0
    for token, pat_str, _compiled_pat, is_custom_token in blocklist:
        if is_custom_token:
            cust_counter += 1
            dup_of = 0
            for prev_tok, prev_pat, prev_num in seen_custom:
                if prev_tok == token and prev_pat == pat_str:
                    dup_of = prev_num
                    break
            seen_custom.append((token, pat_str, cust_counter))
            custom_stats.append(
                {
                    "rule_num": cust_counter,
                    "token": token,
                    "pattern": pat_str,
                    "duplicate_of": dup_of,
                    "total_matches": 0,
                    "whole_word_matches": 0,
                    "substring_matches": 0,
                    "whole_words": [],
                    "substring_words": [],
                    "matched_files": set(),
                }
            )

    generic_leak_count = 0
    custom_leak_count = 0

    for root, dirs, files in os.walk(kit_dir):
        dirs[:] = [d for d in dirs if d not in {".git", ".venv", "venv", "__pycache__"}]
        for fname in files:
            if fname in excluded_filenames or fname.endswith((".zip", ".pyc", ".pyo", ".pyd")):
                continue

            file_path = Path(root) / fname
            rel_path = file_path.relative_to(kit_dir)

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                errors.append(f"Could not read file for de-identification scan: {rel_path}: {e}")
                continue

            lines = content.splitlines()
            for line_no, line in enumerate(lines, start=1):
                line_lower = line.lower()
                cust_idx = 0
                for _rule_idx, (token, _pat_str, compiled_pat, is_custom_token) in enumerate(blocklist, start=1):
                    if not is_custom_token:
                        m = compiled_pat.search(line)
                        if m:
                            generic_leak_count += 1
                            snippet = line.strip()[:100]
                            errors.append(
                                f"LEAK [CRITICAL SECRET]: {rel_path} : line {line_no} "
                                f"matched built-in rule '{token}' -> {snippet}"
                            )
                    else:
                        stat = custom_stats[cust_idx]
                        cust_idx += 1
                        regex_m = compiled_pat.search(line)
                        is_regex_match = regex_m is not None
                        is_sub_match = (not is_regex_match) and (token.lower() in line_lower)
                        if is_regex_match or is_sub_match:
                            custom_leak_count += 1
                            stat["total_matches"] += 1
                            stat["matched_files"].add(str(rel_path))
                            snippet = line.strip()[:100]

                            if is_regex_match and regex_m is not None:
                                stat["whole_word_matches"] += 1
                                matched_val = regex_m.group(0)
                                if matched_val.lower() not in [w.lower() for w in stat["whole_words"]]:
                                    stat["whole_words"].append(matched_val)
                                errors.append(
                                    f"LEAK: {rel_path} : line {line_no} matched custom rule #{stat['rule_num']} "
                                    f"('{token}' - whole-word/regex match '{matched_val}') -> {snippet}"
                                )
                            else:
                                stat["substring_matches"] += 1
                                esc_tok = re.escape(token)
                                word_m = re.search(rf"([A-Za-z0-9_.-]*{esc_tok}[A-Za-z0-9_.-]*)", line, re.IGNORECASE)
                                enclosing_word = word_m.group(1).strip(".") if word_m else token
                                if enclosing_word.lower() not in [w.lower() for w in stat["substring_words"]]:
                                    stat["substring_words"].append(enclosing_word)
                                errors.append(
                                    f"LEAK: {rel_path} : line {line_no} matched custom rule #{stat['rule_num']} "
                                    f"('{token}' - substring inside '{enclosing_word}') -> {snippet}"
                                )

    summary = {
        "generic_rules_count": generic_rules_count,
        "generic_leak_count": generic_leak_count,
        "custom_leak_count": custom_leak_count,
        "custom_stats": custom_stats,
    }
    return errors, summary


def scan_deidentification(kit_dir: Path, blocklist: List[Tuple[str, str, Any, bool]]) -> List[str]:
    """Stage 3: Recursive credential & custom keyword scan across all kit files, asserting 0 leaks."""
    errors, _ = scan_deidentification_detailed(kit_dir, blocklist)
    return errors


def validate_configs(kit_dir: Path) -> List[str]:
    """Stage 4: Configuration templates, .gitignore sanity, and living session markers."""
    errors = []

    # Check .gitignore
    gi_path = kit_dir / ".gitignore"
    if gi_path.exists():
        gi_content = gi_path.read_text(encoding="utf-8", errors="replace")
        if ".env" not in gi_content:
            errors.append(".gitignore must contain a rule blocking '.env'")
        if ".venv" not in gi_content and "venv" not in gi_content:
            errors.append(".gitignore must contain a rule blocking virtual environments ('.venv')")
        if CUSTOM_BLOCKLIST_FILENAME not in gi_content and ".custom_blocklist" not in gi_content:
            errors.append(f".gitignore must contain a rule blocking '{CUSTOM_BLOCKLIST_FILENAME}'")
    else:
        errors.append("Missing .gitignore file in kit root")

    # Check .env.template
    env_tpl_path = kit_dir / ".env.template"
    if env_tpl_path.exists():
        tpl_content = env_tpl_path.read_text(encoding="utf-8", errors="replace")
        if "<" not in tpl_content or ">" not in tpl_content:
            errors.append(".env.template should use bracketed placeholders like <YOUR_VALUE>")
        if re.search(r"password\s*=\s*['\"][^<'\"]+['\"]", tpl_content, re.IGNORECASE):
            errors.append(".env.template appears to contain hardcoded plain-text passwords")
    else:
        errors.append("Missing .env.template file in kit root")

    # Check GEMINI.md living session state headers
    gemini_path = kit_dir / "GEMINI.md"
    if gemini_path.exists():
        g_content = gemini_path.read_text(encoding="utf-8", errors="replace")
        if "#" not in g_content:
            errors.append("GEMINI.md missing markdown headers")
        if not re.search(r"##.*Current.*Status", g_content, re.IGNORECASE):
            errors.append("GEMINI.md missing living session marker: 'Current Status'")
        if not re.search(r"##.*Maintenance", g_content, re.IGNORECASE):
            errors.append("GEMINI.md missing living session marker: 'Maintenance Guidelines'")
        if not re.search(r"##.*(?:Done|Milestones|Changelog)", g_content, re.IGNORECASE):
            errors.append("GEMINI.md missing living session marker: 'Project Milestones / What\'s Done'")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated Validator for PANTHEON AI Agent and Skills Setup Kit."
    )
    parser.add_argument(
        "--kit-dir",
        type=str,
        default=None,
        help="Path to kit directory (defaults to current directory or script parent).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output reporting.",
    )
    args = parser.parse_args()

    # Determine kit directory
    if args.kit_dir:
        kit_dir = Path(args.kit_dir).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        if (script_dir / "GEMINI.md").exists():
            kit_dir = script_dir
        elif (Path.cwd() / "ANTIGRAVITY_SETUP_GUIDE.md").exists():
            kit_dir = Path.cwd()
        elif (Path.cwd() / "Antigravity_Governance_Setup_Kit").exists():
            kit_dir = (Path.cwd() / "Antigravity_Governance_Setup_Kit").resolve()
        else:
            kit_dir = Path.cwd()

    print(f"{CYAN}{BOLD}======================================================================{RESET}")
    print(f"{CYAN}{BOLD}  PANTHEON AI SETUP KIT - AUTOMATED VALIDATOR                        {RESET}")
    print(f"{CYAN}{BOLD}======================================================================{RESET}")
    print(f"Target Directory: {kit_dir}\n")

    if not kit_dir.exists() or not kit_dir.is_dir():
        print(f"{RED}[FAIL] Kit directory does not exist or is not a directory: {kit_dir}{RESET}", file=sys.stderr)
        sys.exit(1)

    blocklist, custom_rule_count = decode_blocklist(kit_dir)
    all_errors: List[str] = []

    # 1. Structure & Size Check
    print(f"[{YELLOW}STAGE 1/4{RESET}] Validating directory structure, file existence, and byte limits...")
    struct_errors = validate_structure(kit_dir)
    if struct_errors:
        all_errors.extend(struct_errors)
        print(f"  {RED}[FAIL] Structure check found {len(struct_errors)} issue(s).{RESET}")
        if args.verbose:
            for err in struct_errors:
                print(f"         ! {err}")
    else:
        print(f"  {GREEN}[PASS] All {len(EXPECTED_FILES)} canonical files exist and GEMINI.md is within 24,000 byte limit.{RESET}")

    # 2. YAML Frontmatter Check
    print(f"[{YELLOW}STAGE 2/4{RESET}] Verifying agent and skill YAML frontmatter schemas...")
    fm_errors = validate_frontmatters(kit_dir)
    if fm_errors:
        all_errors.extend(fm_errors)
        print(f"  {RED}[FAIL] Frontmatter check found {len(fm_errors)} issue(s).{RESET}")
        if args.verbose:
            for err in fm_errors:
                print(f"         ! {err}")
    else:
        print(f"  {GREEN}[PASS] All agent and skill YAML frontmatters and instruction bodies are valid.{RESET}")

    # 3. De-Identification & Secret Scan
    print(
        f"[{YELLOW}STAGE 3/4{RESET}] Scanning for live credentials and custom blocklist leaks "
        f"({len(GENERIC_SECRET_PATTERNS)} built-in secret rules + {custom_rule_count} local custom rule(s))..."
    )
    leak_errors, leak_summary = scan_deidentification_detailed(kit_dir, blocklist)
    if leak_errors:
        all_errors.extend(leak_errors)
        print(
            f"  {RED}[FAIL] Detected {len(leak_errors)} sensitive leak occurrence(s) "
            f"({leak_summary['generic_leak_count']} built-in secret, {leak_summary['custom_leak_count']} custom keyword).{RESET}"
        )
        if args.verbose:
            for err in leak_errors:
                print(f"         ! {err}")
    else:
        print(f"  {GREEN}[PASS] Zero credential or blocklisted strings detected across all kit files.{RESET}")

    # 4. Configuration Sanity Check
    print(f"[{YELLOW}STAGE 4/4{RESET}] Checking configuration templates and .gitignore hygiene...")
    cfg_errors = validate_configs(kit_dir)
    if cfg_errors:
        all_errors.extend(cfg_errors)
        print(f"  {RED}[FAIL] Configuration sanity check found {len(cfg_errors)} issue(s).{RESET}")
        if args.verbose:
            for err in cfg_errors:
                print(f"         ! {err}")
    else:
        print(f"  {GREEN}[PASS] Configuration templates and .gitignore filters are fully compliant.{RESET}")

    # Summary & Exit
    print(f"\n{CYAN}{BOLD}======================================================================{RESET}")
    if all_errors:
        print(f"{RED}{BOLD}VALIDATION FAILED - {len(all_errors)} issue(s) detected:{RESET}", file=sys.stderr)
        for err in all_errors:
            print(f"  - {RED}{err}{RESET}", file=sys.stderr)

        if leak_errors or leak_summary["custom_stats"]:
            print(f"\n{YELLOW}----------------------------------------------------------------------{RESET}", file=sys.stderr)
            print(f"{YELLOW}{BOLD}  VALIDATION MATCH SUMMARY - WHAT MATCHED, WHY & HOW SERIOUS IT IS{RESET}", file=sys.stderr)
            print(f"{YELLOW}----------------------------------------------------------------------{RESET}", file=sys.stderr)

            gen_cnt = leak_summary["generic_leak_count"]
            print(f"  {CYAN}[1] Built-In Live Credential & Secret Rules ({len(GENERIC_SECRET_PATTERNS)} rules):{RESET}", file=sys.stderr)
            if gen_cnt == 0:
                print(f"      * Status   : {GREEN}PASS (0 live private keys, API tokens, or OAuth secrets found){RESET}", file=sys.stderr)
                print("      * Severity : NONE (No actual credentials were leaked)", file=sys.stderr)
            else:
                print(f"      * Status   : {RED}FAIL ({gen_cnt} live credential/secret match(es) detected){RESET}", file=sys.stderr)
                print(f"      * Severity : {RED}CRITICAL - Revoke/rotate exposed keys immediately and move to .env{RESET}", file=sys.stderr)

            c_stats = leak_summary["custom_stats"]
            if c_stats:
                print(
                    f"\n  {CYAN}[2] Custom Keyword Rules Breakdown ({CUSTOM_BLOCKLIST_FILENAME} - {len(c_stats)} rule(s)):{RESET}",
                    file=sys.stderr,
                )
                total_sub = sum(s["substring_matches"] for s in c_stats)
                for s in c_stats:
                    dup_note = f" [Duplicate of Rule #{s['duplicate_of']}]" if s["duplicate_of"] > 0 else ""
                    if s["total_matches"] == 0:
                        print(
                            f"      * Custom Rule #{s['rule_num']}: Keyword '{s['token']}' (Pattern: {s['pattern']}){dup_note}",
                            file=sys.stderr,
                        )
                        print("        - Matches : 0 occurrences", file=sys.stderr)
                    else:
                        sample_sub_words = s["substring_words"][:8]
                        sub_word_str = ", ".join(f"'{w}'" for w in sample_sub_words)
                        if len(s["substring_words"]) > 8:
                            sub_word_str += f", ... (+{len(s['substring_words']) - 8} more)"

                        sample_whole_words = s["whole_words"][:6]
                        whole_word_str = ", ".join(f"'{w}'" for w in sample_whole_words)

                        print(
                            f"      * {YELLOW}Custom Rule #{s['rule_num']}: Keyword '{s['token']}' (Pattern: {s['pattern']}){dup_note}{RESET}",
                            file=sys.stderr,
                        )
                        print(
                            f"        - Matches   : {s['total_matches']} occurrence(s) across {len(s['matched_files'])} file(s) "
                            f"({s['whole_word_matches']} whole-word, {s['substring_matches']} partial substring)",
                            file=sys.stderr,
                        )
                        if s["substring_matches"] > 0 and s["whole_word_matches"] == 0:
                            print(
                                f"        - Why       : Matched case-insensitive substring '{s['token']}' inside longer word(s): {sub_word_str}",
                                file=sys.stderr,
                            )
                            print(
                                f"        - Severity  : {GREEN}LOW (Likely False Positive - short/common word matched inside normal code/docs words){RESET}",
                                file=sys.stderr,
                            )
                        elif s["substring_matches"] > 0 and s["whole_word_matches"] > 0:
                            print(
                                f"        - Why       : Matched whole word '{s['token']}' ({s['whole_word_matches']}x) AND substring inside longer word(s) ({s['substring_matches']}x): {sub_word_str}",
                                file=sys.stderr,
                            )
                            print(
                                f"        - Severity  : {YELLOW}LOW / REVIEW (Mostly partial substring matches inside words like {sub_word_str}; review if '{s['token']}' is a confidential org name){RESET}",
                                file=sys.stderr,
                            )
                        else:
                            print(
                                f"        - Why       : Matched whole-word / regex pattern {s['pattern']} for token(s): {whole_word_str}",
                                file=sys.stderr,
                            )
                            print(
                                f"        - Severity  : {YELLOW}MEDIUM / REVIEW (Exact match for your custom keyword; replace with a placeholder if it is a private org/domain name){RESET}",
                                file=sys.stderr,
                            )

                blocklist_path = kit_dir / CUSTOM_BLOCKLIST_FILENAME
                print(f"\n  {CYAN}[3] Overall Severity & Next Steps:{RESET}", file=sys.stderr)
                if gen_cnt == 0 and total_sub > 0:
                    print(f"      * {GREEN}Good news: 0 real credentials or API keys were detected.{RESET}", file=sys.stderr)
                    print(
                        f"      * {total_sub} of {leak_summary['custom_leak_count']} custom match(es) are partial substring matches "
                        f"(e.g. 'bad' matching inside 'badge' or 'good' inside 'Goodhart').",
                        file=sys.stderr,
                    )
                print("      * To clear or reconfigure your custom keyword list, run:", file=sys.stderr)
                print("          python setup.py --configure-scanner", file=sys.stderr)
                print(f"        Or delete '{blocklist_path}' and re-run 'python validate_kit.py'.", file=sys.stderr)

        print(f"{CYAN}{BOLD}======================================================================{RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}{BOLD}ALL VALIDATION CHECKS PASSED SUCCESSFULLY! (Exit Code 0){RESET}")
        print(f"{GREEN}Status: OK - The kit is clean, fully de-identified, and structurally valid.{RESET}")
        if leak_summary["custom_stats"]:
            labels = ", ".join(f"#{s['rule_num']} '{s['token']}'" for s in leak_summary["custom_stats"])
            print(f"Custom Rules Verified ({len(leak_summary['custom_stats'])}): {labels} (0 matches)")
        print(f"{CYAN}{BOLD}======================================================================{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
