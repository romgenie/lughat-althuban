# tests/aliases/test_sqlalchemy.py
# B-013 third-party aliases — sqlalchemy database toolkit tests
#
# All tests use an in-memory SQLite engine ("sqlite:///:memory:") so no on-disk
# state is created.  ORM tests build a tiny declarative model on the fly.

import pathlib

import pytest
import sqlalchemy as sa

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def قاعده_علائقيه():
    """Return a ModuleProxy wrapping `sqlalchemy`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("قاعده_علائقيه", None, None)
    assert spec is not None, "AliasFinder did not find 'قاعده_علائقيه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSqlaEngine:
    def test_create_engine_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.انشئ_محرك is sa.create_engine

    def test_text_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نص_خام is sa.text

    def test_url_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.رابط_url is sa.URL

    def test_make_url_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.احلل_url is sa.make_url

    def test_inspect_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.افحص_محرك is sa.inspect


class TestSqlaSession:
    def test_session_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import Session

        assert قاعده_علائقيه.جلسه_قاعده is Session

    def test_sessionmaker_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import sessionmaker

        assert قاعده_علائقيه.صانع_جلسات is sessionmaker

    def test_scoped_session_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import scoped_session

        assert قاعده_علائقيه.جلسه_موجهه is scoped_session


class TestSqlaOrmMapping:
    def test_declarative_base_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import DeclarativeBase

        assert قاعده_علائقيه.اساس_تعريفي is DeclarativeBase

    def test_mapped_column_class_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import MappedColumn

        assert قاعده_علائقيه.عمود_موجه is MappedColumn

    def test_mapped_column_factory_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import mapped_column

        assert قاعده_علائقيه.عرف_عمود is mapped_column

    def test_relationship_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import relationship

        assert قاعده_علائقيه.علاقه is relationship

    def test_backref_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import backref

        assert قاعده_علائقيه.علاقه_عكسيه is backref

    def test_mapped_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import Mapped

        assert قاعده_علائقيه.موجه is Mapped

    def test_registry_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import registry

        assert قاعده_علائقيه.سجل_تعيينات is registry


class TestSqlaTypes:
    def test_column_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.عمود is sa.Column

    def test_integer_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_عدد_صحيح is sa.Integer

    def test_string_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_نص is sa.String

    def test_float_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_عشري is sa.Float

    def test_boolean_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_منطقي is sa.Boolean

    def test_date_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_تاريخ is sa.Date

    def test_datetime_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_تاريخ_وقت is sa.DateTime

    def test_time_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_وقت is sa.Time

    def test_text_type_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نوع_نص_طويل is sa.Text

    def test_foreign_key_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.مفتاح_اجنبي is sa.ForeignKey

    def test_primary_key_constraint_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.قيد_مفتاح_رئيسي is sa.PrimaryKeyConstraint

    def test_unique_constraint_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.قيد_فريد is sa.UniqueConstraint

    def test_index_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.فهرس_جدول is sa.Index


class TestSqlaQuery:
    def test_select_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.اختر_من is sa.select

    def test_insert_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.ادخل_صف is sa.insert

    def test_update_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.حدث_صفوف is sa.update

    def test_delete_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.احذف_صفوف is sa.delete

    def test_and_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.اجتماع is sa.and_

    def test_or_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.افتراق is sa.or_

    def test_not_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نفي is sa.not_

    def test_func_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.داله_sql is sa.func

    def test_case_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.حاله_sql is sa.case

    def test_cast_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.حول_نوع is sa.cast

    def test_literal_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.قيمه_حرفيه_sql is sa.literal

    def test_label_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.وسم_عمود is sa.label


class TestSqlaOrmQueryHelpers:
    def test_query_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import Query

        assert قاعده_علائقيه.كائن_استعلام_orm is Query

    def test_joinedload_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import joinedload

        assert قاعده_علائقيه.تحميل_مدمج is joinedload

    def test_subqueryload_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import subqueryload

        assert قاعده_علائقيه.تحميل_فرعي is subqueryload

    def test_selectinload_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import selectinload

        assert قاعده_علائقيه.تحميل_بالاختيار is selectinload

    def test_contains_eager_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import contains_eager

        assert قاعده_علائقيه.يحوي_فورا is contains_eager

    def test_defer_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import defer

        assert قاعده_علائقيه.اجل_تحميل is defer

    def test_undefer_alias(self, قاعده_علائقيه):
        from sqlalchemy.orm import undefer

        assert قاعده_علائقيه.الغ_تاجيل is undefer


class TestSqlaResults:
    def test_row_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.صف_نتيجه is sa.Row

    def test_result_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نتيجه_استعلام is sa.Result

    def test_scalar_result_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نتيجه_عدديه is sa.ScalarResult

    def test_cursor_result_alias(self, قاعده_علائقيه):
        assert قاعده_علائقيه.نتيجه_مؤشر is sa.CursorResult


class TestSqlaExceptions:
    def test_sqlalchemy_error_alias(self, قاعده_علائقيه):
        from sqlalchemy.exc import SQLAlchemyError

        assert قاعده_علائقيه.خطا_sqlalchemy is SQLAlchemyError

    def test_integrity_error_alias(self, قاعده_علائقيه):
        from sqlalchemy.exc import IntegrityError

        assert قاعده_علائقيه.خطا_تكامل_orm is IntegrityError

    def test_operational_error_alias(self, قاعده_علائقيه):
        from sqlalchemy.exc import OperationalError

        assert قاعده_علائقيه.خطا_تشغيلي is OperationalError

    def test_no_result_found_alias(self, قاعده_علائقيه):
        from sqlalchemy.exc import NoResultFound

        assert قاعده_علائقيه.لا_نتيجه is NoResultFound

    def test_multiple_results_found_alias(self, قاعده_علائقيه):
        from sqlalchemy.exc import MultipleResultsFound

        assert قاعده_علائقيه.نتائج_متعدده is MultipleResultsFound


class TestSqlaFunctional:
    """End-to-end ORM smoke tests using the Arabic aliases.

    Builds a tiny ``users`` table on an in-memory SQLite engine and exercises
    insert / select / update / delete via the proxied API.
    """

    @pytest.fixture()
    def setup(self, قاعده_علائقيه):
        from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

        class Base(DeclarativeBase):
            pass

        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(قاعده_علائقيه.نوع_عدد_صحيح, primary_key=True)
            name: Mapped[str] = mapped_column(قاعده_علائقيه.نوع_نص(50), nullable=False)

        engine = قاعده_علائقيه.انشئ_محرك("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine, Base, User

    def test_create_engine_returns_engine(self, قاعده_علائقيه):
        eng = قاعده_علائقيه.انشئ_محرك("sqlite:///:memory:")
        assert eng.dialect.name == "sqlite"

    def test_insert_and_select(self, قاعده_علائقيه, setup):
        engine, Base, User = setup
        Session = قاعده_علائقيه.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="ali"))
            s.add(User(name="omar"))
            s.commit()
            stmt = قاعده_علائقيه.اختر_من(User).where(User.name == "ali")
            row = s.execute(stmt).scalar_one()
            assert row.name == "ali"

    def test_or_filter(self, قاعده_علائقيه, setup):
        engine, Base, User = setup
        Session = قاعده_علائقيه.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add_all([User(name="a"), User(name="b"), User(name="c")])
            s.commit()
            stmt = قاعده_علائقيه.اختر_من(User).where(
                قاعده_علائقيه.افتراق(User.name == "a", User.name == "c")
            )
            names = sorted(r.name for r in s.execute(stmt).scalars())
            assert names == ["a", "c"]

    def test_update_construct(self, قاعده_علائقيه, setup):
        engine, Base, User = setup
        Session = قاعده_علائقيه.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="x"))
            s.commit()
            stmt = قاعده_علائقيه.حدث_صفوف(User).where(User.name == "x").values(name="y")
            s.execute(stmt)
            s.commit()
            got = s.execute(قاعده_علائقيه.اختر_من(User)).scalar_one()
            assert got.name == "y"

    def test_delete_construct(self, قاعده_علائقيه, setup):
        engine, Base, User = setup
        Session = قاعده_علائقيه.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="z"))
            s.commit()
            stmt = قاعده_علائقيه.احذف_صفوف(User).where(User.name == "z")
            s.execute(stmt)
            s.commit()
            count = s.execute(
                قاعده_علائقيه.اختر_من(قاعده_علائقيه.داله_sql.count()).select_from(User)
            ).scalar()
            assert count == 0

    def test_text_construct(self, قاعده_علائقيه):
        eng = قاعده_علائقيه.انشئ_محرك("sqlite:///:memory:")
        with eng.connect() as conn:
            result = conn.execute(قاعده_علائقيه.نص_خام("SELECT 1"))
            assert result.scalar() == 1

    def test_no_result_found_raises(self, قاعده_علائقيه, setup):
        engine, Base, User = setup
        Session = قاعده_علائقيه.صانع_جلسات(bind=engine)
        with Session() as s:
            stmt = قاعده_علائقيه.اختر_من(User).where(User.id == 9999)
            with pytest.raises(قاعده_علائقيه.لا_نتيجه):
                s.execute(stmt).scalar_one()
