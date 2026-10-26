import hashlib
import json
import re
import shutil
import urllib.error
from pathlib import Path

import pytest

import setup as su
import validate_kit as vk

ROOT = Path(__file__).resolve().parent.parent


class FakeResp:
    def __init__(self, data: bytes):
        self._d = data

    def read(self):
        return self._d

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _manifest_for(kit, files, version="9.9.9"):
    return json.dumps(
        {
            "version": version,
            "files": {
                f: hashlib.sha256((kit / f).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for f in files
            },
        }
    ).encode()


@pytest.fixture
def kit(tmp_path):
    for f in ("a.txt", "dir/b.txt"):
        (tmp_path / f).parent.mkdir(exist_ok=True)
        (tmp_path / f).write_bytes(b"hello\r\nworld\r\n")
    return tmp_path


def serve(monkeypatch, payload=None, exc=None):
    def fake(req, timeout=0):
        if exc:
            raise exc
        return FakeResp(payload)

    monkeypatch.setattr(su.urllib.request, "urlopen", fake)


def test_verify_ok_with_crlf_files(kit, monkeypatch, capsys):
    serve(monkeypatch, _manifest_for(kit, ["a.txt", "dir/b.txt"]))
    su.verify_kit_integrity(kit, "v9")
    assert "SHA-256 verified 2 files" in capsys.readouterr().out


def test_verify_mismatch_raises(kit, monkeypatch):
    payload = _manifest_for(kit, ["a.txt", "dir/b.txt"])
    (kit / "a.txt").write_bytes(b"tampered")
    serve(monkeypatch, payload)
    with pytest.raises(RuntimeError, match=r"a\.txt \(digest mismatch\)"):
        su.verify_kit_integrity(kit, "v9")


def test_verify_missing_file_raises(kit, monkeypatch):
    payload = _manifest_for(kit, ["a.txt", "dir/b.txt"])
    (kit / "dir/b.txt").unlink()
    serve(monkeypatch, payload)
    with pytest.raises(RuntimeError, match=r"b\.txt \(missing\)"):
        su.verify_kit_integrity(kit, "v9")


@pytest.mark.parametrize("kind", ["network", "badjson", "nofiles"])
def test_manifest_unavailable_warns_only(kit, monkeypatch, capsys, kind):
    if kind == "network":
        serve(monkeypatch, exc=urllib.error.URLError("offline"))
    elif kind == "badjson":
        serve(monkeypatch, b"not json")
    else:
        serve(monkeypatch, b"{}")
    su.verify_kit_integrity(kit, "v9")
    assert "[WARN] Integrity manifest unavailable" in capsys.readouterr().out


def test_ref_urls():
    assert su.repo_zip_url("v1.0.0").endswith("/archive/v1.0.0.zip")
    assert su.repo_raw_base_url("v1.0.0").endswith("/pantheon-ai-kit/v1.0.0")


# ---------------- uninstall
def _populate(target):
    for f in vk.EXPECTED_FILES:
        dest = target / f
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / f, dest)


def test_uninstall_dry_run_removes_nothing(tmp_path):
    _populate(tmp_path)
    rc = su.execute_uninstallation(tmp_path, ROOT, dry_run=True, force=True)
    assert rc == 0
    assert all((tmp_path / f).exists() for f in vk.EXPECTED_FILES)


def test_uninstall_preserves_custom_and_secrets(tmp_path):
    _populate(tmp_path)
    secret_name = "." + "env"
    for rel, text in (
        (".claude/agents/custom.md", "mine"),
        (".agents/skills/mine/SKILL.md", "mine"),
        (secret_name, "KEY=1"),
    ):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    assert su.execute_uninstallation(tmp_path, ROOT, force=True) == 0
    left = {p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file()}
    assert left == {".claude/agents/custom.md", ".agents/skills/mine/SKILL.md", secret_name}


def test_uninstall_purge_secrets(tmp_path):
    _populate(tmp_path)
    secret = tmp_path / ("." + "env")
    secret.write_text("KEY=1")
    assert su.execute_uninstallation(tmp_path, ROOT, purge_secrets=True, force=True) == 0
    assert not secret.exists()


def test_uninstall_refuses_source_repo_without_force():
    assert su.execute_uninstallation(ROOT, ROOT, dry_run=True, force=False) == 1


# ---------------- parity of the canonical file list across implementations
def _ps1_files():
    text = (ROOT / "validate_and_install.ps1").read_text(encoding="utf-8")
    block = re.search(r"\$RequiredFiles\s*=\s*@\((.*?)\n\)", text, re.S).group(1)
    return re.findall(r'"([^"]+)"', block)


def test_ps1_required_files_match_python():
    assert _ps1_files() == vk.EXPECTED_FILES


def test_setup_fallback_list_matches_python():
    src = (ROOT / "setup.py").read_text(encoding="utf-8")
    block = re.search(r"except Exception:\s*REQUIRED_KIT_FILES = \[(.*?)\n    \]", src, re.S).group(1)
    assert re.findall(r'"([^"]+)"', block) == vk.EXPECTED_FILES
    assert su.REQUIRED_KIT_FILES == vk.EXPECTED_FILES


def test_ps1_uninstall_prunes_every_skill_dir():
    text = (ROOT / "validate_and_install.ps1").read_text(encoding="utf-8")
    for f in vk.EXPECTED_FILES:
        if f.endswith("SKILL.md"):
            assert f.rsplit("/", 1)[0] in text, f
