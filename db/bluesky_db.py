import os
import sqlite3
import datetime

DB_PATH = "data/bluesky.db"


def get_connection():
    """Ensure data folder exists and return a SQLite connection."""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create tables if they don't already exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Posts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        master_cast_id INTEGER,
        timestamp TEXT,
        post_uri TEXT,
        cid TEXT,
        text TEXT,
        world TEXT,
        window TEXT,
        posted INTEGER DEFAULT 1
    )
    """)

    # Analytics table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        post_uri TEXT PRIMARY KEY,
        likes INTEGER DEFAULT 0,
        reposts INTEGER DEFAULT 0,
        replies INTEGER DEFAULT 0,
        quotes INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        last_updated TEXT
    )
    """)

    conn.commit()
    conn.close()


def has_been_posted(master_cast_id, text):
    """
    True if this cast has already been posted on Bluesky.

    Uses master_cast_id (main) and text (just in case we ever
    have legacy or imported rows).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM posts
        WHERE master_cast_id = ?
           OR text = ?
        LIMIT 1
        """,
        (master_cast_id, text),
    )

    exists = cur.fetchone() is not None
    conn.close()
    return exists


def save_post(master_cast_id, post_uri, cid, text, world, window):
    """Record a newly posted Bluesky post."""
    conn = get_connection()
    cur = conn.cursor()

    timestamp = datetime.datetime.now().isoformat()

    cur.execute(
        """
        INSERT INTO posts (master_cast_id, timestamp, post_uri, cid, text, world, window)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (master_cast_id, timestamp, post_uri, cid, text, world, window),
    )

    conn.commit()
    conn.close()


def update_analytics(post_uri, likes, reposts, replies, quotes, score):
    """Upsert analytics for a post."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO analytics (post_uri, likes, reposts, replies, quotes, score, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(post_uri) DO UPDATE SET
            likes=excluded.likes,
            reposts=excluded.reposts,
            replies=excluded.replies,
            quotes=excluded.quotes,
            score=excluded.score,
            last_updated=excluded.last_updated
        """,
        (
            post_uri,
            likes,
            reposts,
            replies,
            quotes,
            score,
            datetime.datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def get_all_posts():
    """Return all Bluesky posts from newest → oldest."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()
    return rows
