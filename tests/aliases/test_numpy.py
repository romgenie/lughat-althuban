# tests/aliases/test_numpy.py
# B-016 stdlib aliases — numpy module tests

import pathlib

import numpy as np
import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نمباي():
    """Return a ModuleProxy wrapping `numpy`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نمباي", None, None)
    assert spec is not None, "AliasFinder did not find 'نمباي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestNumpyCreation:
    def test_array_alias(self, نمباي):
        assert نمباي.مصفوفه is np.array

    def test_zeros_alias(self, نمباي):
        assert نمباي.اصفار is np.zeros

    def test_ones_alias(self, نمباي):
        assert نمباي.وحدات is np.ones

    def test_empty_alias(self, نمباي):
        assert نمباي.فارغه is np.empty

    def test_full_alias(self, نمباي):
        assert نمباي.ممتلئه is np.full

    def test_arange_alias(self, نمباي):
        assert نمباي.مدي is np.arange  # stored as مدي (مدى normalizes: final ى→ي)

    def test_linspace_alias(self, نمباي):
        assert نمباي.فضاء_خطي is np.linspace

    def test_logspace_alias(self, نمباي):
        assert نمباي.فضاء_لوغاريتمي is np.logspace

    def test_eye_alias(self, نمباي):
        assert نمباي.عين is np.eye

    def test_identity_alias(self, نمباي):
        assert نمباي.هويه is np.identity

    def test_zeros_like_alias(self, نمباي):
        assert نمباي.اصفار_مثله is np.zeros_like

    def test_ones_like_alias(self, نمباي):
        assert نمباي.وحدات_مثله is np.ones_like

    def test_empty_like_alias(self, نمباي):
        assert نمباي.فارغه_مثله is np.empty_like

    def test_full_like_alias(self, نمباي):
        assert نمباي.ممتلئه_مثله is np.full_like

    def test_meshgrid_alias(self, نمباي):
        assert نمباي.شبكه is np.meshgrid

    def test_newaxis_alias(self, نمباي):
        assert نمباي.محور_جديد is np.newaxis


class TestNumpyManipulation:
    def test_reshape_alias(self, نمباي):
        assert نمباي.اعد_شكل is np.reshape

    def test_ravel_alias(self, نمباي):
        assert نمباي.بسط is np.ravel

    def test_squeeze_alias(self, نمباي):
        assert نمباي.ضيق is np.squeeze

    def test_expand_dims_alias(self, نمباي):
        assert نمباي.وسع_ابعاد is np.expand_dims

    def test_concatenate_alias(self, نمباي):
        assert نمباي.الصق is np.concatenate

    def test_stack_alias(self, نمباي):
        assert نمباي.كدس is np.stack

    def test_hstack_alias(self, نمباي):
        assert نمباي.كدس_افقي is np.hstack

    def test_vstack_alias(self, نمباي):
        assert نمباي.كدس_راسي is np.vstack

    def test_dstack_alias(self, نمباي):
        assert نمباي.كدس_عمقي is np.dstack

    def test_split_alias(self, نمباي):
        assert نمباي.قسم_صفيف is np.split

    def test_hsplit_alias(self, نمباي):
        assert نمباي.قسم_افقي is np.hsplit

    def test_vsplit_alias(self, نمباي):
        assert نمباي.قسم_راسي is np.vsplit

    def test_transpose_alias(self, نمباي):
        assert نمباي.منقوله is np.transpose

    def test_swapaxes_alias(self, نمباي):
        assert نمباي.ادل_محاور is np.swapaxes

    def test_moveaxis_alias(self, نمباي):
        assert نمباي.حرك_محور is np.moveaxis

    def test_tile_alias(self, نمباي):
        assert نمباي.بلط is np.tile

    def test_repeat_alias(self, نمباي):
        assert نمباي.كرر_عناصر is np.repeat

    def test_flip_alias(self, نمباي):
        assert نمباي.اقلب is np.flip

    def test_roll_alias(self, نمباي):
        assert نمباي.دحرج is np.roll


class TestNumpyMath:
    def test_sum_alias(self, نمباي):
        assert نمباي.مجموع is np.sum

    def test_prod_alias(self, نمباي):
        assert نمباي.حاصل_ضرب is np.prod

    def test_cumsum_alias(self, نمباي):
        assert نمباي.مجموع_تراكمي is np.cumsum

    def test_cumprod_alias(self, نمباي):
        assert نمباي.ضرب_تراكمي is np.cumprod

    def test_diff_alias(self, نمباي):
        assert نمباي.فرق is np.diff

    def test_absolute_alias(self, نمباي):
        assert نمباي.قيمه_مطلقه is np.absolute

    def test_sign_alias(self, نمباي):
        assert نمباي.اشاره is np.sign

    def test_clip_alias(self, نمباي):
        assert نمباي.حدد_نطاق is np.clip

    def test_sqrt_alias(self, نمباي):
        assert نمباي.جذر_تربيعي is np.sqrt

    def test_square_alias(self, نمباي):
        assert نمباي.مربع is np.square

    def test_power_alias(self, نمباي):
        assert نمباي.رفع_للقوه is np.power

    def test_exp_alias(self, نمباي):
        assert نمباي.اسيه_صفيف is np.exp

    def test_log_alias(self, نمباي):
        assert نمباي.لوغاريتم_صفيف is np.log

    def test_dot_alias(self, نمباي):
        assert نمباي.ضرب_نقطي is np.dot

    def test_matmul_alias(self, نمباي):
        assert نمباي.ضرب_مصفوفات is np.matmul

    def test_cross_alias(self, نمباي):
        assert نمباي.ضرب_اتجاهي is np.cross

    def test_inner_alias(self, نمباي):
        assert نمباي.ضرب_داخلي is np.inner

    def test_outer_alias(self, نمباي):
        assert نمباي.ضرب_خارجي is np.outer

    def test_linalg_alias(self, نمباي):
        assert نمباي.جبر_خطي is np.linalg


class TestNumpyStats:
    def test_mean_alias(self, نمباي):
        assert نمباي.متوسط is np.mean

    def test_median_alias(self, نمباي):
        assert نمباي.وسيط_صفيف is np.median

    def test_std_alias(self, نمباي):
        assert نمباي.انحراف_معياري is np.std

    def test_var_alias(self, نمباي):
        assert نمباي.تشتت is np.var

    def test_min_alias(self, نمباي):
        assert نمباي.ادني_قيمه is np.min

    def test_max_alias(self, نمباي):
        assert نمباي.اعلي_قيمه is np.max

    def test_percentile_alias(self, نمباي):
        assert نمباي.مئيني is np.percentile

    def test_quantile_alias(self, نمباي):
        assert نمباي.كميل is np.quantile

    def test_corrcoef_alias(self, نمباي):
        assert نمباي.معامل_ارتباط is np.corrcoef

    def test_histogram_alias(self, نمباي):
        assert نمباي.مدرج_تكراري is np.histogram

    def test_unique_alias(self, نمباي):
        assert نمباي.فريد is np.unique

    def test_sort_alias(self, نمباي):
        assert نمباي.رتب_صفيف is np.sort

    def test_argsort_alias(self, نمباي):
        assert نمباي.فهارس_ترتيب is np.argsort

    def test_argmin_alias(self, نمباي):
        assert نمباي.موضع_ادني is np.argmin

    def test_argmax_alias(self, نمباي):
        assert نمباي.موضع_اعلي is np.argmax

    def test_where_alias(self, نمباي):
        assert نمباي.حيث is np.where

    def test_nonzero_alias(self, نمباي):
        assert نمباي.غير_صفري is np.nonzero

    def test_count_nonzero_alias(self, نمباي):
        assert نمباي.عد_غير_صفري is np.count_nonzero

    def test_searchsorted_alias(self, نمباي):
        assert نمباي.فهرس_ادراج is np.searchsorted


class TestNumpyLogic:
    def test_all_alias(self, نمباي):
        assert نمباي.الكل_صحيح is np.all

    def test_any_alias(self, نمباي):
        assert نمباي.اي_صحيح is np.any

    def test_isnan_alias(self, نمباي):
        assert نمباي.هل_ناقص is np.isnan

    def test_isinf_alias(self, نمباي):
        assert نمباي.هل_لانهائي is np.isinf

    def test_isfinite_alias(self, نمباي):
        assert نمباي.هل_منتهي is np.isfinite

    def test_logical_and_alias(self, نمباي):
        assert نمباي.و_منطقي is np.logical_and

    def test_logical_or_alias(self, نمباي):
        assert نمباي.او_منطقي is np.logical_or

    def test_logical_not_alias(self, نمباي):
        assert نمباي.لا_منطقي is np.logical_not

    def test_logical_xor_alias(self, نمباي):
        assert نمباي.خلافي_منطقي is np.logical_xor


class TestNumpyTypes:
    def test_ndarray_alias(self, نمباي):
        assert نمباي.صفيف_ن is np.ndarray

    def test_dtype_alias(self, نمباي):
        assert نمباي.نوع_بيانات is np.dtype

    def test_nan_alias(self, نمباي):
        import math
        assert math.isnan(نمباي.ناقص)

    def test_inf_alias(self, نمباي):
        import math
        assert math.isinf(نمباي.ما_لانهايه)

    def test_random_submodule_alias(self, نمباي):
        assert نمباي.عشوائيات_صفيف is np.random


class TestNumpyIO:
    def test_save_alias(self, نمباي):
        assert نمباي.احفظ_صفيف is np.save

    def test_load_alias(self, نمباي):
        assert نمباي.احمل_صفيف is np.load

    def test_savetxt_alias(self, نمباي):
        assert نمباي.احفظ_نصي is np.savetxt

    def test_loadtxt_alias(self, نمباي):
        assert نمباي.احمل_نصي is np.loadtxt

    def test_genfromtxt_alias(self, نمباي):
        assert نمباي.من_نص_صفيف is np.genfromtxt


class TestNumpyFunctional:
    """End-to-end tests that actually compute with the aliased functions."""

    def test_array_creation_and_sum(self, نمباي):
        a = نمباي.مصفوفه([1, 2, 3, 4, 5])
        assert نمباي.مجموع(a) == 15

    def test_zeros_shape(self, نمباي):
        a = نمباي.اصفار((3, 4))
        assert a.shape == (3, 4)
        assert نمباي.الكل_صحيح(a == 0)

    def test_ones_shape(self, نمباي):
        a = نمباي.وحدات((2, 3))
        assert a.shape == (2, 3)
        assert نمباي.الكل_صحيح(a == 1)

    def test_arange_values(self, نمباي):
        a = نمباي.مدي(0, 10, 2)
        assert list(a) == [0, 2, 4, 6, 8]

    def test_linspace_length(self, نمباي):
        a = نمباي.فضاء_خطي(0, 1, 11)
        assert len(a) == 11
        assert abs(a[0] - 0.0) < 1e-10
        assert abs(a[-1] - 1.0) < 1e-10

    def test_reshape(self, نمباي):
        a = نمباي.مدي(12)
        b = نمباي.اعد_شكل(a, (3, 4))
        assert b.shape == (3, 4)

    def test_concatenate(self, نمباي):
        a = نمباي.مصفوفه([1, 2])
        b = نمباي.مصفوفه([3, 4])
        c = نمباي.الصق([a, b])
        assert list(c) == [1, 2, 3, 4]

    def test_mean(self, نمباي):
        a = نمباي.مصفوفه([1.0, 2.0, 3.0, 4.0])
        assert abs(نمباي.متوسط(a) - 2.5) < 1e-10

    def test_std(self, نمباي):
        a = نمباي.مصفوفه([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        assert abs(نمباي.انحراف_معياري(a) - 2.0) < 1e-10

    def test_where(self, نمباي):
        a = نمباي.مصفوفه([1, -2, 3, -4, 5])
        pos = نمباي.حيث(a > 0, a, 0)
        assert list(pos) == [1, 0, 3, 0, 5]

    def test_sqrt(self, نمباي):
        a = نمباي.مصفوفه([0.0, 1.0, 4.0, 9.0, 16.0])
        result = نمباي.جذر_تربيعي(a)
        assert list(result) == [0.0, 1.0, 2.0, 3.0, 4.0]

    def test_clip(self, نمباي):
        a = نمباي.مصفوفه([0, 1, 2, 3, 4, 5])
        clipped = نمباي.حدد_نطاق(a, 1, 4)
        assert list(clipped) == [1, 1, 2, 3, 4, 4]

    def test_unique(self, نمباي):
        a = نمباي.مصفوفه([3, 1, 2, 1, 3, 3])
        u = نمباي.فريد(a)
        assert list(u) == [1, 2, 3]

    def test_dot(self, نمباي):
        a = نمباي.مصفوفه([1, 2, 3])
        b = نمباي.مصفوفه([4, 5, 6])
        assert نمباي.ضرب_نقطي(a, b) == 32

    def test_matmul(self, نمباي):
        A = نمباي.مصفوفه([[1, 2], [3, 4]])
        B = نمباي.مصفوفه([[5, 6], [7, 8]])
        C = نمباي.ضرب_مصفوفات(A, B)
        assert C.shape == (2, 2)
        assert C[0, 0] == 19
        assert C[1, 1] == 50

    def test_eye_identity(self, نمباي):
        eye = نمباي.عين(3)
        assert eye.shape == (3, 3)
        assert نمباي.الكل_صحيح(نمباي.ضرب_مصفوفات(eye, eye) == eye)

    def test_isnan(self, نمباي):
        a = نمباي.مصفوفه([1.0, float('nan'), 3.0])
        mask = نمباي.هل_ناقص(a)
        assert list(mask) == [False, True, False]

    def test_argmax(self, نمباي):
        a = نمباي.مصفوفه([3, 1, 4, 1, 5, 9, 2, 6])
        assert نمباي.موضع_اعلي(a) == 5

    def test_sort(self, نمباي):
        a = نمباي.مصفوفه([3, 1, 4, 1, 5])
        s = نمباي.رتب_صفيف(a)
        assert list(s) == [1, 1, 3, 4, 5]

    def test_cumsum(self, نمباي):
        a = نمباي.مصفوفه([1, 2, 3, 4])
        cs = نمباي.مجموع_تراكمي(a)
        assert list(cs) == [1, 3, 6, 10]

    def test_ndarray_instance(self, نمباي):
        a = نمباي.مصفوفه([1, 2, 3])
        assert isinstance(a, نمباي.صفيف_ن)

    def test_save_load_roundtrip(self, نمباي, tmp_path):
        a = نمباي.مصفوفه([1.0, 2.0, 3.0])
        path = tmp_path / "arr.npy"
        نمباي.احفظ_صفيف(str(path), a)
        b = نمباي.احمل_صفيف(str(path))
        assert نمباي.الكل_صحيح(a == b)
