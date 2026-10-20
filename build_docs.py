#!/usr/bin/env python3
"""build_docs.py - Zero-Dependency Standalone Local Docs Compiler.

Compiles all Markdown documentation, templates, specialist agent personas,
and governance skills in the Antigravity Governance Setup Kit into a single,
self-contained, offline-ready, mobile-responsive HTML5 Local Docs portal (`ANTIGRAVITY_DOCS.html`).

Why this Hybrid Architecture?
1. Works over `file://` via double-click in any browser (avoids browser CORS blocks
   that break client-side `fetch('file.md')` wrappers when no HTTP server is running).
2. Works 100% offline / air-gapped (zero external CDN scripts, fonts, or stylesheets).
3. Eliminates documentation drift: re-running `python build_docs.py` recompiles
   `ANTIGRAVITY_DOCS.html` directly from the live `.md` files in under 0.5 seconds.
"""

import datetime
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


DOCS_MANIFEST: List[Dict[str, str]] = [
    {
        "id": "readme",
        "title": "Quickstart & Kit Overview (README)",
        "short_title": "Quickstart & Overview",
        "category": "Onboarding & Guides",
        "badge": "Quickstart",
        "path": "README.md",
        "description": "Concise executive summary, 1-command bootstrap instructions, specialist agent & skill tables, and deep-dive guide links.",
    },
    {
        "id": "setup-guide",
        "title": "Antigravity Setup & Hygiene Guide",
        "short_title": "Setup & Hygiene Guide",
        "category": "Onboarding & Guides",
        "badge": "Primary Manual",
        "path": "ANTIGRAVITY_SETUP_GUIDE.md",
        "description": "Complete architecture, grounding frameworks, software engineering hygiene (.env, .venv, AST linting, pure vs. I/O), language selection (Python vs. PowerShell), and KPI customization manual.",
    },
    {
        "id": "gemini-md",
        "title": "Project State & Rules Template (GEMINI.md)",
        "short_title": "GEMINI.md Template",
        "category": "Workspace Rules & Templates",
        "badge": "Always-On Rule",
        "path": "GEMINI.md",
        "description": "Reusable living handover document and workspace rule template injected automatically into Antigravity sessions.",
    },
    {
        "id": "sage-master-prompt",
        "title": "SAGE Master System Prompt",
        "short_title": "SAGE Master Prompt",
        "category": "Workspace Rules & Templates",
        "badge": "Governance Rule",
        "path": "Governance_Framework/SAGE_Agent_System_Prompt.md",
        "description": "Foundational ITIL 4 & ITIL 5 Service Excellence Auditor system prompt and coaching philosophy.",
    },
    {
        "id": "aegis-master-prompt",
        "title": "AEGIS System Prompt & API Pipeline Blueprint",
        "short_title": "AEGIS Prompt & Blueprint",
        "category": "Workspace Rules & Templates",
        "badge": "Copy-Paste Prompt",
        "path": "Governance_Framework/AEGIS_Agent_System_Prompt.md",
        "description": "Copy-paste configuration analysis prompt template for PAN-OS, FortiOS, Junos, Windows, and Linux, plus an untested future project blueprint for automated API config ingestion.",
    },
    {
        "id": "env-template",
        "title": "Environment Schema (.env.template)",
        "short_title": ".env.template Schema",
        "category": "Workspace Rules & Templates",
        "badge": "Config Contract",
        "path": ".env.template",
        "description": "Safe, version-controlled environment variable contract for ITSM, Identity/Graph API, Webhooks, and Analytics.",
    },
    {
        "id": "agent-aegis",
        "title": "AEGIS — Infrastructure Best-Practice Analyser",
        "short_title": "AEGIS (Best Practice)",
        "category": "Specialist Advisory Agents",
        "badge": "Agent Persona",
        "path": ".agents/agents/aegis_best_practice/agent.md",
        "description": "Specialist auditor for Palo Alto (PAN-OS), FortiGate (FortiOS), Juniper (Junos), Windows Server, and Linux Server against NIST, NCSC, vendor guides, and UKFS-01..06.",
    },
    {
        "id": "agent-atlas",
        "title": "ATLAS — Technical Architecture Advisor",
        "short_title": "ATLAS (Architecture)",
        "category": "Specialist Advisory Agents",
        "badge": "Agent Persona",
        "path": ".agents/agents/atlas_architecture/agent.md",
        "description": "Specialist advisor for modular system design, pure-function vs. I/O separation, and Python/PowerShell runtime parity.",
    },
    {
        "id": "agent-sage",
        "title": "SAGE — Governance & Service Management",
        "short_title": "SAGE (Governance)",
        "category": "Specialist Advisory Agents",
        "badge": "Agent Persona",
        "path": ".agents/agents/sage_governance/agent.md",
        "description": "Specialist advisor for ITIL 4 & ITIL 5 governance, SLA/staleness auditing, KPI calibration, and evidence-based coaching.",
    },
    {
        "id": "agent-sentinel",
        "title": "SENTINEL — Security & Compliance Auditor",
        "short_title": "SENTINEL (Security)",
        "category": "Specialist Advisory Agents",
        "badge": "Agent Persona",
        "path": ".agents/agents/sentinel_security/agent.md",
        "description": "Specialist advisor for zero-trust secret isolation, DPAPI/SecretStore integration, ACL handling, and PII redaction.",
    },
    {
        "id": "agent-spark",
        "title": "SPARK — Contrarian & Automation Innovator",
        "short_title": "SPARK (Innovation)",
        "category": "Specialist Advisory Agents",
        "badge": "Agent Persona",
        "path": ".agents/agents/spark_disruptor/agent.md",
        "description": "Specialist challenger focused on eliminating operational toil, challenging metric gaming, and automating root causes.",
    },
    {
        "id": "skill-best-practice",
        "title": "Infrastructure Best-Practice Analyser & Standards Catalogue",
        "short_title": "Best-Practice Analyser",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/infrastructure-best-practice-analyser/SKILL.md",
        "description": "Multi-platform standards catalogue (NIST 800-41/800-53/CSF 2.0, NCSC, UKFS-01..06, ISO/CIS/PCI/SWIFT placeholders) for PAN-OS, FortiOS, Junos, Windows & Linux.",
    },
    {
        "id": "skill-backlog",
        "title": "Ticket Backlog Governance Skill",
        "short_title": "Backlog Governance",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/ticket-backlog-governance/SKILL.md",
        "description": "Business-hours staleness engine, 5-tier age bucketing, and 4-criterion 145-point backlog prioritization rubric.",
    },
    {
        "id": "skill-productivity",
        "title": "Productivity & Workload Governance Skill",
        "short_title": "Productivity & Pacing",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/productivity-workload-governance/SKILL.md",
        "description": "315-minute daily time target, 80% weekly utilization ceiling, dynamic FTE capacity normalization, and automated event isolation.",
    },
    {
        "id": "skill-quality",
        "title": "Quality Audit Governance Skill",
        "short_title": "Quality Audit (QA)",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/quality-audit-governance/SKILL.md",
        "description": "Dual-metric QA framework combining Binary Resolve Pass % with Granular Diagnostic Score % and 6-month trends.",
    },
    {
        "id": "skill-digest",
        "title": "Teams Standup Digest Notifier Skill",
        "short_title": "Standup Digest Notifier",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/teams-standup-digest-notifier/SKILL.md",
        "description": "Daily morning standup Adaptive Card digest payload assembly, webhook delivery gating, and health indicators.",
    },
    {
        "id": "skill-coaching",
        "title": "Support Governance & Coaching Framework",
        "short_title": "Coaching Framework",
        "category": "Operational & KPI Skills",
        "badge": "Skill Runbook",
        "path": ".agents/skills/support-team-governance-analytics-coaching/SKILL.md",
        "description": "Cross-dimensional synthesis across Backlog, Quality, Productivity, and Customer Sentiment with 3-step coaching plans.",
    },
]


