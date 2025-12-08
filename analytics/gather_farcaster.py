import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
from dotenv import load_dotenv
from farcaster import Warpcast

from db.farcaster_db import get_connection

load_dotenv()
MNEMONIC = os.getenv("FARCASTER")

if not MNEMONIC:
    raise ValueError("Missing FARCASTER mnemonic in .env")

client = Warpcast(mnemonic=MNEMONIC)

# Analytics Functions
# ---------------------
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
    """Warpcast does not expose replies; placeholder."""
    return 0


# Main Analytics Routine
# ---------------------
def gather_analytics():
    """Fetch metrics for all casts and update farcaster.db."""
    print("📊 Gathering analytics for all casts...")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT cast_hash, text, world, window
        FROM casts
        WHERE cast_hash IS NOT NULL
          AND master_cast_id IS NOT NULL
    """)
    rows = cur.fetchall()

    total = len(rows)
    print(f"🔎 Found {total} casts with valid hashes.")

    for i, (cast_hash, text, world, window) in enumerate(rows, start=1):
        print(f"({i}/{total}) → {world}/{window}")

        likes = get_cast_likes_count(cast_hash)
        recasts = get_cast_recasts_count(cast_hash)
        replies = get_replies_count(cast_hash)

        score = likes + (2 * recasts) + (3 * replies)
        now = datetime.datetime.now().isoformat()

        cur.execute("""
            INSERT INTO analytics (cast_hash, likes, recasts, replies, score, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(cast_hash)
            DO UPDATE SET
                likes = excluded.likes,
                recasts = excluded.recasts,
                replies = excluded.replies,
                score = excluded.score,
                last_updated = excluded.last_updated
        """, (cast_hash, likes, recasts, replies, score, now))

        conn.commit()

    conn.close()
    print("✅ Analytics refreshed successfully.")

# Manual Utilities
# ---------------------
def manual_lookup():
    """Interactive lookup for casts by hash, timestamp, or text fragment."""
    conn = get_connection()
    cur = conn.cursor()

    print("Lookup options:")
    print("1️⃣  Search by cast hash")
    print("2️⃣  Search by timestamp (YYYY-MM-DD or partial match)")
    print("3️⃣  Search by text fragment")
    choice = input("→ ")

    query = input("Enter your search term: ").strip()

    if choice == "1":
        cur.execute("""
            SELECT c.timestamp, c.text, c.world, c.window, a.likes, a.recasts, a.replies, a.score, a.last_updated
            FROM casts c
            LEFT JOIN analytics a ON c.cast_hash = a.cast_hash
            WHERE c.cast_hash LIKE ?
            ORDER BY c.timestamp DESC
        """, (f"%{query}%",))
    elif choice == "2":
        cur.execute("""
            SELECT c.timestamp, c.text, c.world, c.window, a.likes, a.recasts, a.replies, a.score, a.last_updated
            FROM casts c
            LEFT JOIN analytics a ON c.cast_hash = a.cast_hash
            WHERE c.timestamp LIKE ?
            ORDER BY c.timestamp DESC
        """, (f"%{query}%",))
    elif choice == "3":
        cur.execute("""
            SELECT c.timestamp, c.text, c.world, c.window, a.likes, a.recasts, a.replies, a.score, a.last_updated
            FROM casts c
            LEFT JOIN analytics a ON c.cast_hash = a.cast_hash
            WHERE c.text LIKE ?
            ORDER BY c.timestamp DESC
        """, (f"%{query}%",))
    else:
        print("❌ Invalid choice.")
        conn.close()
        return

    results = cur.fetchall()
    conn.close()

    if not results:
        print("⚠️ No results found.")
        return

    print(f"✅ Found {len(results)} result(s):\n")
    for r in results:
        ts, text, world, window, likes, recasts, replies, score, last_updated = r
        print(f"🕒 {ts}")
        print(f"🌍 {world}/{window}")
        print(f"📝 {text[:120]}{'...' if len(text) > 120 else ''}")
        print(f"❤️ {likes or 0} 🔁 {recasts or 0} 💬 {replies or 0} 📊 {score or 0}")
        print(f"⏱️  Last updated: {last_updated}\n")


def get_recent(days=7):
    """Retrieve all casts posted within the last N days."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.timestamp, c.text, c.world, c.window, a.likes, a.recasts, a.replies, a.score
        FROM casts c
        LEFT JOIN analytics a ON c.cast_hash = a.cast_hash
        WHERE c.timestamp >= datetime('now', ?)
        ORDER BY c.timestamp DESC
    """, (f'-{days} days',))
    rows = cur.fetchall()
    conn.close()

    print(f"🕓 Showing casts from the last {days} days:")
    for r in rows:
        ts, text, world, window, likes, recasts, replies, score = r
        print(f"[{ts}] {world}/{window} → ❤️ {likes} 🔁 {recasts} 💬 {replies} 📊 {score}")
    return rows

def show_missing_hashes():
    """List all casts missing a cast_hash."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, timestamp, text, world, window
        FROM casts
        WHERE cast_hash IS NULL OR cast_hash = ''
        ORDER BY timestamp DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("✅ No missing hashes — all casts are linked.")
        return

    print(f"⚠️ {len(rows)} casts missing hash values:\n")
    for r in rows:
        cast_id, ts, text, world, window = r
        print(f"🆔 {cast_id} | {world}/{window} | {ts}")
        print(f"   📝 {text[:100]}{'...' if len(text) > 100 else ''}\n")
    return rows


def update_cast_hash():
    """Manually assign a hash to a cast."""
    conn = get_connection()
    cur = conn.cursor()

    print("Manual Hash Update:")
    text_snippet = input("Enter a few words from the cast text: ").strip()

    # find possible matches
    cur.execute("""
        SELECT id, timestamp, text, world, window, cast_hash
        FROM casts
        WHERE text LIKE ?
        ORDER BY timestamp DESC
    """, (f"%{text_snippet}%",))
    matches = cur.fetchall()

    if not matches:
        print("⚠️ No matches found for that text.")
        conn.close()
        return

    print(f"Found {len(matches)} possible match(es):\n")
    for m in matches:
        cast_id, ts, text, world, window, cast_hash = m
        print(f"[{cast_id}] {world}/{window} @ {ts}")
        print(f"   📝 {text[:120]}{'...' if len(text) > 120 else ''}")
        print(f"   Current hash: {cast_hash or '(none)'}\n")

    cast_id = input("Enter ID of the cast to update: ").strip()
    new_hash = input("Enter new cast hash: ").strip()

    cur.execute("UPDATE casts SET cast_hash = ? WHERE id = ?", (new_hash, cast_id))
    conn.commit()
    conn.close()
    print(f"✅ Updated cast {cast_id} with hash {new_hash}")

def add_manual_cast():
    """
    Adds a manually posted cast into the local database.
    Since Warpcast no longer exposes an API to fetch cast content,
    the user must provide the cast text.
    """
    conn = get_connection()
    cur = conn.cursor()

    print("➕ Add a manually posted cast")
    print("Warpcast does NOT expose cast content via API anymore.")
    print("You'll need to paste the text manually.\n")

    cast_hash = input("Cast hash (from Warpcast URL): ").strip()

    if not cast_hash:
        print("❌ Cast hash is required.")
        return

    text = input("Cast text (copy/paste from Warpcast): ").strip()

    if not text:
        print("❌ Cast text is required (no API can fetch it).")
        return

    # auto-assign timestamp
    timestamp = datetime.datetime.now().isoformat()

    # For manual casts, we treat the cast as its own master
    master_cast_id = cast_hash

    # Leave world/window empty or let user fill them later
    world = None
    window = None

    try:
        cur.execute("""
            INSERT INTO casts (cast_hash, master_cast_id, text, world, window, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(cast_hash)
            DO UPDATE SET
                master_cast_id = excluded.master_cast_id,
                text = excluded.text,
                world = excluded.world,
                window = excluded.window,
                timestamp = excluded.timestamp
        """, (cast_hash, master_cast_id, text, world, window, timestamp))

        conn.commit()
        print("✅ Cast successfully added to the database.")

    except Exception as e:
        print(f"❌ Database error: {e}")

    finally:
        conn.close()

    print("\n--- Cast Summary ---")
    print(f"Hash: {cast_hash}")
    print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
    print(f"Timestamp: {timestamp}")
    print("---------------------\n")

# Entry Point
# ---------------------
if __name__ == "__main__":
    print("Select mode:")
    print("1️⃣  Gather analytics for all casts")
    print("2️⃣  Manual lookup (hash, time, or text)")
    print("3️⃣  Show recent casts")
    print("4️⃣  Show missing hashes")
    print("5️⃣  Manually update a hash")
    print("6️⃣  Add a manually posted cast")
    mode = input("→ ")

    if mode == "1":
        gather_analytics()
    elif mode == "2":
        manual_lookup()
    elif mode == "3":
        days = int(input("Days to look back: ").strip() or "7")
        get_recent(days)
    elif mode == "4":
        show_missing_hashes()
    elif mode == "5":
        update_cast_hash()
    elif mode == "6":
        add_manual_cast()
    else:
        print("❌ Invalid choice.")
