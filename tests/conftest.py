import os, psycopg, pytest
from psycopg.rows import dict_row

os.environ.setdefault("POSTGRES_TEST_DB", "museum_test_db")
os.environ["POSTGRES_DB"] = os.environ["POSTGRES_TEST_DB"]

TEST_DB = os.getenv("POSTGRES_TEST_DB", "museum_test_db")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = int(os.getenv("POSTGRES_PORT", 6543))
USER = os.getenv("POSTGRES_USER", "museum")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "123456789")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    admin_dsn = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname=postgres"
    with psycopg.connect(admin_dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS "{TEST_DB}" WITH (FORCE)')
            cur.execute(f'CREATE DATABASE "{TEST_DB}"')

    test_dsn = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={TEST_DB}"
    with psycopg.connect(test_dsn) as conn:
        with conn.cursor() as cur:
            with open("schema.sql", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()

    yield

    with psycopg.connect(admin_dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS "{TEST_DB}" WITH (FORCE)')

@pytest.fixture
def db_conn():
    dsn = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={TEST_DB}"
    conn = psycopg.connect(dsn, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()

@pytest.fixture(autouse=True)
def clean_tables():
    dsn = f"host={HOST} port={PORT} user={USER} password={PASSWORD} dbname={TEST_DB}"
    conn = psycopg.connect(dsn, autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE exhibits, authors, collections RESTART IDENTITY CASCADE")
    finally:
        conn.close()
    yield