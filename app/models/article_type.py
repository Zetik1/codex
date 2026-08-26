from sqlalchemy import JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ArticleType(Base):
    __tablename__ = "article_types"

    __table_args__ = (
        UniqueConstraint("library_id", "slug", name="uq_article_type_library_slug"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    library_id: Mapped[int] = mapped_column(index=True)
    slug: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(100))
    fields_schema: Mapped[list[dict]] = mapped_column(JSON, default=list)