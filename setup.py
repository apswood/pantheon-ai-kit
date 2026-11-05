#!/usr/bin/env python3
"""setup.py - PANTHEON AI Agent and Skills Setup Kit for Service Governance Bootstrapper.

Provides zero-clone remote kit download (when run standalone), cross-platform
workspace initialization, runtime readiness inspection, virtual environment (.venv)
provisioning, .env.template mirroring, optional custom keyword leak scanner builder
(.custom_blocklist.json), local HTML wiki compilation, and automated kit validation.

================================================================================
ARCHITECTURAL NOTE: SYSTEMS SCRIPTING (POWERSHELL) VS. GENERAL-PURPOSE (PYTHON)
================================================================================
For Systems Engineers and Technical Leaders adopting AI-assisted development in
Antigravity, one of the most consequential architectural decisions is choosing
when to write automation in a systems-familiar shell language (PowerShell) vs.
a general-purpose programming language (Python)—and when to combine both.

1. WHY PYTHON IS RECOMMENDED FOR DATA ANALYSIS, INTEGRATIONS & AI PAIR-PROGRAMMING:
   - AI Code Generation Quality: Frontier AI models (Gemini, Claude, GPT) have
     their deepest training distribution in Python. AI agents produce cleaner,
     more idiomatic, and significantly less bug-prone code in Python on the
     first pass than in shell languages.
   - Data Analysis & Mathematical Clarity: Multi-dimensional KPI calculations,
     SLA business-hours arithmetic, regex journal cleaning, and longitudinal
     aggregations are concise and deterministic in Python (especially with
     `pandas`, `numpy`, and standard library `datetime`/`collections`).
   - Cross-Platform Portability & Packaging: Python runs identically on Windows
     workstations, Linux CI/CD runners, and Docker/Azure Container Apps, and can
     be compiled into standalone single-file `.exe` binaries (`PyInstaller`)
     for colleagues who have no development tools installed.
   - Fast Static Verification: Tools like `Ruff` and `Mypy` statically verify
     AST syntax, imports, and types in milliseconds before any API is called.

2. WHEN TO CHOOSE POWERSHELL (7.2+):
   - Windows & M365 OS-Native Integration: Interacting directly with Windows
     DPAPI (`Microsoft.PowerShell.SecretStore`), Active Directory, Windows Task
     Scheduler, Registry/Services, or Exchange/Teams administration modules.
   - Zero-Python Windows Jump Hosts: Running self-contained operational relays
     on locked-down Windows servers where installing Python is restricted.
   - IMPORTANT GOTCHA: Always target PowerShell 7.2+ (`pwsh`), never legacy
     Windows PowerShell 5.1 (`powershell.exe`), which lacks `-SkipHttpErrorCheck`,
     adds UTF-8 BOMs by default, and unwraps single-element arrays in JSON.

3. WHEN & HOW TO COMBINE LANGUAGES (POLYGLOT PATTERNS):
   - Pattern A (Thin OS Wrapper + Python Analytical Core): Use PowerShell for
     Task Scheduler triggers or DPAPI SecretStore retrieval, and invoke Python
     for REST API pagination, KPI math, and HTML/Markdown report generation.
   - Pattern B (Dual-Runtime Parity via Shared JSON Fixtures): When maintaining
     both a Python and PowerShell port of a critical relay, isolate pure logic
     (`src/` in Python, `Private/` in PowerShell) and validate both against the
     exact same language-neutral `Tests/fixtures/*.json` test cases.
================================================================================
"""

import argparse
import base64
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import venv
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CUSTOM_BLOCKLIST_FILENAME = ".custom_blocklist.json"
# Git ref (tag, branch or commit SHA) to download from. Pin to a release tag (e.g. v1.0.0) for reproducible installs.
# Override with --ref or the PANTHEON_REF environment variable.
REPO_REF = os.environ.get("PANTHEON_REF") or "main"
MANIFEST_FILENAME = "kit_manifest.json"


def repo_zip_url(ref: str) -> str:
    return f"https://github.com/apswood/pantheon-ai-kit/archive/{ref}.zip"


def repo_raw_base_url(ref: str) -> str:
    return f"https://raw.githubusercontent.com/apswood/pantheon-ai-kit/{ref}"

try:
    from validate_kit import EXPECTED_FILES as _CANONICAL_FILES  # type: ignore[import-not-found]

    REQUIRED_KIT_FILES: List[str] = list(_CANONICAL_FILES)
except Exception:
    REQUIRED_KIT_FILES = [
        "README.md",
        "ANTIGRAVITY_SETUP_GUIDE.md",
        "ANTIGRAVITY_DOCS.html",
        "GEMINI.md",
        "GOVERNANCE.md",
        ".env.template",
        ".gitignore",
        "setup.py",
        "install.sh",
        "install.cmd",
        "build_docs.py",
        "validate_kit.py",
        "validate_and_install.ps1",
        ".agents/agents/aegis_best_practice/agent.md",
        ".agents/agents/atlas_architecture/agent.md",
        ".agents/agents/hermes_migration/agent.md",
        ".agents/agents/sage_governance/agent.md",
        ".agents/agents/sentinel_security/agent.md",
        ".agents/agents/spark_disruptor/agent.md",
        ".agents/skills/infrastructure-best-practice-analyser/SKILL.md",
        ".agents/skills/pantheon-setup/SKILL.md",
        ".agents/skills/productivity-workload-governance/SKILL.md",
        ".agents/skills/quality-audit-governance/SKILL.md",
        ".agents/skills/server-migration-infrastructure-replication/SKILL.md",
        ".agents/skills/support-team-governance-analytics-coaching/SKILL.md",
        ".agents/skills/teams-standup-digest-notifier/SKILL.md",
        ".agents/skills/ticket-backlog-governance/SKILL.md",
        "Governance_Framework/AEGIS_Agent_System_Prompt.md",
        "Governance_Framework/HERMES_Agent_System_Prompt.md",
        "Governance_Framework/SAGE_Agent_System_Prompt.md",
        ".agents/rules/sage-governance-prompt.md",
        "CLAUDE.md",
        ".claude/agents/aegis_best_practice.md",
        ".claude/agents/atlas_architecture.md",
        ".claude/agents/hermes_migration.md",
        ".claude/agents/sage_governance.md",
        ".claude/agents/sentinel_security.md",
        ".claude/agents/spark_disruptor.md",
        ".claude/skills/infrastructure-best-practice-analyser/SKILL.md",
        ".claude/skills/pantheon-setup/SKILL.md",
        ".claude/skills/productivity-workload-governance/SKILL.md",
        ".claude/skills/quality-audit-governance/SKILL.md",
        ".claude/skills/server-migration-infrastructure-replication/SKILL.md",
        ".claude/skills/support-team-governance-analytics-coaching/SKILL.md",
        ".claude/skills/teams-standup-digest-notifier/SKILL.md",
        ".claude/skills/ticket-backlog-governance/SKILL.md",
        ".claude/rules/sage-governance-prompt.md",
        "AGENTS.md",
        ".codex/agents/aegis_best_practice.toml",
        ".codex/agents/atlas_architecture.toml",
        ".codex/agents/hermes_migration.toml",
        ".codex/agents/sage_governance.toml",
        ".codex/agents/sentinel_security.toml",
        ".codex/agents/spark_disruptor.toml",
        "docs_template/portal.html",
        "docs_template/portal.css",
        "docs_template/portal.js",
        "docs_template/fonts/IBMPlexSans-var.woff2",
        "docs_template/fonts/IBMPlexMono-400.woff2",
        "docs_template/fonts/LICENSE.txt",
        "tools/sync_claude.py",
        "tools/sync_codex.py",
        "tools/kit_catalog.py",
    ]


LANGUAGE_RECOMMENDATION_MATRIX: List[Tuple[str, str, str]] = [
    (
        "Data Analysis, KPI Math & Scoring Rubrics",
        "Python (Primary)",
        "Clean datetime/float math, pandas/stdlib ergonomics, highest AI code accuracy",
    ),
    (
        "REST API Ingestion (ITSM, Graph, Webhooks)",
        "Python (Primary)",
        "TCP session pooling, backoff/retry control, strict JSON schema typing",
    ),
    (
        "Web Dashboards, API Proxies & Containers",
        "Python (FastAPI)",
        "Native async web servers, auth middleware, Linux Docker container portability",
    ),
    (
        "Portable Single-File CLI Executables (.exe)",
        "Python (PyInstaller)",
        "Compiles script + runtime + libraries into a zero-dependency Windows binary",
    ),
    (
        "Windows DPAPI Vaults, AD & M365 Cmdlets",
        "PowerShell 7.2+",
        "Native SecretStore, ActiveDirectory, and MicrosoftTeams module integration",
    ),
    (
        "Host Task Scheduler & OS Service Wrappers",
        "PowerShell 7.2+",
        "Direct Windows Task Scheduler, Event Log, and WMI/CIM orchestration",
    ),
]


