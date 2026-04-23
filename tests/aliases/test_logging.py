# tests/aliases/test_logging.py
# B-036 stdlib aliases — logging module tests
#
# Uses an in-memory StringIO handler to capture log output without touching
# the file system or the root logger configuration.

import io
import logging
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def تسجيل():
    """Return a ModuleProxy wrapping `logging`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("تسجيل", None, None)
    assert spec is not None, "AliasFinder did not find 'تسجيل'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


@pytest.fixture()
def مسجل_تجريبي():
    """Return a fresh Logger with an in-memory StreamHandler; tear down after test."""
    logger = logging.getLogger("test_arabic_" + str(id(object())))
    logger.setLevel(logging.DEBUG)
    buf = io.StringIO()
    handler = logging.StreamHandler(buf)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    yield logger, buf
    logger.handlers.clear()


class TestLoggingProxy:
    # ── Level constant aliases ────────────────────────────────────────────────

    def test_debug_level_alias(self, تسجيل):
        """مستوى_تصحيح maps to logging.DEBUG."""
        assert تسجيل.مستوى_تصحيح == logging.DEBUG

    def test_info_level_alias(self, تسجيل):
        """مستوى_معلومات maps to logging.INFO."""
        assert تسجيل.مستوى_معلومات == logging.INFO

    def test_warning_level_alias(self, تسجيل):
        """مستوى_تحذير maps to logging.WARNING."""
        assert تسجيل.مستوى_تحذير == logging.WARNING

    def test_error_level_alias(self, تسجيل):
        """مستوى_خطا maps to logging.ERROR."""
        assert تسجيل.مستوى_خطا == logging.ERROR

    def test_critical_level_alias(self, تسجيل):
        """مستوى_حرج maps to logging.CRITICAL."""
        assert تسجيل.مستوى_حرج == logging.CRITICAL

    def test_notset_level_alias(self, تسجيل):
        """مستوى_لاشيء maps to logging.NOTSET."""
        assert تسجيل.مستوى_لاشيء == logging.NOTSET

    # ── Class aliases ─────────────────────────────────────────────────────────

    def test_logger_class_alias(self, تسجيل):
        """مسجل maps to logging.Logger."""
        assert تسجيل.مسجل is logging.Logger

    def test_handler_class_alias(self, تسجيل):
        """معالج maps to logging.Handler."""
        assert تسجيل.معالج is logging.Handler

    def test_formatter_class_alias(self, تسجيل):
        """منسق_سجل maps to logging.Formatter."""
        assert تسجيل.منسق_سجل is logging.Formatter

    def test_filter_class_alias(self, تسجيل):
        """مرشح maps to logging.Filter."""
        assert تسجيل.مرشح is logging.Filter

    def test_stream_handler_alias(self, تسجيل):
        """معالج_دفق maps to logging.StreamHandler."""
        assert تسجيل.معالج_دفق is logging.StreamHandler

    def test_file_handler_alias(self, تسجيل):
        """معالج_ملف maps to logging.FileHandler."""
        assert تسجيل.معالج_ملف is logging.FileHandler

    def test_null_handler_alias(self, تسجيل):
        """معالج_فارغ maps to logging.NullHandler."""
        assert تسجيل.معالج_فارغ is logging.NullHandler

    # ── Module-level function aliases ─────────────────────────────────────────

    def test_get_logger_alias(self, تسجيل):
        """احضر_مسجل maps to logging.getLogger."""
        assert تسجيل.احضر_مسجل is logging.getLogger

    def test_basic_config_alias(self, تسجيل):
        """ضبط_اساسي maps to logging.basicConfig."""
        assert تسجيل.ضبط_اساسي is logging.basicConfig

    def test_get_level_name_alias(self, تسجيل):
        """احضر_اسم_مستوي maps to logging.getLevelName."""
        assert تسجيل.احضر_اسم_مستوي is logging.getLevelName

    def test_module_debug_alias(self, تسجيل):
        """تصحيح maps to logging.debug."""
        assert تسجيل.تصحيح is logging.debug

    def test_module_info_alias(self, تسجيل):
        """معلومات maps to logging.info."""
        assert تسجيل.معلومات is logging.info

    def test_module_warning_alias(self, تسجيل):
        """تحذير maps to logging.warning."""
        assert تسجيل.تحذير is logging.warning

    def test_module_error_alias(self, تسجيل):
        """خطا maps to logging.error."""
        assert تسجيل.خطا is logging.error

    def test_module_critical_alias(self, تسجيل):
        """حرج maps to logging.critical."""
        assert تسجيل.حرج is logging.critical

    def test_shutdown_alias(self, تسجيل):
        """اغلق maps to logging.shutdown."""
        assert تسجيل.اغلق is logging.shutdown

    # ── Logger unbound method aliases ─────────────────────────────────────────

    def test_logger_setlevel_unbound(self, تسجيل):
        """ضبط_مستوي is Logger.setLevel (unbound)."""
        assert تسجيل.ضبط_مستوي is logging.Logger.setLevel

    def test_logger_addhandler_unbound(self, تسجيل):
        """اضف_معالج is Logger.addHandler (unbound)."""
        assert تسجيل.اضف_معالج is logging.Logger.addHandler

    def test_logger_geteffectivelevel_unbound(self, تسجيل):
        """احضر_مستوى_فعلي is Logger.getEffectiveLevel (unbound)."""
        assert تسجيل.احضر_مستوى_فعلي is logging.Logger.getEffectiveLevel

    # ── Handler unbound method aliases ────────────────────────────────────────

    def test_handler_setformatter_unbound(self, تسجيل):
        """ضبط_منسق is Handler.setFormatter (unbound)."""
        assert تسجيل.ضبط_منسق is logging.Handler.setFormatter

    def test_handler_setlevel_unbound(self, تسجيل):
        """ضبط_مستوى_معالج is Handler.setLevel (unbound)."""
        assert تسجيل.ضبط_مستوى_معالج is logging.Handler.setLevel

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_get_logger_returns_logger(self, تسجيل):
        """احضر_مسجل('test') returns a Logger instance."""
        logger = تسجيل.احضر_مسجل("arabic_test_logger")
        assert isinstance(logger, logging.Logger)

    def test_logger_writes_to_stream(self, تسجيل, مسجل_تجريبي):
        """Logger.info writes to the in-memory buffer via StreamHandler."""
        logger, buf = مسجل_تجريبي
        logger.info("رسالة تجريبية")
        output = buf.getvalue()
        assert "رسالة تجريبية" in output

    def test_logger_debug_unbound(self, تسجيل, مسجل_تجريبي):
        """تصحيح_مسجل (Logger.debug unbound) writes DEBUG messages."""
        logger, buf = مسجل_تجريبي
        تسجيل.تصحيح_مسجل(logger, "debug: اختبار")
        assert "debug: اختبار" in buf.getvalue()

    def test_logger_setlevel_unbound_functional(self, تسجيل):
        """ضبط_مستوي (Logger.setLevel unbound) changes effective level."""
        logger = logging.getLogger("arabic_setlevel_test")
        تسجيل.ضبط_مستوي(logger, logging.WARNING)
        assert logger.getEffectiveLevel() == logging.WARNING
        تسجيل.ضبط_مستوي(logger, logging.DEBUG)

    def test_level_name_roundtrip(self, تسجيل):
        """احضر_اسم_مستوي('DEBUG') → 10 == DEBUG."""
        assert تسجيل.احضر_اسم_مستوي(logging.DEBUG) == "DEBUG"
        assert تسجيل.احضر_اسم_مستوي("DEBUG") == logging.DEBUG

    def test_formatter_format_unbound(self, تسجيل):
        """نسق_سجله (Formatter.format unbound) formats a LogRecord."""
        fmt = logging.Formatter("%(levelname)s: %(message)s")
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="مرحبا",
            args=(),
            exc_info=None,
        )
        result = تسجيل.نسق_سجله(fmt, record)
        assert "INFO" in result
        assert "مرحبا" in result
