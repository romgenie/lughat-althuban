# tests/aliases/test_pillow.py
# B-018: Arabic aliases for Pillow image processing — صور

import pathlib

import pytest

PIL = pytest.importorskip("PIL", reason="Pillow not installed — skipping")

from PIL import Image  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def صور():
    """Return a ModuleProxy wrapping `PIL.Image`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("صور", None, None)
    assert spec is not None, "AliasFinder did not find 'صور'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core functions ────────────────────────────────────────────────────────────


class TestCoreFunctions:
    def test_open_alias(self, صور):
        assert صور.افتح_صوره is Image.open

    def test_new_alias(self, صور):
        assert صور.جديد is Image.new

    def test_fromarray_alias(self, صور):
        assert صور.من_مصفوفه is Image.fromarray

    def test_frombytes_alias(self, صور):
        assert صور.من_بايتات is Image.frombytes

    def test_frombuffer_alias(self, صور):
        assert صور.من_مخزن is Image.frombuffer

    def test_merge_alias(self, صور):
        assert صور.ادمج_قنوات is Image.merge

    def test_blend_alias(self, صور):
        assert صور.امزج is Image.blend

    def test_composite_alias(self, صور):
        assert صور.مركب is Image.composite

    def test_alpha_composite_alias(self, صور):
        assert صور.مركب_شفافيه is Image.alpha_composite


# ── Image class ───────────────────────────────────────────────────────────────


class TestImageClass:
    def test_image_class_alias(self, صور):
        assert صور.فئه_الصوره is Image.Image

    def test_image_class_is_type(self, صور):
        assert isinstance(صور.فئه_الصوره, type)


# ── Resampling constants ──────────────────────────────────────────────────────


class TestResamplingConstants:
    def test_nearest_alias(self, صور):
        assert صور.اقرب == Image.NEAREST

    def test_lanczos_alias(self, صور):
        assert صور.لانكزوس == Image.LANCZOS

    def test_bilinear_alias(self, صور):
        assert صور.ثنائي_خطي == Image.BILINEAR

    def test_bicubic_alias(self, صور):
        assert صور.تكعيبي == Image.BICUBIC

    def test_box_alias(self, صور):
        assert صور.صندوقي == Image.BOX

    def test_hamming_alias(self, صور):
        assert صور.هامينغ == Image.HAMMING


# ── Transpose constants ───────────────────────────────────────────────────────


class TestTransposeConstants:
    def test_flip_left_right_alias(self, صور):
        assert صور.اقلب_افقيا == Image.FLIP_LEFT_RIGHT

    def test_flip_top_bottom_alias(self, صور):
        assert صور.اقلب_عموديا == Image.FLIP_TOP_BOTTOM

    def test_rotate_90_alias(self, صور):
        assert صور.دوران_90 == Image.ROTATE_90

    def test_rotate_180_alias(self, صور):
        assert صور.دوران_180 == Image.ROTATE_180

    def test_rotate_270_alias(self, صور):
        assert صور.دوران_270 == Image.ROTATE_270


# ── Exceptions ────────────────────────────────────────────────────────────────


class TestExceptions:
    def test_unidentified_image_error_alias(self, صور):
        assert صور.خطا_صوره_مجهوله is Image.UnidentifiedImageError

    def test_decompression_bomb_error_alias(self, صور):
        assert صور.خطا_ضغط_انفجاري is Image.DecompressionBombError

    def test_errors_are_exceptions(self, صور):
        assert issubclass(صور.خطا_صوره_مجهوله, Exception)
        assert issubclass(صور.خطا_ضغط_انفجاري, Exception)


# ── Functional ────────────────────────────────────────────────────────────────


class TestFunctional:
    def test_new_creates_image(self, صور):
        """جديد creates a blank PIL.Image.Image instance."""
        img = صور.جديد("RGB", (100, 100), color=(255, 0, 0))
        assert isinstance(img, صور.فئه_الصوره)
        assert img.size == (100, 100)
        assert img.mode == "RGB"

    def test_fromarray_roundtrip(self, صور):
        """من_مصفوفه converts a numpy-style list-of-lists to an Image."""
        pytest.importorskip("numpy")
        import numpy as np

        arr = np.zeros((50, 50, 3), dtype=np.uint8)
        arr[:, :, 0] = 128  # red channel
        img = صور.من_مصفوفه(arr)
        assert isinstance(img, صور.فئه_الصوره)
        assert img.size == (50, 50)

    def test_blend_produces_image(self, صور):
        """امزج blends two images with a given alpha."""
        a = صور.جديد("RGB", (10, 10), color=(0, 0, 0))
        b = صور.جديد("RGB", (10, 10), color=(255, 255, 255))
        blended = صور.امزج(a, b, alpha=0.5)
        assert isinstance(blended, صور.فئه_الصوره)
        px = blended.getpixel((0, 0))
        assert px == (127, 127, 127)

    def test_merge_rgb_channels(self, صور):
        """ادمج_قنوات merges three L-mode images into one RGB image."""
        r = صور.جديد("L", (4, 4), 200)
        g = صور.جديد("L", (4, 4), 100)
        b = صور.جديد("L", (4, 4), 50)
        rgb = صور.ادمج_قنوات("RGB", (r, g, b))
        assert rgb.mode == "RGB"
        assert rgb.getpixel((0, 0)) == (200, 100, 50)

    def test_resampling_constants_are_distinct(self, صور):
        """The six resampling constants all have distinct values."""
        values = {
            صور.اقرب,
            صور.لانكزوس,
            صور.ثنائي_خطي,
            صور.تكعيبي,
            صور.صندوقي,
            صور.هامينغ,
        }
        assert len(values) == 6

    def test_unidentified_image_error_raised(self, صور, tmp_path):
        """خطا_صوره_مجهوله is raised when opening a non-image file."""
        bad = tmp_path / "not_an_image.jpg"
        bad.write_bytes(b"this is not an image")
        with pytest.raises(صور.خطا_صوره_مجهوله):
            صور.افتح_صوره(str(bad))
