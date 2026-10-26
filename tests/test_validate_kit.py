import base64
import re

import pytest

import validate_kit as vk


def _match(label, text):
    rules, _ = vk.decode_blocklist(None)
    for lab, _pat, compiled, _custom in rules:
        if lab == label:
            return bool(compiled.search(text))
    raise AssertionError(f"no rule {label}")


# Fake secrets are assembled at runtime so source scanners do not flag this file.
POSITIVES = {
    "PEM Private Key Header": "-----BEGIN " + "RSA PRIVATE KEY-----",
    "GitHub Personal Access Token": "gh" + "p_" + "a" * 36,
    "AWS Access Key ID": "AK" + "IA" + "A" * 16,
    "Slack API Token": "xo" + "xb-" + "1" * 11 + "-" + "2" * 11 + "-abcDEF",
    "Hardcoded OAuth Client Secret": "client_" + "secret = '" + "a" * 40 + "'",
}


@pytest.mark.parametrize("label,sample", POSITIVES.items(), ids=list(POSITIVES))
def test_secret_patterns_match(label, sample):
    assert _match(label, sample)


@pytest.mark.parametrize(
    "label,sample",
    [
        ("PEM Private Key Header", "-----BEGIN PUBLIC KEY-----"),
        ("GitHub Personal Access Token", "ghp_tooshort"),
        ("AWS Access Key ID", "AKIA123"),
        ("Slack API Token", "xoxb-short"),
        ("Hardcoded OAuth Client Secret", "client_secret = os.environ['X']"),
    ],
)
def test_secret_patterns_ignore_benign(label, sample):
    assert not _match(label, sample)


def test_every_generic_pattern_has_a_positive_case():
    assert {label for label, _ in vk.GENERIC_SECRET_PATTERNS} == set(POSITIVES)


def test_custom_blocklist_roundtrip(tmp_path):
    def enc(s):
        return base64.b64encode(s[::-1].encode()).decode()

    (tmp_path / vk.CUSTOM_BLOCKLIST_FILENAME).write_text(
        '[{"NameB64": "%s", "PatB64": "%s"}]' % (enc("AcmeCorp"), enc(r"\bacmecorp\b")), encoding="utf-8"
    )
    rules, count = vk.decode_blocklist(tmp_path)
    assert count == 1
    label, _pat, compiled, is_custom = rules[-1]
    assert label == "AcmeCorp" and is_custom and compiled.search("hello ACMECORP")


def test_frontmatter_valid():
    ok, meta, body, err = vk.parse_yaml_frontmatter("---\nname: x\ntools:\n  - a\n  - b\n---\n\nBody text")
    assert ok and not err
    assert meta["name"] == "x" and meta["tools"] == ["a", "b"]
    assert "Body text" in body


@pytest.mark.parametrize("content", ["no frontmatter", "---\nname: x\n"])
def test_frontmatter_invalid(content):
    ok, _meta, _body, err = vk.parse_yaml_frontmatter(content)
    assert not ok and err


def test_structure_flags_missing_empty_and_oversize_gemini(tmp_path):
    errors = vk.validate_structure(tmp_path)
    assert len(errors) == len(vk.EXPECTED_FILES)
    for rel in vk.EXPECTED_FILES:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x", encoding="utf-8")
    assert vk.validate_structure(tmp_path) == []
    (tmp_path / "GEMINI.md").write_text("x" * 24000, encoding="utf-8")
    assert any("24,000" in e for e in vk.validate_structure(tmp_path))
    (tmp_path / "GEMINI.md").write_text("x" * 23999, encoding="utf-8")
    assert vk.validate_structure(tmp_path) == []
    (tmp_path / "README.md").write_text("", encoding="utf-8")
    assert any("empty" in e.lower() for e in vk.validate_structure(tmp_path))


def test_real_repo_passes_all_stages():
    root = vk.Path(vk.__file__).resolve().parent
    assert vk.validate_structure(root) == []
    assert vk.validate_frontmatters(root) == []
    rules, _ = vk.decode_blocklist(None)
    assert vk.scan_deidentification(root, rules) == []
    assert vk.validate_configs(root) == []


def test_expected_files_unique_and_regex_compiles():
    assert len(vk.EXPECTED_FILES) == len(set(vk.EXPECTED_FILES))
    for _label, pat in vk.GENERIC_SECRET_PATTERNS:
        re.compile(pat)
