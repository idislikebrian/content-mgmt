import datetime
from utils.config import get_farcaster_client
from db.farcaster_db import add_cast_entry

client = get_farcaster_client()

def post_to_farcaster(text, world, window):
    try:
        response = client.post_cast(text=text)
        cast_hash = getattr(getattr(response, "cast", None), "hash", None)

        print(f"\n✅ Posted [{world}] → [{window}]")
        print(f"📝 {text}")
        print(f"⏰ {datetime.datetime.now().isoformat()}")
        print(f"🔗 Hash: {cast_hash}")

        # ✅ Save to DB (using your existing helper)
        add_cast_entry(cast_hash=cast_hash, text=text, world=world, window=window)

        if not cast_hash:
            print("⚠️  Warning: No hash returned — check the API response structure.")


    except Exception as e:
        print(f"❌ Failed to post: {e}")