def split_frontmatter(raw_text: str) -> Tuple[Dict[str, str], str]:
    """Extract YAML frontmatter if present and return (meta_dict, body_markdown)."""
    lines = raw_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, raw_text

    end_idx = -1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx == -1:
        return {}, raw_text

    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")

    meta: Dict[str, str] = {}
    current_key = ""
    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            k, v = line.split(":", 1)
            current_key = k.strip()
            v_clean = v.strip()
            if v_clean in (">", ">-", "|", "|-"):
                meta[current_key] = ""
            else:
                meta[current_key] = v_clean.strip("'\"")
        elif current_key:
            prev = meta.get(current_key, "")
            meta[current_key] = (prev + " " + stripped).strip()

    return meta, body


def slugify(text: str) -> str:
    """Create a URL-safe anchor slug from heading text."""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"[^\w\s-]", "", clean).strip().lower()
    return re.sub(r"[\s_-]+", "-", clean) or "section"


def render_inline(text: str, page_id: str = "") -> str:
    """Convert inline Markdown (code spans, links, bold, italic) to safe HTML."""
    code_tokens: List[str] = []

    def _save_code(match: re.Match) -> str:
        code_content = html.escape(match.group(1))
        idx = len(code_tokens)
        code_tokens.append(f'<code class="inline-code">{code_content}</code>')
        return f"\x00CODE{idx}\x00"

    processed = re.sub(r"`([^`]+)`", _save_code, text)
    processed = html.escape(processed)

    # Links: [label](url)
    def _render_link(match: re.Match) -> str:
        label = match.group(1)
        url = html.unescape(match.group(2)).strip()

        # 1. Links pointing to GitHub Pages portal hash (https://apswood.github.io/pantheon-ai-kit/#...)
        gh_pages_prefix = "https://apswood.github.io/pantheon-ai-kit/#"
        if url.startswith(gh_pages_prefix):
            hash_target = url[len(gh_pages_prefix) :].strip()
            if hash_target:
                return (
                    f'<a href="#{html.escape(hash_target)}" class="docs-internal-link" '
                    f'onclick="navigateToHash(\'{html.escape(hash_target)}\'); return false;">{label}</a>'
                )

        # 2. Same-page anchor links (#section-slug)
        if url.startswith("#") and len(url) > 1:
            raw_anchor = url[1:]
            # Check if raw_anchor is already a page ID or prefixed with a page ID
            is_known_prefix = any(
                raw_anchor == m["id"] or raw_anchor.startswith(m["id"] + "-")
                for m in DOCS_MANIFEST
            )
            full_anchor = raw_anchor if is_known_prefix or not page_id else f"{page_id}-{slugify(raw_anchor)}"
            return (
                f'<a href="#{html.escape(full_anchor)}" class="docs-internal-link" '
                f'onclick="navigateToHash(\'{html.escape(full_anchor)}\'); return false;">{label}</a>'
            )

        # 3. Relative file links with or without #anchor (e.g., ANTIGRAVITY_SETUP_GUIDE.md#67-...)
        file_part, sep, anchor_part = url.partition("#")
        clean_file = file_part.lstrip("./")
        for item in DOCS_MANIFEST:
            if clean_file == item["path"] or file_part.endswith("/" + item["path"]):
                if sep and anchor_part:
                    target_hash = (
                        anchor_part
                        if anchor_part.startswith(item["id"] + "-")
                        else f"{item['id']}-{slugify(anchor_part)}"
                    )
                    return (
                        f'<a href="#{html.escape(target_hash)}" class="docs-internal-link" '
                        f'onclick="navigateToPage(\'{item["id"]}\', \'{html.escape(target_hash)}\'); return false;">{label}</a>'
                    )
                return (
                    f'<a href="#{item["id"]}" class="docs-internal-link" '
                    f'onclick="navigateToPage(\'{item["id"]}\'); return false;">{label}</a>'
                )

        target = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""
        return f'<a href="{html.escape(url)}"{target}>{label}</a>'

    processed = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _render_link, processed)

    # Bold + Italic
    processed = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", processed)
    processed = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", processed)
    processed = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", processed)

    # Restore inline code tokens
    for idx, token_html in enumerate(code_tokens):
        processed = processed.replace(f"\x00CODE{idx}\x00", token_html)

    return processed


