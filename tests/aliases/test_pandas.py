# tests/aliases/test_pandas.py
# B-017 stdlib aliases — pandas module tests

import pathlib

import pandas as pd
import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def بانداس():
    """Return a ModuleProxy wrapping `pandas`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("بانداس", None, None)
    assert spec is not None, "AliasFinder did not find 'بانداس'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestPandasStructures:
    def test_dataframe_alias(self, بانداس):
        assert بانداس.اطار_بيانات is pd.DataFrame

    def test_series_alias(self, بانداس):
        assert بانداس.سلسله_بيانات is pd.Series

    def test_index_alias(self, بانداس):
        assert بانداس.فهرس is pd.Index

    def test_multiindex_alias(self, بانداس):
        assert بانداس.فهرس_متعدد is pd.MultiIndex

    def test_rangeindex_alias(self, بانداس):
        assert بانداس.فهرس_نطاق is pd.RangeIndex

    def test_datetimeindex_alias(self, بانداس):
        assert بانداس.فهرس_تاريخ is pd.DatetimeIndex

    def test_categoricalindex_alias(self, بانداس):
        assert بانداس.فهرس_فئوي is pd.CategoricalIndex


class TestPandasReaders:
    def test_read_csv_alias(self, بانداس):
        assert بانداس.اقرا_csv is pd.read_csv

    def test_read_excel_alias(self, بانداس):
        assert بانداس.اقرا_اكسل is pd.read_excel

    def test_read_json_alias(self, بانداس):
        assert بانداس.اقرا_json is pd.read_json

    def test_read_sql_alias(self, بانداس):
        assert بانداس.اقرا_sql is pd.read_sql

    def test_read_parquet_alias(self, بانداس):
        assert بانداس.اقرا_parquet is pd.read_parquet

    def test_read_html_alias(self, بانداس):
        assert بانداس.اقرا_html is pd.read_html


class TestPandasCombination:
    def test_concat_alias(self, بانداس):
        assert بانداس.ادمج_بيانات is pd.concat

    def test_merge_alias(self, بانداس):
        assert بانداس.اندمج is pd.merge

    def test_crosstab_alias(self, بانداس):
        assert بانداس.جدول_تقاطع is pd.crosstab

    def test_pivot_table_alias(self, بانداس):
        assert بانداس.جدول_محوري is pd.pivot_table

    def test_get_dummies_alias(self, بانداس):
        assert بانداس.ترميز_وهمي is pd.get_dummies


class TestPandasDatetime:
    def test_to_datetime_alias(self, بانداس):
        assert بانداس.لتاريخ is pd.to_datetime

    def test_to_timedelta_alias(self, بانداس):
        assert بانداس.لفرق_زمني is pd.to_timedelta

    def test_to_numeric_alias(self, بانداس):
        assert بانداس.لرقمي is pd.to_numeric

    def test_date_range_alias(self, بانداس):
        assert بانداس.نطاق_تاريخ is pd.date_range

    def test_period_range_alias(self, بانداس):
        assert بانداس.نطاق_فتره is pd.period_range

    def test_timestamp_alias(self, بانداس):
        assert بانداس.طابع_زمني_باندا is pd.Timestamp

    def test_timedelta_alias(self, بانداس):
        assert بانداس.فرق_زمني_باندا is pd.Timedelta

    def test_period_alias(self, بانداس):
        assert بانداس.فتره is pd.Period


class TestPandasCategorical:
    def test_categorical_alias(self, بانداس):
        assert بانداس.فئوي is pd.Categorical

    def test_cut_alias(self, بانداس):
        assert بانداس.قطع is pd.cut

    def test_qcut_alias(self, بانداس):
        assert بانداس.قطع_متكافئ is pd.qcut


class TestPandasNA:
    def test_isna_alias(self, بانداس):
        assert بانداس.هل_مفقود is pd.isna

    def test_notna_alias(self, بانداس):
        assert بانداس.ليس_مفقودا is pd.notna

    def test_NA_alias(self, بانداس):
        assert بانداس.مفقود is pd.NA

    def test_NaT_alias(self, بانداس):
        assert بانداس.تاريخ_مفقود is pd.NaT


class TestPandasOptions:
    def test_set_option_alias(self, بانداس):
        assert بانداس.اضبط_خيار is pd.set_option

    def test_get_option_alias(self, بانداس):
        assert بانداس.احضر_خيار is pd.get_option

    def test_reset_option_alias(self, بانداس):
        assert بانداس.اعد_خيار is pd.reset_option


class TestPandasFunctional:
    """End-to-end tests that actually compute with the aliased functions."""

    def test_dataframe_creation(self, بانداس):
        df = بانداس.اطار_بيانات({"name": ["Alice", "Bob"], "age": [30, 25]})
        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_series_creation(self, بانداس):
        s = بانداس.سلسله_بيانات([10, 20, 30])
        assert len(s) == 3
        assert s.sum() == 60

    def test_concat_rows(self, بانداس):
        df1 = بانداس.اطار_بيانات({"x": [1, 2]})
        df2 = بانداس.اطار_بيانات({"x": [3, 4]})
        result = بانداس.ادمج_بيانات([df1, df2], ignore_index=True)
        assert len(result) == 4
        assert list(result["x"]) == [1, 2, 3, 4]

    def test_merge_inner_join(self, بانداس):
        left = بانداس.اطار_بيانات({"id": [1, 2, 3], "val": ["a", "b", "c"]})
        right = بانداس.اطار_بيانات({"id": [2, 3, 4], "score": [10, 20, 30]})
        merged = بانداس.اندمج(left, right, on="id")
        assert len(merged) == 2
        assert list(merged["id"]) == [2, 3]

    def test_to_datetime_parses_string(self, بانداس):
        dt = بانداس.لتاريخ("2024-01-15")
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15

    def test_date_range_length(self, بانداس):
        rng = بانداس.نطاق_تاريخ("2024-01-01", periods=7, freq="D")
        assert len(rng) == 7

    def test_isna_scalar(self, بانداس):
        assert بانداس.هل_مفقود(None) is True
        assert بانداس.هل_مفقود(pd.NA) is True
        assert بانداس.هل_مفقود(1) is False

    def test_notna_scalar(self, بانداس):
        assert بانداس.ليس_مفقودا("hello") is True
        assert بانداس.ليس_مفقودا(float("nan")) is False

    def test_to_numeric(self, بانداس):
        s = بانداس.سلسله_بيانات(["1", "2", "three", "4"])
        result = بانداس.لرقمي(s, errors="coerce")
        assert result[0] == 1.0
        assert pd.isna(result[2])

    def test_get_dummies(self, بانداس):
        s = بانداس.سلسله_بيانات(["cat", "dog", "cat", "bird"])
        dummies = بانداس.ترميز_وهمي(s)
        assert set(dummies.columns) == {"bird", "cat", "dog"}
        assert dummies.shape == (4, 3)

    def test_cut_bins(self, بانداس):
        s = بانداس.سلسله_بيانات([1, 7, 5, 2, 8])
        cats = بانداس.قطع(s, bins=[0, 3, 6, 10])
        assert hasattr(cats, "cat")  # it's a Categorical

    def test_pivot_table(self, بانداس):
        df = بانداس.اطار_بيانات(
            {"dept": ["A", "A", "B", "B"], "sales": [10, 20, 30, 40]}
        )
        pt = بانداس.جدول_محوري(df, values="sales", index="dept", aggfunc="sum")
        assert pt.loc["A", "sales"] == 30
        assert pt.loc["B", "sales"] == 70

    def test_crosstab(self, بانداس):
        a = بانداس.سلسله_بيانات(["foo", "foo", "bar"])
        b = بانداس.سلسله_بيانات(["one", "two", "one"])
        ct = بانداس.جدول_تقاطع(a, b)
        assert ct.loc["foo", "one"] == 1
        assert ct.loc["foo", "two"] == 1

    def test_timestamp(self, بانداس):
        ts = بانداس.طابع_زمني_باندا("2024-06-15 12:30:00")
        assert ts.year == 2024
        assert ts.hour == 12

    def test_categorical(self, بانداس):
        cat = بانداس.فئوي(["a", "b", "a", "c"], categories=["a", "b", "c"])
        assert len(cat) == 4
        assert "b" in cat.categories

    def test_nat_is_missing(self, بانداس):
        assert pd.isna(بانداس.تاريخ_مفقود)

    def test_index_creation(self, بانداس):
        idx = بانداس.فهرس(["x", "y", "z"])
        assert len(idx) == 3

    def test_range_index(self, بانداس):
        idx = بانداس.فهرس_نطاق(5)
        assert list(idx) == [0, 1, 2, 3, 4]
