# tests/aliases/test_subprocess.py
# B-039 stdlib aliases — subprocess module tests

import pathlib
import subprocess

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def عملية_فرعية():
    """Return a ModuleProxy wrapping `subprocess`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("عملية_فرعية", None, None)
    assert spec is not None, "AliasFinder did not find 'عملية_فرعية'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSubprocessProxy:
    # ── High-level API aliases ────────────────────────────────────────────────

    def test_run_alias(self, عملية_فرعية):
        """شغل_امر maps to subprocess.run."""
        assert عملية_فرعية.شغل_امر is subprocess.run

    def test_call_alias(self, عملية_فرعية):
        """استدعي maps to subprocess.call."""
        assert عملية_فرعية.استدعي is subprocess.call

    def test_check_call_alias(self, عملية_فرعية):
        """استدعي_وتحقق maps to subprocess.check_call."""
        assert عملية_فرعية.استدعي_وتحقق is subprocess.check_call

    def test_check_output_alias(self, عملية_فرعية):
        """احضر_مخرجات maps to subprocess.check_output."""
        assert عملية_فرعية.احضر_مخرجات is subprocess.check_output

    def test_getoutput_alias(self, عملية_فرعية):
        """احضر_ناتج maps to subprocess.getoutput."""
        assert عملية_فرعية.احضر_ناتج is subprocess.getoutput

    def test_getstatusoutput_alias(self, عملية_فرعية):
        """احضر_حاله_وناتج maps to subprocess.getstatusoutput."""
        assert عملية_فرعية.احضر_حاله_وناتج is subprocess.getstatusoutput

    # ── Low-level class ───────────────────────────────────────────────────────

    def test_popen_alias(self, عملية_فرعية):
        """فتح_عمليه maps to subprocess.Popen."""
        assert عملية_فرعية.فتح_عمليه is subprocess.Popen

    # ── Sentinel constants ────────────────────────────────────────────────────

    def test_pipe_alias(self, عملية_فرعية):
        """انبوب maps to subprocess.PIPE."""
        assert عملية_فرعية.انبوب is subprocess.PIPE

    def test_stdout_alias(self, عملية_فرعية):
        """مخرجات_قياسيه maps to subprocess.STDOUT."""
        assert عملية_فرعية.مخرجات_قياسيه is subprocess.STDOUT

    def test_devnull_alias(self, عملية_فرعية):
        """مجهول maps to subprocess.DEVNULL."""
        assert عملية_فرعية.مجهول is subprocess.DEVNULL

    # ── Result / exception types ──────────────────────────────────────────────

    def test_completed_process_alias(self, عملية_فرعية):
        """عمليه_مكتمله maps to subprocess.CompletedProcess."""
        assert عملية_فرعية.عمليه_مكتمله is subprocess.CompletedProcess

    def test_subprocess_error_alias(self, عملية_فرعية):
        """خطا_عمليه_فرعيه maps to subprocess.SubprocessError."""
        assert عملية_فرعية.خطا_عمليه_فرعيه is subprocess.SubprocessError

    def test_called_process_error_alias(self, عملية_فرعية):
        """خطا_استدعاء_عمليه maps to subprocess.CalledProcessError."""
        assert عملية_فرعية.خطا_استدعاء_عمليه is subprocess.CalledProcessError

    def test_timeout_expired_alias(self, عملية_فرعية):
        """انتهاء_مهله_عمليه maps to subprocess.TimeoutExpired."""
        assert عملية_فرعية.انتهاء_مهله_عمليه is subprocess.TimeoutExpired

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_run_echo(self, عملية_فرعية):
        """شغل_امر executes a command and returns CompletedProcess."""
        import sys

        result = عملية_فرعية.شغل_امر(
            [sys.executable, "-c", "print('hello')"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_check_output_captures(self, عملية_فرعية):
        """احضر_مخرجات returns the command's stdout as bytes."""
        import sys

        out = عملية_فرعية.احضر_مخرجات([sys.executable, "-c", "print('test')"])
        assert b"test" in out

    def test_called_process_error_raised(self, عملية_فرعية):
        """احضر_مخرجات raises خطا_استدعاء_عمليه on non-zero exit."""
        import sys

        with pytest.raises(عملية_فرعية.خطا_استدعاء_عمليه):
            عملية_فرعية.احضر_مخرجات([sys.executable, "-c", "import sys; sys.exit(1)"])

    def test_pipe_captures_stdout(self, عملية_فرعية):
        """انبوب sentinel works with Popen to capture stdout."""
        import sys

        proc = عملية_فرعية.فتح_عمليه(
            [sys.executable, "-c", "print('pipe_test')"],
            stdout=عملية_فرعية.انبوب,
        )
        stdout, _ = proc.communicate()
        assert b"pipe_test" in stdout

    def test_completed_process_is_instance(self, عملية_فرعية):
        """Result of شغل_امر is an instance of عمليه_مكتمله."""
        import sys

        result = عملية_فرعية.شغل_امر([sys.executable, "-c", "pass"], capture_output=True)
        assert isinstance(result, عملية_فرعية.عمليه_مكتمله)

    def test_timeout_expired_is_subclass(self, عملية_فرعية):
        """انتهاء_مهله_عمليه is a subclass of خطا_عمليه_فرعيه."""
        assert issubclass(عملية_فرعية.انتهاء_مهله_عمليه, عملية_فرعية.خطا_عمليه_فرعيه)
