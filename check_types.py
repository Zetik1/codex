from sqlalchemy import select

from app.db import SessionLocal, init_db
from app import models  # noqa: F401
from app.models import ArticleType

init_db()

with SessionLocal() as session:
    race = ArticleType(
        library_id=1,
        slug="race",
        name="Раса",
        fields_schema=[
            {"key": "level", "label": "Уровень", "type": "select", "options": ["низшая", "высшая"]},
            {"key": "power", "label": "Сила", "type": "number"},
            {"key": "is_dead", "label": "Погибла", "type": "bool"},
        ],
    )
    session.add(race)
    session.commit()
    print("сохранено, id=", race.id)

with SessionLocal() as session:
    stmt = select(ArticleType).where(ArticleType.library_id == 1)
    for article_type in session.scalars(stmt):
        print(f"[{article_type.id}] {article_type.slug} - {article_type.name}")
        for field in article_type.fields_schema:
            print(f"    {field['key']:10} | {field['label']:10} | {field['type']}")