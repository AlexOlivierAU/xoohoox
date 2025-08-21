import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# Configure logging
logger = logging.getLogger(__name__)

# Create database URL
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# Create database engine
try:
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        # SQLite configuration
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
    else:
        # PostgreSQL configuration
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300
        )
    logger.debug(f"Created database engine with URL: {SQLALCHEMY_DATABASE_URL}")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create session maker
try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.debug("Created database session maker")
except Exception as e:
    logger.error(f"Failed to create session maker: {str(e)}")
    raise

# Create declarative base
try:
    Base = declarative_base()
    logger.debug("Created declarative base")
except Exception as e:
    logger.error(f"Failed to create declarative base: {str(e)}")
    raise

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()