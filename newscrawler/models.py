from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Date, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"), echo = True)


def create_table(engine):
    Base.metadata.create_all(engine)


class Article(Base):
    __tablename__ = "article"

    id = Column('id', Text, primary_key=True)
    date = Column('date', Date)
    title = Column('title', Text)
    content = Column('content', Text)
    location = Column('location', Text)
    author = Column('author', Text)
    url = Column('url', Text)

