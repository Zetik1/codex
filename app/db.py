#from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
#from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite:///codex.db",
    echo=True,
    connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine) 

def init_db():
    Base.metadata.create_all(bind=engine)