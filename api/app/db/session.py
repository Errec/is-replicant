"""Session module to create a database session."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings

# Create the engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session (optional, useful in multithreaded environments)
SessionScoped = scoped_session(SessionLocal)

def get_db():
    """Dependency that provides a SQLAlchemy session."""
    db = SessionScoped()  # or SessionLocal() if scoped session is not used
    try:
        yield db
    finally:
        db.close()