def markdown_to_html(md_text: str, page_id: str) -> Tuple[str, List[Dict[str, Any]]]:
    """Convert a Markdown document into rich semantic HTML and extract a TOC list."""
    lines = md_text.splitlines()
    out: List[str] = []
    toc: List[Dict[str, Any]] = []
    used_slugs: Dict[str, int] = {}

    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 1. Empty line
        if not stripped:
            i += 1
            continue

        # 2. Fenced code block (``` or ~~~)
        fence_match = re.match(r"^(\s*)(`{3,}|~{3,})(.*)$", line)
        if fence_match:
            fence_chars = fence_match.group(2)
            lang = fence_match.group(3).strip() or "text"
            code_lines: List[str] = []
            i += 1
            while i < n:
                close_match = re.match(r"^\s*" + re.escape(fence_chars) + r"\s*$", lines[i])
                if close_match:
                    i += 1
                    break
                code_lines.append(lines[i])
                i += 1
            raw_code = "\n".join(code_lines)
            escaped_code = html.escape(raw_code)
            lang_badge = html.escape(lang.upper())
            out.append(
                f'<div class="code-block-wrapper">'
                f'<div class="code-block-header">'
                f'<span class="code-lang">{lang_badge}</span>'
                f'<button type="button" class="copy-btn" onclick="copyCodeBlock(this)" title="Copy code to clipboard">Copy</button>'
                f"</div>"
                f'<pre class="code-pre"><code>{escaped_code}</code></pre>'
                f"</div>"
            )
            continue

        # 3. Horizontal rule
        if re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", stripped):
            out.append('<hr class="section-divider" />')
            i += 1
            continue

        # 4. Headings (# to ######)
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            raw_title = heading_match.group(2).strip()
            base_slug = f"{page_id}-{slugify(raw_title)}"
            count = used_slugs.get(base_slug, 0)
            used_slugs[base_slug] = count + 1
            slug = f"{base_slug}-{count}" if count > 0 else base_slug
            rendered_title = render_inline(raw_title, page_id)
            clean_title = re.sub(r"<[^>]+>", "", rendered_title)

            if level in (2, 3):
                toc.append({"level": level, "id": slug, "title": clean_title})

            out.append(
                f'<h{level} id="{slug}" class="doc-heading doc-h{level}">'
                f"{rendered_title}"
                f'<a class="heading-anchor" href="#{slug}" title="Link to this section">#</a>'
                f"</h{level}>"
            )
            i += 1
            continue

        # 5. Markdown Table
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # Skip header and alignment row
            body_rows: List[List[str]] = []
            while i < n and "|" in lines[i].strip() and lines[i].strip():
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                body_rows.append(row_cells)
                i += 1

            table_html = ['<div class="table-responsive"><table class="docs-table"><thead><tr>']
            for cell in header_cells:
                table_html.append(f"<th>{render_inline(cell, page_id)}</th>")
            table_html.append("</tr></thead><tbody>")
            for row in body_rows:
                table_html.append("<tr>")
                for idx_c in range(len(header_cells)):
                    val = row[idx_c] if idx_c < len(row) else ""
                    table_html.append(f"<td>{render_inline(val, page_id)}</td>")
                table_html.append("</tr>")
            table_html.append("</tbody></table></div>")
            out.append("".join(table_html))
            continue

        # 6. Blockquote / GitHub Alert (> [!NOTE], > [!IMPORTANT], etc.)
        if stripped.startswith(">"):
            quote_lines: List[str] = []
            while i < n and lines[i].strip().startswith(">"):
                q_line = re.sub(r"^\s*>\s?", "", lines[i])
                quote_lines.append(q_line)
                i += 1

            first_line = quote_lines[0].strip() if quote_lines else ""
            alert_match = re.match(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", first_line, re.IGNORECASE)
            if alert_match:
                alert_type = alert_match.group(1).upper()
                remainder_first = alert_match.group(2).strip()
                alert_body_lines = ([remainder_first] if remainder_first else []) + quote_lines[1:]
                body_rendered = "<br/>".join(render_inline(x, page_id) for x in alert_body_lines if x.strip())
                out.append(
                    f'<div class="callout callout-{alert_type.lower()}">'
                    f'<div class="callout-title">{alert_type}</div>'
                    f'<div class="callout-body">{body_rendered}</div>'
                    f"</div>"
                )
            else:
                body_rendered = "<br/>".join(render_inline(x, page_id) for x in quote_lines if x.strip())
                out.append(f'<blockquote class="docs-quote">{body_rendered}</blockquote>')
            continue

        # 7. Unordered or Ordered Lists
        list_match = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", line)
        if list_match:
            is_ordered = bool(re.match(r"^\d+\.$", list_match.group(2)))
            tag = "ol" if is_ordered else "ul"
            items_html: List[str] = [f'<{tag} class="docs-list">']

            while i < n:
                curr = lines[i]
                if not curr.strip():
                    if i + 1 < n and re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", lines[i + 1]):
                        i += 1
                        continue
                    break

                m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", curr)
                if m:
                    indent = len(m.group(1))
                    item_content = render_inline(m.group(3).strip(), page_id)
                    sub_class = ' class="nested-list-item"' if indent >= 2 else ""
                    items_html.append(f"<li{sub_class}>{item_content}")
                    i += 1
                    while i < n:
                        next_line = lines[i]
                        if not next_line.strip():
                            break
                        if re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", next_line) or re.match(r"^(#{1,6})\s+", next_line.strip()):
                            break
                        if next_line.strip().startswith("```"):
                            break
                        if next_line.startswith("  ") or next_line.startswith("\t"):
                            items_html.append(f"<br/>{render_inline(next_line.strip(), page_id)}")
                            i += 1
                        else:
                            break
                    items_html.append("</li>")
                else:
                    break

            items_html.append(f"</{tag}>")
            out.append("".join(items_html))
            continue

        # 8. Standard Paragraph
        para_lines: List[str] = []
        while i < n:
            curr = lines[i]
            curr_s = curr.strip()
            if not curr_s:
                break
            if (
                curr_s.startswith("#")
                or curr_s.startswith("```")
                or curr_s.startswith("~~~")
                or curr_s.startswith(">")
                or re.match(r"^(\*{3,}|-{3,}|_{3,})\s*$", curr_s)
                or re.match(r"^(\s*)([-*+]|\d+\.)\s+", curr)
                or ("|" in curr_s and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]))
            ):
                break
            para_lines.append(render_inline(curr_s, page_id))
            i += 1

        if para_lines:
            out.append(f'<p class="docs-para">{" ".join(para_lines)}</p>')

    return "\n".join(out), toc


