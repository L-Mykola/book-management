from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from app.settings.settings import settings


def get_engine():
    db_url = f"postgresql://{settings.PG_USER}:{settings.PG_PASSWORD}@{settings.PG_HOST}/{settings.PG_DB}"
    if not database_exists(db_url):
        create_database(db_url)
    return create_engine(db_url, echo=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