def verify_kit_integrity(kit_dir: Path, ref: str) -> None:
    """Verify downloaded files against kit_manifest.json fetched separately from the pinned ref.

    Raises RuntimeError on any digest mismatch or missing file. A manifest that cannot be fetched only warns,
    so installs from refs that predate the manifest still work.
    """
    url = f"{repo_raw_base_url(ref)}/{MANIFEST_FILENAME}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Pantheon-AI-Kit-Bootstrap/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            manifest = json.loads(resp.read().decode("utf-8"))
        expected: Dict[str, str] = manifest["files"]
    except Exception as exc:
        print(f"                   [WARN] Integrity manifest unavailable at ref '{ref}' ({exc}); skipping SHA-256 verification.")
        return

    bad: List[str] = []
    for rel_path, want in expected.items():
        path = kit_dir / rel_path
        if not path.is_file():
            bad.append(f"{rel_path} (missing)")
            continue
        got = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        if got != want:
            bad.append(f"{rel_path} (digest mismatch)")
    if bad:
        raise RuntimeError(
            f"Integrity check FAILED for ref '{ref}' - refusing to continue:\n  " + "\n  ".join(bad)
        )
    print(f"                   [OK] SHA-256 verified {len(expected)} files against {MANIFEST_FILENAME} (ref '{ref}', v{manifest.get('version', '?')}).")


