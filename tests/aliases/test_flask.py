# tests/aliases/test_flask.py
# B-010 Flask alias tests
#
# Tests the module proxy, ClassFactory, and InstanceProxy chain:
#   فلاسك.فلاسك  →  ClassFactory
#   فلاسك.فلاسك(__name__)  →  InstanceProxy wrapping a real Flask app
#   @تطبيق.طريق('/')  →  app.route('/')  (bound via InstanceProxy.__getattr__)

import pathlib

import pytest

# Skip entire module if flask is not installed
flask = pytest.importorskip("flask")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def فلاسك_موديل():
    """Module proxy wrapping flask."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("فلاسك", None, None)
    assert spec is not None, "AliasFinder did not find 'فلاسك'"
    return spec.loader.create_module(spec)


@pytest.fixture()
def تطبيق(فلاسك_موديل):
    """A proxied Flask app instance (InstanceProxy) with TESTING=True."""
    app_proxy = فلاسك_موديل.فلاسك(__name__)
    # Access the underlying Flask app to set config
    flask_app = object.__getattribute__(app_proxy, "_wrapped")
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret"
    return app_proxy


# ---------------------------------------------------------------------------
# Module-proxy tests
# ---------------------------------------------------------------------------


class TestFlaskModuleProxy:
    def test_module_proxy_repr(self, فلاسك_موديل):
        """Module proxy repr identifies itself as an arabic-proxy of flask."""
        assert "flask" in repr(فلاسك_موديل)
        assert "arabic-proxy" in repr(فلاسك_موديل)

    def test_flask_class_is_class_factory(self, فلاسك_موديل):
        """فلاسك.فلاسك returns a ClassFactory, not the raw Flask class."""
        from arabicpython.aliases._proxy import ClassFactory

        factory = فلاسك_موديل.فلاسك
        assert isinstance(factory, ClassFactory)
        assert "Flask" in repr(factory)

    def test_blueprint_class_is_class_factory(self, فلاسك_موديل):
        """فلاسك.مخطط returns a ClassFactory for Blueprint."""
        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(فلاسك_موديل.مخطط, ClassFactory)

    def test_jsonify_alias(self, فلاسك_موديل, تطبيق):
        """حول_json maps to flask.jsonify and returns a JSON response."""
        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.app_context():
            resp = فلاسك_موديل.حول_json({"مفتاح": "قيمه"})
            assert resp.is_json

    def test_redirect_alias(self, فلاسك_موديل, تطبيق):
        """حول maps to flask.redirect."""
        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.app_context():
            resp = فلاسك_موديل.حول("/هدف")
            assert resp.status_code == 302

    def test_request_local_proxy(self, فلاسك_موديل):
        """طلب maps to flask.request (the LocalProxy)."""
        assert فلاسك_موديل.طلب is flask.request

    def test_session_local_proxy(self, فلاسك_موديل):
        """جلسه maps to flask.session (the LocalProxy)."""
        assert فلاسك_موديل.جلسه is flask.session

    def test_url_for_alias(self, فلاسك_موديل):
        """رابط_ل maps to flask.url_for."""
        assert فلاسك_موديل.رابط_ل is flask.url_for


# ---------------------------------------------------------------------------
# InstanceProxy tests
# ---------------------------------------------------------------------------


class TestInstanceProxy:
    def test_instance_is_instance_proxy(self, تطبيق):
        """فلاسك.فلاسك(__name__) returns an InstanceProxy."""
        from arabicpython.aliases._proxy import InstanceProxy

        assert isinstance(تطبيق, InstanceProxy)

    def test_instance_proxy_repr(self, تطبيق):
        """InstanceProxy repr identifies the wrapped class."""
        assert "Flask" in repr(تطبيق)
        assert "arabic-instance-proxy" in repr(تطبيق)

    def test_route_decorator_registers_route(self, تطبيق):
        """@تطبيق.طريق('/') registers a route on the underlying Flask app."""

        @تطبيق.طريق("/مرحبا")
        def مرحبا():
            return "مرحبا!"

        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.test_client() as عميل:
            resp = عميل.get("/مرحبا")
            assert resp.status_code == 200
            assert "مرحبا" in resp.data.decode("utf-8")

    def test_get_decorator(self, تطبيق):
        """@تطبيق.احصل maps to app.get (GET-only shorthand decorator)."""

        @تطبيق.احصل("/ping")
        def ping():
            return "pong"

        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.test_client() as client:
            assert client.get("/ping").status_code == 200
            assert client.post("/ping").status_code == 405  # Method Not Allowed

    def test_post_decorator(self, تطبيق):
        """@تطبيق.انشر maps to app.post (POST-only shorthand decorator)."""

        @تطبيق.انشر("/data")
        def receive_data():
            return "ok"

        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.test_client() as client:
            assert client.post("/data").status_code == 200

    def test_test_client_arabic(self, تطبيق):
        """عميل_تجريبي maps to app.test_client()."""

        @تطبيق.طريق("/tc")
        def tc():
            return "tc"

        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        client = تطبيق.عميل_تجريبي()
        with flask_app.test_client() as std_client:
            assert std_client.get("/tc").status_code == 200

    def test_errorhandler_decorator(self, تطبيق):
        """@تطبيق.معالج_الخطا(404) registers a custom 404 handler."""

        @تطبيق.معالج_الخطا(404)
        def not_found(e):
            return "غير موجود", 404

        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        with flask_app.test_client() as client:
            resp = client.get("/no_such_route_xyz")
            assert resp.status_code == 404
            assert "غير موجود" in resp.data.decode("utf-8")

    def test_english_passthrough_on_instance(self, تطبيق):
        """English attribute names on the InstanceProxy pass through to Flask app."""
        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        # .config is an English attribute — passes through
        assert تطبيق.config is flask_app.config

    def test_run_method_resolves(self, تطبيق):
        """يعمل resolves to the Flask app's run method (not called, just resolved)."""
        import flask as _flask

        run_method = تطبيق.يعمل
        assert callable(run_method)
        # Confirm it's the bound method on the real app
        flask_app = object.__getattribute__(تطبيق, "_wrapped")
        assert run_method == flask_app.run
