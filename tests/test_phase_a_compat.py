"""B-002: Phase A compatibility suite.

Pins all Phase A user-facing artifacts so no Phase B change can silently
break them. Per ADR 0008.B.3: any program that runs on Phase A's last release
must run unchanged on every Phase B release.

Tests
-----
1. test_phase_a_example_runs_unchanged   — parametrized; 7 example .apy programs
2. test_dictionary_ar_v1_unchanged       — SHA-256 snapshot of dictionaries/ar-v1.md
3. test_search_engine_app_runs           — smoke test for apps/search_engine
4. test_prayer_times_app_runs            — smoke test for apps/prayer_times
5. test_run_apy_program_decodes_arabic_correctly — helper function unit test

Public API
----------
run_apy_program(path, *, timeout, cwd, extra_args)
    Run an .apy file in a subprocess; return (returncode, stdout, stderr).
    Importable by future packets that need to assert Phase A compat.
"""

from __future__ import annotations

import difflib
import hashlib
import os
import pathlib
import subprocess
import sys
import tempfile

import pytest

__all__ = ["run_apy_program"]

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES_DIR = PROJECT_ROOT / "examples"
APPS_DIR = PROJECT_ROOT / "apps"
SNAPSHOTS_DIR = PROJECT_ROOT / "tests" / "snapshots" / "phase_a"
OUTPUTS_DIR = SNAPSHOTS_DIR / "expected_outputs"
DICT_HASH_FILE = SNAPSHOTS_DIR / "dictionary_ar_v1.sha256"
DICT_FILE = PROJECT_ROOT / "dictionaries" / "ar-v1.md"

# ─────────────────────────────────────────────────────────────────────────────
# Public helper
# ─────────────────────────────────────────────────────────────────────────────


def run_apy_program(
    path: pathlib.Path,
    *,
    timeout: float = 10.0,
    cwd: pathlib.Path | None = None,
    extra_args: list[str] | None = None,
) -> tuple[int, str, str]:
    """Execute an .apy file in a subprocess and capture (returncode, stdout, stderr).

    Uses ``sys.executable -m arabicpython.cli <path>`` to invoke the dialect.
    UTF-8 is enforced on both pipes.

    Parameters
    ----------
    path:
        Absolute path to the .apy file.
    timeout:
        Seconds; raises subprocess.TimeoutExpired if exceeded.
    cwd:
        Working directory for the subprocess. Defaults to ``path.parent`` so
        that relative imports (e.g. ``helper.apy`` in examples/) resolve
        correctly. Pass ``PROJECT_ROOT`` explicitly for apps that reference
        repo-relative file paths at runtime.
    extra_args:
        Additional command-line arguments forwarded to the .apy program.

    Returns
    -------
    tuple[int, str, str]
        ``(returncode, stdout_text, stderr_text)``. Both texts are decoded as
        UTF-8 with ``errors='replace'`` so assertion failures surface the bug
        rather than crashing the test harness on encoding mismatch.

    Examples
    --------
    >>> rc, out, err = run_apy_program(EXAMPLES_DIR / "01_hello.apy")
    >>> rc
    0
    >>> "مرحبا" in out
    True
    """
    effective_cwd = cwd if cwd is not None else path.parent

    # Ensure the project root is on PYTHONPATH so the arabicpython package is
    # importable inside the subprocess, and so that apps' cross-module imports
    # (e.g. ``from apps.search_engine.indexer import …``) also resolve.
    env = os.environ.copy()
    existing_pp = env.get("PYTHONPATH", "")
    project_root_str = str(PROJECT_ROOT)
    if project_root_str not in existing_pp.split(os.pathsep):
        env["PYTHONPATH"] = (
            project_root_str + os.pathsep + existing_pp if existing_pp else project_root_str
        )

    # UTF-8 in/out for the child process — matches the CLI's own reconfigure call
    env.setdefault("PYTHONUTF8", "1")

    cmd = [sys.executable, "-m", "arabicpython.cli", str(path)]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(
        cmd,
        cwd=str(effective_cwd),
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )
    return result.returncode, result.stdout, result.stderr


# ─────────────────────────────────────────────────────────────────────────────
# 1. Parametrized example runner
# ─────────────────────────────────────────────────────────────────────────────

# helper.apy is an importee, not a runnable program.
# B01_http.apy makes live HTTP calls — excluded from the compat suite.
# B30_filesystem_walk.apy requires a CLI argument (directory path) — excluded.
_EXCLUDED = {
    "helper.apy",  # imported by 07_imports.apy, not a standalone program
    "B01_http.apy",  # makes live HTTP call; requires @pytest.mark.network
    "B10_flask_hello.apy",  # starts a blocking HTTP server
    "B30_filesystem_walk.apy",  # requires a CLI argument (directory path)
}

_EXAMPLE_PARAMS = sorted(p for p in EXAMPLES_DIR.glob("*.apy") if p.name not in _EXCLUDED)


