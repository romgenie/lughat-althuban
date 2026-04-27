# tests/test_test_runner.py
# B-051: Arabic test runner — ثعبان اختبر

from arabicpython.test_runner import _translate_args, run_tests

# ── _translate_args unit tests ────────────────────────────────────────────────


class TestTranslateArgs:
    def test_verbose_flag(self):
        assert _translate_args(["--مطول"]) == ["-v"]

    def test_quiet_flag(self):
        assert _translate_args(["--هادئ"]) == ["-q"]

    def test_stop_on_first_failure(self):
        assert _translate_args(["--توقف_اول"]) == ["-x"]

    def test_no_header(self):
        assert _translate_args(["--بلا_رأس"]) == ["--no-header"]

    def test_no_warnings(self):
        assert _translate_args(["--بلا_تحذيرات"]) == ["-p", "no:warnings"]

    def test_coverage_bare(self):
        assert _translate_args(["--غطاء"]) == ["--cov"]

    def test_coverage_with_path(self):
        assert _translate_args(["--غطاء=arabicpython"]) == ["--cov=arabicpython"]

    def test_keyword_filter(self):
        assert _translate_args(["--اسم=test_foo"]) == ["-k", "test_foo"]

    def test_marker_filter(self):
        assert _translate_args(["--علامه=network"]) == ["-m", "network"]

    def test_traceback_style(self):
        assert _translate_args(["--تقرير=short"]) == ["--tb=short"]

    def test_parallel_workers(self):
        assert _translate_args(["--منفذ=4"]) == ["-n", "4"]

    def test_unknown_args_forwarded_verbatim(self):
        assert _translate_args(["tests/", "--unknown"]) == ["tests/", "--unknown"]

    def test_mixed_arabic_and_plain_args(self):
        result = _translate_args(["--مطول", "tests/aliases/", "--توقف_اول"])
        assert result == ["-v", "tests/aliases/", "-x"]

    def test_empty_input(self):
        assert _translate_args([]) == []

    def test_multiple_flags(self):
        result = _translate_args(["--مطول", "--هادئ", "--توقف_اول"])
        assert result == ["-v", "-q", "-x"]

    def test_keyword_filter_with_spaces_in_value(self):
        result = _translate_args(["--اسم=foo or bar"])
        assert result == ["-k", "foo or bar"]

    def test_traceback_no(self):
        assert _translate_args(["--تقرير=no"]) == ["--tb=no"]


# ── run_tests integration tests ───────────────────────────────────────────────


class TestRunTests:
    def test_passing_suite_returns_zero(self, tmp_path):
        """A trivially-passing test file → exit code 0."""
        t = tmp_path / "test_ok.py"
        t.write_text("def test_pass(): assert 1 + 1 == 2\n", encoding="utf-8")
        code = run_tests([str(tmp_path), "--بلا_رأس", "--تقرير=no"])
        assert code == 0

    def test_failing_suite_returns_nonzero(self, tmp_path):
        """A failing test file → non-zero exit code."""
        t = tmp_path / "test_fail.py"
        t.write_text("def test_fail(): assert False\n", encoding="utf-8")
        code = run_tests([str(tmp_path), "--بلا_رأس", "--تقرير=no"])
        assert code != 0

    def test_stop_on_first_failure(self, tmp_path):
        """--توقف_اول maps to -x; suite aborts after first failure."""
        t = tmp_path / "test_two_fails.py"
        t.write_text(
            "def test_first(): assert False\n" "def test_second(): assert False\n",
            encoding="utf-8",
        )
        code = run_tests([str(tmp_path), "--توقف_اول", "--بلا_رأس", "--تقرير=no"])
        assert code != 0

    def test_keyword_filter_selects_tests(self, tmp_path):
        """--اسم= filters by keyword; only matching tests run."""
        t = tmp_path / "test_mixed.py"
        t.write_text(
            "def test_alpha(): assert True\n" "def test_beta(): assert False\n",
            encoding="utf-8",
        )
        # Run only test_alpha — should pass
        code = run_tests([str(tmp_path), "--اسم=alpha", "--بلا_رأس", "--تقرير=no"])
        assert code == 0

    def test_empty_directory_returns_no_tests_exit_code(self, tmp_path):
        """No test files collected → pytest exit code 5 (no tests collected)."""
        code = run_tests([str(tmp_path), "--بلا_رأس"])
        assert code == 5  # pytest.ExitCode.NO_TESTS_COLLECTED

    def test_verbose_flag_forwarded(self, tmp_path, capsys):
        """--مطول is forwarded to pytest (-v); output contains PASSED."""
        t = tmp_path / "test_v.py"
        t.write_text("def test_verbose(): assert True\n", encoding="utf-8")
        run_tests([str(tmp_path), "--مطول", "--بلا_رأس", "--تقرير=no"])
        out, _ = capsys.readouterr()
        assert "PASSED" in out


# ── CLI integration ───────────────────────────────────────────────────────────


class TestCLIDispatch:
    def test_اختبر_subcommand_dispatches(self, tmp_path):
        """ثعبان اختبر <path> is handled by run_tests, returns 0 for pass."""
        from arabicpython.cli import main

        t = tmp_path / "test_cli.py"
        t.write_text("def test_ok(): assert True\n", encoding="utf-8")
        code = main(["اختبر", str(tmp_path), "--بلا_رأس", "--تقرير=no"])
        assert code == 0

    def test_اختبر_failing_returns_nonzero(self, tmp_path):
        from arabicpython.cli import main

        t = tmp_path / "test_cli_fail.py"
        t.write_text("def test_bad(): assert False\n", encoding="utf-8")
        code = main(["اختبر", str(tmp_path), "--بلا_رأس", "--تقرير=no"])
        assert code != 0
