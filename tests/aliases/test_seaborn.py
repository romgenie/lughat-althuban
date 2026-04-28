# tests/aliases/test_seaborn.py
# B-057: Arabic aliases for seaborn

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

seaborn = pytest.importorskip("seaborn", reason="seaborn not installed")


@pytest.fixture(scope="module")
def رسوم_احصائيه():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("رسوم_احصائيه", None, None)
    assert spec is not None, "AliasFinder did not find 'رسوم_احصائيه'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestSeabornAliasesExist:
    def test_lineplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.خط_بياني is seaborn.lineplot

    def test_scatterplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.مخطط_نقاط is seaborn.scatterplot

    def test_histplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.توزيع_بيانات is seaborn.histplot

    def test_kdeplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.كثافه_احتماليه is seaborn.kdeplot

    def test_barplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.مخطط_شريطي is seaborn.barplot

    def test_boxplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.مخطط_صندوقي is seaborn.boxplot

    def test_heatmap(self, رسوم_احصائيه):
        assert رسوم_احصائيه.خريطه_حراره is seaborn.heatmap

    def test_pairplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.شبكه_زوجيه is seaborn.pairplot

    def test_set_theme(self, رسوم_احصائيه):
        assert رسوم_احصائيه.ضبط_موضوع is seaborn.set_theme

    def test_set_style(self, رسوم_احصائيه):
        assert رسوم_احصائيه.ضبط_نمط is seaborn.set_style

    def test_load_dataset(self, رسوم_احصائيه):
        assert رسوم_احصائيه.حمل_بيانات is seaborn.load_dataset

    def test_color_palette(self, رسوم_احصائيه):
        assert رسوم_احصائيه.احضر_لوحه is seaborn.color_palette

    def test_violinplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.مخطط_كمان is seaborn.violinplot

    def test_relplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.شبكه_علاقات is seaborn.relplot

    def test_jointplot(self, رسوم_احصائيه):
        assert رسوم_احصائيه.مخطط_مشترك is seaborn.jointplot


class TestSeabornTomlMeta:
    def test_toml_parseable(self):
        import tomllib
        p = ALIASES_DIR / "seaborn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "seaborn"
        assert data["meta"]["arabic_name"] == "رسوم_احصائيه"

    def test_entry_count(self):
        import tomllib
        p = ALIASES_DIR / "seaborn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 20
