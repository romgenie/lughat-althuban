# Spec Packet B-013: aliases-sqlalchemy-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for SQLAlchemy (Core and ORM). Focus on both the traditional 1.x style and the modern 2.0 style.

## Non-goals

- No specialized database drivers mapping (asyncpg, etc.).
- No Alembic mapping (separate packet if needed).

## Files

### Files to create

- `arabicpython/aliases/sqlalchemy.toml`
- `tests/test_aliases_sqlalchemy.py`
- `examples/B13_sqlalchemy_demo.apy`
- `examples/B13_README-ar.md`

## Public interfaces

### `arabicpython/aliases/sqlalchemy.toml`

[meta]
arabic_name = "سا_ألكيمي"
python_module = "sqlalchemy"
dict_version = "ar-v1"
schema_version = 1

[entries]
# === Core ===
"جدول" = "Table"
"عمود" = "Column"
"نص" = "String"
"رقم_صحيح" = "Integer"
"رقم_عشري" = "Float"
"منطقي" = "Boolean"
"تاريخ" = "Date"
"وقت" = "DateTime"
"مفتاح_أجنبي" = "ForeignKey"
"بيانات_وصفية" = "MetaData"
"إنشاء_محرك" = "create_engine"
"نص_خام" = "text"
"وظائف" = "func"

# === SQL Expressions ===
"اختر" = "select"
"أدرج" = "insert"
"حدث" = "update"
"احذف" = "delete"
"و_" = "and_"
"أو_" = "or_"
"تنازلي" = "desc"
"تصاعدي" = "asc"
"ربط" = "join"
"ربط_خارجي" = "outerjoin"

# === ORM ===
"جلسة" = "orm.Session"
"صانع_جلسات" = "orm.sessionmaker"
"جلسة_نطاق" = "orm.scoped_session"
"قاعدة_تصريحية" = "orm.DeclarativeBase"
"عمود_مخطط" = "orm.mapped_column"
"مخطط" = "orm.Mapped"
"علاقة" = "orm.relationship"
"تحميل_متأخر" = "orm.lazyload"
"تحميل_فوري" = "orm.joinedload"
"تحميل_فرعي" = "orm.subqueryload"

# === Exceptions ===
"خطأ_قاعدة_بيانات" = "exc.DatabaseError"
"خطأ_تشغيلي" = "exc.OperationalError"
"خطأ_برمجي" = "exc.ProgrammingError"
"خطأ_سلامة" = "exc.IntegrityError"

# (Adding more to reach 50)
"محرك" = "engine.Engine"
"اتصال" = "engine.Connection"
"نتيجة" = "engine.Result"
"صف" = "engine.Row"
"قيمة" = "sql.expression.column"
"تسمية" = "sql.expression.label"
"تجميع_حسب" = "sql.expression.group_by"
"ترتيب_حسب" = "sql.expression.order_by"
"تصفية" = "sql.expression.filter"
"تصفية_حسب" = "sql.expression.filter_by"
"حد" = "sql.expression.limit"
"إزاحة" = "sql.expression.offset"

# Count: ~48. Final implementation must reach 50.

### `examples/B13_sqlalchemy_demo.apy`

```python
استورد سا_ألكيمي من sqlalchemy
من sqlalchemy.orm استورد قاعدة_تصريحية, عمود_مخطط, مخطط, صانع_جلسات

محرك = سا_ألكيمي.إنشاء_محرك("sqlite:///:memory:")
صانع = صانع_جلسات(bind=محرك)

صنف القاعدة(قاعدة_تصريحية):
    نصيحة

صنف مستخدم(القاعدة):
    __tablename__ = "users"
    معرف: مخطط[رقم_صحيح] = عمود_مخطط(primary_key=حقيقة)
    اسم: مخطط[نص] = عمود_مخطط()

القاعدة.metadata.create_all(محرك)

جلسة = صانع()
جديد = مستخدم(اسم="أحمد")
جلسة.add(جديد)
جلسة.commit()

مستخدم_موجود = جلسة.execute(سا_ألكيمي.اختر(مستخدم).filter_by(اسم="أحمد")).scalar_one()
اطبع(f"تم العثور على: {مستخدم_موجود.اسم}")
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Method-on-instance limitation:** Like B-010, this packet only maps module-level attributes. Methods on instances (e.g., `session.add`, `session.commit`) remain in English in this version.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Verification of Core table creation and SQL execution.
- Verification of ORM mapping (Declarative) and Session operations.
- Verification of 2.0 style `select` queries.

## Acceptance checklist

- [ ] `arabicpython/aliases/sqlalchemy.toml` shipped with at least 50 entries.
- [ ] All integration tests pass.
- [ ] `examples/B13_sqlalchemy_demo.apy` runs end-to-end.
- [ ] `examples/B13_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
