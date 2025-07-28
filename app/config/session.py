from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import SETTINGS

connect_args = {"check_same_thread": SETTINGS.db_multi_thread}
engine = create_engine(SETTINGS.db_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
