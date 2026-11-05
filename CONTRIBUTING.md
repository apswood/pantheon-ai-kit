# Contributing

> [!IMPORTANT]
> All contributions must conform to the project charter, licensing standards, and British English editorial voice documented in **[`GOVERNANCE.md`](GOVERNANCE.md)**.

## Ground rules

- `.agents/` is the source of truth for agents, skills and rules. **Never hand-edit `.claude/`, `.codex/` or
  `AGENTS.md`**; they are generated.
- `GEMINI.md` must stay under 24,000 bytes (the validator warns at 19,200).
- No real secrets, tenant IDs, customer names or internal hostnames anywhere. Use `<REDACTED>` or RFC 5737 doc IPs.
- Never edit `ANTIGRAVITY_DOCS.html` directly. Portal markup, styles and scripts live in `docs_template/`
  (`portal.html`, `portal.css`, `portal.js`; IBM Plex fonts in `docs_template/fonts/` are embedded as base64 so the
  portal works offline). Content rendering lives in `build_docs.py`. The build must stay deterministic: no clocks,
  random values or environment-dependent output.
- Conventional Commits: Use `feat:`, `fix:`, `docs:`, etc.
- **Strict No AI Attribution Policy**: Do not include `Co-Authored-By: Claude`, `Generated with Cursor`, or similar AI credits in commits or pull requests. Human committers take sole responsibility for merged code.

## Contributing an Agent or Skill

If you have developed or adopted an agent or skill in your local workspace (using `python setup.py --new-agent` or `python setup.py --new-skill`), sharing it with the wider community is welcomed under the following standards:

### Sharing with the Community: Essential Prerequisites

Before opening a pull request to contribute a new agent or skill, verify that your contribution satisfies these criteria:

1. **Public Availability & Zero Confidentiality**: The work must be suitable for permanent public release under the permissive MIT licence. Never submit any configuration, prompt, regex, or example containing confidential, proprietary, or client-sensitive details, internal URLs, or real credentials.
2. **Intellectual Property & Rights**: You must hold the legal right to contribute the material, ensuring it does not infringe on third-party intellectual property, proprietary vendor agreements, or employer IP clauses.
3. **Meaningful Enhancement**: Contributions must meaningfully enhance the toolkit's service governance, operational excellence, infrastructure hardening, or architectural audit capabilities.
4. **Extend Existing First (Avoid Duplication)**: Check existing agents and skills first before creating a new one:
   - For ITSM metrics, ticket quality, or pacing: extend **S.A.G.E.** or `ticket-backlog-governance` / `quality-audit-governance`.
   - For network, firewall, or OS hardening: extend **AEGIS** or `infrastructure-best-practice-analyser`.
   - For server rebuilds or migration runbooks: extend **HERMES** or `server-migration-infrastructure-replication`.
   - If your idea overlaps with an existing component, **extend or refine that component first** rather than creating a competing duplicate.
5. **Independent Projects in Open Source**: If your use case diverges significantly from PANTHEON's charter or represents an independent commercial tool, we warmly encourage you to publish and maintain your own project in the spirit of open source.

### Developing Your Agent or Skill with an LLM

You do not need prior prompt-engineering expertise to create a high-quality agent or skill. Follow this step-by-step development process:

#### Step 1: Scaffold the Structure
Run the built-in generator in your workspace:
```bash
python setup.py --new-agent <agent_name> --role "Description of agent role"
# or
python setup.py --new-skill <skill_name> --description "Description of skill"
```

#### Step 2: Know Which File to Edit
- **For an Agent**: Edit `.agents/agents/<agent_name>/agent.md`. An agent is an autonomous specialist persona with its own isolated context window and scoped tools (e.g. `view_file`, `grep_search`).
- **For a Skill**: Edit `.agents/skills/<skill_name>/SKILL.md`. A skill is an on-demand standard operating procedure, rubric, or calculation reference injected into the current session via progressive disclosure.

#### Step 3: Polish and Finalise Using an LLM
Use an AI coding assistant (Google Antigravity, Claude Code, or an external LLM) to flesh out the template. Provide the LLM with this prompt:

> "I am developing an agent or skill for the PANTHEON AI Kit in `<file_path>`.  
> Its objective is: `<describe your goal in 1-2 sentences>`.  
> Please help me draft and refine the markdown following PANTHEON standards:  
> 1. British English (`en-GB`) orthography (e.g. *analyse*, *prioritise*, *optimise*).  
> 2. Pragmatic, GOV.UK-inspired technical clarity (quiet competence; no conversational filler or tech buzzwords).  
> 3. Objective, evidence-based evaluation steps (formulas, thresholds, and clear acceptance criteria).  
> 4. Strict credential isolation (mandatory `<REDACTED>` for sensitive tokens, RFC 5737 for documentation IPs).  
> 5. A sharp, concise YAML frontmatter `description` explaining exactly when the agent or skill should be triggered."

#### Step 4: Test and Adopt Locally
Test the agent or skill in your AI assistant sessions. Adopt it in your local workspace using:
```bash
python setup.py --adopt
```
Verify that `python validate_kit.py` exits with code 0.

### Step-by-Step Contribution Workflow (Submitting to Upstream)

1. **Scaffold and Validate Locally**:
   Ensure your agent (`.agents/agents/<name>/agent.md`) or skill (`.agents/skills/<name>/SKILL.md`) has valid YAML frontmatter, contains zero credentials, and conforms to British English (`en-GB`).
2. **Assign to a Kit Group**:
   Open `build_docs.py` and assign your new component to the most appropriate group in `GROUPS` (`operational-excellence`, `infrastructure-and-resilience`, or `build-and-secure`).
3. **Register in Documentation**:
   Add an entry to `DOCS_MANIFEST` in `build_docs.py` and mention the capability in the matching section of `README.md`.
4. **Tool Mapping**:
   If your agent uses Antigravity tools, ensure they are mapped to Claude Code tools in `tools/sync_claude.py` (`TOOL_MAP`) and described in `tools/sync_codex.py` (`CAPABILITY_MAP`).
5. **Regenerate & Test**:
   Run the regeneration sequence below. All automated validation checks and tests must pass.

## Regenerate in this order

After changing `.agents/`, `README.md`, `ANTIGRAVITY_SETUP_GUIDE.md`, `GEMINI.md`, `VERSION` or `build_docs.py`:

```bash
python tools/sync_claude.py       # .agents/ -> .claude/
python tools/sync_codex.py        # .agents/ -> .codex/agents/, AGENTS.md
python build_docs.py              # markdown -> ANTIGRAVITY_DOCS.html
python tools/build_manifest.py    # SHA-256 digests -> kit_manifest.json (must come last)
python validate_kit.py            # must exit 0
pwsh -NoProfile -File validate_and_install.ps1 -ValidateOnly
python -m pytest -q tests
```

CI runs the same steps with `--check` and fails if any generated file is stale. Order matters because the manifest
hashes the generated files.

## Adding or removing a canonical file

Update `EXPECTED_FILES` in `validate_kit.py`, the fallback list in `setup.py`, `$RequiredFiles` in
`validate_and_install.ps1` (and the uninstall prune lists in both installers if it introduces a new folder). Tests in
`tests/test_setup.py` fail when the three lists disagree, and the validator fails when prose states a wrong count.

## Releasing

1. Update `VERSION` and `CHANGELOG.md`, run the regenerate sequence, commit.
2. Tag `vX.Y.Z` and push the tag. Installs pinned to the tag are then immutable.
3. Update README examples if they reference a specific tag.