def build_docs_html(kit_dir: Path) -> Path:
    """Compile all manifest files in kit_dir into ANTIGRAVITY_DOCS.html."""
    pages_data: List[Dict[str, Any]] = []

    for entry in DOCS_MANIFEST:
        file_path = kit_dir / entry["path"]
        if not file_path.exists():
            raise FileNotFoundError(f"Missing source file for docs compilation: {file_path}")

        raw_content = file_path.read_text(encoding="utf-8")
        if entry["path"].endswith(".env.template"):
            meta: Dict[str, str] = {}
            md_body = (
                "# Environment Configuration Schema (`.env.template`)\n\n"
                "> Copy this file to `.env` in your workspace root and populate your local values. "
                "The `.gitignore` policy strictly prevents `.env` from being committed to Git.\n\n"
                f"```ini\n{raw_content}\n```"
            )
        else:
            meta, md_body = split_frontmatter(raw_content)

        rendered_html, toc = markdown_to_html(md_body, entry["id"])

        # Prepend YAML Frontmatter metadata banner for Agents and Skills
        if meta:
            meta_rows = "".join(
                f'<div class="fm-item"><span class="fm-key">{html.escape(k)}:</span> '
                f'<span class="fm-val">{html.escape(str(v))}</span></div>'
                for k, v in meta.items()
            )
            fm_banner = (
                f'<div class="frontmatter-card">'
                f'<div class="frontmatter-header">Antigravity Discovery Frontmatter (YAML)</div>'
                f'<div class="frontmatter-body">{meta_rows}</div>'
                f"</div>"
            )
            rendered_html = fm_banner + "\n" + rendered_html

        plain_text = re.sub(r"<[^>]+>", " ", rendered_html)
        plain_text = re.sub(r"\s+", " ", html.unescape(plain_text)).strip()

        pages_data.append(
            {
                "id": entry["id"],
                "title": entry["title"],
                "short_title": entry["short_title"],
                "category": entry["category"],
                "badge": entry["badge"],
                "path": entry["path"],
                "description": entry["description"],
                "html": rendered_html,
                "toc": toc,
                "search_text": plain_text,
                "line_count": len(raw_content.splitlines()),
                "byte_size": len(raw_content.encode("utf-8")),
            }
        )

    # Group pages by category for sidebar rendering
    categories: Dict[str, List[Dict[str, Any]]] = {}
    for p in pages_data:
        categories.setdefault(p["category"], []).append(p)

    default_page_id = "readme"
    sidebar_nav_html: List[str] = []
    for cat_name, items in categories.items():
        sidebar_nav_html.append(f'<div class="nav-category"><div class="nav-category-title">{html.escape(cat_name)}</div>')
        for item in items:
            active_cls = " active" if item["id"] == default_page_id else ""
            sidebar_nav_html.append(
                f'<button type="button" class="nav-item{active_cls}" id="nav-{item["id"]}" '
                f'onclick="navigateToPage(\'{item["id"]}\')">'
                f'<span class="nav-item-title">{html.escape(item["short_title"])}</span>'
                f'<span class="nav-item-badge">{html.escape(item["badge"])}</span>'
                f"</button>"
            )
        sidebar_nav_html.append("</div>")

    # Build pre-rendered <article> panels so page content works even if JS is restricted
    articles_html: List[str] = []
    for p in pages_data:
        hidden_cls = "" if p["id"] == default_page_id else " hidden"
        kb_size = f"{p['byte_size'] / 1024:.1f} KB"
        articles_html.append(
            f'<article class="docs-article{hidden_cls}" id="page-{p["id"]}" data-page-id="{p["id"]}">'
            f'<div class="article-meta-bar">'
            f'<div class="meta-breadcrumbs">'
            f'<span class="meta-cat">{html.escape(p["category"])}</span>'
            f'<span class="meta-sep">/</span>'
            f'<code class="meta-path">{html.escape(p["path"])}</code>'
            f"</div>"
            f'<div class="meta-stats">'
            f'<span class="stat-pill">{p["line_count"]} lines</span>'
            f'<span class="stat-pill">{kb_size}</span>'
            f"</div>"
            f"</div>"
            f'<p class="article-lead">{html.escape(p["description"])}</p>'
            f'<div class="article-body">{p["html"]}</div>'
            f"</article>"
        )

    # Lightweight JSON index for TOC & instant client-side full-text search
    client_index = [
        {
            "id": p["id"],
            "title": p["title"],
            "short_title": p["short_title"],
            "category": p["category"],
            "path": p["path"],
            "toc": p["toc"],
            "search_text": p["search_text"],
        }
        for p in pages_data
    ]
    index_json = json.dumps(client_index, ensure_ascii=False)
    build_timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_docs = len(pages_data)

    docs_portal = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PANTHEON AI Kit for Service Governance — Antigravity Local Docs</title>
  <style>
    :root[data-theme="dark"] {{
      --bg-primary: #0d1117;
      --bg-secondary: #161b22;
      --bg-tertiary: #21262d;
      --bg-elevated: #1c2128;
      --border-color: #30363d;
      --border-subtle: #21262d;
      --text-primary: #e6edf3;
      --text-secondary: #8b949e;
      --text-muted: #6e7681;
      --accent-primary: #58a6ff;
      --accent-hover: #79c0ff;
      --accent-subtle: rgba(56, 139, 253, 0.15);
      --success-color: #3fb950;
      --warning-color: #d29922;
      --danger-color: #f85149;
      --code-bg: #11161d;
      --inline-code-bg: rgba(110, 118, 129, 0.25);
      --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.5);
    }}

    :root[data-theme="light"] {{
      --bg-primary: #ffffff;
      --bg-secondary: #f6f8fa;
      --bg-tertiary: #eaeef2;
      --bg-elevated: #ffffff;
      --border-color: #d0d7de;
      --border-subtle: #eaeef2;
      --text-primary: #1f2328;
      --text-secondary: #57606a;
      --text-muted: #6e7781;
      --accent-primary: #0969da;
      --accent-hover: #0550ae;
      --accent-subtle: rgba(9, 105, 218, 0.1);
      --success-color: #1a7f37;
      --warning-color: #9a6700;
      --danger-color: #cf222e;
      --code-bg: #f6f8fa;
      --inline-code-bg: rgba(175, 184, 193, 0.25);
      --shadow-lg: 0 8px 24px rgba(140, 149, 159, 0.2);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      overflow-x: clip;
      max-width: 100%;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.65;
      font-size: 15px;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}

    /* Top Header Bar */
    .top-navbar {{
      position: sticky;
      top: 0;
      z-index: 150;
      min-height: 60px;
      background-color: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 20px;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
      flex: 1 1 auto;
    }}

    .mobile-menu-btn {{
      display: none;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background-color: var(--bg-tertiary);
      color: var(--text-primary);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      flex-shrink: 0;
    }}

    .mobile-menu-btn:hover {{
      border-color: var(--accent-primary);
    }}

    .brand-badge {{
      background: linear-gradient(135deg, #238636, #1f6feb);
      color: #ffffff;
      font-weight: 700;
      font-size: 11.5px;
      letter-spacing: 0.6px;
      padding: 4px 9px;
      border-radius: 6px;
      text-transform: uppercase;
      flex-shrink: 0;
    }}

    .brand-title {{
      font-size: 15.5px;
      font-weight: 600;
      color: var(--text-primary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .brand-subtitle {{
      font-size: 12px;
      color: var(--text-secondary);
      display: none;
      white-space: nowrap;
    }}

    @media (min-width: 1240px) {{
      .brand-subtitle {{
        display: inline;
      }}
    }}

    .header-controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }}

    .search-wrapper {{
      position: relative;
      width: clamp(190px, 26vw, 320px);
    }}

    .search-input {{
      width: 100%;
      padding: 7px 12px 7px 32px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-size: 13px;
      outline: none;
      transition: border-color 0.15s;
    }}

    .search-input:focus {{
      border-color: var(--accent-primary);
    }}

    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 13px;
      pointer-events: none;
    }}

    .search-results-dropdown {{
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      width: min(460px, calc(100vw - 24px));
      max-height: min(440px, 68vh);
      overflow-y: auto;
      background-color: var(--bg-elevated);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      box-shadow: var(--shadow-lg);
      display: none;
      z-index: 250;
    }}

    .search-results-dropdown.open {{
      display: block;
    }}

    .search-hit {{
      display: block;
      width: 100%;
      text-align: left;
      padding: 10px 14px;
      background: none;
      border: none;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-primary);
      cursor: pointer;
    }}

    .search-hit:hover {{
      background-color: var(--accent-subtle);
    }}

    .search-hit-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--accent-primary);
      margin-bottom: 2px;
      overflow-wrap: break-word;
    }}

    .search-hit-snippet {{
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.4;
      overflow-wrap: break-word;
    }}

    .theme-btn {{
      padding: 6px 11px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background-color: var(--bg-tertiary);
      color: var(--text-primary);
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .theme-btn:hover {{
      border-color: var(--accent-primary);
    }}

    /* Mobile Backdrop Overlay for Drawer */
    .sidebar-backdrop {{
      display: none;
      position: fixed;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.55);
      z-index: 290;
      backdrop-filter: blur(2px);
    }}

    .sidebar-backdrop.open {{
      display: block;
    }}

    /* 3-Column Docs Layout */
    .docs-layout {{
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr) 250px;
      flex: 1;
      max-width: 1680px;
      width: 100%;
      margin: 0 auto;
    }}

    /* Left Navigation Sidebar */
    .left-sidebar {{
      background-color: var(--bg-secondary);
      border-right: 1px solid var(--border-color);
      padding: 20px 14px;
      height: calc(100vh - 60px);
      position: sticky;
      top: 60px;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    }}

    .mobile-sidebar-header {{
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 4px 8px 14px;
      margin-bottom: 14px;
      border-bottom: 1px solid var(--border-color);
    }}

    .mobile-sidebar-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text-primary);
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}

    .mobile-sidebar-close {{
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background-color: var(--bg-tertiary);
      color: var(--text-primary);
      font-size: 12px;
      cursor: pointer;
    }}

    .nav-category {{
      margin-bottom: 20px;
    }}

    .nav-category-title {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      padding: 0 10px 6px;
    }}

    .nav-item {{
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      text-align: left;
      padding: 8px 10px;
      margin-bottom: 3px;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-secondary);
      font-size: 13px;
      cursor: pointer;
      transition: all 0.12s ease;
    }}

    .nav-item:hover {{
      background-color: var(--bg-tertiary);
      color: var(--text-primary);
    }}

    .nav-item.active {{
      background-color: var(--accent-subtle);
      border-color: rgba(88, 166, 255, 0.35);
      color: var(--accent-primary);
      font-weight: 600;
    }}

    .nav-item-title {{
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .nav-item-badge {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 10px;
      background-color: var(--bg-tertiary);
      color: var(--text-muted);
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .nav-item.active .nav-item-badge {{
      background-color: var(--accent-primary);
      color: #ffffff;
    }}

    /* Mobile / Tablet Collapsible On-This-Page TOC */
    .mobile-toc {{
      display: none;
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      margin-bottom: 20px;
      overflow: hidden;
    }}

    .mobile-toc summary {{
      padding: 10px 14px;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--accent-primary);
      cursor: pointer;
      user-select: none;
      list-style: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .mobile-toc summary::-webkit-details-marker {{
      display: none;
    }}

    .mobile-toc summary::after {{
      content: "▾";
      font-size: 12px;
      color: var(--text-secondary);
      transition: transform 0.15s ease;
    }}

    .mobile-toc[open] summary::after {{
      transform: rotate(180deg);
    }}

    .mobile-toc-body {{
      padding: 8px 14px 12px;
      border-top: 1px solid var(--border-subtle);
      max-height: 48vh;
      overflow-y: auto;
    }}

    /* Center Content Area */
    .content-pane {{
      padding: 34px 44px 80px;
      min-width: 0;
      max-width: 100%;
    }}

    .docs-article.hidden {{
      display: none;
    }}

    .article-meta-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      padding-bottom: 14px;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border-color);
    }}

    .meta-breadcrumbs {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      font-size: 13px;
      min-width: 0;
    }}

    .meta-cat {{
      color: var(--accent-primary);
      font-weight: 600;
    }}

    .meta-sep {{
      color: var(--text-muted);
    }}

    .meta-path {{
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-color);
      padding: 2px 8px;
      border-radius: 4px;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12px;
      color: var(--text-secondary);
      word-break: break-all;
    }}

    .meta-stats {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .stat-pill {{
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 12px;
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      white-space: nowrap;
    }}

    .article-lead {{
      font-size: 14px;
      color: var(--text-secondary);
      background-color: var(--bg-secondary);
      border-left: 3px solid var(--accent-primary);
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      margin-bottom: 24px;
      overflow-wrap: break-word;
    }}

    /* YAML Frontmatter Card */
    .frontmatter-card {{
      background-color: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      margin-bottom: 24px;
      overflow: hidden;
    }}

    .frontmatter-header {{
      background-color: var(--bg-tertiary);
      padding: 6px 14px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: var(--text-secondary);
      border-bottom: 1px solid var(--border-color);
    }}

    .frontmatter-body {{
      padding: 12px 14px;
      font-size: 13px;
      overflow-wrap: break-word;
      word-break: break-word;
    }}

    .fm-item {{
      margin-bottom: 4px;
    }}

    .fm-key {{
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-weight: 600;
      color: var(--accent-primary);
    }}

    .fm-val {{
      color: var(--text-primary);
    }}

    /* Typography */
    .doc-heading {{
      color: var(--text-primary);
      font-weight: 600;
      line-height: 1.3;
      scroll-margin-top: 86px;
      overflow-wrap: break-word;
    }}

    .doc-h1 {{
      font-size: 26px;
      margin: 8px 0 18px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-color);
    }}

    .doc-h2 {{
      font-size: 20px;
      margin: 32px 0 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .doc-h3 {{
      font-size: 16.5px;
      margin: 22px 0 10px;
      color: var(--accent-hover);
    }}

    .doc-h4, .doc-h5, .doc-h6 {{
      font-size: 15px;
      margin: 18px 0 8px;
    }}

    .heading-anchor {{
      margin-left: 8px;
      color: var(--text-muted);
      text-decoration: none;
      opacity: 0;
      font-weight: 400;
      transition: opacity 0.15s;
    }}

    .doc-heading:hover .heading-anchor {{
      opacity: 1;
    }}

    .docs-para {{
      margin-bottom: 14px;
      color: var(--text-primary);
      overflow-wrap: break-word;
      word-break: break-word;
    }}

    .docs-list {{
      margin: 0 0 16px 22px;
    }}

    .docs-list li {{
      margin-bottom: 6px;
      overflow-wrap: break-word;
      word-break: break-word;
    }}

    .docs-list li.nested-list-item {{
      margin-left: 18px;
      list-style-type: circle;
    }}

    .section-divider {{
      border: 0;
      border-top: 1px solid var(--border-color);
      margin: 28px 0;
    }}

    a {{
      color: var(--accent-primary);
      text-decoration: none;
      overflow-wrap: break-word;
    }}

    a:hover {{
      text-decoration: underline;
    }}

    .inline-code {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 0.88em;
      background-color: var(--inline-code-bg);
      padding: 2px 6px;
      border-radius: 4px;
      overflow-wrap: anywhere;
      word-break: break-word;
    }}

    /* Code Blocks */
    .code-block-wrapper {{
      margin: 16px 0 22px;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      overflow: hidden;
      background-color: var(--code-bg);
      max-width: 100%;
    }}

    .code-block-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 14px;
      background-color: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
    }}

    .code-lang {{
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-secondary);
      letter-spacing: 0.5px;
    }}

    .copy-btn {{
      background-color: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      font-size: 11px;
      padding: 3px 10px;
      border-radius: 4px;
      cursor: pointer;
    }}

    .copy-btn:hover {{
      border-color: var(--accent-primary);
    }}

    .code-pre {{
      padding: 14px 16px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      white-space: pre;
      word-wrap: normal;
      overflow-wrap: normal;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 13px;
      line-height: 1.5;
      color: var(--text-primary);
      max-width: 100%;
    }}

    /* Tables */
    .table-responsive {{
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 16px 0 24px;
      border: 1px solid var(--border-color);
      border-radius: 8px;
    }}

    .docs-table {{
      width: 100%;
      min-width: 520px;
      border-collapse: collapse;
      font-size: 13.5px;
    }}

    .docs-table th {{
      background-color: var(--bg-secondary);
      color: var(--text-primary);
      font-weight: 600;
      text-align: left;
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
    }}

    .docs-table td {{
      padding: 9px 14px;
      border-bottom: 1px solid var(--border-subtle);
      vertical-align: top;
      overflow-wrap: break-word;
    }}

    .docs-table tr:last-child td {{
      border-bottom: none;
    }}

    .docs-table tr:hover td {{
      background-color: var(--bg-secondary);
    }}

    /* Callouts & Blockquotes */
    .docs-quote {{
      margin: 16px 0;
      padding: 12px 16px;
      border-left: 4px solid var(--border-color);
      background-color: var(--bg-secondary);
      color: var(--text-secondary);
      border-radius: 0 6px 6px 0;
      overflow-wrap: break-word;
    }}

    .callout {{
      margin: 18px 0;
      padding: 14px 16px;
      border-left: 4px solid var(--accent-primary);
      background-color: var(--bg-secondary);
      border-radius: 0 8px 8px 0;
      overflow-wrap: break-word;
    }}

    .callout-title {{
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.6px;
      margin-bottom: 6px;
      color: var(--accent-primary);
    }}

    .callout-important, .callout-warning {{
      border-left-color: var(--warning-color);
    }}
    .callout-important .callout-title, .callout-warning .callout-title {{
      color: var(--warning-color);
    }}

    .callout-caution {{
      border-left-color: var(--danger-color);
    }}
    .callout-caution .callout-title {{
      color: var(--danger-color);
    }}

    .callout-tip {{
      border-left-color: var(--success-color);
    }}
    .callout-tip .callout-title {{
      color: var(--success-color);
    }}

    /* Right Table of Contents Sidebar */
    .toc-sidebar {{
      padding: 24px 16px;
      height: calc(100vh - 60px);
      position: sticky;
      top: 60px;
      overflow-y: auto;
      border-left: 1px solid var(--border-subtle);
    }}

    .toc-header {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin-bottom: 10px;
    }}

    .toc-link {{
      display: block;
      font-size: 12.5px;
      color: var(--text-secondary);
      padding: 4px 0 4px 10px;
      border-left: 2px solid var(--border-subtle);
      text-decoration: none;
      line-height: 1.35;
      overflow-wrap: break-word;
    }}

    .toc-link:hover {{
      color: var(--accent-primary);
      text-decoration: none;
    }}

    .toc-link.toc-level-3 {{
      padding-left: 22px;
      font-size: 12px;
    }}

    .docs-footer {{
      margin-top: 48px;
      padding-top: 18px;
      border-top: 1px solid var(--border-color);
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }}

    /* Responsive Breakpoints */
    @media (max-width: 1240px) {{
      .docs-layout {{
        grid-template-columns: 260px minmax(0, 1fr);
      }}
      .toc-sidebar {{
        display: none;
      }}
      .mobile-toc {{
        display: block;
      }}
    }}

    @media (max-width: 960px) {{
      .mobile-menu-btn {{
        display: inline-flex;
      }}
      .docs-layout {{
        grid-template-columns: minmax(0, 1fr);
      }}
      .left-sidebar {{
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: min(310px, 86vw);
        height: 100vh;
        z-index: 300;
        transform: translateX(-105%);
        transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-lg);
      }}
      .left-sidebar.open {{
        transform: translateX(0);
      }}
      .mobile-sidebar-header {{
        display: flex;
      }}
      .content-pane {{
        padding: 24px 22px 64px;
      }}
    }}

    @media (max-width: 680px) {{
      .top-navbar {{
        padding: 8px 12px;
        gap: 8px;
      }}
      .brand-title {{
        font-size: 14px;
      }}
      .header-controls {{
        width: 100%;
        order: 3;
      }}
      .search-wrapper {{
        flex: 1 1 auto;
        width: 100%;
      }}
      .search-results-dropdown {{
        left: 0;
        right: 0;
        width: 100%;
      }}
      .content-pane {{
        padding: 16px 14px 48px;
      }}
      .doc-heading {{
        scroll-margin-top: 112px;
      }}
      .doc-h1 {{
        font-size: 21px;
        margin: 4px 0 14px;
      }}
      .doc-h2 {{
        font-size: 17.5px;
        margin: 24px 0 10px;
      }}
      .doc-h3 {{
        font-size: 15px;
      }}
      body {{
        font-size: 14.5px;
      }}
      .code-pre {{
        font-size: 12px;
        padding: 10px 12px;
      }}
      .docs-table {{
        font-size: 12.5px;
      }}
      .docs-table th, .docs-table td {{
        padding: 8px 10px;
      }}
    }}

    @media print {{
      .top-navbar, .left-sidebar, .toc-sidebar, .mobile-toc, .sidebar-backdrop, .copy-btn {{
        display: none !important;
      }}
      .docs-layout {{
        display: block;
      }}
      .content-pane {{
        padding: 0;
      }}
    }}
  </style>
