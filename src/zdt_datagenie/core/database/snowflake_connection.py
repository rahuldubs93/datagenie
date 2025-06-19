import os
import pandas as pd
from dotenv import load_dotenv
from timeit import default_timer as timer
from sqlalchemy import create_engine

from zdt_datagenie.core.utils.logger import get_logger

load_dotenv()

database_url = os.getenv("database_url")

engine = create_engine(database_url, pool_size=50, max_overflow=100)

logger = get_logger("snowflake_connection")


def execute_query(sql: str, intent: str = None):
    try:
        return _execute_query_internal(sql, intent)
    except Exception:
        global engine
        engine = create_engine(database_url, pool_size=50, max_overflow=100)
        return _execute_query_internal(sql, intent)


def _execute_query_internal(sql: str, intent: str):
    start = timer()
    with engine.connect() as conn:
        try:
            rows = conn.execute(sql)
            df_rows = pd.DataFrame(rows.all(), columns=rows.keys())
            return df_rows
        except Exception as e:
            logger.exception(f"Snowflake query failed: {str(e)}")
            raise
        finally:
            end = timer()
            query_name = "" if not intent else intent
            logger.critical(f"{query_name} Query took {(end - start)} secs to run.")
