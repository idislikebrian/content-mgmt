import os
import json
import sqlite3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT, "data", "master_casts.db")
CASTS_JSON = os.path.join(ROOT, "data", "casts.json")

# -----------------------------
# Utility: connect + ensure table
# -----------------------------
def connect():
    conn = sqlite3.connect(DB_PATH)
    return conn

def ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS casts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            world TEXT,
            window TEXT,
            text TEXT NOT NULL,
            posted INTEGER DEFAULT 0
        );
    """)
    conn.commit()

# -----------------------------
# Check if a cast already exists
# -----------------------------
def cast_exists(conn, text):
    cur = conn.execute("SELECT id FROM casts WHERE text = ?", (text,))
    return cur.fetchone() is not None

# -----------------------------
# Import logic
# -----------------------------
def import_casts():
    # Load JSON
    with open(CASTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = connect()
    ensure_table(conn)

    inserted = 0
    skipped = 0

    for world, windows in data.items():
        for window, cast_list in windows.items():
            for text in cast_list:

                if cast_exists(conn, text):
                    skipped += 1
                    continue

                conn.execute(
                    """
                    INSERT INTO casts (world, window, text, posted)
                    VALUES (?, ?, ?, 0)
                    """,
                    (world, window, text)
                )
                inserted += 1

    conn.commit()
    conn.close()

    print(f"\n✔ Import complete!")
    print(f"   → Inserted: {inserted}")
    print(f"   → Skipped (duplicates): {skipped}")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    import_casts()
