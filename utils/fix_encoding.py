import sqlite3
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT, "data", "master_casts.db")

def fix_mojibake(s):
    if s is None:
        return s
    try:
        return s.encode("latin1").decode("utf-8")
    except:
        return s  # leave unchanged if it fails

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

rows = cur.execute("SELECT id, text FROM casts").fetchall()

patched = 0
for cast_id, text in rows:
    fixed = fix_mojibake(text)
    if fixed != text:
        cur.execute("UPDATE casts SET text = ? WHERE id = ?", (fixed, cast_id))
        patched += 1

conn.commit()
conn.close()

print(f"✔ Fixed {patched} mojibake entries.")
