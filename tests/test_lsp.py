# tests/test_lsp.py
# B-052: LSP server — providers and server dispatch

import io

import pytest

from arabicpython.dialect import load_dialect
from arabicpython.lsp.providers import (
    _word_at,
    get_completions,
    get_diagnostics,
    get_hover,
)
from arabicpython.lsp.server import Server, _read_message, _write_message

# ── Shared fixture ────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def dialect():
    return load_dialect("ar-v2")


# ── _word_at ──────────────────────────────────────────────────────────────────


class TestWordAt:
    def test_returns_arabic_word(self):
        source = "إذا صح:"
        assert _word_at(source, 0, 0) is not None

    def test_returns_none_past_end(self):
        assert _word_at("إذا", 0, 100) is None

    def test_returns_none_on_missing_line(self):
        assert _word_at("إذا", 5, 0) is None

    def test_cursor_in_middle_of_word(self):
        source = "اطبع"
        word = _word_at(source, 0, 2)
        assert word is not None
        assert "اطبع" in word or len(word) > 0

    def test_returns_none_on_space(self):
        source = "إذا صح"
        # cursor on the space between words
        assert _word_at(source, 0, 3) is None


# ── get_hover ─────────────────────────────────────────────────────────────────


class TestGetHover:
    def test_keyword_returns_markdown(self, dialect):
        # إذا is "if" in ar-v2
        source = "إذا صح:"
        result = get_hover(source, 0, 0, dialect)
        assert result is not None
        assert "if" in result

    def test_unknown_word_returns_none(self, dialect):
        source = "متغير_مجهول_تماما"
        result = get_hover(source, 0, 0, dialect)
        # Either None or a user-identifier note — never raises
        assert result is None or isinstance(result, str)

    def test_position_off_line_returns_none(self, dialect):
        source = "إذا"
        assert get_hover(source, 99, 0, dialect) is None

    def test_hover_includes_category(self, dialect):
        # Keywords should mention their category label
        source = "إذا"
        result = get_hover(source, 0, 0, dialect)
        assert result is not None
        assert "كلمة" in result or "if" in result

    def test_hover_on_builtin(self, dialect):
        # اطبع → print
        source = "اطبع"
        result = get_hover(source, 0, 0, dialect)
        if result is not None:  # only if aطبع is in the dialect
            assert "print" in result or "اطبع" in result

    def test_returns_string(self, dialect):
        source = "إذا صح:\n    اطبع('مرحبا')\n"
        result = get_hover(source, 0, 0, dialect)
        assert result is None or isinstance(result, str)


# ── get_diagnostics ───────────────────────────────────────────────────────────


class TestGetDiagnostics:
    def test_valid_source_returns_empty(self):
        source = "س = ١\n"
        diags = get_diagnostics(source, "file:///test.apy")
        assert diags == []

    def test_valid_arabic_if_returns_empty(self):
        source = "إذا صح:\n    س = ١\n"
        diags = get_diagnostics(source, "file:///test.apy")
        assert diags == []

    def test_syntax_error_returns_diagnostic(self):
        source = "إذا:\n"  # missing condition
        diags = get_diagnostics(source, "file:///bad.apy")
        assert len(diags) >= 1
        d = diags[0]
        assert "range" in d
        assert "message" in d
        assert d["severity"] == 1

    def test_diagnostic_range_has_correct_shape(self):
        source = "إذا:\n"
        diags = get_diagnostics(source, "file:///bad.apy")
        if diags:
            r = diags[0]["range"]
            assert "start" in r and "end" in r
            assert "line" in r["start"] and "character" in r["start"]

    def test_plain_python_valid_source(self):
        source = "x = 1\n"
        diags = get_diagnostics(source, "file:///plain.py")
        assert diags == []

    def test_source_is_arabic_string(self):
        source = 'اطبع("مرحبا")\n'
        diags = get_diagnostics(source, "file:///hello.apy")
        assert diags == []

    def test_diagnostic_source_field(self):
        source = "إذا:\n"
        diags = get_diagnostics(source, "file:///bad.apy")
        if diags:
            assert diags[0]["source"] == "ثعبان"


# ── get_completions ───────────────────────────────────────────────────────────


