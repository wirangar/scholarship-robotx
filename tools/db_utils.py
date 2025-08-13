# -*- coding: utf-8 -*-
"""
Database utility script for creating tables.
"""
import sys
import os

# This is a bit of a hack to make sure we can import the project modules
# when running this script from the command line.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import engine, Base
from utils.models import User, RoommateProfile # Import all models here
from utils.logger import get_logger

logger = get_logger(__name__)

def create_all_tables():
    """
    Creates all tables in the database defined by the models imported above.
    """
    try:
        logger.info("Attempting to create all database tables...")
        # The Base metadata knows about all the classes that inherited from it.
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Successfully created all tables.")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        logger.error("Please ensure the DATABASE_URL is correct and the database server is running.")

if __name__ == "__main__":
    # This allows us to run `python tools/db_utils.py` from the root directory
    # to create the tables.
    create_all_tables()
