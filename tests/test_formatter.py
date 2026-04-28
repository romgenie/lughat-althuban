# tests/test_formatter.py
# B-055: Formatter tests

from pathlib import Path

import pytest

from arabicpython.formatter import format_source, format_file


class TestFormatSource:
    def test_idempotent_clean_source(self):
        src = "اطبع('مرحبا')\n"
        assert format_source(src) == src

    def test_trailing_newline_added(self):
        assert format_source("اطبع('مرحبا')") == "اطبع('مرحبا')\n"

    def test_trailing_newline_deduplicated(self):
        assert format_source("اطبع('مرحبا')\n\n\n") == "اطبع('مرحبا')\n"

    def test_trailing_whitespace_removed(self):
        src = "س = 1   \n"
        assert format_source(src) == "س = 1\n"

    def test_tabs_to_spaces(self):
        src = "\tاطبع('مرحبا')\n"
        assert format_source(src) == "    اطبع('مرحبا')\n"

    def test_comment_space_added(self):
        src = "#تعليق\n"
        assert format_source(src) == "# تعليق\n"

    def test_comment_space_already_present(self):
        src = "# تعليق\n"
        assert format_source(src) == "# تعليق\n"

    def test_shebang_untouched(self):
        src = "#!/usr/bin/env ثعبان\n"
        assert format_source(src) == src

    def test_double_hash_untouched(self):
        src = "## قسم\n"
        assert format_source(src) == src

    def test_comma_space_added(self):
        result = format_source("اطبع(أ,ب)\n")
        assert result == "اطبع(أ, ب)\n"

    def test_comma_space_already_present(self):
        src = "اطبع(أ, ب)\n"
        assert format_source(src) == src

    def test_comma_inside_string_untouched(self):
        src = "س = 'أ,ب'\n"
        assert format_source(src) == src

    def test_collapse_excess_blank_lines(self):
        src = "أ = 1\n\n\n\n\nب = 2\n"
        result = format_source(src)
        assert "\n\n\n\n" not in result
        assert "أ = 1" in result
        assert "ب = 2" in result

    def test_two_blank_lines_preserved(self):
        src = "أ = 1\n\n\nب = 2\n"
        result = format_source(src)
        # exactly 2 blank lines (3 newlines in a row) are kept
        assert "أ = 1\n\n\nب = 2\n" == result

    def test_inline_comment_space(self):
        src = "س = 1  #تعليق\n"
        result = format_source(src)
        assert "# تعليق" in result

    def test_multiline_string_comment_untouched(self):
        src = '"""\n#لا تعديل\n"""\n'
        result = format_source(src)
        assert "#لا تعديل" in result

    def test_idempotent_after_one_pass(self):
        src = "#تعليق\nاطبع(أ,ب)\n   \n"
        once = format_source(src)
        twice = format_source(once)
        assert once == twice


class TestFormatFile:
    def test_format_file_changes(self, tmp_path):
        p = tmp_path / "test.apy"
        p.write_text("#تعليق\n", encoding="utf-8")
        changed = format_file(p)
        assert changed is True
        assert p.read_text(encoding="utf-8") == "# تعليق\n"

    def test_format_file_no_change(self, tmp_path):
        p = tmp_path / "test.apy"
        p.write_text("# تعليق\n", encoding="utf-8")
        changed = format_file(p)
        assert changed is False

    def test_format_file_check_mode(self, tmp_path):
        p = tmp_path / "test.apy"
        p.write_text("#تعليق\n", encoding="utf-8")
        changed = format_file(p, check=True)
        assert changed is True
        # File should NOT have been modified in check mode
        assert p.read_text(encoding="utf-8") == "#تعليق\n"


class TestFormatterCLI:
    def test_cli_stdin(self, capsys, monkeypatch):
        import io
        from arabicpython.formatter import main
        monkeypatch.setattr("sys.stdin", io.StringIO("#تعليق\n"))
        rc = main([])
        out = capsys.readouterr().out
        assert rc == 0
        assert "# تعليق" in out

    def test_cli_file(self, tmp_path):
        from arabicpython.formatter import main
        p = tmp_path / "f.apy"
        p.write_text("#تعليق\n", encoding="utf-8")
        rc = main([str(p)])
        assert rc == 0
        assert p.read_text(encoding="utf-8") == "# تعليق\n"

    def test_cli_check_exit1(self, tmp_path):
        from arabicpython.formatter import main
        p = tmp_path / "f.apy"
        p.write_text("#تعليق\n", encoding="utf-8")
        rc = main(["--check", str(p)])
        assert rc == 1

    def test_cli_check_exit0_clean(self, tmp_path):
        from arabicpython.formatter import main
        p = tmp_path / "f.apy"
        p.write_text("# تعليق\n", encoding="utf-8")
        rc = main(["--check", str(p)])
        assert rc == 0

    def test_cli_missing_file(self, tmp_path):
        from arabicpython.formatter import main
        rc = main([str(tmp_path / "missing.apy")])
        assert rc == 1