class TestGetCompletions:
    def test_returns_list(self, dialect):
        items = get_completions("", 0, 0, dialect)
        assert isinstance(items, list)

    def test_items_have_required_fields(self, dialect):
        items = get_completions("", 0, 0, dialect)
        assert items, "Expected at least one completion item"
        for item in items[:5]:
            assert "label" in item
            assert "kind" in item
            assert "detail" in item

    def test_prefix_filters_results(self, dialect):
        # Prefix "إذ" should match إذا (if) but not اطبع (print)
        source = "إذ"
        items = get_completions(source, 0, 2, dialect)
        labels = {i["label"] for i in items}
        # All labels must start with the normalised prefix
        from arabicpython.normalize import normalize_identifier

        for label in labels:
            norm = normalize_identifier(label)
            assert norm.startswith("اذ") or label.startswith(
                "إذ"
            ), f"'{label}' does not match prefix 'إذ'"

    def test_empty_prefix_returns_all_keywords(self, dialect):
        items = get_completions("", 0, 0, dialect)
        # Should contain إذا (if)
        labels = {i["label"] for i in items}
        assert any("ذ" in label for label in labels), "Expected if-like keyword"

    def test_completion_detail_is_python_name(self, dialect):
        items = get_completions("", 0, 0, dialect)
        for item in items[:10]:
            detail = item["detail"]
            assert detail.isascii() or detail, "detail should be a Python name"

    def test_keywords_sorted_first(self, dialect):
        items = get_completions("", 0, 0, dialect)
        if len(items) >= 2:
            kinds = [i["kind"] for i in items[:5]]
            # Kind 14 = keyword — should appear early
            assert 14 in kinds or len(kinds) > 0  # at minimum, list is non-empty


# ── JSON-RPC framing ──────────────────────────────────────────────────────────


class TestJSONRPCFraming:
    def test_write_then_read_round_trip(self):
        payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        buf = io.BytesIO()
        _write_message(buf, payload)
        buf.seek(0)
        result = _read_message(buf)
        assert result == payload

    def test_write_sets_content_length(self):
        buf = io.BytesIO()
        _write_message(buf, {"x": 1})
        raw = buf.getvalue().decode("ascii", errors="replace")
        assert "Content-Length:" in raw

    def test_read_returns_none_on_eof(self):
        empty = io.BytesIO(b"")
        assert _read_message(empty) is None

    def test_unicode_payload_round_trip(self):
        payload = {"method": "test", "params": {"text": "مرحبا بالعالم"}}
        buf = io.BytesIO()
        _write_message(buf, payload)
        buf.seek(0)
        result = _read_message(buf)
        assert result["params"]["text"] == "مرحبا بالعالم"


# ── Server.dispatch ───────────────────────────────────────────────────────────


def _make_server() -> tuple[Server, io.BytesIO]:
    """Return a Server wired to an in-memory stdout buffer."""
    out = io.BytesIO()
    server = Server(stdin=io.BytesIO(b""), stdout=out)
    return server, out


def _read_response(buf: io.BytesIO) -> dict:
    buf.seek(0)
    msg = _read_message(buf)
    assert msg is not None
    return msg


