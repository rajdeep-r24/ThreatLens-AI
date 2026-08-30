from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings
from app.models.user import Base

# Configure engine kwargs for SQLite if needed
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database() -> None:
    """Create all tables in the database if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator:
    """Database session generator."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
