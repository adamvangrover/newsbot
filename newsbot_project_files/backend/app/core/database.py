import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = os.environ.get("POSTGRES_USER", "newsbot")
DATABASE_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "newsbot")
DATABASE_HOST = os.environ.get("POSTGRES_HOST", "db")
DATABASE_PORT = os.environ.get("POSTGRES_PORT", "5432")
DATABASE_NAME = os.environ.get("POSTGRES_DB", "newsbot")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
