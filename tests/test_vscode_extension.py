# tests/test_vscode_extension.py
# B-053: VSCode extension structural tests
#
# These tests validate the extension's static files (package.json, grammar,
# language-config.json, extension.js) without requiring a live VSCode runtime.

import json
import re
from pathlib import Path

import pytest

VSCODE_DIR = Path(__file__).parent.parent / "editors" / "vscode"
GRAMMAR_PATH = VSCODE_DIR / "syntaxes" / "apy.tmLanguage.json"
PACKAGE_PATH = VSCODE_DIR / "package.json"
LANG_CONFIG_PATH = VSCODE_DIR / "language-config.json"
EXTENSION_PATH = VSCODE_DIR / "extension.js"
GENERATOR_PATH = Path(__file__).parent.parent / "tools" / "generate_vscode_grammar.py"


# ── File existence ────────────────────────────────────────────────────────────


class TestFilesExist:
    def test_package_json_exists(self):
        assert PACKAGE_PATH.exists()

    def test_grammar_exists(self):
        assert GRAMMAR_PATH.exists()

    def test_language_config_exists(self):
        assert LANG_CONFIG_PATH.exists()

    def test_extension_js_exists(self):
        assert EXTENSION_PATH.exists()

    def test_vscodeignore_exists(self):
        assert (VSCODE_DIR / ".vscodeignore").exists()

    def test_generator_script_exists(self):
        assert GENERATOR_PATH.exists()


# ── package.json ──────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def pkg():
    return json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))


class TestPackageJson:
    def test_name(self, pkg):
        assert pkg["name"] == "apython"

    def test_main_is_extension_js(self, pkg):
        assert pkg["main"] == "./extension.js"

    def test_contributes_language_apy(self, pkg):
        langs = pkg["contributes"]["languages"]
        ids = [lang["id"] for lang in langs]
        assert "apy" in ids

    def test_apy_extension_registered(self, pkg):
        langs = {lang["id"]: lang for lang in pkg["contributes"]["languages"]}
        assert ".apy" in langs["apy"]["extensions"]

    def test_grammar_contribution(self, pkg):
        grammars = pkg["contributes"]["grammars"]
        assert any(g["language"] == "apy" for g in grammars)

    def test_grammar_scope_name(self, pkg):
        grammars = {g["language"]: g for g in pkg["contributes"]["grammars"]}
        assert grammars["apy"]["scopeName"] == "source.apy"

    def test_grammar_path_points_to_file(self, pkg):
        grammars = {g["language"]: g for g in pkg["contributes"]["grammars"]}
        grammar_rel = grammars["apy"]["path"]
        grammar_abs = VSCODE_DIR / grammar_rel.lstrip("./")
        assert grammar_abs.exists(), f"Grammar file not found: {grammar_abs}"

    def test_language_config_path_points_to_file(self, pkg):
        langs = {lang["id"]: lang for lang in pkg["contributes"]["languages"]}
        cfg_rel = langs["apy"]["configuration"]
        cfg_abs = VSCODE_DIR / cfg_rel.lstrip("./")
        assert cfg_abs.exists(), f"Language config not found: {cfg_abs}"

    def test_activation_event_for_apy(self, pkg):
        events = pkg.get("activationEvents", [])
        assert "onLanguage:apy" in events

    def test_server_path_configuration_exists(self, pkg):
        props = pkg["contributes"]["configuration"]["properties"]
        assert "apython.serverPath" in props

    def test_trace_configuration_exists(self, pkg):
        props = pkg["contributes"]["configuration"]["properties"]
        assert "apython.trace.server" in props

    def test_vscode_languageclient_dependency(self, pkg):
        deps = pkg.get("dependencies", {})
        assert "vscode-languageclient" in deps

    def test_version_semver(self, pkg):
        version = pkg["version"]
        assert re.match(r"^\d+\.\d+\.\d+", version)

    def test_license(self, pkg):
        assert pkg["license"] == "Apache-2.0"


# ── TextMate grammar ──────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def grammar():
    return json.loads(GRAMMAR_PATH.read_text(encoding="utf-8"))


