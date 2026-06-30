"""
init_db.py — Initialises the SQLite database at Flask startup.

Behaviour:
  - First run  : creates the 'users' table and seeds it from the Excel file.
  - Subsequent : compares the Excel file's last-modified time against a
    'db_meta' bookkeeping table. If the Excel is newer the users table is
    dropped and reseeded automatically.
"""
import os
import pandas as pd
from sqlalchemy import inspect as sa_inspect, text

from app.database.db import engine, Base

EXCEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "documents",
        "databases",
        "users_table.xlsx",
    )
)

# Bookkeeping table DDL — stores the mtime of the Excel at last seed
_CREATE_META = """
CREATE TABLE IF NOT EXISTS db_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
"""
_META_KEY = "users_excel_mtime"


def _get_excel_mtime() -> str:
    """Return the Excel file's last-modified timestamp as a string."""
    return str(os.path.getmtime(EXCEL_PATH))


def _get_stored_mtime(conn) -> str | None:
    """Return the mtime recorded in db_meta, or None if not present."""
    row = conn.execute(
        text("SELECT value FROM db_meta WHERE key = :k"), {"k": _META_KEY}
    ).fetchone()
    return row[0] if row else None


def _set_stored_mtime(conn, mtime: str):
    conn.execute(
        text(
            "INSERT INTO db_meta (key, value) VALUES (:k, :v) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value"
        ),
        {"k": _META_KEY, "v": mtime},
    )
    conn.commit()


def _seed_users():
    """Drop (if exists), recreate, and populate the users table from Excel."""
    inspector = sa_inspect(engine)
    if inspector.has_table("users"):
        Base.metadata.tables["users"].drop(engine)

    Base.metadata.create_all(engine)

    df = pd.read_excel(EXCEL_PATH)
    df.to_sql("users", con=engine, if_exists="append", index=False)
    return len(df)


def init_db():
    """Seed or reseed the users table when the Excel file has changed."""
    excel_mtime = _get_excel_mtime()

    with engine.connect() as conn:
        # Ensure bookkeeping table exists
        conn.execute(text(_CREATE_META))
        conn.commit()

        stored_mtime = _get_stored_mtime(conn)

    needs_seed = (stored_mtime is None) or (stored_mtime != excel_mtime)

    if needs_seed:
        count = _seed_users()
        with engine.connect() as conn:
            conn.execute(text(_CREATE_META))
            _set_stored_mtime(conn, excel_mtime)
