import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to local SQLite database for easy setup/testing, or use environment variable for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./threatlens.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to provide database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
