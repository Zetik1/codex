import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import ArticleType

RACE_FIELDS = [
    {"key": "level", "label": "Уровень", "type": "select", "options": ["низшая", "высшая"]},
    {"key": "power", "label": "Сила", "type": "number"},
    {"key": "is_dead", "label": "Погибла", "type": "bool"},
]


@pytest.fixture
def session_factory(tmp_path):
    engine = create_engine(f"sqlite:///{(tmp_path / 'test.db').as_posix()}")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)


def test_race_type_saved_and_read(session_factory):
    with session_factory() as session:
        session.add(
            ArticleType(
                library_id=1,
                slug="race",
                name="Раса",
                fields_schema=RACE_FIELDS,
            )
        )
        session.commit()

    with session_factory() as session:
        race = session.scalars(
            select(ArticleType).where(
                ArticleType.library_id == 1,
                ArticleType.slug == "race",
            )
        ).one()

        assert race.name == "Раса"
        assert [f["key"] for f in race.fields_schema] == ["level", "power", "is_dead"]
        assert [f["type"] for f in race.fields_schema] == ["select", "number", "bool"]
        assert race.fields_schema[0]["options"] == ["низшая", "высшая"]
        assert "options" not in race.fields_schema[1]


def test_same_slug_allowed_in_other_library(session_factory):
    with session_factory() as session:
        session.add_all([
            ArticleType(library_id=1, slug="race", name="Раса", fields_schema=RACE_FIELDS),
            ArticleType(library_id=2, slug="race", name="Раса", fields_schema=RACE_FIELDS),
        ])
        session.commit()

    with session_factory() as session:
        mine = session.scalars(
            select(ArticleType).where(ArticleType.library_id == 1)
        ).all()

        assert len(mine) == 1
        assert mine[0].library_id == 1