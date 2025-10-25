import os
import sqlite3
import datetime
import json

DB_PATH = "data/threads.db"
OLD_JSON_PATH = "data/used_threads.json"  # if you ever migrate old data

def get_connection():
    """Ensure data folder exists and return DB connection."""
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create Threads tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Main posts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS threads_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        post_id TEXT,
        text TEXT,
        world TEXT,
        window TEXT,
        posted INTEGER DEFAULT 1
    )
    """)

    # Engagement analytics table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS threads_analytics (
        post_id TEXT PRIMARY KEY,
        likes INTEGER DEFAULT 0,
        replies INTEGER DEFAULT 0,
        reposts INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        last_updated TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_post_entry(post_id, text, world, window, timestamp=None):
    """Insert a Threads post into the database."""
    conn = get_connection()
    cur = conn.cursor()
    if not timestamp:
        timestamp = datetime.datetime.now().isoformat()

    cur.execute("""
        INSERT INTO threads_posts (timestamp, post_id, text, world, window, posted)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (timestamp, post_id, text, world, window))

    conn.commit()
    conn.close()


def get_all_posts():
    """Fetch all threads posts (latest first)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM threads_posts ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def add_or_update_analytics(post_id, likes=0, replies=0, reposts=0, score=0):
    """Insert or update analytics entry for a given post."""
    conn = get_connection()
    cur = conn.cursor()
    last_updated = datetime.datetime.now().isoformat()

    cur.execute("""
        INSERT INTO threads_analytics (post_id, likes, replies, reposts, score, last_updated)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(post_id) DO UPDATE SET
            likes=excluded.likes,
            replies=excluded.replies,
            reposts=excluded.reposts,
            score=excluded.score,
            last_updated=excluded.last_updated
    """, (post_id, likes, replies, reposts, score, last_updated))

    conn.commit()
    conn.close()
