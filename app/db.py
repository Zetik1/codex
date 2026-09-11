#from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
#from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite:///codex.db",
    echo=False,
    connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine) 

def init_db() -> None:
    from app import models  # noqa: F401 - регистрация моделей в Base.metadata

    Base.metadata.create_all(bind=engine)