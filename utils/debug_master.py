import sqlite3, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB = os.path.join(ROOT, "data", "master_casts.db")

conn = sqlite3.connect(DB)
rows = conn.execute("SELECT id, world, window, text FROM casts ORDER BY id DESC LIMIT 20;").fetchall()

for r in rows:
    print(r)