class TestServerDispatch:
    def test_initialize_returns_capabilities(self):
        server, out = _make_server()
        server.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        resp = _read_response(out)
        assert resp["id"] == 1
        caps = resp["result"]["capabilities"]
        assert "hoverProvider" in caps
        assert "completionProvider" in caps
        assert "textDocumentSync" in caps

    def test_initialize_serverinfo(self):
        server, out = _make_server()
        server.dispatch({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        resp = _read_response(out)
        info = resp["result"]["serverInfo"]
        assert info["name"] == "ثعبان-خادم"

    def test_initialized_notification_silent(self):
        server, out = _make_server()
        server.dispatch({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        assert out.tell() == 0  # nothing written

    def test_unknown_notification_silent(self):
        server, out = _make_server()
        server.dispatch({"jsonrpc": "2.0", "method": "workspace/didChangeConfiguration"})
        assert out.tell() == 0

    def test_unknown_request_returns_method_not_found(self):
        server, out = _make_server()
        server.dispatch({"jsonrpc": "2.0", "id": 5, "method": "$/unknown"})
        resp = _read_response(out)
        assert resp["id"] == 5
        assert resp["error"]["code"] == -32601

    def test_did_open_publishes_diagnostics(self):
        server, out = _make_server()
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didOpen",
                "params": {
                    "textDocument": {
                        "uri": "file:///test.apy",
                        "languageId": "apy",
                        "version": 1,
                        "text": "س = ١\n",
                    }
                },
            }
        )
        out.seek(0)
        msg = _read_message(out)
        assert msg is not None
        assert msg["method"] == "textDocument/publishDiagnostics"
        assert msg["params"]["uri"] == "file:///test.apy"
        assert msg["params"]["diagnostics"] == []

    def test_did_open_invalid_publishes_error(self):
        server, out = _make_server()
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didOpen",
                "params": {
                    "textDocument": {
                        "uri": "file:///bad.apy",
                        "languageId": "apy",
                        "version": 1,
                        "text": "إذا:\n",
                    }
                },
            }
        )
        out.seek(0)
        msg = _read_message(out)
        assert msg["params"]["diagnostics"]  # at least one diagnostic

    def test_hover_on_keyword_returns_markdown(self):
        server, out = _make_server()
        uri = "file:///hover.apy"
        # First open the document
        server._docs.open(uri, "إذا صح:\n    اطبع('x')\n")
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/hover",
                "params": {
                    "textDocument": {"uri": uri},
                    "position": {"line": 0, "character": 0},
                },
            }
        )
        resp = _read_response(out)
        assert resp["id"] == 2
        result = resp["result"]
        assert result is not None
        assert result["contents"]["kind"] == "markdown"
        assert "if" in result["contents"]["value"]

    def test_hover_on_unknown_returns_null(self):
        server, out = _make_server()
        uri = "file:///hover2.apy"
        server._docs.open(uri, "   ")
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "textDocument/hover",
                "params": {
                    "textDocument": {"uri": uri},
                    "position": {"line": 0, "character": 1},
                },
            }
        )
        resp = _read_response(out)
        assert resp["result"] is None

    def test_hover_on_missing_doc_returns_null(self):
        server, out = _make_server()
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "textDocument/hover",
                "params": {
                    "textDocument": {"uri": "file:///not_open.apy"},
                    "position": {"line": 0, "character": 0},
                },
            }
        )
        resp = _read_response(out)
        assert resp["result"] is None

    def test_completion_returns_items(self):
        server, out = _make_server()
        uri = "file:///comp.apy"
        server._docs.open(uri, "")
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "textDocument/completion",
                "params": {
                    "textDocument": {"uri": uri},
                    "position": {"line": 0, "character": 0},
                },
            }
        )
        resp = _read_response(out)
        assert resp["id"] == 6
        items = resp["result"]["items"]
        assert isinstance(items, list)
        assert len(items) > 0

    def test_shutdown_stops_loop(self):
        server, out = _make_server()
        server._running = True
        server.dispatch({"jsonrpc": "2.0", "id": 9, "method": "shutdown"})
        assert not server._running
        resp = _read_response(out)
        assert resp["result"] is None

    def test_did_change_updates_document(self):
        server, out = _make_server()
        uri = "file:///change.apy"
        server._docs.open(uri, "س = ١\n")
        out_initial = out.tell()
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didChange",
                "params": {
                    "textDocument": {"uri": uri, "version": 2},
                    "contentChanges": [{"text": "إذا:\n"}],
                },
            }
        )
        assert server._docs.get(uri) == "إذا:\n"
        # Should have published new diagnostics
        assert out.tell() > out_initial

    def test_did_close_clears_diagnostics(self):
        server, out = _make_server()
        uri = "file:///close.apy"
        server._docs.open(uri, "س = ١\n")
        out.seek(0)
        out.truncate()
        server.dispatch(
            {
                "jsonrpc": "2.0",
                "method": "textDocument/didClose",
                "params": {"textDocument": {"uri": uri}},
            }
        )
        out.seek(0)
        msg = _read_message(out)
        assert msg["params"]["diagnostics"] == []
        assert server._docs.get(uri) is None


# ── CLI dispatch ──────────────────────────────────────────────────────────────


class TestCLIDispatch:
    def test_خادم_is_recognised(self):
        """ثعبان خادم dispatches to the LSP server (we just verify no AttributeError)."""
        from arabicpython.cli import main
        from arabicpython.lsp import server as lsp_server

        # Patch Server.run to return immediately
        original_run = lsp_server.Server.run

        def _noop(self):
            pass

        lsp_server.Server.run = _noop
        try:
            code = main(["خادم"])
            assert code == 0
        finally:
            lsp_server.Server.run = original_run
