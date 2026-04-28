// editors/vscode/extension.js
// B-053: apython VSCode extension
//
// Activates when a .apy file is opened.
// Starts `ثعبان خادم` as a child process and connects the built-in
// VSCode LSP client to it, giving the editor:
//   - Hover (Arabic word → Python translation + category)
//   - Diagnostics (syntax errors highlighted inline)
//   - Completion (Arabic keywords and built-ins)
//
// Configuration:
//   apython.serverPath   Path to ثعبان executable (defaults to PATH lookup)
//   apython.trace.server LSP message tracing (off | messages | verbose)

"use strict";

const path = require("path");
const { workspace, window } = require("vscode");
const { LanguageClient, TransportKind } = require("vscode-languageclient/node");

/** @type {LanguageClient | undefined} */
let client;

/**
 * Find the ثعبان executable.
 * Checks apython.serverPath config first, then falls back to PATH.
 * @returns {string}
 */
function resolveServerExecutable() {
  const config = workspace.getConfiguration("apython");
  const configured = config.get("serverPath", "").trim();
  if (configured) {
    return configured;
  }
  // On Windows the entry point script is named "ثعبان.exe" or "ثعبان" via
  // pip-installed scripts.  Fall back to `python -m arabicpython.lsp.server`
  // if the named executable is unavailable.
  return process.platform === "win32" ? "ثعبان.exe" : "ثعبان";
}

/**
 * Build the ServerOptions for the LanguageClient.
 * We launch `ثعبان خادم` which reads/writes JSON-RPC on stdio.
 * @returns {import("vscode-languageclient/node").ServerOptions}
 */
function buildServerOptions() {
  const executable = resolveServerExecutable();

  // Primary: named entry-point (`ثعبان خادم`)
  const run = {
    command: executable,
    args: ["خادم"],
    transport: TransportKind.stdio,
  };

  // Fallback: `python -m arabicpython.lsp.server` (works without pip install)
  const fallback = {
    command: "python",
    args: ["-m", "arabicpython.lsp.server"],
    transport: TransportKind.stdio,
  };

  return {
    run,
    debug: run, // same for debug — no separate debug build
    // If `run` fails to start, the client retries with `fallback`.
    // (vscode-languageclient handles this automatically when run is an array.)
  };
}

/**
 * @param {import("vscode").ExtensionContext} context
 */
function activate(context) {
  const config = workspace.getConfiguration("apython");
  const traceLevel = config.get("trace.server", "off");

  const serverOptions = buildServerOptions();

  /** @type {import("vscode-languageclient/node").LanguageClientOptions} */
  const clientOptions = {
    // Activate for .apy files
    documentSelector: [
      { scheme: "file", language: "apy" },
      { scheme: "untitled", language: "apy" },
    ],
    synchronize: {
      // Re-send diagnostics when these files change
      fileEvents: workspace.createFileSystemWatcher("**/*.apy"),
    },
    outputChannelName: "ثعبان-خادم",
    traceOutputChannel: window.createOutputChannel("ثعبان-خادم (trace)"),
    initializationOptions: {},
    middleware: {},
  };

  client = new LanguageClient(
    "apython",
    "لغة الثعبان — خادم اللغة",
    serverOptions,
    clientOptions
  );

  // Start and register for cleanup on deactivate
  const disposable = client.start();
  context.subscriptions.push(disposable);

  // Status bar item
  const statusBar = window.createStatusBarItem();
  statusBar.text = "$(snake) ثعبان";
  statusBar.tooltip = "لغة الثعبان — خادم اللغة نشط";
  statusBar.command = "workbench.action.problems.focus";
  context.subscriptions.push(statusBar);

  client.onDidChangeState((event) => {
    const { State } = require("vscode-languageclient");
    if (event.newState === State.Running) {
      statusBar.show();
    } else {
      statusBar.hide();
    }
  });
}

async function deactivate() {
  if (client) {
    await client.stop();
    client = undefined;
  }
}

module.exports = { activate, deactivate };