class TestGrammar:
    def test_scope_name(self, grammar):
        assert grammar["scopeName"] == "source.apy"

    def test_file_type_apy(self, grammar):
        assert "apy" in grammar["fileTypes"]

    def test_has_repository(self, grammar):
        assert "repository" in grammar

    def test_keyword_rule_exists(self, grammar):
        assert "keyword" in grammar["repository"]

    def test_keyword_rule_has_match(self, grammar):
        kw = grammar["repository"]["keyword"]
        assert "match" in kw
        assert len(kw["match"]) > 10  # non-trivial pattern

    def test_keyword_rule_covers_if(self, grammar):
        # إذا (if) must appear in the keyword pattern
        match_pat = grammar["repository"]["keyword"]["match"]
        assert "إذا" in match_pat or "اذا" in match_pat  # raw or normalised form

    def test_literal_rule_exists(self, grammar):
        assert "literal" in grammar["repository"]
        assert "match" in grammar["repository"]["literal"]

    def test_builtin_function_rule_exists(self, grammar):
        assert "builtin-function" in grammar["repository"]

    def test_builtin_type_rule_exists(self, grammar):
        assert "builtin-type" in grammar["repository"]

    def test_builtin_exception_rule_exists(self, grammar):
        assert "builtin-exception" in grammar["repository"]

    def test_comment_rule(self, grammar):
        comment = grammar["repository"]["comment"]
        assert comment["match"].startswith("#")

    def test_number_rule_exists(self, grammar):
        assert "number" in grammar["repository"]

    def test_operator_rule_exists(self, grammar):
        assert "operator" in grammar["repository"]

    def test_string_rules_exist(self, grammar):
        repo = grammar["repository"]
        assert "string-double" in repo
        assert "string-single" in repo
        assert "string-triple-double" in repo
        assert "string-triple-single" in repo

    def test_string_escape_rule(self, grammar):
        assert "string-escape" in grammar["repository"]

    def test_patterns_list_non_empty(self, grammar):
        assert len(grammar["patterns"]) >= 5

    def test_all_patterns_reference_valid_rules(self, grammar):
        repo = grammar["repository"]
        for p in grammar["patterns"]:
            ref = p.get("include", "")
            if ref.startswith("#"):
                key = ref[1:]
                assert key in repo, f"Pattern #{key} not in repository"


# ── language-config.json ──────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def lang_config():
    return json.loads(LANG_CONFIG_PATH.read_text(encoding="utf-8"))


class TestLanguageConfig:
    def test_line_comment_is_hash(self, lang_config):
        assert lang_config["comments"]["lineComment"] == "#"

    def test_brackets_defined(self, lang_config):
        brackets = lang_config["brackets"]
        pairs = [(b[0], b[1]) for b in brackets]
        assert ("(", ")") in pairs
        assert ("[", "]") in pairs
        assert ("{", "}") in pairs

    def test_auto_closing_pairs_defined(self, lang_config):
        assert "autoClosingPairs" in lang_config
        assert len(lang_config["autoClosingPairs"]) >= 3

    def test_word_pattern_includes_arabic(self, lang_config):
        pattern = lang_config.get("wordPattern", "")
        # Should include Arabic character range
        assert "ء" in pattern or "\\u" in pattern or "ي" in pattern


# ── extension.js ──────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def ext_source():
    return EXTENSION_PATH.read_text(encoding="utf-8")


class TestExtensionJs:
    def test_exports_activate(self, ext_source):
        assert "activate" in ext_source
        assert "module.exports" in ext_source

    def test_exports_deactivate(self, ext_source):
        assert "deactivate" in ext_source

    def test_uses_language_client(self, ext_source):
        assert "LanguageClient" in ext_source

    def test_launches_خادم_subcommand(self, ext_source):
        assert "خادم" in ext_source

    def test_uses_stdio_transport(self, ext_source):
        assert "stdio" in ext_source.lower() or "TransportKind" in ext_source

    def test_document_selector_for_apy(self, ext_source):
        assert '"apy"' in ext_source or "'apy'" in ext_source

    def test_resolves_server_executable(self, ext_source):
        assert "resolveServerExecutable" in ext_source or "serverPath" in ext_source

    def test_status_bar_item(self, ext_source):
        assert "statusBar" in ext_source or "createStatusBarItem" in ext_source


# ── Generator script ──────────────────────────────────────────────────────────


class TestGeneratorScript:
    def test_generator_is_valid_python(self):
        """The generator script must parse without SyntaxError."""
        import ast

        source = GENERATOR_PATH.read_text(encoding="utf-8")
        ast.parse(source)  # raises SyntaxError if invalid

    def test_generator_produces_valid_grammar(self, tmp_path, monkeypatch):
        """Running build_grammar() returns a valid grammar dict."""
        import importlib.util

        spec = importlib.util.spec_from_file_location("gen", GENERATOR_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        grammar = mod.build_grammar("ar-v2")
        assert grammar["scopeName"] == "source.apy"
        assert "keyword" in grammar["repository"]
        assert (
            "إذا" in grammar["repository"]["keyword"]["match"]
            or "اذا" in grammar["repository"]["keyword"]["match"]
        )
