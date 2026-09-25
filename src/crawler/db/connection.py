import sqlite3
from pathlib import Path

from .schema import ALL_DDL

DB_PATH = Path("data/jobs.db")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        for ddl in ALL_DDL:
            conn.executescript(ddl)
