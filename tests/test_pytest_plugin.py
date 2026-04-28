# tests/test_pytest_plugin.py
# B-062: pytest plugin for .apy test files

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# ── helper ────────────────────────────────────────────────────────────────────

def _run(args: list, cwd=None) -> tuple[int, str, str]:
    """Run pytest in a subprocess; return (returncode, stdout, stderr).

    The plugin is auto-loaded via the pytest11 entry point — no -p needed.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *args, "--tb=short", "-q", "--no-header"],
        capture_output=True, text=True, encoding="utf-8", cwd=cwd,
    )
    return result.returncode, result.stdout, result.stderr


# ── discovery ─────────────────────────────────────────────────────────────────

class TestDiscovery:
    def test_arabic_prefix_collected(self, tmp_path):
        """اختبار_*.apy files are discovered."""
        (tmp_path / "اختبار_بسيط.apy").write_text(
            "دالة test_نجاح():\n    اكد 1 + 1 == 2\n",
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "1 passed" in out

    def test_english_prefix_collected(self, tmp_path):
        """test_*.apy files are also discovered."""
        (tmp_path / "test_simple.apy").write_text(
            "دالة test_add():\n    اكد 2 + 2 == 4\n",
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "1 passed" in out

    def test_arabic_suffix_collected(self, tmp_path):
        """*_اختبار.apy files are discovered."""
        (tmp_path / "حساب_اختبار.apy").write_text(
            "دالة test_ضرب():\n    اكد 3 * 3 == 9\n",
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "1 passed" in out

    def test_non_test_file_not_collected(self, tmp_path):
        """A plain .apy file without a test prefix is NOT collected."""
        (tmp_path / "مكتبة.apy").write_text(
            "دالة مساعد():\n    ارجع 42\n", encoding="utf-8"
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        # exit 5 = no tests collected
        assert rc == 5 or "no tests ran" in out or "collected 0" in out

    def test_multiple_functions_in_one_file(self, tmp_path):
        """All test functions in a single .apy file are collected."""
        (tmp_path / "اختبار_متعدد.apy").write_text(
            textwrap.dedent("""\
            دالة test_جمع():
                اكد 1 + 1 == 2

            دالة test_ضرب():
                اكد 3 * 4 == 12

            دالة test_قسمة():
                اكد 10 / 2 == 5.0
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "3 passed" in out


# ── failures ──────────────────────────────────────────────────────────────────

class TestFailureReporting:
    def test_failing_assert_reported(self, tmp_path):
        """A failing اكد (assert) produces a test failure, not a crash."""
        (tmp_path / "اختبار_فاشل.apy").write_text(
            "دالة test_خطأ():\n    اكد 1 == 2\n", encoding="utf-8"
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 1
        assert "1 failed" in out

    def test_raised_exception_reported(self, tmp_path):
        """An unhandled exception in a test function is reported as a failure."""
        (tmp_path / "اختبار_استثناء.apy").write_text(
            "دالة test_استثناء():\n    ارفع خطا_قيمه('فشل')\n",
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 1
        assert "1 failed" in out or "error" in out.lower()

    def test_translation_error_reported_gracefully(self, tmp_path):
        """A syntax error in an .apy file is reported, not a silent crash."""
        (tmp_path / "اختبار_خطأ_صياغة.apy").write_text(
            "دالة test_شيء():\n    اطبع(\n",  # unclosed paren
            encoding="utf-8",
        )
        rc, out, err = _run([str(tmp_path)], cwd=tmp_path)
        assert rc != 0


# ── Arabic language features ──────────────────────────────────────────────────

class TestArabicFeatures:
    def test_import_in_apy_test(self, tmp_path):
        """استورد works inside an .apy test file."""
        (tmp_path / "اختبار_استيراد.apy").write_text(
            textwrap.dedent("""\
            استورد رياضيات

            دالة test_جذر():
                اكد رياضيات.جذر(9) == 3.0

            دالة test_باي():
                اكد رياضيات.pi > 3.14
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out

    def test_class_based_tests(self, tmp_path):
        """صنف-based test grouping is collected correctly."""
        (tmp_path / "اختبار_صنف.apy").write_text(
            textwrap.dedent("""\
            صنف TestحسابArabic:
                دالة test_جمع(ذات):
                    اكد 5 + 5 == 10

                دالة test_طرح(ذات):
                    اكد 10 - 3 == 7
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out

    def test_control_flow_in_test(self, tmp_path):
        """Arabic control flow (لكل، اذا) works inside test functions."""
        (tmp_path / "اختبار_تدفق.apy").write_text(
            textwrap.dedent("""\
            دالة test_حلقة():
                مجموع = 0
                لكل رقم في نطاق(1, 6):
                    مجموع += رقم
                اكد مجموع == 15

            دالة test_شرط():
                اذا صحيح:
                    نتيجة = "نجح"
                وإلا:
                    نتيجة = "فشل"
                اكد نتيجة == "نجح"
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out

    def test_fixture_in_apy_test(self, tmp_path):
        """pytest fixtures defined in .apy files work correctly."""
        (tmp_path / "اختبار_تهيئة.apy").write_text(
            textwrap.dedent("""\
            استورد pytest

            @pytest.fixture
            دالة أرقام():
                ارجع [1, 2, 3, 4, 5]

            دالة test_مجموع(أرقام):
                اكد sum(أرقام) == 15

            دالة test_طول(أرقام):
                اكد طول(أرقام) == 5
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out

    def test_pytest_raises_in_apy(self, tmp_path):
        """pytest.raises works inside .apy test files."""
        (tmp_path / "اختبار_استثناءات.apy").write_text(
            textwrap.dedent("""\
            استورد pytest

            دالة test_قسمة_صفر():
                مع pytest.raises(ZeroDivisionError):
                    _ = 1 / 0

            دالة test_خطأ_نوع():
                مع pytest.raises(TypeError):
                    _ = "نص" + 1
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out

    def test_alias_module_in_apy_test(self, tmp_path):
        """Arabic alias modules (e.g. رياضيات) work in .apy test files."""
        (tmp_path / "اختبار_رياضيات.apy").write_text(
            textwrap.dedent("""\
            استورد رياضيات

            دالة test_جذر():
                اكد رياضيات.جذر(16) == 4.0

            دالة test_باي():
                اكد رياضيات.pi > 3.14
            """),
            encoding="utf-8",
        )
        rc, out, _ = _run([str(tmp_path)], cwd=tmp_path)
        assert rc == 0, out
        assert "2 passed" in out


# ── pyproject entry point ─────────────────────────────────────────────────────

class TestEntryPoint:
    def test_entry_point_in_pyproject(self):
        """The pytest11 entry point is declared in pyproject.toml."""
        import tomllib
        p = Path(__file__).parent.parent / "pyproject.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        ep = data.get("project", {}).get("entry-points", {}).get("pytest11", {})
        assert "apy" in ep, f"pytest11 entry point 'apy' missing; got: {ep}"
        assert ep["apy"] == "arabicpython.pytest_plugin"
