"""
seed_db.py — Standalone script to sync the SQLite database from users_table.xlsx.
Run with:  python seed_db.py

Behaviour:
  - Always reseeds (drops + recreates) the users table from the Excel file.
  - Updates the mtime bookmark so Flask startup won't re-seed unnecessarily.
"""
import os
import sys
import io

# Force UTF-8 output on Windows (handles emoji in directory paths)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
from sqlalchemy import create_engine, Column, String, MetaData, inspect, text
from sqlalchemy.orm import declarative_base

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(BASE_DIR, "ticketing.db")
DB_URL     = f"sqlite:///{DB_PATH}"
EXCEL_PATH = os.path.join(BASE_DIR, "app", "documents", "databases", "users_table.xlsx")

engine   = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base     = declarative_base()
metadata = MetaData()

_CREATE_META = """
CREATE TABLE IF NOT EXISTS db_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
"""
_META_KEY = "users_excel_mtime"


class User(Base):
    __tablename__ = "users"
    user_id        = Column(String, primary_key=True)
    password       = Column(String, nullable=False)
    short_username = Column(String, unique=True, nullable=False)
    full_name      = Column(String, nullable=False)


if __name__ == "__main__":
    excel_mtime = str(os.path.getmtime(EXCEL_PATH))

    # 1. Load Excel
    df = pd.read_excel(EXCEL_PATH)
    print(f"Loaded {len(df)} rows from Excel file.")

    # 2. Drop + recreate users table for a clean slate
    insp = inspect(engine)
    if insp.has_table("users"):
        Base.metadata.tables["users"].drop(engine)
        print("Dropped existing 'users' table.")

    Base.metadata.create_all(engine)
    print("Created 'users' table schema.")

    # 3. Insert rows
    df.to_sql("users", con=engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} users.")

    # 4. Update mtime bookmark so Flask startup skips re-seed
    with engine.connect() as conn:
        conn.execute(text(_CREATE_META))
        conn.execute(
            text(
                "INSERT INTO db_meta (key, value) VALUES (:k, :v) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value"
            ),
            {"k": _META_KEY, "v": excel_mtime},
        )
        conn.commit()
    print("Updated Excel mtime bookmark in db_meta.")

    # 5. Verify
    result = pd.read_sql_query("SELECT * FROM users", con=engine)
    print(f"\nVerification: {len(result)} rows in database.")
    print(result.to_string(index=False))
    print("\nDatabase: ticketing.db")
