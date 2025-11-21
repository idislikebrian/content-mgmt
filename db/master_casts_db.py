import os
import sqlite3
import datetime

DB_PATH = "data/master_casts.db"


def get_connection():
    """Ensure data folder exists and return SQLite connection."""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the master_casts table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS master_casts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        world TEXT NOT NULL,
        window TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(world, window, text)
    )
    """)

    conn.commit()
    conn.close()


def insert_cast(world: str, window: str, text: str):
    """Insert a cast into the master table (ignores duplicates)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO master_casts (world, window, text, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (world, window, text, datetime.datetime.now().isoformat()),
    )

    conn.commit()
    conn.close()


def get_random_cast_for_window(window: str):
    """
    Return a random cast from master_casts for a given window.

    Returns:
        (id, world, window, text) or None
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, world, window, text
        FROM master_casts
        WHERE window = ?
        ORDER BY RANDOM()
        LIMIT 1
        """,
        (window,),
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return row  # (id, world, window, text)
    return None
