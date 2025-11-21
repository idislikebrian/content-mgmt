import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
from dotenv import load_dotenv
from atproto import Client
from db.bluesky_db import get_connection, update_analytics

load_dotenv()

# Bluesky client
def get_bluesky_client():
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")

    if not handle or not password:
        raise ValueError("Missing BLUESKY_HANDLE or BLUESKY_PASSWORD")

    client = Client()
    client.login(handle, password)
    return client

client = get_bluesky_client()

# Fetch stats from a post URI
# -----------------------------
def fetch_post_stats(uri):
    print(f"🔎 Fetching: {uri}")

    try:
        res = client.get_posts(uris=[uri])
    except Exception as e:
        print(f"⚠️ API error for {uri}: {e}")
        return 0, 0, 0, 0

    if not res.posts:
        print(f"⚠️ No post returned for URI: {uri}")
        return 0, 0, 0, 0

    post = res.posts[0]

    # ★★ THE CORRECT FIELDS ★★
    likes = post.like_count or 0
    reposts = post.repost_count or 0
    replies = post.reply_count or 0
    quotes = post.quote_count or 0

    return likes, reposts, replies, quotes


# Main Analytics Routine
# -----------------------------
def gather_bluesky_analytics():
    print("📊 Gathering analytics for Bluesky posts...")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT post_uri, world, window FROM posts WHERE post_uri IS NOT NULL")
    rows = cur.fetchall()
    conn.close()

    print(f"🔎 Found {len(rows)} Bluesky posts.\n")

    for i, (post_uri, world, window) in enumerate(rows, start=1):
        print(f"({i}/{len(rows)}) → {world}/{window}")

        likes, reposts, replies, quotes = fetch_post_stats(post_uri)

        score = likes + 2 * reposts + 3 * replies + 4 * quotes

        update_analytics(
            post_uri=post_uri,
            likes=likes,
            reposts=reposts,
            replies=replies,
            quotes=quotes,
            score=score,
        )

    print("\n✅ Bluesky analytics updated.")

if __name__ == "__main__":
    gather_bluesky_analytics()