</head>
<body>
  <header class="top-navbar">
    <div class="brand-group">
      <button type="button" class="mobile-menu-btn" onclick="toggleMobileSidebar()" aria-label="Toggle documentation menu">
        &#9776; <span>Docs</span>
      </button>
      <span class="brand-badge">PANTHEON AI</span>
      <span class="brand-title">Service Governance &amp; Hardening Kit</span>
      <span class="brand-subtitle">— Offline Local Documentation Portal ({total_docs} Modules)</span>
    </div>
    <button type="button" class="theme-btn" id="theme-toggle-btn" onclick="toggleTheme()">
      Light / Dark
    </button>
    <div class="header-controls">
      <div class="search-wrapper">
        <span class="search-icon">&#128269;</span>
        <input
          type="search"
          id="docs-search-input"
          class="search-input"
          placeholder="Search all {total_docs} kit docs (Press / to focus)..."
          autocomplete="off"
        />
        <div id="search-results" class="search-results-dropdown"></div>
      </div>
    </div>
  </header>

  <div id="sidebar-backdrop" class="sidebar-backdrop" onclick="closeMobileSidebar()"></div>

  <div class="docs-layout">
    <aside class="left-sidebar" id="left-sidebar" aria-label="Documentation Navigation">
      <div class="mobile-sidebar-header">
        <span class="mobile-sidebar-title">Documentation ({total_docs})</span>
        <button type="button" class="mobile-sidebar-close" onclick="closeMobileSidebar()">&#10005; Close</button>
      </div>
      {"".join(sidebar_nav_html)}
    </aside>

    <main class="content-pane" id="main-content">
      <details class="mobile-toc" id="mobile-toc-details">
        <summary>On This Page (Section Jump)</summary>
        <nav class="mobile-toc-body" id="mobile-toc-container"></nav>
      </details>
      {"".join(articles_html)}
      <footer class="docs-footer">
        <span>PANTHEON AI Agent and Skills Setup Kit for Service Governance (ITIL 4 &amp; ITIL 5, NIST, NCSC / Cyber Essentials Plus, UKFS-01..06)</span>
        <span>Compiled from live Markdown sources ({build_timestamp}) via <code>python build_docs.py</code></span>
      </footer>
    </main>

    <aside class="toc-sidebar" aria-label="On This Page">
      <div class="toc-header">On This Page</div>
      <nav id="toc-container"></nav>
    </aside>
  </div>

  <script>
    const DOCS_INDEX = {index_json};
    let currentPageId = "{default_page_id}";

    function toggleMobileSidebar() {{
      const sb = document.getElementById("left-sidebar");
      const bd = document.getElementById("sidebar-backdrop");
      if (!sb || !bd) return;
      const isOpen = sb.classList.toggle("open");
      bd.classList.toggle("open", isOpen);
    }}

    function closeMobileSidebar() {{
      const sb = document.getElementById("left-sidebar");
      const bd = document.getElementById("sidebar-backdrop");
      if (sb) sb.classList.remove("open");
      if (bd) bd.classList.remove("open");
    }}

    function renderToc(pageId) {{
      const tocContainer = document.getElementById("toc-container");
      const mobileTocContainer = document.getElementById("mobile-toc-container");
      const mobileTocDetails = document.getElementById("mobile-toc-details");
      const pageObj = DOCS_INDEX.find(p => p.id === pageId);
      if (!pageObj || !pageObj.toc || pageObj.toc.length === 0) {{
        const emptyHtml = '<span style="font-size:12px;color:var(--text-muted);">No subsections</span>';
        if (tocContainer) tocContainer.innerHTML = emptyHtml;
        if (mobileTocContainer) mobileTocContainer.innerHTML = emptyHtml;
        if (mobileTocDetails) mobileTocDetails.open = false;
        return;
      }}
      const linksHtml = pageObj.toc.map(item => {{
        const cls = item.level === 3 ? "toc-link toc-level-3" : "toc-link";
        const safeTitle = item.title.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return `<a href="#${{item.id}}" class="${{cls}}" onclick="closeMobileToc()">${{safeTitle}}</a>`;
      }}).join("");
      if (tocContainer) tocContainer.innerHTML = linksHtml;
      if (mobileTocContainer) mobileTocContainer.innerHTML = linksHtml;
      if (mobileTocDetails) mobileTocDetails.open = false;
    }}

    function closeMobileToc() {{
      const mobileTocDetails = document.getElementById("mobile-toc-details");
      if (mobileTocDetails) mobileTocDetails.open = false;
    }}

    function navigateToPage(pageId, scrollTargetId) {{
      const targetArticle = document.getElementById("page-" + pageId);
      if (!targetArticle) return;

      closeMobileSidebar();

      document.querySelectorAll(".docs-article").forEach(el => el.classList.add("hidden"));
      targetArticle.classList.remove("hidden");

      document.querySelectorAll(".nav-item").forEach(btn => btn.classList.remove("active"));
      const activeBtn = document.getElementById("nav-" + pageId);
      if (activeBtn) activeBtn.classList.add("active");

      currentPageId = pageId;
      renderToc(pageId);

      if (scrollTargetId) {{
        const anchorEl = document.getElementById(scrollTargetId) || document.getElementById(scrollTargetId.replace(/-+/g, "-"));
        if (anchorEl) {{
          anchorEl.scrollIntoView({{ behavior: "smooth" }});
          history.replaceState(null, "", "#" + anchorEl.id);
          return;
        }}
      }}
      window.scrollTo({{ top: 0, behavior: "instant" }});
      history.replaceState(null, "", "#" + pageId);
    }}

    function navigateToHash(hashValue) {{
      const cleanHash = (hashValue || "").replace(/^#/, "");
      if (!cleanHash) return;
      const directPage = DOCS_INDEX.find(p => p.id === cleanHash);
      if (directPage) {{
        navigateToPage(directPage.id);
        return;
      }}
      for (const p of DOCS_INDEX) {{
        if (cleanHash.startsWith(p.id + "-")) {{
          navigateToPage(p.id, cleanHash);
          return;
        }}
      }}
      const existingEl = document.getElementById(cleanHash);
      if (existingEl) {{
        existingEl.scrollIntoView({{ behavior: "smooth" }});
      }}
    }}

    function copyCodeBlock(btn) {{
      const wrapper = btn.closest(".code-block-wrapper");
      if (!wrapper) return;
      const codeEl = wrapper.querySelector("code");
      if (!codeEl) return;
      navigator.clipboard.writeText(codeEl.innerText).then(() => {{
        const orig = btn.innerText;
        btn.innerText = "Copied!";
        setTimeout(() => {{ btn.innerText = orig; }}, 1500);
      }});
    }}

    function toggleTheme() {{
      const root = document.documentElement;
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {{ localStorage.setItem("agy_docs_theme", next); }} catch (e) {{}}
    }}

    // Full-text instant search
    const searchInput = document.getElementById("docs-search-input");
    const searchDropdown = document.getElementById("search-results");

    if (searchInput && searchDropdown) {{
      searchInput.addEventListener("input", () => {{
        const q = searchInput.value.trim().toLowerCase();
        if (q.length < 2) {{
          searchDropdown.classList.remove("open");
          searchDropdown.innerHTML = "";
          return;
        }}

        const hits = [];
        for (const page of DOCS_INDEX) {{
          const hay = (page.title + " " + page.search_text).toLowerCase();
          const idx = hay.indexOf(q);
          if (idx !== -1) {{
            const start = Math.max(0, idx - 45);
            const snippet = page.search_text.substring(start, start + 140);
            hits.push({{ page, snippet }});
          }}
        }}

        if (hits.length === 0) {{
          searchDropdown.innerHTML = '<div class="search-hit"><div class="search-hit-snippet">No matching documents found.</div></div>';
        }} else {{
          searchDropdown.innerHTML = hits.slice(0, 10).map(h => `
            <button type="button" class="search-hit" onclick="selectSearchResult('${{h.page.id}}')">
              <div class="search-hit-title">${{h.page.title}} <span style="color:var(--text-muted);font-weight:400;">(${{h.page.path}})</span></div>
              <div class="search-hit-snippet">...${{h.snippet.replace(/</g, "&lt;")}}...</div>
            </button>
          `).join("");
        }}
        searchDropdown.classList.add("open");
      }});

      document.addEventListener("click", (e) => {{
        if (!e.target.closest(".search-wrapper")) {{
          searchDropdown.classList.remove("open");
        }}
      }});

      document.addEventListener("keydown", (e) => {{
        if (e.key === "/" && document.activeElement !== searchInput) {{
          e.preventDefault();
          searchInput.focus();
        }} else if (e.key === "Escape") {{
          searchDropdown.classList.remove("open");
          closeMobileSidebar();
        }}
      }});
    }}

    function selectSearchResult(pageId) {{
      searchDropdown.classList.remove("open");
      navigateToPage(pageId);
    }}

    window.addEventListener("hashchange", () => {{
      const hash = window.location.hash.replace(/^#/, "");
      if (hash) navigateToHash(hash);
    }});

    // Initialize theme & initial URL hash
    (function init() {{
      try {{
        const savedTheme = localStorage.getItem("agy_docs_theme");
        if (savedTheme === "light" || savedTheme === "dark") {{
          document.documentElement.setAttribute("data-theme", savedTheme);
        }}
      }} catch (e) {{}}

      const hash = window.location.hash.replace(/^#/, "");
      if (hash) {{
        navigateToHash(hash);
        return;
      }}
      renderToc(currentPageId);
    }})();
  </script>
</body>
</html>
"""

    output_path = kit_dir / "ANTIGRAVITY_DOCS.html"
    output_path.write_text(docs_portal, encoding="utf-8")
    return output_path


def main() -> int:
    kit_dir = Path(__file__).resolve().parent
    try:
        out_file = build_docs_html(kit_dir)
        size_kb = out_file.stat().st_size / 1024
        print(f"[OK] Compiled {len(DOCS_MANIFEST)} kit documents into standalone local docs: {out_file.name} ({size_kb:.1f} KB)")
        return 0
    except Exception as exc:
        print(f"[ERROR] Failed to build ANTIGRAVITY_DOCS.html: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
