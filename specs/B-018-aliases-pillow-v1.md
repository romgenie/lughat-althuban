# Spec Packet B-018: aliases-pillow-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: small
**Owner**: —

## Goal

Ship the Arabic alias mapping for `Pillow` (PIL fork) core surface: Image manipulation, filters, and drawing.

## Non-goals

- No support for obscure image formats or low-level CMS (Color Management System) aliases.

## Files

### Files to create

- `arabicpython/aliases/pillow.toml`
- `tests/test_aliases_pillow.py`
- `examples/B18_pillow_demo.apy`
- `examples/B18_README-ar.md`

## Public interfaces

### `arabicpython/aliases/pillow.toml`

[meta]
arabic_name = "بيلو"
python_module = "PIL"
dict_version = "ar-v1"
schema_version = 1

[entries]
# === Image Core ===
"صورة" = "Image"
"افتح_صورة" = "Image.open"
"صورة_جديدة" = "Image.new"
"من_مصفوفة" = "Image.fromarray"
"مزج" = "Image.blend"
"تركيب" = "Image.composite"

# === Filters ===
"مرشح_صورة" = "ImageFilter"
"تمويه" = "ImageFilter.BLUR"
"تحديد" = "ImageFilter.CONTOUR"
"تفصيل" = "ImageFilter.DETAIL"
"تحسين_الحواف" = "ImageFilter.EDGE_ENHANCE"
"نقش" = "ImageFilter.EMBOSS"
"شحذ" = "ImageFilter.SHARPEN"
"تنعيم" = "ImageFilter.SMOOTH"

# === Drawing ===
"رسم_صورة" = "ImageDraw"
"ارسم" = "ImageDraw.Draw"

# === Fonts ===
"خط_صورة" = "ImageFont"
"نوع_حقيقي" = "ImageFont.truetype"
"تحميل_افتراضي" = "ImageFont.load_default"

# === Ops ===
"عمليات_صورة" = "ImageOps"
"تدرج_رمادي" = "ImageOps.grayscale"
"عكس" = "ImageOps.invert"
"مرآة" = "ImageOps.mirror"
"قلب" = "ImageOps.flip"

# === Colors ===
"ألوان_صورة" = "ImageColor"
"احصل_على_rgb" = "ImageColor.getrgb"

# (Adding more to reach 25)
"تعديل_الحجم" = "Image.Resampling"
"وضع" = "Image.mode"
"تنسيق" = "Image.format"
"حجم" = "Image.size"
"بيانات_إكسيف" = "Image.getexif"

# Count: 25 entries.

### `examples/B18_pillow_demo.apy`

```python
من PIL استورد صورة, مرشح_صورة

# إنشاء صورة جديدة
صورة_جديدة = صورة.صورة_جديدة("RGB", (200, 200), "red")
صورة_جديدة.save("test.png")

# فتح وتعديل
مع صورة.افتح_صورة("test.png") ك ص:
    مموهة = ص.filter(مرشح_صورة.تمويه)
    مموهة.save("test_blur.png")
    اطبع(f"حجم الصورة: {ص.size}")
```

## Implementation constraints

- Cite B-010 as structural prior.
- Include "method-on-instance" limitation disclaimer.
- Acceptance checklist must include Phase A compat assertion.
- Ensure all Arabic names round-trip through `normalize_identifier`.

## Test requirements

- Verification of Image creation and file saving.
- Verification of filter application.
- Verification of drawing primitives (if mapped).
