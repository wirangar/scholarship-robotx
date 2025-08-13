# -*- coding: utf-8 -*-
"""
Database utility functions for connecting to PostgreSQL with SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    # Create the database engine
    engine = create_engine(DATABASE_URL)

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a Base class for our models to inherit from
    Base = declarative_base()

    logger.info("Successfully configured database connection.")

except ImportError as e:
    logger.error(f"SQLAlchemy or psycopg2 not installed? Error: {e}")
    engine = None
    SessionLocal = None
    Base = object # Fallback to a plain object if SQLAlchemy is not available
except Exception as e:
    logger.error(f"Failed to connect to the database: {e}")
    engine = None
    SessionLocal = None
    Base = object

def get_db():
    """
    Dependency to get a database session.
    This can be used with FastAPI's dependency injection.
    """
    if not SessionLocal:
        return None

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
