import pymysql
import os

# ---------------------------------------------------------------------------
# Connection configuration — override any of these via environment variables
# ---------------------------------------------------------------------------
DB_CONFIG = {
    "host":      os.environ.get("MYSQL_HOST",     "localhost"),
    "port":      int(os.environ.get("MYSQL_PORT", 3306)),
    "user":      os.environ.get("MYSQL_USER",     "root"),
    "password":  os.environ.get("MYSQL_PASSWORD", "root"),
    "charset":   "utf8mb4",
    "cursorclass": pymysql.cursors.Cursor,  # returns tuple rows
}

DB_NAME   = os.environ.get("MYSQL_DATABASE", "music_library")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    """Return a new PyMySQL connection to the music_library database."""
    return pymysql.connect(database=DB_NAME, **DB_CONFIG)


def create_tables():
    """
    Run schema.sql against MySQL.
    Connects without a database so CREATE DATABASE can execute first.
    Each non-empty statement in the file is executed separately.
    """
    # Read the schema file
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        raw_sql = f.read()

    # Split on semicolons, skip comments and blank lines
    statements = [
        stmt.strip()
        for stmt in raw_sql.split(";")
        if stmt.strip() and not stmt.strip().startswith("--")
    ]

    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cursor:
        for statement in statements:
            cursor.execute(statement)
    conn.commit()
    conn.close()
