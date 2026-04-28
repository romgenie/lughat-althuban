# tests/aliases/test_scipy.py
# B-058: Arabic aliases for scipy

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

scipy = pytest.importorskip("scipy", reason="scipy not installed")


@pytest.fixture(scope="module")
def علوم_حسابيه():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("علوم_حسابيه", None, None)
    assert spec is not None, "AliasFinder did not find 'علوم_حسابيه'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestScipyAliasesExist:
    def test_stats_alias(self, علوم_حسابيه):
        import scipy.stats
        assert علوم_حسابيه.احصاء_متقدم is scipy.stats

    def test_optimize_alias(self, علوم_حسابيه):
        import scipy.optimize
        assert علوم_حسابيه.تحسين is scipy.optimize

    def test_integrate_alias(self, علوم_حسابيه):
        import scipy.integrate
        assert علوم_حسابيه.تكامل is scipy.integrate

    def test_linalg_alias(self, علوم_حسابيه):
        import scipy.linalg
        assert علوم_حسابيه.جبر_خطي_علمي is scipy.linalg

    def test_interpolate_alias(self, علوم_حسابيه):
        import scipy.interpolate
        assert علوم_حسابيه.استيفاء is scipy.interpolate

    def test_fft_alias(self, علوم_حسابيه):
        import scipy.fft
        assert علوم_حسابيه.تحويل_فوريه is scipy.fft

    def test_signal_alias(self, علوم_حسابيه):
        import scipy.signal
        assert علوم_حسابيه.معالجه_اشارات is scipy.signal

    def test_sparse_alias(self, علوم_حسابيه):
        import scipy.sparse
        assert علوم_حسابيه.مصفوفات_مبعثره is scipy.sparse

    def test_spatial_alias(self, علوم_حسابيه):
        import scipy.spatial
        assert علوم_حسابيه.هندسه_فضائيه is scipy.spatial

    def test_constants_alias(self, علوم_حسابيه):
        import scipy.constants
        assert علوم_حسابيه.ثوابت is scipy.constants

    def test_special_alias(self, علوم_حسابيه):
        import scipy.special
        assert علوم_حسابيه.دالات_خاصه is scipy.special


class TestScipyTomlMeta:
    def test_toml_parseable(self):
        import tomllib
        p = ALIASES_DIR / "scipy.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "scipy"
        assert data["meta"]["arabic_name"] == "علوم_حسابيه"

    def test_entry_count(self):
        import tomllib
        p = ALIASES_DIR / "scipy.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 10
