import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

dsn = "sqlite:///test.db"

engine = create_engine(dsn, echo=True)

session = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass


# Создаем декларативное описание нашей таблицы
class Note(Base):
    __tablename__ = "notes"
    uuid = Column(String(36), primary_key=True, default=lambda : str(uuid.uuid4()))
    title = Column(String(64), unique=True, nullable=False)
    content = Column(Text(300), nullable=False)
    created_at = Column(DateTime, default=datetime.now())


def drop_tables():
    Base.metadata.drop_all(engine)


def create_tables():
    Base.metadata.create_all(engine)


def add_notes():
    with session as conn:
        conn.add(Note(title="title", content="conrent"))
        conn.commit()