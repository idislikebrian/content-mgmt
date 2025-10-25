import os
import sqlite3
import json
import datetime

DB_PATH = "data/farcaster.db"
OLD_JSON_PATH = "data/used_casts.json"  # adjust if file is in root

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Casts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS casts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        cast_hash TEXT,
        text TEXT,
        world TEXT,
        window TEXT,
        posted INTEGER DEFAULT 1
    )
    """)

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

def migrate_from_json():
    """Import used_casts.json into the database if it exists."""
    if not os.path.exists(OLD_JSON_PATH):
        print("ℹ️ No used_casts.json found — skipping migration.")
        return

    conn = get_connection()
    cur = conn.cursor()

    with open(OLD_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Corrupted used_casts.json — skipping migration.")
            return

    migrated = 0
    for entry in data:
        cur.execute("""
            INSERT OR IGNORE INTO casts (timestamp, cast_hash, text, world, window, posted)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (
            entry.get("timestamp"),
            entry.get("cast_hash"),
            entry.get("text"),
            entry.get("world"),
            entry.get("window"),
        ))
        migrated += 1

    conn.commit()
    conn.close()
    print(f"✅ Migrated {migrated} entries from used_casts.json → farcaster.db")

def add_cast_entry(cast_hash, text, world, window):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cur.execute("""
        INSERT INTO casts (timestamp, cast_hash, text, world, window, posted)
        VALUES (?, ?, ?, ?, ?, 1)
    """, (timestamp, cast_hash, text, world, window))
    conn.commit()
    conn.close()

def get_all_casts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM casts ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
