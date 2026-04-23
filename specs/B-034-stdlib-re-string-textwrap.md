# Spec Packet B-034: stdlib-re-string-textwrap

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for `re`, `string`, and `textwrap`. This packet provides tools for regular expression matching, advanced string templates, and text formatting (wrapping/indenting).

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/re.toml` — Floor: 15 entries.
- `arabicpython/aliases/string.toml` — Floor: 15 entries.
- `arabicpython/aliases/textwrap.toml` — Floor: 10 entries.
- `tests/aliases/test_re.py`
- `tests/aliases/test_string.py`
- `tests/aliases/test_textwrap.py`
- `tests/aliases/test_stdlib_B034_cross_consistency.py`
- `examples/B34_text_processing.apy` — Demo: Extract emails with regex, format as text block.
- `examples/B34_README-ar.md`

## Translation choices (must-include floor)

**`re.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `طابق` | `match` | |
| `ابحث` | `search` | |
| `استبدل` | `sub` | |
| `استبدل_عد` | `subn` | |
| `قسم` | `split` | |
| `ابحث_عن_الكل` | `findall` | |
| `كرر_البحث` | `finditer` | |
| `ترجم` | `compile` | |
| `هروب` | `escape` | |
| `تطابق_كامل` | `fullmatch` | |
| `نمط` | `Pattern` | |
| `تطابق` | `Match` | |
| `تجاهل_الحالة` | `IGNORECASE` | |
| `متعدد_الاسطر` | `MULTILINE` | |
| `نقطة_الكل` | `DOTALL` | |

**`string.toml` — floor 15:**

| Arabic | Python | Notes |
|---|---|---|
| `قالب` | `Template` | |
| `حروف_اسكي` | `ascii_letters` | |
| `حروف_صغيرة` | `ascii_lowercase` | |
| `حروف_كبيرة` | `ascii_uppercase` | |
| `ارقام` | `digits` | |
| `ارقام_ست_عشرية` | `hexdigits` | |
| `ارقام_ثمانية` | `octdigits` | |
| `علامات_ترقيم` | `punctuation` | |
| `قابل_للطباعة` | `printable` | |
| `مسافات` | `whitespace` | |
| `كبر_الكلمات` | `capwords` | |
| `نسق` | `Formatter` | |
| `استبدل` | `substitute` | Template.substitute |
| `استبدل_امن` | `safe_substitute` | Template.safe_substitute |
| `محدد` | `delimiter` | |

**`textwrap.toml` — floor 10:**

| Arabic | Python | Notes |
|---|---|---|
| `ملء` | `fill` | |
| `لف` | `wrap` | |
| `ازل_الازاحة` | `dedent` | |
| `ازح` | `indent` | |
| `قصر` | `shorten` | |
| `ملف_نصوص` | `TextWrapper` | |
| `عرض` | `width` | |
| `مسافة_بادئة_اولى` | `initial_indent` | |
| `مسافة_بادئة_لاحقة` | `subsequent_indent` | |
| `مكان_فارغ_واحد` | `expand_tabs` | |

## Test requirements

1. **Regex Matching**: Compile an Arabic regex pattern and use it to search in an Arabic string.
2. **Template Substitution**: Use `قالب` with Arabic keys and values.
3. **Dedent/Indent**: Verify that `ازل_الازاحة` correctly removes common leading whitespace.

## Acceptance checklist

- [ ] TOML files created (floor 40 total).
- [ ] Tests passing.
- [ ] Demo `B34_text_processing.apy` runs.
- [ ] No collisions with previous packets.
- [ ] Normalization round-trip verified.
