import sqlite3
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT, "data", "master_casts.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Find bad rows
rows = cur.execute("""
    SELECT id, text FROM casts
    WHERE text LIKE '%â€™%' OR text LIKE '%â€œ%' OR text LIKE '%â€%' 
""").fetchall()

print("\nFound mojibake rows:")
for r in rows:
    print(r)

# Delete them
cur.execute("""
    DELETE FROM casts
    WHERE text LIKE '%â€™%' OR text LIKE '%â€œ%' OR text LIKE '%â€%'
""")

conn.commit()
conn.close()

print(f"\n✔ Deleted {len(rows)} mojibake entries.")
