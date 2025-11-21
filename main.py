import datetime
import time

from utils.helpers import get_current_window

# DB initializers
from db.master_casts_db import init_db as init_master_db
from db.farcaster_db import init_db as init_farcaster_db
from db.bluesky_db import init_db as init_bluesky_db

# Post functions
from posters.farcaster_poster import post_to_farcaster
from posters.bluesky_poster import post_to_bluesky

# New scheduler logic
from logic.post_scheduler import (
    pick_cast_for_farcaster,
    pick_cast_for_bluesky
)

print("🚀 Auto-caster starting…")

# Init all DBs
init_master_db()
init_farcaster_db()
init_bluesky_db()
print("✅ Databases initialized.\n")


def print_preview(platform, row):
    """Nice preview message before posting."""
    master_cast_id, world, window, text = row
    print(f"\n=== 🚀 NEXT POST → {platform.upper()} ===")
    print(f"🗂 World:   {world}")
    print(f"🪟 Window:  {window}")
    print(f"📝 Text:    {text}")
    print(f"🆔 Cast ID: {master_cast_id}")
    print("=====================================\n")


try:
    while True:
        now = datetime.datetime.now()

        # Allowed posting minutes
        if now.minute in [27, 58]:
            window = get_current_window()

            if not window:
                print("⚠️ Outside posting hours.")
                time.sleep(60)
                continue

            print(f"\n⏱ Active window: {window}")

            # Pick independently
            fc_row = pick_cast_for_farcaster(window)
            bs_row = pick_cast_for_bluesky(window)

            # === Farcaster ===
            if fc_row:
                print_preview("farcaster", fc_row)
                master_cast_id, world, win, text = fc_row
                post_to_farcaster(master_cast_id, text, world, win)
            else:
                print("✔️ No fresh Farcaster cast this window.")

            # === Bluesky ===
            if bs_row:
                print_preview("bluesky", bs_row)
                master_cast_id, world, win, text = bs_row
                post_to_bluesky(master_cast_id, text, world, win)
            else:
                print("✔️ No fresh Bluesky cast this window.")

            # Avoid duplicate posting within same minute
            time.sleep(60)

        else:
            print("+checked at:", now)
            time.sleep(10)

except KeyboardInterrupt:
    print("\n🛑 Auto-caster stopped manually.")
