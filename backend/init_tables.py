import sys
import os
import logging

# Add the current directory to sys.path to ensure 'app' can be imported
# This assumes the script is run from the 'backend' directory
sys.path.append(os.getcwd())

from app.db.session import engine
from app.db.base_class import Base
# Import models so they are registered with Base.metadata
from app.models import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
