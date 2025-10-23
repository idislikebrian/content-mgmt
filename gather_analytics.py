import os
import json
import csv
from farcaster import Warpcast
from dotenv import load_dotenv

load_dotenv()

client = Warpcast(mnemonic=os.getenv("MNEMONIC_ENV_VAR"))

USED_LOG_PATH = "used_casts.json"
CSV_PATH = "cast_analytics.csv"

# ---------------------
# Helper Functions
# ---------------------
def load_used_casts():
    if not os.path.exists(USED_LOG_PATH):
        print("⚠️ No used_casts.json found.")
        return []
    with open(USED_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_cast_likes_count(cast_hash):
    try:
        likes = client.get_cast_likes(cast_hash).likes
        return len(likes)
    except Exception as e:
        print(f"⚠️ Error fetching likes for {cast_hash}: {e}")
        return 0

def get_cast_recasts_count(cast_hash):
    try:
        recasters = client.get_cast_recasters(cast_hash).users
        return len(recasters)
    except Exception as e:
        print(f"⚠️ Error fetching recasts for {cast_hash}: {e}")
        return 0

def get_replies_count(cast_hash):
    """Approximation: get reply count via search_casts or similar if supported."""
    try:
        # Not all Warpcast APIs expose replies directly.
        # Placeholder for future API support or manual query.
        return 0
    except Exception as e:
        print(f"⚠️ Error fetching replies for {cast_hash}: {e}")
        return 0

def load_existing_rows():
    if not os.path.exists(CSV_PATH):
        return {}
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["cast_hash"]: row for row in reader}

def save_to_csv(rows):
    fieldnames = [
        "timestamp",
        "cast_hash",
        "text",
        "world",
        "window",
        "likes",
        "recasts",
        "replies",
        "score"
    ]
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows.values():
            writer.writerow(r)

# ---------------------
# Main Analytics Routine
# ---------------------
def gather_analytics():
    print("📊 Gathering cast analytics...")

    used_casts = load_used_casts()
    if not used_casts:
        print("⚠️ No used casts found.")
        return

    existing_rows = load_existing_rows()
    updated_rows = existing_rows.copy()

    for entry in used_casts:
        cast_hash = entry.get("cast_hash")
        text = entry.get("text", "")
        timestamp = entry.get("timestamp", "")
        world = entry.get("world", "")
        window = entry.get("window", "")

        if not cast_hash:
            print(f"⚠️ Skipping entry with missing hash: {text[:40]}...")
            continue

        print(f"🔍 Fetching engagement for cast {cast_hash[:10]}...")

        likes = get_cast_likes_count(cast_hash)
        recasts = get_cast_recasts_count(cast_hash)
        replies = get_replies_count(cast_hash)
        score = likes + (2 * recasts) + (3 * replies)

        updated_rows[cast_hash] = {
            "timestamp": timestamp,
            "cast_hash": cast_hash,
            "text": text,
            "world": world,
            "window": window,
            "likes": likes,
            "recasts": recasts,
            "replies": replies,
            "score": score
        }

    save_to_csv(updated_rows)
    print(f"✅ Analytics updated for {len(updated_rows)} total casts.")
    print(f"📁 Saved to {CSV_PATH}")

# ---------------------
# Run Script
# ---------------------
if __name__ == "__main__":
    gather_analytics()
