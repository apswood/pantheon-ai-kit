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
from typing import Dict, List, Optional, Tuple


CUSTOM_BLOCKLIST_FILENAME = ".custom_blocklist.json"
REPO_ZIP_URL = "https://github.com/apswood/pantheon-ai-kit/archive/refs/heads/main.zip"
REPO_RAW_BASE_URL = "https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main"

REQUIRED_KIT_FILES: List[str] = [
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


def ensure_kit_files_present(kit_dir: Path) -> None:
    """Download missing kit components from GitHub if setup.py is executed standalone without cloning."""
    key_markers = [
        kit_dir / "GEMINI.md",
        kit_dir / "validate_kit.py",
        kit_dir / "build_docs.py",
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
            req = urllib.request.Request(REPO_ZIP_URL, headers={"User-Agent": "Pantheon-AI-Kit-Bootstrap/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(zip_path, "wb") as out_f:
                shutil.copyfileobj(resp, out_f)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(tmp_path / "extracted")
            extracted_roots = [p for p in (tmp_path / "extracted").iterdir() if p.is_dir()]
            src_root = extracted_roots[0] if extracted_roots else (tmp_path / "extracted")
            if (src_root / "GEMINI.md").exists():
                for item in src_root.iterdir():
                    dest = kit_dir / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                downloaded_zip = True
                print("                   [OK] Downloaded and extracted all PANTHEON AI Setup Kit components.")
        except Exception as exc:
            print(f"                   [WARN] Archive download failed ({exc}). Falling back to raw file download...")

    if not downloaded_zip:
        for rel_path in REQUIRED_KIT_FILES:
            dest_file = kit_dir / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            raw_url = f"{REPO_RAW_BASE_URL}/{rel_path}"
            req = urllib.request.Request(raw_url, headers={"User-Agent": "Pantheon-AI-Kit-Bootstrap/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp, open(dest_file, "wb") as out_f:
                shutil.copyfileobj(resp, out_f)
        print(f"                   [OK] Downloaded all {len(REQUIRED_KIT_FILES)} canonical files from GitHub.")


def encode_reversed_base64(plain_text: str) -> str:
    """Reverse UTF-8 string and Base64-encode it to match the $EncodedRules format."""
    reversed_text = plain_text[::-1]
    return base64.b64encode(reversed_text.encode("utf-8")).decode("utf-8")


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
                existing_rules.append(build_keyword_rule(lbl, rgx))
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
    print("           How to add organization-specific keywords:")
    print("             * Enter a single keyword (e.g. <YourCompanyName>) OR multiple")
    print("               comma-separated keywords on one line (e.g. <Company>, <internal.domain>)")
    print("             * Optional custom regex: use 'Label::Regex' (e.g. CorpDomain::\\bcorp\\.local\\b)")
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
            existing_rules.append(rule)
            added += 1
            print(f"             + Added encoded rule (#{len(existing_rules)}) for '{lbl}' -> NameB64='{rule['NameB64']}'")

        try:
            more = input("           Add more keywords? [y/N - Press Enter to finish & save]: ").strip().lower()
        except EOFError:
            more = "n"
        if more not in ("y", "yes"):
            break

    if added > 0 or lib_path.exists():
        lib_path.write_text(json.dumps(existing_rules, indent=2), encoding="utf-8")
        ensure_gitignore_entry(workspace_dir, CUSTOM_BLOCKLIST_FILENAME)
        print(f"           [OK] Saved {len(existing_rules)} encoded rule(s) to {lib_path} (gitignored).")
    else:
        print("           [SKIP] No custom keywords added.")


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
    ensure_kit_files_present(kit_dir)

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

    # 4. Compile standalone local HTML docs (ANTIGRAVITY_DOCS.html)
    docs_builder = kit_dir / "build_docs.py"
    if docs_builder.exists():
        print("[STEP 4/5] Compiling standalone HTML5 Local Docs (ANTIGRAVITY_DOCS.html)...")
        res = subprocess.run([sys.executable, str(docs_builder)], cwd=str(kit_dir), capture_output=True, text=True)
        if res.returncode == 0:
            print(f"           {res.stdout.strip()}")
        else:
            print(f"           [ERROR] Docs build failed:\n{res.stderr}", file=sys.stderr)
            return res.returncode

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
        "--skip-validation",
        action="store_true",
        help="Skip running validate_kit.py after bootstrapping.",
    )

    args = parser.parse_args()
    kit_dir = Path(__file__).resolve().parent
    target_dir = Path(args.target_dir).resolve() if args.target_dir else kit_dir

    if args.guide_only:
        print_language_guide()
        return 0

    return bootstrap_workspace(
        kit_dir=kit_dir,
        target_dir=target_dir,
        init_env=args.init_env,
        create_venv=args.venv,
        skip_validation=args.skip_validation,
        force_configure_scanner=args.configure_scanner,
        skip_custom_scanner=args.skip_custom_scanner,
        cli_scanner_keywords=args.scanner_keywords,
    )


if __name__ == "__main__":
    sys.exit(main())
