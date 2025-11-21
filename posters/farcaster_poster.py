import os
import datetime
from dotenv import load_dotenv
from farcaster import Warpcast

from db.farcaster_db import add_cast_entry

load_dotenv()  # loads FARCASTER from .env


def get_farcaster_client():
    """
    Returns an authenticated Warpcast client using FARCASTER mnemonic.
    """
    mnemonic = os.getenv("FARCASTER")

    if not mnemonic:
        raise ValueError("Missing FARCASTER in .env (should contain your mnemonic phrase)")

    return Warpcast(mnemonic=mnemonic)


def post_to_farcaster(master_cast_id, text, world, window):
    """
    Posts to Farcaster and records the result.
    """
    client = get_farcaster_client()

    try:
        response = client.post_cast(text=text)

        cast_hash = getattr(getattr(response, "cast", None), "hash", None)

        print(f"\n✅ Posted to Farcaster [{world}] → [{window}]")
        print(f"📝 {text}")
        print(f"⏰ {datetime.datetime.now().isoformat()}")
        print(f"🔗 Hash: {cast_hash}")

        add_cast_entry(
            master_cast_id=master_cast_id,
            cast_hash=cast_hash,
            text=text,
            world=world,
            window=window,
        )

        return cast_hash

    except Exception as e:
        print(f"❌ Failed to post to Farcaster: {e}")
        return None
