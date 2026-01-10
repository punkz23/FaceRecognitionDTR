import sys
import os
import logging

# Add the current directory to sys.path to ensure 'app' can be imported
sys.path.append(os.getcwd())

from app.db.session import engine
from app.db.base_class import Base
# Import models so they are registered with Base.metadata
from app.models.models import User, Department, Branch, Schedule, AttendanceLog, FaceEncoding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reinit_db():
    logger.info("Dropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped successfully!")
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error re-initializing database: {e}")
        raise

if __name__ == "__main__":
    reinit_db()
