# tests/test_linter.py
# B-056: Linter tests

import pytest

from arabicpython.linter import lint_source, Diagnostic


def codes(diags):
    return [d.code for d in diags]


class TestLineLengthW001:
    def test_short_line_ok(self):
        src = "س = 1\n"
        assert "W001" not in codes(lint_source(src))

    def test_long_line_flagged(self):
        src = "س = " + "أ" * 100 + "\n"
        assert "W001" in codes(lint_source(src))


class TestTrailingWhitespaceW002:
    def test_no_trailing_ok(self):
        src = "س = 1\n"
        assert "W002" not in codes(lint_source(src))

    def test_trailing_space_flagged(self):
        src = "س = 1   \n"
        assert "W002" in codes(lint_source(src))


class TestTabIndentW003:
    def test_space_indent_ok(self):
        src = "إذا صحيح:\n    مرر\n"
        assert "W003" not in codes(lint_source(src))

    def test_tab_indent_flagged(self):
        src = "إذا صحيح:\n\tمرر\n"
        assert "W003" in codes(lint_source(src))


class TestMixedIdentifierW004:
    def test_pure_arabic_ok(self):
        src = "متغير = 1\n"
        assert "W004" not in codes(lint_source(src))

    def test_pure_latin_ok(self):
        src = "x = 1\n"
        assert "W004" not in codes(lint_source(src))

    def test_mixed_flagged(self):
        src = "متغيرX = 1\n"
        assert "W004" in codes(lint_source(src))


class TestV1KeywordE001:
    def test_v1_keyword_in_v2_file_flagged(self):
        src = "# arabicpython: dict=ar-v2\nمع الملف كـ م:\n    مرر\n"
        assert "E001" in codes(lint_source(src))

    def test_v1_keyword_in_no_directive_file_not_flagged(self):
        # Without a directive we don't know the version — don't flag
        src = "مع الملف كـ م:\n    مرر\n"
        assert "E001" not in codes(lint_source(src))

    def test_v2_keyword_baasm_ok(self):
        src = "# arabicpython: dict=ar-v2\nمع الملف باسم م:\n    مرر\n"
        assert "E001" not in codes(lint_source(src))


class TestNoIntroI001:
    def test_file_with_comment_ok(self):
        src = "# مرحبا\nس = 1\n"
        assert "I001" not in codes(lint_source(src))

    def test_file_without_intro_flagged(self):
        src = "س = 1\n"
        assert "I001" in codes(lint_source(src))

    def test_file_with_docstring_ok(self):
        src = '"""وصف الملف"""\nس = 1\n'
        assert "I001" not in codes(lint_source(src))


class TestDiagnosticStr:
    def test_str_representation(self):
        d = Diagnostic("test.apy", 3, 5, "W001", "line too long", "warning")
        s = str(d)
        assert "test.apy" in s
        assert "3" in s
        assert "W001" in s
        assert "warning"[0].upper() in s


class TestCLI:
    def test_cli_clean_file(self, tmp_path):
        from arabicpython.linter import main
        p = tmp_path / "ok.apy"
        p.write_text("# ملف نظيف\nس = 1\n", encoding="utf-8")
        rc = main([str(p)])
        assert rc == 0

    def test_cli_missing_file(self, tmp_path):
        from arabicpython.linter import main
        rc = main([str(tmp_path / "missing.apy")])
        assert rc == 1

    def test_cli_select(self, tmp_path, capsys):
        from arabicpython.linter import main
        p = tmp_path / "bad.apy"
        p.write_text("س = 1   \n", encoding="utf-8")
        rc = main(["--select", "W002", str(p)])
        out = capsys.readouterr().out
        assert "W002" in out

    def test_cli_no_info_suppresses_i001(self, tmp_path, capsys):
        from arabicpython.linter import main
        p = tmp_path / "f.apy"
        p.write_text("س = 1\n", encoding="utf-8")
        main(["--no-info", str(p)])
        out = capsys.readouterr().out
        assert "I001" not in out
