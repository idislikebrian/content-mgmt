import os
import sys
import sqlite3
import pandas as pd
import json

# ---------------------------------------
# PATHS
# ---------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT, "data", "farcaster.db")
EXPORT_DIR = os.path.join(ROOT, "exports")

os.makedirs(EXPORT_DIR, exist_ok=True)

CSV_PATH = os.path.join(EXPORT_DIR, "casts_export.csv")
JSON_PATH = os.path.join(EXPORT_DIR, "casts_export.json")

# ---------------------------------------
# CONNECT
# ---------------------------------------
print("Connecting to database:", DB_PATH)
conn = sqlite3.connect(DB_PATH)

# ---------------------------------------
# QUERY: JOIN CASTS + ANALYTICS
# ---------------------------------------
query = """
SELECT
    c.id,
    c.timestamp,
    c.cast_hash,
    c.text,
    c.world,
    c.window,
    c.posted,
    c.master_cast_id,
    c.cid,
    a.likes,
    a.recasts,
    a.replies,
    a.score AS engagement_score,
    a.last_updated
FROM casts c
LEFT JOIN analytics a
    ON c.cast_hash = a.cast_hash
ORDER BY c.id ASC;
"""

df = pd.read_sql_query(query, conn)

# Fill missing analytics with zeros
df[["likes", "recasts", "replies", "engagement_score"]] = df[
    ["likes", "recasts", "replies", "engagement_score"]
].fillna(0).astype(int)

# ---------------------------------------
# SAVE CSV + JSON
# ---------------------------------------
df.to_csv(CSV_PATH, index=False)
df.to_json(JSON_PATH, orient="records", indent=2)

print("\nExport complete!")
print("CSV saved to:", CSV_PATH)
print("JSON saved to:", JSON_PATH)
print("\nPaste the JSON into ChatGPT for content analysis + new post generation.")