def ensure_kit_files_present(
    kit_dir: Path,
    include_docs: bool = False,
    include_prompts: bool = False,
    include_examples: bool = False,
) -> None:
    """Download missing kit components from GitHub if setup.py is executed standalone without cloning.
    Installs minimal runtime essentials into client workspaces to guarantee zero clutter."""
    key_markers = [
        kit_dir / "GEMINI.md",
        kit_dir / "validate_kit.py",
        kit_dir / ".agents" / "agents" / "aegis_best_practice" / "agent.md",
    ]
    if all(p.exists() for p in key_markers):
        return

    print("\n[REMOTE BOOTSTRAP] Local kit files not found. Downloading PANTHEON AI Setup Kit from GitHub...")
    print(f"                   Destination: {kit_dir}")
    kit_dir.mkdir(parents=True, exist_ok=True)

    downloaded_zip = False
    with tempfile.TemporaryDirectory(prefix="pantheon_kit_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        zip_path = tmp_path / "pantheon-ai-kit.zip"
        try:
            req = urllib.request.Request(repo_zip_url(REPO_REF), headers={"User-Agent": "Pantheon-AI-Kit-Bootstrap/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(zip_path, "wb") as out_f:
                shutil.copyfileobj(resp, out_f)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_path / "extracted")
            extracted_roots = [p for p in (tmp_path / "extracted").iterdir() if p.is_dir()]
            src_root = extracted_roots[0] if extracted_roots else (tmp_path / "extracted")

            # Verify integrity of the complete download in temporary directory
            verify_kit_integrity(src_root, REPO_REF)

            if (src_root / "GEMINI.md").exists():
                runtime_files = [
                    "GEMINI.md", "GOVERNANCE.md", ".env.template", ".gitignore",
                    "setup.py", "validate_kit.py", "validate_and_install.ps1",
                    "CLAUDE.md", "AGENTS.md", "install.sh", "install.cmd",
                ]
                runtime_dirs = [".agents", ".claude", ".codex"]
                if include_docs:
                    runtime_files.append("ANTIGRAVITY_SETUP_GUIDE.md")
                if include_prompts:
                    runtime_dirs.append("Governance_Framework")
                if include_examples:
                    runtime_dirs.append("examples")

                for rf in runtime_files:
                    sf = src_root / rf
                    if sf.is_file():
                        shutil.copy2(sf, kit_dir / rf)

                for rd in runtime_dirs:
                    sd = src_root / rd
                    if sd.is_dir():
                        shutil.copytree(sd, kit_dir / rd, dirs_exist_ok=True)

                downloaded_zip = True
                print("                   [OK] Downloaded and installed runtime components cleanly (zero clutter).")
        except Exception as exc:
            print(f"                   [WARN] Archive download failed ({exc}). Falling back to raw file download...")

    if not downloaded_zip:
        files_to_fetch = [
            "GEMINI.md", "GOVERNANCE.md", ".env.template", ".gitignore",
            "setup.py", "validate_kit.py", "validate_and_install.ps1",
            "CLAUDE.md", "AGENTS.md", "install.sh", "install.cmd",
        ]
        if include_docs:
            files_to_fetch.append("ANTIGRAVITY_SETUP_GUIDE.md")
        for rel_path in REQUIRED_KIT_FILES:
            if rel_path.startswith((".agents/", ".claude/", ".codex/")):
                files_to_fetch.append(rel_path)

        for rel_path in files_to_fetch:
            dest_file = kit_dir / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            raw_url = f"{repo_raw_base_url(REPO_REF)}/{rel_path}"
            req = urllib.request.Request(raw_url, headers={"User-Agent": "Pantheon-AI-Kit-Bootstrap/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp, open(dest_file, "wb") as out_f:
                shutil.copyfileobj(resp, out_f)
        print("                   [OK] Downloaded runtime files cleanly from GitHub.")


def encode_reversed_base64(plain_text: str) -> str:
    """Reverse UTF-8 string and Base64-encode it to match the $EncodedRules format."""
    reversed_text = plain_text[::-1]
    return base64.b64encode(reversed_text.encode("utf-8")).decode("utf-8")


def decode_reversed_base64(encoded_text: str) -> str:
    """Decode Base64 and reverse UTF-8 string back to plaintext."""
    raw = base64.b64decode(encoded_text.encode("utf-8")).decode("utf-8")
    return raw[::-1]


def build_keyword_rule(label: str, custom_regex: Optional[str] = None) -> Dict[str, str]:
    """Create a {NameB64, PatB64} encoded rule entry from a keyword/label and optional regex."""
    clean_label = label.strip()
    if custom_regex and custom_regex.strip():
        pat_str = custom_regex.strip()
    else:
        escaped = re.escape(clean_label).replace(r"\ ", r"(?:\s+|\.)")
        pat_str = rf"\b{escaped}\b"
    return {
        "NameB64": encode_reversed_base64(clean_label),
        "PatB64": encode_reversed_base64(pat_str),
    }


def parse_keyword_entries(raw_input: str) -> List[Tuple[str, Optional[str]]]:
    """Parse single, comma-separated, or multi-line keyword inputs (supporting 'Label::Regex')."""
    results: List[Tuple[str, Optional[str]]] = []
    for line in raw_input.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.lower() in ("done", "exit", "quit", "q"):
            continue
        for part in line_clean.split(","):
            tok = part.strip()
            if not tok or tok.lower() in ("done", "exit", "quit", "q"):
                continue
            if "::" in tok:
                lbl, rgx = tok.split("::", 1)
                if lbl.strip():
                    results.append((lbl.strip(), rgx.strip() if rgx.strip() else None))
            else:
                results.append((tok, None))
    return results


def ensure_gitignore_entry(workspace_dir: Path, entry_name: str = CUSTOM_BLOCKLIST_FILENAME) -> None:
    """Ensure the custom encoded keyword library file is listed in .gitignore so it is never committed."""
    gi_path = workspace_dir / ".gitignore"
    if gi_path.exists():
        content = gi_path.read_text(encoding="utf-8", errors="replace")
        if entry_name not in content:
            sep = "\n" if content.endswith("\n") else "\n\n"
            addition = f"{sep}# Local company-specific encoded leak scanner keyword library ($EncodedRules)\n{entry_name}\n"
            gi_path.write_text(content + addition, encoding="utf-8")
            print(f"           [GITIGNORE] Added '{entry_name}' to {gi_path}")
    else:
        gi_path.write_text(
            f".env\n.venv/\n# Local company-specific encoded leak scanner keyword library ($EncodedRules)\n{entry_name}\n",
            encoding="utf-8",
        )
        print(f"           [GITIGNORE] Created {gi_path} with '{entry_name}'")


def configure_custom_scanner(
    workspace_dir: Path,
    cli_keywords: Optional[List[str]] = None,
    force_interactive: bool = False,
    skip_custom_scanner: bool = False,
) -> None:
    """Optionally build or append to a local custom $EncodedRules library (.custom_blocklist.json)."""
    lib_path = workspace_dir / CUSTOM_BLOCKLIST_FILENAME
    existing_rules: List[Dict[str, str]] = []

    if lib_path.exists():
        try:
            loaded = json.loads(lib_path.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                for item in loaded:
                    if isinstance(item, dict) and item.get("NameB64") and item.get("PatB64"):
                        existing_rules.append(
                            {"NameB64": str(item["NameB64"]), "PatB64": str(item["PatB64"])}
                        )
        except Exception:
            pass

    # Handle non-interactive CLI keywords if provided via --add-scanner-keyword
    if cli_keywords:
        for kw_arg in cli_keywords:
            for lbl, rgx in parse_keyword_entries(kw_arg):
                rule = build_keyword_rule(lbl, rgx)
                if not any(
                    r.get("NameB64") == rule["NameB64"] and r.get("PatB64") == rule["PatB64"]
                    for r in existing_rules
                ):
                    existing_rules.append(rule)
        lib_path.write_text(json.dumps(existing_rules, indent=2), encoding="utf-8")
        ensure_gitignore_entry(workspace_dir, CUSTOM_BLOCKLIST_FILENAME)
        print(
            f"[STEP 3/5] Saved {len(existing_rules)} custom encoded rule(s) to {lib_path.name} "
            f"(protected by .gitignore)."
        )
        return

    if skip_custom_scanner:
        print(
            "[STEP 3/5] Skipped custom keyword scanner setup (--skip-custom-scanner). "
            "Using built-in generic credential checks."
        )
        return

    if not force_interactive and not sys.stdin.isatty():
        print(
            "[STEP 3/5] Non-interactive session: skipping optional custom $EncodedRules scanner prompt "
            "(pass --configure-scanner or --add-scanner-keyword to configure)."
        )
        return

    if not force_interactive:
        print("\n[STEP 3/5] [OPTIONAL] Custom Organization / Keyword Leak Scanner ($EncodedRules)")
        print("           Would you like to set up a more specific leak scanner and build a local")
        print(f"           library of company/project keywords in '{CUSTOM_BLOCKLIST_FILENAME}' (gitignored)?")
        try:
            ans = input("           Configure custom keyword scanner now? [y/N - Press Enter to skip]: ").strip().lower()
        except EOFError:
            ans = "n"
        if ans not in ("y", "yes"):
            print("           [SKIP] Skipped custom keyword scanner setup (run 'python setup.py --configure-scanner' anytime).")
            return

    print("\n           ----------------------------------------------------------------------")
    print("             CUSTOM KEYWORD LEAK SCANNER BUILDER ($EncodedRules Library)")
    print("           ----------------------------------------------------------------------")
    print(f"           Currently loaded custom rules in {CUSTOM_BLOCKLIST_FILENAME}: {len(existing_rules)}")
    if existing_rules:
        preview_labels: List[str] = []
        for idx, r_item in enumerate(existing_rules, start=1):
            try:
                dec_lbl = decode_reversed_base64(r_item["NameB64"])
                preview_labels.append(f"#{idx} '{dec_lbl}'")
            except Exception:
                preview_labels.append(f"#{idx} <encoded>")
        print(f"           Loaded Rules: {', '.join(preview_labels)}")
        try:
            clear_ans = input(
                "           Would you like to [K]eep existing rules or [C]lear/reset the list first? [K/c - Press Enter to keep]: "
            ).strip().lower()
        except EOFError:
            clear_ans = "k"
        if clear_ans in ("c", "clear", "reset"):
            existing_rules.clear()
            if lib_path.exists():
                lib_path.unlink(missing_ok=True)
            print(f"           [RESET] Cleared all previous custom rules from {CUSTOM_BLOCKLIST_FILENAME}.")

    print("           How to add organization-specific keywords:")
    print("             * Enter a single keyword (e.g. <YourCompanyName>) OR multiple")
    print("               comma-separated keywords on one line (e.g. <Company>, <internal.domain>)")
    print("             * Optional custom regex: use 'Label::Regex' (e.g. CorpDomain::\\bcorp\\.local\\b)")
    print("             * Tip: Avoid short common English words (like 'bad' or 'good'), which match")
    print("               inside normal words (such as 'badge' or 'Goodhart').")
    print("             * To finish at any prompt: press [Enter] on an empty line or type 'done'")
    print("           All rules are Reversed UTF-8 + Base64 encoded and added to .gitignore.\n")

    added = 0
    while True:
        try:
            raw_line = input("           Enter keyword(s) to block (comma-separated, or press Enter / type 'done' to finish): ").strip()
        except EOFError:
            break
        if not raw_line or raw_line.lower() in ("done", "exit", "quit", "q"):
            break

        parsed_entries = parse_keyword_entries(raw_line)
        for lbl, rgx in parsed_entries:
            rule = build_keyword_rule(lbl, rgx)
            dup_idx = next(
                (
                    i + 1
                    for i, ex in enumerate(existing_rules)
                    if ex.get("NameB64") == rule["NameB64"] and ex.get("PatB64") == rule["PatB64"]
                ),
                None,
            )
            if dup_idx is not None:
                print(f"             [SKIP] '{lbl}' is already in the list as Rule #{dup_idx} (skipped duplicate).")
                continue

            existing_rules.append(rule)
            added += 1
            print(f"             + Added encoded rule (#{len(existing_rules)}) for '{lbl}' -> NameB64='{rule['NameB64']}'")
            if len(lbl) <= 3 and rgx is None:
                print(
                    f"               [TIP] '{lbl}' is very short ({len(lbl)} chars) and will also be checked as a substring (e.g. inside longer words)."
                )

        try:
            more = input("           Add more keywords? [y/N - Press Enter to finish & save]: ").strip().lower()
        except EOFError:
            more = "n"
        if more not in ("y", "yes"):
            break

    if existing_rules:
        lib_path.write_text(json.dumps(existing_rules, indent=2), encoding="utf-8")
        ensure_gitignore_entry(workspace_dir, CUSTOM_BLOCKLIST_FILENAME)
        print(f"           [OK] Saved {len(existing_rules)} encoded rule(s) to {lib_path} (gitignored).")
    else:
        print("           [SKIP] No custom keywords active.")


def plan_uninstallation(
    target_dir: Path,
    purge_secrets: bool = False,
    purge_venv: bool = False,
) -> Tuple[List[Path], List[Path]]:
    """Resolve exact files and directories eligible for deletion.

    Returns (files_to_delete, dirs_to_prune).
    """
    files_to_delete: List[Path] = []

    # Tier 1: Canonical Kit Files (a profile install never copies .gitignore; it belongs to the user's project)
    installed_list = target_dir / ".pantheon-installed.json"
    for rel_path in REQUIRED_KIT_FILES:
        if rel_path == ".gitignore" and installed_list.is_file():
            continue
        candidate = target_dir / rel_path
        if candidate.is_file() or candidate.is_symlink():
            if candidate not in files_to_delete:
                files_to_delete.append(candidate)

    # Tier 1b: Files a profile install recorded (pantheon.profile.json is kept unless secrets are purged)
    if installed_list.is_file():
        try:
            recorded = json.loads(installed_list.read_text(encoding="utf-8")).get("files", [])
        except (OSError, ValueError, AttributeError):
            recorded = []
        for rel_path in [*recorded, ".pantheon-installed.json"]:
            candidate = target_dir / rel_path
            if candidate.is_file() and candidate not in files_to_delete:
                files_to_delete.append(candidate)

    # Tier 2: Generated Docs and Caches
    generated_markers = ["ANTIGRAVITY_DOCS.html"]
    for gen in generated_markers:
        candidate = target_dir / gen
        if candidate.is_file() and candidate not in files_to_delete:
            files_to_delete.append(candidate)

    # Tier 3: User Secrets and Keyword Blocklists
    if purge_secrets:
        for sec in [".env", CUSTOM_BLOCKLIST_FILENAME, "pantheon.profile.json"]:
            candidate = target_dir / sec
            if candidate.is_file() and candidate not in files_to_delete:
                files_to_delete.append(candidate)

    # Directories targeted for pruning (deepest first)
    dirs_to_prune = [
        target_dir / ".agents" / "agents" / "aegis_best_practice",
        target_dir / ".agents" / "agents" / "atlas_architecture",
        target_dir / ".agents" / "agents" / "hermes_migration",
        target_dir / ".agents" / "agents" / "sage_governance",
        target_dir / ".agents" / "agents" / "sentinel_security",
        target_dir / ".agents" / "agents" / "spark_disruptor",
        target_dir / ".agents" / "skills" / "infrastructure-best-practice-analyser",
        target_dir / ".agents" / "skills" / "pantheon-setup",
        target_dir / ".agents" / "skills" / "productivity-workload-governance",
        target_dir / ".agents" / "skills" / "quality-audit-governance",
        target_dir / ".agents" / "skills" / "server-migration-infrastructure-replication",
        target_dir / ".agents" / "skills" / "support-team-governance-analytics-coaching",
        target_dir / ".agents" / "skills" / "teams-standup-digest-notifier",
        target_dir / ".agents" / "skills" / "ticket-backlog-governance",
        target_dir / ".agents" / "rules",
        target_dir / ".agents" / "agents",
        target_dir / ".agents" / "skills",
        target_dir / ".agents",
        target_dir / "docs_template" / "fonts",
        target_dir / "docs_template",
        target_dir / ".claude" / "skills" / "infrastructure-best-practice-analyser",
        target_dir / ".claude" / "skills" / "pantheon-setup",
        target_dir / ".claude" / "skills" / "ticket-backlog-governance",
        target_dir / ".claude" / "skills" / "productivity-workload-governance",
        target_dir / ".claude" / "skills" / "quality-audit-governance",
        target_dir / ".claude" / "skills" / "server-migration-infrastructure-replication",
        target_dir / ".claude" / "skills" / "teams-standup-digest-notifier",
        target_dir / ".claude" / "skills" / "support-team-governance-analytics-coaching",
        target_dir / ".claude" / "rules",
        target_dir / ".claude" / "agents",
        target_dir / ".claude" / "skills",
        target_dir / ".claude",
        target_dir / ".codex" / "agents",
        target_dir / ".codex",
        target_dir / "Governance_Framework",
        target_dir / "tools",
    ]
    if purge_venv:
        dirs_to_prune.insert(0, target_dir / ".venv")

    return files_to_delete, dirs_to_prune


def execute_uninstallation(
    target_dir: Path,
    kit_dir: Path,
    purge_secrets: bool = False,
    purge_venv: bool = False,
    dry_run: bool = False,
    force: bool = False,
) -> int:
    """Safely uninstall kit files with root source repository protection."""
    # Safety Check: Prevent self-destruction of the source repository
    is_source_repo = (target_dir / ".git").exists() and (target_dir / "setup.py").resolve() == Path(__file__).resolve()
    if is_source_repo and not force:
        print("[ERROR] Target directory appears to be the PANTHEON source repository clone.", file=sys.stderr)
        print("        To prevent accidental source deletion, pass --target-dir <path> of an external workspace", file=sys.stderr)
        print("        or supply --force if you specifically intend to strip kit files from this workspace.", file=sys.stderr)
        return 1

    files_to_delete, dirs_to_prune = plan_uninstallation(target_dir, purge_secrets, purge_venv)

    print("\n" + "=" * 78)
    print(f"  PANTHEON AI SETUP KIT - UNINSTALLATION & CLEANUP{' (DRY RUN)' if dry_run else ''}")
    print("=" * 78)
    print(f"  Target Workspace : {target_dir}")
    print(f"  Files Identified : {len(files_to_delete)}")
    print(f"  Purge Secrets    : {'YES (.env & custom blocklist will be deleted)' if purge_secrets else 'NO (kept intact)'}")
    print(f"  Purge .venv      : {'YES' if purge_venv else 'NO'}")
    print("=" * 78)

    if not files_to_delete and not any(d.exists() for d in dirs_to_prune):
        print("No PANTHEON AI Setup Kit files found in target workspace.")
        return 0

    for f in files_to_delete:
        try:
            rel = f.relative_to(target_dir)
        except ValueError:
            rel = f
        print(f"  [-] {rel}")

    if dry_run:
        print("\n[DRY RUN] No files were removed.")
        return 0

    if not force and sys.stdin.isatty():
        try:
            confirm = input("\nAre you sure you want to delete these kit components? [y/N]: ").strip().lower()
        except EOFError:
            confirm = "n"
        if confirm not in ("y", "yes"):
            print("[ABORTED] Uninstallation cancelled by user.")
            return 0

    # 1. Delete canonical files (defer setup.py until end if it's running)
    deleted_count = 0
    setup_file: Optional[Path] = None
    for f in files_to_delete:
        if f.name == "setup.py" and f.resolve() == Path(__file__).resolve():
            setup_file = f
            continue
        try:
            if f.exists():
                f.unlink()
                deleted_count += 1
        except Exception as exc:
            print(f"  [WARN] Failed to delete {f.name}: {exc}", file=sys.stderr)

    # 2. Prune directories bottom-up only if empty
    for d in dirs_to_prune:
        if d.exists() and d.is_dir():
            if d.name == ".venv" and purge_venv:
                try:
                    shutil.rmtree(d, ignore_errors=True)
                    print(f"  [REMOVED DIR] {d.relative_to(target_dir)}")
                except Exception as exc:
                    print(f"  [WARN] Failed to remove .venv: {exc}", file=sys.stderr)
            else:
                try:
                    # Remove only if directory is empty (preserves custom files added by user)
                    if not any(d.iterdir()):
                        d.rmdir()
                        print(f"  [REMOVED EMPTY DIR] {d.relative_to(target_dir)}")
                except Exception:
                    pass

    # Finally delete running setup.py if it was targeted
    if setup_file and setup_file.exists():
        try:
            setup_file.unlink()
            deleted_count += 1
        except Exception as exc:
            print(f"  [WARN] Failed to delete {setup_file.name}: {exc}", file=sys.stderr)

    print(f"\n[OK] Successfully uninstalled {deleted_count} kit file(s).")
    return 0



CANONICAL_AGENTS = {
    "aegis_best_practice",
    "atlas_architecture",
    "hermes_migration",
    "sage_governance",
    "sentinel_security",
    "spark_disruptor",
}

CANONICAL_SKILLS = {
    "infrastructure-best-practice-analyser",
    "pantheon-setup",
    "productivity-workload-governance",
    "quality-audit-governance",
    "server-migration-infrastructure-replication",
    "support-team-governance-analytics-coaching",
    "teams-standup-digest-notifier",
    "ticket-backlog-governance",
}


def scan_workspace_agents_and_skills(workspace_dir: Path) -> Dict[str, Any]:
    """Scan workspace for canonical, adopted, unmanaged, and disabled agents/skills."""
    agents_dir = workspace_dir / ".agents"
    if not agents_dir.is_dir():
        return {
            "canonical_agents": [],
            "canonical_skills": [],
            "unmanaged": [],
            "adopted": {"agents": [], "skills": []},
            "disabled": [],
        }

    inst_file = workspace_dir / ".pantheon-installed.json"
    manifest: Dict[str, Any] = {}
    if inst_file.is_file():
        try:
            manifest = json.loads(inst_file.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}

    adopted = manifest.get("adopted", {"agents": [], "skills": []})
    adopted_names = set(adopted.get("agents", [])) | set(adopted.get("skills", []))

    disabled_dir = agents_dir / ".disabled"
    disabled_items = [d.name for d in disabled_dir.iterdir()] if disabled_dir.is_dir() else []

    found_agents: List[str] = []
    found_skills: List[str] = []
    unmanaged: List[Dict[str, str]] = []

    # Check .agents/agents
    if (agents_dir / "agents").is_dir():
        for d in (agents_dir / "agents").iterdir():
            if d.is_dir() and d.name != ".disabled":
                if d.name in CANONICAL_AGENTS:
                    found_agents.append(d.name)
                elif d.name not in adopted_names:
                    unmanaged.append({"name": d.name, "kind": "agent", "path": str(d.relative_to(workspace_dir))})

    # Check .agents/skills
    if (agents_dir / "skills").is_dir():
        for d in (agents_dir / "skills").iterdir():
            if d.is_dir() and d.name != ".disabled":
                if d.name in CANONICAL_SKILLS:
                    found_skills.append(d.name)
                elif d.name not in adopted_names:
                    unmanaged.append({"name": d.name, "kind": "skill", "path": str(d.relative_to(workspace_dir))})

    # Check direct children under .agents/
    for d in agents_dir.iterdir():
        if d.is_dir() and d.name not in ("agents", "skills", "rules", ".disabled", "__pycache__"):
            if d.name not in adopted_names and not any(u["name"] == d.name for u in unmanaged):
                kind = "skill" if (d / "SKILL.md").is_file() else "agent"
                unmanaged.append({"name": d.name, "kind": kind, "path": str(d.relative_to(workspace_dir))})

    return {
        "canonical_agents": sorted(found_agents),
        "canonical_skills": sorted(found_skills),
        "unmanaged": unmanaged,
        "adopted": adopted,
        "disabled": sorted(disabled_items),
    }


def adopt_items(workspace_dir: Path, names: Optional[List[str]] = None) -> int:
    """Adopt existing custom agents/skills into PANTHEON governance and lifecycle management."""
    scan = scan_workspace_agents_and_skills(workspace_dir)
    unmanaged = scan["unmanaged"]
    if not unmanaged:
        print("[INFO] No unmanaged agents or skills detected in workspace to adopt.")
        return 0

    to_adopt = unmanaged
    if names:
        to_adopt = [u for u in unmanaged if u["name"] in names]

    inst_file = workspace_dir / ".pantheon-installed.json"
    manifest: Dict[str, Any] = {}
    if inst_file.is_file():
        try:
            manifest = json.loads(inst_file.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}

    adopted = manifest.setdefault("adopted", {"agents": [], "skills": []})
    for item in to_adopt:
        target_list = adopted["agents"] if item["kind"] == "agent" else adopted["skills"]
        if item["name"] not in target_list:
            target_list.append(item["name"])
        print(f"  [ADOPTED] Adopted {item['kind']} '{item['name']}' ({item['path']}) into PANTHEON governance.")

    inst_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\n[OK] Successfully adopted {len(to_adopt)} item(s). You can now manage them with --enable, --disable, or --uninstall-item.")
    return 0


def disable_item(workspace_dir: Path, name: str) -> int:
    """Switch off an agent or skill by moving it to .agents/.disabled/ (retaining full history)."""
    agents_dir = workspace_dir / ".agents"
    disabled_dir = agents_dir / ".disabled"
    disabled_dir.mkdir(parents=True, exist_ok=True)

    candidates = [
        agents_dir / "agents" / name,
        agents_dir / "skills" / name,
        agents_dir / name,
    ]
    found = next((c for c in candidates if c.exists()), None)
    if not found:
        if (disabled_dir / name).exists():
            print(f"[INFO] '{name}' is already disabled (stored in {disabled_dir.relative_to(workspace_dir) / name}).")
            return 0
        print(f"[ERROR] Agent or skill '{name}' not found in {agents_dir}.", file=sys.stderr)
        return 1

    dest = disabled_dir / name
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    shutil.move(str(found), str(dest))

    # Also handle Claude Code mirror if present
    claude_candidate = workspace_dir / ".claude" / ("agents" if "agent" in str(found) else "skills") / (f"{name}.md" if "agent" in str(found) else name)
    if claude_candidate.exists():
        claude_disabled = workspace_dir / ".claude" / ".disabled"
        claude_disabled.mkdir(parents=True, exist_ok=True)
        shutil.move(str(claude_candidate), str(claude_disabled / claude_candidate.name))

    print(f"[DISABLED] '{name}' switched off. Moved to {dest.relative_to(workspace_dir)} (inactive in AI sessions).")
    print(f"           Run 'python setup.py --enable {name}' at any time to switch it back on.")
    return 0


def enable_item(workspace_dir: Path, name: str) -> int:
    """Switch on a previously disabled agent or skill, restoring it to the active directory."""
    agents_dir = workspace_dir / ".agents"
    disabled_item = agents_dir / ".disabled" / name
    if not disabled_item.exists():
        for c in (agents_dir / "agents" / name, agents_dir / "skills" / name, agents_dir / name):
            if c.exists():
                print(f"[INFO] '{name}' is already active at {c.relative_to(workspace_dir)}.")
                return 0
        print(f"[ERROR] Disabled item '{name}' not found in {agents_dir / '.disabled'}.", file=sys.stderr)
        return 1

    if (disabled_item / "SKILL.md").is_file():
        dest = agents_dir / "skills" / name
    elif (disabled_item / "agent.md").is_file():
        dest = agents_dir / "agents" / name
    elif name in CANONICAL_SKILLS:
        dest = agents_dir / "skills" / name
    elif name in CANONICAL_AGENTS:
        dest = agents_dir / "agents" / name
    else:
        dest = agents_dir / "agents" / name

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(disabled_item), str(dest))

    claude_disabled = workspace_dir / ".claude" / ".disabled"
    if claude_disabled.is_dir():
        for f in claude_disabled.glob(f"{name}*"):
            c_dest = workspace_dir / ".claude" / ("agents" if f.name.endswith(".md") else "skills") / f.name
            c_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(c_dest))

    print(f"[ENABLED] '{name}' switched on. Restored to {dest.relative_to(workspace_dir)} (active in AI sessions).")
    return 0


def scaffold_agent(workspace_dir: Path, name: str, role: Optional[str] = None) -> int:
    """Scaffold a new specialist agent compliant with PANTHEON schema and British English standards."""
    clean_name = re.sub(r"[^a-zA-Z0-9_]+", "_", name.lower()).strip("_")
    dest_dir = workspace_dir / ".agents" / "agents" / clean_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    agent_file = dest_dir / "agent.md"
    if agent_file.exists():
        print(f"[ERROR] Agent '{clean_name}' already exists at {agent_file}.", file=sys.stderr)
        return 1

    desc = role or f"Specialist agent for {clean_name.replace('_', ' ').title()}."
    title = clean_name.replace('_', ' ').title()

    template = f"""---
name: {clean_name}
description: {desc}
tools:
  - view_file
  - grep_search
  - find_by_name
---

# {title} Specialist Agent

You are an advisory specialist persona focused on {clean_name.replace('_', ' ')}.

## Operational Role & Objective
- Provide authoritative, evidence-based recommendations.
- Preserve operational safety and adhere to standard operating procedures.

## Core Responsibilities
1. Analyse relevant configuration files, logs, and system states.
2. Formulate pragmatic, non-destructive remediation plans.
3. Validate operational prerequisites before proposing structural modifications.

## Governance & Language Standards
- Adhere to British English (en-GB) orthography (e.g. analyse, prioritise, optimise).
- Treat all sensitive credentials as confidential and never print raw tokens (<REDACTED>).
- Refuse unverified speculative modifications.
"""
    agent_file.write_text(template, encoding="utf-8")
    rel_path = agent_file.relative_to(workspace_dir)
    print("\n[CREATED] Specialist agent scaffold created at:")
    print(f"          {rel_path}")
    print("\n" + "=" * 70)
    print("  HOW TO DEVELOP YOUR SPECIALIST AGENT")
    print("=" * 70)
    print("\n1. Understanding the Agent Concept:")
    print("   An agent is an autonomous specialist persona that operates in an isolated")
    print("   context window with scoped tools (e.g. view_file, grep_search).")
    print("   It acts like an independent expert consultant in your pair-programming sessions.")
    print("\n2. File to Edit:")
    print(f"   {rel_path}")
    print("\n3. Finalising & Polishing with an LLM:")
    print("   You do not need prior prompt-engineering experience. Copy and paste the prompt")
    print("   below into Google Antigravity, Claude Code, or your preferred LLM:")
    print("-" * 70)
    print('   "I am developing a specialist agent for the PANTHEON AI Kit in:')
    print(f'    {rel_path}')
    print(f'    Its objective is: {desc}')
    print('    Please help me flesh out and refine its prompt following PANTHEON standards:')
    print('    - British English (en-GB) spelling and quiet, professional competence.')
    print('    - Objective, evidence-based evaluation steps, formulas, and thresholds.')
    print('    - Strict credential isolation (mandatory <REDACTED> for all secrets).')
    print('    - Concise, trigger-accurate YAML frontmatter description."')
    print("-" * 70)
    print("\n4. Local Testing & Management:")
    print("   - Adopt into kit tracking:       python setup.py --adopt")
    print(f"   - Temporarily disable / enable:  python setup.py --disable {clean_name} / --enable {clean_name}")
    print("   - Validate workspace integrity:  python validate_kit.py")
    print("\n5. Sharing with the Wider Community:")
    print("   If this agent could benefit others, please review CONTRIBUTING.md before sharing:")
    print("   - Ensure it contains no proprietary IP, employer secrets, or private data.")
    print("   - If functionality overlaps with an existing agent, consider extending that agent")
    print("     rather than duplicating it. You are also welcome to publish your own project!")
    print("=" * 70 + "\n")
    return 0


def scaffold_skill(workspace_dir: Path, name: str, description: Optional[str] = None) -> int:
    """Scaffold a new governance skill compliant with PANTHEON schema and British English standards."""
    clean_name = re.sub(r"[^a-zA-Z0-9\-]+", "-", name.lower()).strip("-")
    dest_dir = workspace_dir / ".agents" / "skills" / clean_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    skill_file = dest_dir / "SKILL.md"
    if skill_file.exists():
        print(f"[ERROR] Skill '{clean_name}' already exists at {skill_file}.", file=sys.stderr)
        return 1

    desc = description or f"Operational governance skill for {clean_name.replace('-', ' ')}."
    title = clean_name.replace('-', ' ').title()

    template = f"""---
name: {clean_name}
description: {desc}
---

# {title} Governance Skill

## Overview
{desc}

## When to Use This Skill
- Activate when auditing or evaluating {clean_name.replace('-', ' ')}.
- Use during operational reviews and team handovers.

## Procedural Workflow
1. **Initial Assessment**: Inspect relevant operational datasets.
2. **Analysis & Calculation**: Apply objective rubric criteria and business-hour rules.
3. **Synthesis & Reporting**: Present evidence-based recommendations in British English (en-GB).

## Hard Invariants
- British English (en-GB) documentation and report formatting.
- Strict isolation of sensitive configuration variables (<REDACTED>).
"""
    skill_file.write_text(template, encoding="utf-8")
    rel_path = skill_file.relative_to(workspace_dir)
    print("\n[CREATED] Governance skill scaffold created at:")
    print(f"          {rel_path}")
    print("\n" + "=" * 70)
    print("  HOW TO DEVELOP YOUR GOVERNANCE SKILL")
    print("=" * 70)
    print("\n1. Understanding the Skill Concept:")
    print("   A skill is an on-demand standard operating procedure (SOP), rubric, or calculation")
    print("   reference injected into the active agent session when its YAML frontmatter")
    print("   'description' matches the user's intent. It provides deep, progressive expertise.")
    print("\n2. File to Edit:")
    print(f"   {rel_path}")
    print("\n3. Finalising & Polishing with an LLM:")
    print("   You do not need prior prompt-engineering experience. Copy and paste the prompt")
    print("   below into Google Antigravity, Claude Code, or your preferred LLM:")
    print("-" * 70)
    print('   "I am developing a governance skill for the PANTHEON AI Kit in:')
    print(f'    {rel_path}')
    print(f'    Its objective is: {desc}')
    print('    Please help me refine the instructions and workflow following PANTHEON standards:')
    print('    - British English (en-GB) spelling and clear procedural steps.')
    print('    - Concrete rubrics, mathematical definitions, or compliance checklists.')
    print('    - Strict credential isolation (mandatory <REDACTED> for all secrets).')
    print('    - A sharp frontmatter description specifying exactly when this skill should trigger."')
    print("-" * 70)
    print("\n4. Local Testing & Management:")
    print("   - Adopt into kit tracking:       python setup.py --adopt")
    print(f"   - Temporarily disable / enable:  python setup.py --disable {clean_name} / --enable {clean_name}")
    print("   - Validate workspace integrity:  python validate_kit.py")
    print("\n5. Sharing with the Wider Community:")
    print("   If this skill could benefit others, please review CONTRIBUTING.md before sharing:")
    print("   - Ensure it contains no proprietary IP, employer secrets, or private data.")
    print("   - If functionality overlaps with an existing skill, consider extending that skill")
    print("     first. You are also welcome to publish your own project in open source!")
    print("=" * 70 + "\n")
    return 0


def uninstall_single_item(workspace_dir: Path, name: str, force: bool = False) -> int:
    """Surgically remove an individual agent or skill (canonical or adopted)."""
    agents_dir = workspace_dir / ".agents"
    targets = [
        agents_dir / "agents" / name,
        agents_dir / "skills" / name,
        agents_dir / name,
        agents_dir / ".disabled" / name,
    ]
    found = [t for t in targets if t.exists()]
    if not found:
        print(f"[ERROR] Item '{name}' not found in {agents_dir}.", file=sys.stderr)
        return 1

    target = found[0]
    if not force:
        confirm = input(f"Are you sure you want to permanently delete {target.relative_to(workspace_dir)}? [y/N]: ").strip().lower()
        if confirm not in ("y", "yes"):
            print("[CANCELLED] Deletion cancelled.")
            return 0

    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()

    for m in (workspace_dir / ".claude", workspace_dir / ".codex"):
        if m.is_dir():
            for match in m.rglob(f"*{name}*"):
                if match.is_file():
                    match.unlink()

    print(f"[OK] Successfully uninstalled '{name}'.")
    return 0

def load_catalog(kit_dir: Path) -> Any:
    """Import tools/kit_catalog.py from the kit (after a standalone bootstrap has fetched it)."""
    tools_dir = str(kit_dir / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    import kit_catalog  # type: ignore[import-not-found]

    return kit_catalog


def kit_version(kit_dir: Path) -> str:
    path = kit_dir / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else "unknown"


def build_profile(args: argparse.Namespace, target_dir: Path, catalog: Any) -> Optional[Dict[str, Any]]:
    """Profile from --profile (or the workspace's saved one), with any shortcut flags layered on top."""
    if not (args.profile or args.groups or args.tools or args.integrations or args.set):
        return None
    source = Path(args.profile) if args.profile else target_dir / catalog.PROFILE_FILENAME
    profile: Dict[str, Any] = {}
    if source.is_file():
        loaded = catalog.read_json(source)
        if not isinstance(loaded, dict):
            raise ValueError(f"{source} is not a JSON object")
        profile = loaded
    elif args.profile:
        raise ValueError(f"profile not found: {source}")

    def names(value: str) -> List[str]:
        return [v.strip() for v in value.split(",") if v.strip()]

    if args.groups is not None:
        profile["groups"] = names(args.groups)
    if args.tools is not None:
        profile["tools"] = names(args.tools)
    if args.integrations is not None:
        profile["integrations"] = names(args.integrations)
    profile.setdefault("tools", list(catalog.TOOLS))
    for item in args.set or []:
        key, sep, raw = item.partition("=")
        if not sep:
            raise ValueError(f"--set expects KEY=VALUE, got '{item}'")
        try:
            value: Any = json.loads(raw)
            if not isinstance(value, (int, float)):
                value = raw
        except ValueError:
            value = raw
        profile.setdefault("thresholds", {})[key.strip()] = value
    profile["schema"] = catalog.PROFILE_SCHEMA
    return profile


def detect_workspace(kit_dir: Path, target_dir: Path) -> Dict[str, Any]:
    """What is already in the target workspace. Reports .env key names only, never values."""
    catalog = load_catalog(kit_dir)
    profile = catalog.read_json(target_dir / catalog.PROFILE_FILENAME)
    env_path = target_dir / ".env"
    env: Dict[str, Any] = {"exists": env_path.is_file()}
    if isinstance(profile, dict) and not catalog.validate_profile(profile):
        keys = catalog.env_keys(profile)
        values = catalog.template_values(env_path.read_text(encoding="utf-8", errors="replace")) if env_path.is_file() else {}
        env["missing_keys"] = [k for k in keys["plain"] + keys["secret"] + keys["thresholds"] if k not in values]
        env["empty_secret_keys"] = [k for k in keys["secret"] if k in values and not values[k].strip()]
    pwsh_path, pwsh_ver = detect_executable(["pwsh"])
    scan = scan_workspace_agents_and_skills(target_dir)
    return {
        "kit_dir": str(kit_dir),
        "kit_version": kit_version(kit_dir),
        "target_dir": str(target_dir),
        "target_is_kit": target_dir.resolve() == kit_dir.resolve(),
        "profile": profile,
        "tools_present": {
            "antigravity": (target_dir / ".agents").is_dir(),
            "claude-code": (target_dir / ".claude").is_dir() or (target_dir / "CLAUDE.md").is_file(),
            "codex": (target_dir / ".codex").is_dir() or (target_dir / "AGENTS.md").is_file(),
        },
        "agents_and_skills": scan,
        "runtimes": {"python": sys.version.split()[0], "pwsh": pwsh_ver if pwsh_path else None},
        "env": env,
        "catalogue": catalog.catalogue(),
    }


def print_profile_plan(plan: Dict[str, Any], dry_run: bool) -> None:
    files = plan["files"]
    sel = plan["selection"]
    print("=" * 78)
    print(f"  PANTHEON SETUP - PROFILE INSTALL{' (DRY RUN)' if dry_run else ''}")
    print("=" * 78)
    print(f"  Target workspace : {plan['target_dir']}")
    print(f"  Groups           : {', '.join(sel['groups']) or '(none - setup skill only)'}")
    print(f"  Tools            : {', '.join(sel['tools'])}")
    print(f"  Agents           : {', '.join(sel['agents']) or '(none)'}")
    print(f"  Skills           : {', '.join(sel['skills'])}")
    if plan["local_baselines"]:
        print(f"  Local baselines  : {', '.join(f'{k}={v}' for k, v in plan['local_baselines'].items())}")
    print("=" * 78)
    for label, mark in (("add", "+"), ("update", "~"), ("remove", "-")):
        for rel in files[label]:
            print(f"  [{mark}] {rel}")
    print(f"  ({len(files['unchanged'])} file(s) already current)")
    env = plan["env"]
    if env["create"]:
        print(f"  [+] .env (new, {len(env['add_keys'])} key(s))")
    elif env["add_keys"] or env["set_keys"]:
        print(f"  [~] .env (add {', '.join(env['add_keys']) or 'nothing'}; set {', '.join(env['set_keys']) or 'nothing'})")
    if not plan["changes"]:
        print("\n[OK] Workspace already matches the profile. Nothing to do.")


def apply_profile(
    kit_dir: Path,
    target_dir: Path,
    profile: Dict[str, Any],
    dry_run: bool = False,
    as_json: bool = False,
    assume_yes: bool = False,
) -> int:
    """Install exactly what a profile selects into a separate workspace. Idempotent; prints a plan first."""
    catalog = load_catalog(kit_dir)
    if target_dir.resolve() == kit_dir.resolve():
        print("[ERROR] A profile install needs a separate workspace: pass --target-dir <your project folder>.", file=sys.stderr)
        print("        The kit folder stays the full source, so you can enable more groups later.", file=sys.stderr)
        return 1
    errors = catalog.validate_profile(profile)
    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 2

    profile = {**profile, "kit_version": kit_version(kit_dir)}
    plan = catalog.plan_install(kit_dir, target_dir, profile)
    if as_json:
        print(json.dumps({k: v for k, v in plan.items() if not k.startswith("_")}, indent=2))
    else:
        print_profile_plan(plan, dry_run)
    if dry_run or not plan["changes"]:
        return 0

    if (plan["files"]["update"] or plan["files"]["remove"]) and not assume_yes:
        if not sys.stdin.isatty():
            print("[ERROR] This changes or removes existing files; re-run with -y to confirm.", file=sys.stderr)
            return 1
        try:
            confirm = input("\nApply these changes? [y/N]: ").strip().lower()
        except EOFError:
            confirm = "n"
        if confirm not in ("y", "yes"):
            print("[ABORTED] No changes made.")
            return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    for rel in plan["files"]["add"] + plan["files"]["update"]:
        path = target_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(plan["_wanted"][rel].encode("utf-8"))
    for rel in plan["files"]["remove"]:
        path = target_dir / rel
        path.unlink(missing_ok=True)
        for parent in path.parents:
            if parent == target_dir or any(parent.iterdir()):
                break
            parent.rmdir()
    if plan["_env_text"] is not None:
        (target_dir / ".env").write_text(plan["_env_text"], encoding="utf-8")
    if plan["_profile_text"] is not None:
        (target_dir / catalog.PROFILE_FILENAME).write_text(plan["_profile_text"], encoding="utf-8")
    installed = {"kit_dir": str(kit_dir), "kit_version": profile["kit_version"], "files": sorted(plan["_wanted"])}
    (target_dir / catalog.INSTALLED_FILENAME).write_text(json.dumps(installed, indent=2) + "\n", encoding="utf-8")

    gi_path = target_dir / ".gitignore"
    gi_text = gi_path.read_text(encoding="utf-8") if gi_path.is_file() else ""
    if ".env" not in gi_text.splitlines():
        gi_path.write_text(gi_text + ("" if gi_text.endswith("\n") or not gi_text else "\n") + ".env\n", encoding="utf-8")

    if not as_json:
        print(f"\n[OK] Applied profile to {target_dir}.")
        secrets = plan["env"]["secret_keys_to_fill"]
        if secrets:
            print(f"     Fill these secret values yourself in .env or SecretStore: {', '.join(secrets)}")
    return 0


def detect_executable(names: List[str]) -> Tuple[Optional[str], str]:
    """Locate an executable on PATH and return (resolved_path, version_string)."""
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            try:
                cmd = [resolved, "--version"] if "python" in name else [resolved, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                ver = (proc.stdout or proc.stderr).strip().splitlines()[0] if (proc.stdout or proc.stderr) else "detected"
                return resolved, ver
            except Exception:
                return resolved, "detected"
    return None, "not found"


def print_language_guide() -> None:
    """Print the Systems Engineer's Language Selection & Polyglot Matrix."""
    print("\n" + "=" * 78)
    print("  LANGUAGE SELECTION GUIDE: POWERSHELL (SYSTEMS) VS. PYTHON (ANALYTICS & AI)")
    print("=" * 78)
    print(f"  {'Operational Task / Workload':<42} | {'Recommended':<18}")
    print("  " + "-" * 74)
    for task, lang, reason in LANGUAGE_RECOMMENDATION_MATRIX:
        print(f"  {task:<42} | {lang:<18}")
        print(f"    -> Why: {reason}")
    print("=" * 78)


def bootstrap_workspace(
    kit_dir: Path,
    target_dir: Path,
    init_env: bool = False,
    create_venv: bool = False,
    skip_validation: bool = False,
    force_configure_scanner: bool = False,
    skip_custom_scanner: bool = False,
    cli_scanner_keywords: Optional[List[str]] = None,
    include_docs: bool = False,
    include_prompts: bool = False,
    include_examples: bool = False,
) -> int:
    """Execute workspace initialization, optional custom scanner setup, docs build, and validation."""
    print("=" * 78)
    print("  PANTHEON AI SETUP KIT - PYTHON BOOTSTRAP & RUNTIME CHECK")
    print("=" * 78)
    print(f"  Host OS        : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Python Runtime : {sys.version.split()[0]} ({sys.executable})")

    pwsh_path, pwsh_ver = detect_executable(["pwsh"])
    ps5_path, ps5_ver = detect_executable(["powershell"])
    if pwsh_path:
        print(f"  PowerShell 7+  : {pwsh_ver} ({pwsh_path}) [RECOMMENDED FOR PS TASKS]")
    else:
        print("  PowerShell 7+  : Not detected on PATH (Install PowerShell 7.2+ for PS relays)")
    if ps5_path:
        print(f"  Windows PS 5.1 : {ps5_ver} (Legacy - supported for bootstrap, avoid for JSON APIs)")

    print_language_guide()

    # If setup.py was downloaded standalone without the rest of the repo, fetch the missing kit files
    ensure_kit_files_present(kit_dir, include_docs=include_docs, include_prompts=include_prompts, include_examples=include_examples)

    # 1. Mirror .env.template -> .env in target directory when initializing a project workspace
    env_template = kit_dir / ".env.template"
    target_env = target_dir / ".env"
    if (init_env or target_dir != kit_dir) and env_template.exists():
        if not target_env.exists():
            shutil.copy2(env_template, target_env)
            print(f"\n[STEP 1/5] Created local .env from .env.template at: {target_env}")
            print("           (Populate your tenant/API keys inside .env; .gitignore blocks it from Git)")
        else:
            print(f"\n[STEP 1/5] Local .env already exists at: {target_env} (preserved existing file)")
    else:
        print("\n[STEP 1/5] Verified .env.template contract (pass --init-env or --target-dir to create local .env)")

    # 2. Optional Virtual Environment (.venv) provisioning
    venv_dir = target_dir / ".venv"
    req_file = target_dir / "requirements.txt"
    if create_venv or req_file.exists():
        if not venv_dir.exists():
            print(f"[STEP 2/5] Provisioning isolated Python virtual environment at: {venv_dir}...")
            venv.create(venv_dir, with_pip=True)
            print("           [OK] Virtual environment created.")
        else:
            print(f"[STEP 2/5] Virtual environment already exists at: {venv_dir}")

        if req_file.exists():
            pip_exe = venv_dir / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
            if pip_exe.exists():
                print(f"           Installing dependencies from {req_file.name}...")
                subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=False)
                subprocess.run([str(pip_exe), "install", "-r", str(req_file)], check=False)
    else:
        print("[STEP 2/5] Skipping .venv creation (pass --venv to create a dedicated virtual environment)")

    # 3. Optional & Skippable Custom Keyword Leak Scanner Setup (.custom_blocklist.json / $EncodedRules)
    configure_custom_scanner(
        workspace_dir=target_dir,
        cli_keywords=cli_scanner_keywords,
        force_interactive=force_configure_scanner,
        skip_custom_scanner=skip_custom_scanner,
    )

    # 4. Local documentation compilation (opt-in for clutter-free workspaces)
    docs_builder = kit_dir / "build_docs.py"
    if include_docs and docs_builder.exists():
        print("[STEP 4/5] Compiling standalone HTML5 Local Docs (ANTIGRAVITY_DOCS.html)...")
        res = subprocess.run([sys.executable, str(docs_builder)], cwd=str(kit_dir), capture_output=True, text=True)
        if res.returncode == 0:
            print(f"           {res.stdout.strip()}")
        else:
            print(f"           [ERROR] Docs build failed:\n{res.stderr}", file=sys.stderr)
            return res.returncode
    else:
        print("[STEP 4/5] Online documentation available at: https://apswood.github.io/pantheon-ai-kit/")
        print("           (Minimal footprint: ANTIGRAVITY_DOCS.html not compiled; pass --include-docs to compile local HTML).")

    # 5. Run kit structural & zero-leak validator (validate_kit.py)
    validator = kit_dir / "validate_kit.py"
    if not skip_validation and validator.exists():
        print("[STEP 5/5] Running automated kit validator (validate_kit.py)...")
        val_res = subprocess.run([sys.executable, str(validator)], cwd=str(kit_dir))
        if val_res.returncode != 0:
            return val_res.returncode
    else:
        print("[STEP 5/5] Validation skipped.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap the PANTHEON AI Agent and Skills Setup Kit for Service Governance."
    )
    parser.add_argument(
        "--ref",
        type=str,
        default=None,
        help="Git tag/branch/SHA to download from when bootstrapping (default: $PANTHEON_REF or 'main'). Pin a release tag.",
    )
    parser.add_argument(
        "--target-dir",
        type=str,
        default=None,
        help="Target workspace directory to initialize (defaults to the setup kit directory).",
    )
    parser.add_argument(
        "--init-env",
        action="store_true",
        help="Copy .env.template to .env in the target directory if .env does not exist.",
    )
    parser.add_argument(
        "--venv",
        action="store_true",
        help="Provision a local Python virtual environment (.venv) in the target directory.",
    )
    parser.add_argument(
        "--configure-scanner",
        action="store_true",
        help="Interactively build or append to the local custom $EncodedRules keyword library (.custom_blocklist.json).",
    )
    parser.add_argument(
        "--add-scanner-keyword",
        action="append",
        dest="scanner_keywords",
        default=None,
        help="Add custom keyword(s) (comma-separated or 'Label::RegexPattern') to .custom_blocklist.json and ensure it is in .gitignore.",
    )
    parser.add_argument(
        "--skip-custom-scanner",
        action="store_true",
        help="Skip the optional interactive custom keyword leak scanner prompt.",
    )
    parser.add_argument(
        "--guide-only",
        action="store_true",
        help="Print the Python vs. PowerShell language selection guide and exit.",
    )
    parser.add_argument(
        "--adopt",
        action="store_true",
        help="Adopt existing unmanaged agents/skills in the target workspace into PANTHEON governance.",
    )
    parser.add_argument(
        "--enable",
        type=str,
        default=None,
        metavar="NAME",
        help="Switch on an agent or skill by restoring it from .agents/.disabled/.",
    )
    parser.add_argument(
        "--disable",
        type=str,
        default=None,
        metavar="NAME",
        help="Switch off an agent or skill by moving it to .agents/.disabled/ (retaining all history).",
    )
    parser.add_argument(
        "--new-agent",
        type=str,
        default=None,
        metavar="NAME",
        help="Scaffold a new specialist agent adhering to PANTHEON standards and prompt to contribute upstream.",
    )
    parser.add_argument(
        "--new-skill",
        type=str,
        default=None,
        metavar="NAME",
        help="Scaffold a new governance skill adhering to PANTHEON standards and prompt to contribute upstream.",
    )
    parser.add_argument(
        "--role",
        type=str,
        default=None,
        help="Optional role description when scaffolding with --new-agent.",
    )
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Optional description when scaffolding with --new-skill.",
    )
    parser.add_argument(
        "--uninstall-item",
        type=str,
        default=None,
        metavar="NAME",
        help="Surgically remove a specific canonical or adopted agent or skill.",
    )
    parser.add_argument(
        "--include-docs",
        action="store_true",
        help="Download ANTIGRAVITY_SETUP_GUIDE.md and compile offline ANTIGRAVITY_DOCS.html.",
    )
    parser.add_argument(
        "--include-prompts",
        action="store_true",
        help="Download master prompt reference blueprints in Governance_Framework/.",
    )
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="Download synthetic examples and sample datasets.",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip running validate_kit.py after bootstrapping.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Safely uninstall PANTHEON AI Setup Kit files from target workspace.",
    )
    parser.add_argument(
        "--purge-secrets",
        action="store_true",
        help="Delete .env and .custom_blocklist.json during uninstallation.",
    )
    parser.add_argument(
        "--purge-venv",
        action="store_true",
        help="Delete local virtual environment (.venv) during uninstallation.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the uninstallation or profile install plan without changing any files.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Confirm uninstallation non-interactively.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass source repository self-deletion protection and confirmation prompts.",
    )

    profile_opts = parser.add_argument_group("guided setup (used by the /pantheon-setup skill)")
    profile_opts.add_argument(
        "--detect",
        action="store_true",
        help="Report what is installed in --target-dir and what can be enabled, then exit.",
    )
    profile_opts.add_argument(
        "--profile",
        type=str,
        default=None,
        help="Install exactly what this pantheon.profile.json selects into --target-dir.",
    )
    profile_opts.add_argument("--groups", default=None, help="Comma-separated kit groups (overrides the profile).")
    profile_opts.add_argument(
        "--tools", default=None, help="Comma-separated tools: antigravity, claude-code, codex (overrides the profile)."
    )
    profile_opts.add_argument(
        "--integrations", default=None, help="Comma-separated integrations, e.g. itsm,teams (overrides the profile)."
    )
    profile_opts.add_argument(
        "--set",
        action="append",
        default=None,
        metavar="KEY=VALUE",
        help="Override a governance threshold, e.g. TARGET_DAILY_PACING_MINUTES=300 (repeatable).",
    )
    profile_opts.add_argument("--json", action="store_true", help="Print --detect or the profile plan as JSON.")

    args = parser.parse_args()
    global REPO_REF
    if args.ref:
        REPO_REF = args.ref
    kit_dir = Path(__file__).resolve().parent
    target_dir = Path(args.target_dir).resolve() if args.target_dir else kit_dir

    if args.guide_only:
        print_language_guide()
        return 0

    if args.adopt:
        return adopt_items(target_dir)

    if args.disable:
        return disable_item(target_dir, args.disable)

    if args.enable:
        return enable_item(target_dir, args.enable)

    if args.new_agent:
        return scaffold_agent(target_dir, args.new_agent, args.role)

    if args.new_skill:
        return scaffold_skill(target_dir, args.new_skill, args.description)

    if args.uninstall_item:
        return uninstall_single_item(target_dir, args.uninstall_item, force=args.force or args.yes)

    if args.detect:
        ensure_kit_files_present(kit_dir, include_docs=args.include_docs, include_prompts=args.include_prompts, include_examples=args.include_examples)
        report = detect_workspace(kit_dir, target_dir)
        if not args.json:
            report.pop("catalogue")
        print(json.dumps(report, indent=2))
        return 0

    if not args.uninstall:
        ensure_kit_files_present(kit_dir, include_docs=args.include_docs, include_prompts=args.include_prompts, include_examples=args.include_examples)
        try:
            profile = build_profile(args, target_dir, load_catalog(kit_dir))
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 2
        if profile is not None:
            return apply_profile(
                kit_dir, target_dir, profile, dry_run=args.dry_run, as_json=args.json, assume_yes=args.yes or args.force
            )

    if args.uninstall:
        return execute_uninstallation(
            target_dir=target_dir,
            kit_dir=kit_dir,
            purge_secrets=args.purge_secrets,
            purge_venv=args.purge_venv,
            dry_run=args.dry_run,
            force=args.force or args.yes,
        )

    return bootstrap_workspace(
        kit_dir=kit_dir,
        target_dir=target_dir,
        init_env=args.init_env,
        create_venv=args.venv,
        skip_validation=args.skip_validation,
        force_configure_scanner=args.configure_scanner,
        skip_custom_scanner=args.skip_custom_scanner,
        cli_scanner_keywords=args.scanner_keywords,
        include_docs=args.include_docs,
        include_prompts=args.include_prompts,
        include_examples=args.include_examples,
    )


if __name__ == "__main__":
    sys.exit(main())
