import time
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def wait_for_data():
    conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn_str)
    
    while True:
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM countries"))
                count = result.scalar()
                
                if count and count > 0:
                    logger.info(f"Data ready in table 'countries', count={count}")
                    break
                else:
                    logger.info("Table 'countries' is empty, waiting...")
        except OperationalError as e:
            logger.warning(f"Database not ready yet: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        time.sleep(5)

if __name__ == "__main__":
    logger.info("Waiting for data to be ready in DB...")
    wait_for_data()