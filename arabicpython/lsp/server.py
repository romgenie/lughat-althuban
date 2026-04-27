"""B-052: apython LSP server — JSON-RPC 2.0 over stdio.

Start with:
    ثعبان خادم

or programmatically:
    from arabicpython.lsp.server import main
    main()

Protocol
--------
Messages are framed with HTTP-style headers:
    Content-Length: <n>\\r\\n
    \\r\\n
    <UTF-8 JSON payload of exactly n bytes>

The server is single-threaded and synchronous.  For a .apy file it provides:
  - Hover: Arabic word → Python translation + category
  - Diagnostics: syntax errors reported as LSP diagnostics
  - Completion: all Arabic keywords/builtins filtered by typed prefix
  - Standard initialize / shutdown / exit lifecycle
"""

from __future__ import annotations

import json
import sys
from typing import IO

from arabicpython.lsp.providers import get_completions, get_diagnostics, get_hover

# ── JSON-RPC framing ──────────────────────────────────────────────────────────


def _read_message(stdin: IO[bytes]) -> dict | None:
    """Read one LSP message from *stdin*.  Returns None on EOF."""
    headers: dict[str, str] = {}
    while True:
        raw = stdin.readline()
        if not raw:
            return None  # EOF
        line = raw.decode("ascii", errors="replace").rstrip("\r\n")
        if not line:
            break  # blank line = end of headers
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()

    length = int(headers.get("content-length", 0))
    if length == 0:
        return None
    body = stdin.read(length)
    return json.loads(body.decode("utf-8"))


def _write_message(stdout: IO[bytes], payload: dict) -> None:
    """Write one LSP message to *stdout*."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    stdout.write(header + body)
    stdout.flush()


# ── Document store ────────────────────────────────────────────────────────────


class _DocumentStore:
    """Simple in-memory store of open document texts."""

    def __init__(self) -> None:
        self._docs: dict[str, str] = {}

    def open(self, uri: str, text: str) -> None:
        self._docs[uri] = text

    def change(self, uri: str, text: str) -> None:
        self._docs[uri] = text

    def close(self, uri: str) -> None:
        self._docs.pop(uri, None)

    def get(self, uri: str) -> str | None:
        return self._docs.get(uri)


# ── Server ────────────────────────────────────────────────────────────────────


class Server:
    """Synchronous LSP server.

    Instantiate and call :meth:`run` to start the stdin/stdout loop.
    The optional *stdin*/*stdout* parameters let tests inject byte streams.
    """

    def __init__(
        self,
        stdin: IO[bytes] | None = None,
        stdout: IO[bytes] | None = None,
    ) -> None:
        self._stdin: IO[bytes] = stdin or sys.stdin.buffer
        self._stdout: IO[bytes] = stdout or sys.stdout.buffer
        self._docs = _DocumentStore()
        self._dialect = None  # loaded lazily on first use
        self._running = False

    # ── Dialect (lazy) ────────────────────────────────────────────────────────

    def _get_dialect(self):
        if self._dialect is None:
            from arabicpython.dialect import load_dialect

            self._dialect = load_dialect("ar-v2")
        return self._dialect

    # ── I/O helpers ───────────────────────────────────────────────────────────

    def _send(self, payload: dict) -> None:
        _write_message(self._stdout, payload)

    def _respond(self, req_id, result) -> None:
        self._send({"jsonrpc": "2.0", "id": req_id, "result": result})

    def _error(self, req_id, code: int, message: str) -> None:
        self._send(
            {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": code, "message": message},
            }
        )

    def _notify(self, method: str, params: dict) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _publish_diagnostics(self, uri: str, source: str) -> None:
        diags = get_diagnostics(source, uri)
        self._notify(
            "textDocument/publishDiagnostics",
            {"uri": uri, "diagnostics": diags},
        )

    # ── Request / notification handlers ──────────────────────────────────────

    def _handle_initialize(self, req_id, params: dict) -> None:
        self._respond(
            req_id,
            {
                "capabilities": {
                    "textDocumentSync": {
                        "openClose": True,
                        "change": 1,  # Full sync
                    },
                    "hoverProvider": True,
                    "completionProvider": {
                        "triggerCharacters": [],
                        "resolveProvider": False,
                    },
                },
                "serverInfo": {
                    "name": "ثعبان-خادم",
                    "version": "0.1.0",
                },
            },
        )

    def _handle_did_open(self, params: dict) -> None:
        doc = params["textDocument"]
        self._docs.open(doc["uri"], doc["text"])
        self._publish_diagnostics(doc["uri"], doc["text"])

    def _handle_did_change(self, params: dict) -> None:
        doc = params["textDocument"]
        changes = params.get("contentChanges", [])
        if changes:
            text = changes[-1]["text"]  # full-sync: last change is full content
            self._docs.change(doc["uri"], text)
            self._publish_diagnostics(doc["uri"], text)

    def _handle_did_close(self, params: dict) -> None:
        uri = params["textDocument"]["uri"]
        self._docs.close(uri)
        # Clear diagnostics on close
        self._notify("textDocument/publishDiagnostics", {"uri": uri, "diagnostics": []})

    def _handle_hover(self, req_id, params: dict) -> None:
        uri = params["textDocument"]["uri"]
        pos = params["position"]
        source = self._docs.get(uri)
        if source is None:
            self._respond(req_id, None)
            return

        md = get_hover(source, pos["line"], pos["character"], self._get_dialect())
        if md is None:
            self._respond(req_id, None)
        else:
            self._respond(req_id, {"contents": {"kind": "markdown", "value": md}})

    def _handle_completion(self, req_id, params: dict) -> None:
        uri = params["textDocument"]["uri"]
        pos = params["position"]
        source = self._docs.get(uri) or ""

        items = get_completions(source, pos["line"], pos["character"], self._get_dialect())
        self._respond(req_id, {"isIncomplete": False, "items": items})

    def _handle_shutdown(self, req_id) -> None:
        self._respond(req_id, None)
        self._running = False

    # ── Main loop ─────────────────────────────────────────────────────────────

    def dispatch(self, msg: dict) -> None:
        """Dispatch a single parsed JSON-RPC message."""
        method = msg.get("method", "")
        req_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            self._handle_initialize(req_id, params)
        elif method == "initialized":
            pass  # notification, no response
        elif method == "textDocument/didOpen":
            self._handle_did_open(params)
        elif method == "textDocument/didChange":
            self._handle_did_change(params)
        elif method == "textDocument/didClose":
            self._handle_did_close(params)
        elif method == "textDocument/hover":
            self._handle_hover(req_id, params)
        elif method == "textDocument/completion":
            self._handle_completion(req_id, params)
        elif method == "shutdown":
            self._handle_shutdown(req_id)
        elif method == "exit":
            sys.exit(0 if not self._running else 1)
        elif req_id is not None:
            # Unknown request — respond with MethodNotFound
            self._error(req_id, -32601, f"Method not found: {method}")
        # Unknown notifications are silently ignored per LSP spec

    def run(self) -> None:
        """Read and dispatch messages until EOF or shutdown."""
        self._running = True
        while self._running:
            msg = _read_message(self._stdin)
            if msg is None:
                break
            try:
                self.dispatch(msg)
            except Exception as exc:  # noqa: BLE001
                # Log to stderr (never stdout — that's the JSON-RPC channel)
                sys.stderr.write(f"ثعبان-خادم: خطأ داخلي: {exc}\n")


# ── Entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    """Start the LSP server on stdio. Called by `ثعبان خادم`."""
    Server().run()
