import sqlite3

def inspect(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print(f"\n=== Inspecting {db_path} ===\n")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()

    print("Tables:")
    for t in tables:
        print(" -", t[0])

    for t in tables:
        print(f"\n--- {t[0]} ---")
        cur.execute(f"PRAGMA table_info({t[0]})")
        for row in cur.fetchall():
            print(row)

        cur.execute(f"SELECT COUNT(*) FROM {t[0]}")
        print("Rows:", cur.fetchone()[0])

    conn.close()


inspect("data/farcaster.db")
inspect("data/bluesky.db")
inspect("data/master_casts.db")

