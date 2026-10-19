import os, psycopg
from contextlib import contextmanager
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 6543)),
    "dbname": os.getenv("POSTGRES_DB", "museum_db"),
    "user": os.getenv("POSTGRES_USER", "museum"),
    "password": os.getenv("POSTGRES_PASSWORD", "123456789")
}

@contextmanager
def get_connection():
    conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute(query: str, params: tuple = (), fetch: str | None = None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch == "one":
                return cur.fetchone()
            if fetch == "all":
                return cur.fetchall()
            return None
        