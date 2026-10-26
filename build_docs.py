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

import base64
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
        "id": "claude-md",
        "title": "Claude Code Entry Point (CLAUDE.md)",
        "short_title": "CLAUDE.md (Claude Code)",
        "category": "Workspace Rules & Templates",
        "badge": "Claude Code",
        "path": "CLAUDE.md",
        "description": "Claude Code entry point that imports the shared GEMINI.md ledger and explains the generated .claude/ mirror.",
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


EMOJI_RE = re.compile("(?:[\U0001F000-\U0001FAFF\u2705\u274c\u2753\u27a1\u26a1\ufe0f\u200d])+ ?")
BOX_DRAWING_RE = re.compile("[\u2500-\u257f]")


def strip_emoji(text: str) -> str:
    """Remove pictographic emoji (and one trailing space) so the portal reads as plain, consistent type."""
    return EMOJI_RE.sub("", text)


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
            lang_badge = html.escape(lang.lower())
            is_diagram = bool(BOX_DRAWING_RE.search(raw_code))
            wrapper_cls = "code-block-wrapper code-diagram" if is_diagram else "code-block-wrapper"
            scroll_note = ' <span class="scroll-note">(scrolls sideways)</span>' if is_diagram else ""
            out.append(
                f'<div class="{wrapper_cls}">'
                f'<div class="code-block-header">'
                f'<span class="code-lang">{lang_badge}{scroll_note}</span>'
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

            # Columns whose every filled cell is a bare number (optionally with a unit) are right-aligned.
            num_re = re.compile(r"[+-]?[\d.,]+\s?(?:%|h|min|d|pts|points|KB|MB|bytes)?")
            numeric_cols = set()
            for col in range(len(header_cells)):
                col_vals = [re.sub(r"[`*$]", "", r[col]).strip() for r in body_rows if col < len(r) and r[col].strip()]
                if col_vals and all(num_re.fullmatch(v) for v in col_vals):
                    numeric_cols.add(col)

            table_html = ['<div class="table-responsive"><table class="docs-table"><thead><tr>']
            for col, cell in enumerate(header_cells):
                th_cls = ' class="num"' if col in numeric_cols else ""
                table_html.append(f"<th{th_cls}>{render_inline(cell, page_id)}</th>")
            table_html.append("</tr></thead><tbody>")
            for row in body_rows:
                table_html.append("<tr>")
                for idx_c in range(len(header_cells)):
                    val = row[idx_c] if idx_c < len(row) else ""
                    label = html.escape(re.sub(r"[`*]", "", header_cells[idx_c]), quote=True)
                    td_cls = ' class="num"' if idx_c in numeric_cols else ""
                    table_html.append(f'<td{td_cls} data-label="{label}">{render_inline(val, page_id)}</td>')
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


TEMPLATE_DIR = Path(__file__).resolve().parent / "docs_template"

TOOL_VARIANT = '<span data-tool-only="{tool}"><span class="tool-tag">{label}</span>{body}</span>'


def tool_pair(antigravity: str, claude: str) -> str:
    """Render both tool variants; the portal script shows the one for the selected tool (both without scripting)."""
    return TOOL_VARIANT.format(tool="antigravity", label="Antigravity", body=antigravity) + TOOL_VARIANT.format(
        tool="claude", label="Claude Code", body=claude
    )


def render_invoke_card(entry: Dict[str, str]) -> str:
    """Per-agent / per-skill card showing where the file lives and how to invoke it in each tool."""
    path = entry["path"]
    parts = path.split("/")
    if len(parts) == 4 and parts[0] == ".agents" and parts[1] == "agents":
        name = parts[2]
        lives = tool_pair(f"<code>.agents/agents/{name}/agent.md</code>", f"<code>.claude/agents/{name}.md</code>")
        invoke = f"<code>@{name}</code> or ask by name in plain language"
    elif len(parts) == 4 and parts[0] == ".agents" and parts[1] == "skills":
        name = parts[2]
        lives = tool_pair(f"<code>.agents/skills/{name}/SKILL.md</code>", f"<code>.claude/skills/{name}/SKILL.md</code>")
        invoke = f"<code>/{name}</code>"
    else:
        return ""
    context = tool_pair("<code>GEMINI.md</code>", "<code>CLAUDE.md</code> (imports GEMINI.md)")
    return (
        '<div class="invoke-card"><dl class="live-rows">'
        f'<div class="live-row"><dt>Lives in</dt><dd>{lives}</dd></div>'
        f'<div class="live-row"><dt>Invoke</dt><dd>{invoke}</dd></div>'
        f'<div class="live-row"><dt>Context file</dt><dd>{context}</dd></div>'
        "</dl></div>"
    )


def render_home(pages_data: List[Dict[str, Any]]) -> str:
    """Home view shown above the README: what the kit is, the one primary action, and the live tool switch."""

    def rows(category: str) -> str:
        items = []
        for p in pages_data:
            if p["category"] != category:
                continue
            pid = p["id"]
            items.append(
                f'<li><a class="home-row" href="#{pid}" onclick="navigateToPage(\'{pid}\'); return false;">'
                f'<span class="home-row-name">{html.escape(p["short_title"])}</span>'
                f'<span class="home-row-desc">{html.escape(p["description"])}</span></a></li>'
            )
        return "".join(items)

    live = (
        '<div class="live-panel">'
        "<h2>Pick your tool</h2>"
        "<p>The same agents and skills run in both. Paths and commands below follow your choice everywhere in these docs.</p>"
        '<div class="seg" role="group" aria-label="Tool">'
        '<button type="button" data-set-tool="antigravity" aria-pressed="true">Antigravity</button>'
        '<button type="button" data-set-tool="claude" aria-pressed="false">Claude Code</button>'
        "</div>"
        '<dl class="live-rows">'
        f'<div class="live-row"><dt>Agents live in</dt><dd>{tool_pair("<code>.agents/agents/</code>", "<code>.claude/agents/</code>")}</dd></div>'
        f'<div class="live-row"><dt>Skills live in</dt><dd>{tool_pair("<code>.agents/skills/</code>", "<code>.claude/skills/</code>")}</dd></div>'
        f'<div class="live-row"><dt>Context file</dt><dd>{tool_pair("<code>GEMINI.md</code>", "<code>CLAUDE.md</code>, which imports GEMINI.md")}</dd></div>'
        '<div class="live-row"><dt>Ask an agent</dt><dd><code>@aegis_best_practice</code> or plain language</dd></div>'
        '<div class="live-row"><dt>Run a skill</dt><dd><code>/ticket-backlog-governance</code></dd></div>'
        "</dl></div>"
    )
    return (
        '<section class="home" id="home" aria-label="Welcome">'
        "<h1>Governance agents and skills</h1>"
        '<div class="home-lead-row"><div>'
        '<p class="home-sentence">Five advisory agents and six skills for ITIL, NIST and UK resilience standards. '
        "One command installs them; they run in Antigravity or Claude Code.</p>"
        '<div class="home-actions">'
        "<a class=\"btn btn-primary\" href=\"#readme-1-quickstart-installation\" "
        "onclick=\"navigateToPage('readme', 'readme-1-quickstart-installation'); return false;\">Quickstart</a>"
        "<a class=\"link-quiet\" href=\"#setup-guide\" onclick=\"navigateToPage('setup-guide'); return false;\">Read the setup guide</a>"
        "</div></div>"
        f"{live}</div>"
        '<div class="home-lists">'
        f'<div><h2>Five specialist agents</h2><ul class="home-list">{rows("Specialist Advisory Agents")}</ul></div>'
        f'<div><h2>Six operational skills</h2><ul class="home-list">{rows("Operational & KPI Skills")}</ul></div>'
        "</div></section>"
    )


def render_portal(
    total_docs: int,
    sidebar_nav: str,
    articles: str,
    build_label: str,
    index_json: str,
    default_page_id: str,
    home: str = "",
) -> str:
    """Fill docs_template/portal.html (CSS and JS are separate files) with the compiled content."""
    template = (TEMPLATE_DIR / "portal.html").read_text(encoding="utf-8")
    css = (TEMPLATE_DIR / "portal.css").read_text(encoding="utf-8").rstrip("\n")
    for token, font_file in (("@@FONT_SANS@@", "IBMPlexSans-var.woff2"), ("@@FONT_MONO@@", "IBMPlexMono-400.woff2")):
        css = css.replace(token, base64.b64encode((TEMPLATE_DIR / "fonts" / font_file).read_bytes()).decode("ascii"))
    js = (TEMPLATE_DIR / "portal.js").read_text(encoding="utf-8").rstrip("\n")
    # Assets first, content last: compiled markdown may legitimately contain "@@" sequences.
    page = template.replace("@@CSS@@", css).replace("@@JS@@", js)
    replacements = {
        "@@TOTAL_DOCS@@": str(total_docs),
        "@@BUILD_LABEL@@": build_label,
        "@@DEFAULT_PAGE@@": default_page_id,
        "@@SIDEBAR_NAV@@": sidebar_nav,
        "@@ARTICLES@@": articles,
        "@@HOME@@": home,
        "@@INDEX_JSON@@": index_json,
    }
    # Single pass so substituted content is never re-scanned for tokens.
    return re.sub("|".join(re.escape(k) for k in replacements), lambda m: replacements[m.group(0)], page)


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
        md_body = strip_emoji(md_body)
        meta = {k: strip_emoji(str(v)) for k, v in meta.items()}

        rendered_html, toc = markdown_to_html(md_body, entry["id"])
        # Long Markdown titles wrap past two lines on a phone; show the short manifest title (the id and anchor stay).
        rendered_html = re.sub(
            r'(<h1 [^>]*>).*?(<a class="heading-anchor")',
            lambda m: m.group(1) + html.escape(entry["title"]) + m.group(2),
            rendered_html,
            count=1,
            flags=re.DOTALL,
        )

        # Prepend YAML Frontmatter metadata banner for Agents and Skills
        if meta:
            meta_rows = "".join(
                f'<div class="fm-item"><span class="fm-key">{html.escape(k)}:</span> '
                f'<span class="fm-val">{html.escape(str(v))}</span></div>'
                for k, v in meta.items()
            )
            fm_banner = (
                f'<div class="frontmatter-card">'
                f'<div class="frontmatter-header">Discovery frontmatter (YAML)</div>'
                f'<div class="frontmatter-body">{meta_rows}</div>'
                f"</div>"
            )
            # Cards follow the page title so the h1 stays the first thing on screen.
            cards = render_invoke_card(entry) + "\n" + fm_banner + "\n"
            title_end = rendered_html.find("</h1>")
            if title_end == -1:
                rendered_html = cards + rendered_html
            else:
                split_at = title_end + len("</h1>")
                rendered_html = rendered_html[:split_at] + "\n" + cards + rendered_html[split_at:]

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
    # Deterministic (no wall-clock) so CI can detect stale committed docs by rebuilding and diffing.
    version_file = Path(__file__).resolve().parent / "VERSION"
    build_timestamp = "kit v" + (version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "dev")
    total_docs = len(pages_data)

    docs_portal = render_portal(
        total_docs=total_docs,
        sidebar_nav="".join(sidebar_nav_html),
        articles="".join(articles_html),
        build_label=build_timestamp,
        index_json=index_json,
        default_page_id=default_page_id,
        home=render_home(pages_data),
    )

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
