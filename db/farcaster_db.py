import os
import sqlite3
import datetime

DB_PATH = "data/farcaster.db"


def get_connection():
    """Ensure data folder exists and return a SQLite connection."""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def _ensure_master_cast_id_column(cur):
    """Add master_cast_id column if missing (for DB migrations)."""
    cur.execute("PRAGMA table_info(casts)")
    cols = [row[1] for row in cur.fetchall()]
    if "master_cast_id" not in cols:
        cur.execute("ALTER TABLE casts ADD COLUMN master_cast_id INTEGER")

    # Add cid column for schema alignment with Bluesky
    if "cid" not in cols:
        cur.execute("ALTER TABLE casts ADD COLUMN cid TEXT")


def init_db():
    """Create tables if they don't exist and ensure schema is fully up to date."""
    conn = get_connection()
    cur = conn.cursor()

    # Main table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS casts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_cast_id INTEGER,
            timestamp TEXT,
            cast_hash TEXT,
            cid TEXT,
            text TEXT,
            world TEXT,
            window TEXT,
            posted INTEGER DEFAULT 1
        )
    """)

    # Migrate columns if needed
    _ensure_master_cast_id_column(cur)

    # Analytics table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            cast_hash TEXT PRIMARY KEY,
            likes INTEGER DEFAULT 0,
            recasts INTEGER DEFAULT 0,
            replies INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            last_updated TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_cast_entry(master_cast_id, cast_hash, text, world, window, cid=None):
    """Insert a newly posted Farcaster cast."""
    conn = get_connection()
    cur = conn.cursor()

    timestamp = datetime.datetime.now().isoformat()

    cur.execute("""
        INSERT INTO casts (master_cast_id, timestamp, cast_hash, cid, text, world, window, posted)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (
        master_cast_id,
        timestamp,
        cast_hash,
        cid,
        text,
        world,
        window
    ))

    conn.commit()
    conn.close()


def has_been_posted(master_cast_id, text):
    """
    True if this cast has already been posted on Farcaster.
    Matching by both:
      - master_cast_id (new system)
      - text (legacy support)
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM casts
        WHERE master_cast_id = ?
           OR text = ?
        LIMIT 1
    """, (master_cast_id, text))

    exists = cur.fetchone() is not None
    conn.close()
    return exists


def get_all_casts():
    """Return all Farcaster casts from newest → oldest."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM casts ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
