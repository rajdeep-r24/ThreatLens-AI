# Backward-compatibility alias for app.db.session
from app.db.session import engine, SessionLocal, Base, init_database
from app.api.deps import get_db

__all__ = ["engine", "SessionLocal", "Base", "init_database", "get_db"]