@pytest.mark.parametrize("example_path", _EXAMPLE_PARAMS, ids=lambda p: p.stem)
def test_phase_a_example_runs_unchanged(example_path: pathlib.Path) -> None:
    """Each Phase A example must exit 0, produce no stderr, and match its snapshot."""
    snapshot_file = OUTPUTS_DIR / f"{example_path.stem}.txt"
    assert snapshot_file.exists(), (
        f"No snapshot found for {example_path.name}. " f"Expected: {snapshot_file}"
    )

    # 07_imports needs cwd=examples_dir (so `import helper` resolves via '' in sys.path)
    # All other examples also benefit from cwd=path.parent — it's always examples_dir here.
    rc, stdout, stderr = run_apy_program(example_path)

    assert rc == 0, f"{example_path.name} exited with code {rc}.\n" f"stderr:\n{stderr}"
    assert stderr == "", f"{example_path.name} wrote unexpected output to stderr:\n{stderr}"

    # Read snapshot with universal newline suppression so \r\n on Windows
    # doesn't cause spurious mismatches.
    expected = snapshot_file.read_text(encoding="utf-8")
    # Normalise the subprocess stdout to LF as well
    actual = stdout.replace("\r\n", "\n")

    if actual != expected:
        diff = "".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile=f"expected ({snapshot_file.name})",
                tofile=f"actual ({example_path.name})",
            )
        )
        pytest.fail(f"{example_path.name}: stdout does not match snapshot.\n\n{diff}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Dictionary snapshot
# ─────────────────────────────────────────────────────────────────────────────


def test_dictionary_ar_v1_unchanged() -> None:
    """dictionaries/ar-v1.md must not have changed since Phase A ship.

    Per ADR 0008.B.0 the ar-v1 dictionary is frozen forever. If a genuine
    change is needed, introduce ar-v1.1.md or ar-v2.md via a new ADR instead
    of modifying this file.
    """
    # Normalise CRLF→LF before hashing so Windows and Linux/macOS agree.
    content = DICT_FILE.read_bytes().replace(b"\r\n", b"\n")
    actual_digest = hashlib.sha256(content).hexdigest()
    expected_digest = DICT_HASH_FILE.read_text(encoding="utf-8").strip()

    assert actual_digest == expected_digest, (
        "dictionaries/ar-v1.md has changed since Phase A ship. "
        "Per ADR 0008.B.0 it is immutable. "
        "If a change is genuinely needed, write a superseding ADR introducing "
        "ar-v1.1.md or ar-v2.md, do not modify ar-v1.md.\n"
        f"  expected SHA-256: {expected_digest}\n"
        f"  actual   SHA-256: {actual_digest}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. Search engine smoke test
# ─────────────────────────────────────────────────────────────────────────────


def test_search_engine_app_runs() -> None:
    """apps/search_engine/cli.apy must exit 0 and return a result for a fixed query.

    The corpus in apps/search_engine/docs/ is committed, so results are
    deterministic for a fixed query term.
    """
    cli = APPS_DIR / "search_engine" / "cli.apy"
    if not cli.exists():
        pytest.skip(f"search_engine CLI not found at {cli}")

    # Run with cwd=PROJECT_ROOT so the script's relative path
    # "apps/search_engine/docs" resolves correctly.
    rc, stdout, stderr = run_apy_program(
        cli,
        cwd=PROJECT_ROOT,
        extra_args=["الخوارزمي"],
    )

    assert rc == 0, f"search_engine/cli.apy exited {rc}.\nstderr:\n{stderr}"
    # The corpus contains a document about الخوارزمي; check headline markers.
    assert "النتائج" in stdout, f"Expected 'النتائج' in search output.\nstdout:\n{stdout}"
    assert (
        "الخوارزمي" in stdout
    ), f"Expected document 'الخوارزمي' in search output.\nstdout:\n{stdout}"


# ─────────────────────────────────────────────────────────────────────────────
# 4. Prayer times smoke test
# ─────────────────────────────────────────────────────────────────────────────

_PRAYER_NAMES = ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"]


def test_prayer_times_app_runs() -> None:
    """apps/prayer_times/الرئيسي.apy must exit 0 and show all five prayer names.

    A fixed city (الرياض) and date (2026-01-15) are passed so prayer times are
    deterministic. The 'next prayer' countdown line depends on the current clock
    and is intentionally not asserted on.
    """
    entry = APPS_DIR / "prayer_times" / "الرئيسي.apy"
    if not entry.exists():
        pytest.skip(f"prayer_times entry point not found at {entry}")

    rc, stdout, stderr = run_apy_program(
        entry,
        cwd=PROJECT_ROOT,
        extra_args=["الرياض", "2026-01-15"],
    )

    assert rc == 0, f"prayer_times/الرئيسي.apy exited {rc}.\nstderr:\n{stderr}"
    for prayer in _PRAYER_NAMES:
        assert prayer in stdout, f"Expected prayer name '{prayer}' in output.\nstdout:\n{stdout}"


# ─────────────────────────────────────────────────────────────────────────────
# 5. run_apy_program helper unit test
# ─────────────────────────────────────────────────────────────────────────────


def test_run_apy_program_decodes_arabic_correctly() -> None:
    """run_apy_program must return Arabic text as proper Unicode, not mojibake."""
    with tempfile.NamedTemporaryFile(suffix=".apy", mode="w", encoding="utf-8", delete=False) as f:
        f.write('اطبع("مرحبا")\n')
        tmp_path = pathlib.Path(f.name)

    try:
        rc, stdout, stderr = run_apy_program(tmp_path)
        assert rc == 0, f"Temp .apy exited {rc}.\nstderr:\n{stderr}"
        assert "مرحبا" in stdout, (
            f"Expected 'مرحبا' in stdout but got: {stdout!r}\n"
            "(mojibake or encoding replacement characters detected)"
        )
    finally:
        tmp_path.unlink(missing_ok=True)
