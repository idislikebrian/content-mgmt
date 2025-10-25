import datetime, time, asyncio
from utils.helpers import get_current_window, get_random_cast

from posters.farcaster_poster import post_to_farcaster
from posters.threads_poster import post_to_threads

from db.farcaster_db import init_db, get_connection

print("🚀 Auto-caster starting...")

# initialize db
init_db()

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM casts")
total_casts = cur.fetchone()[0]
conn.close()
print(f"📦 Loaded {total_casts} casts from farcaster.db\n")

try:
    while True:
        now = datetime.datetime.now()
        if now.minute in [27, 58]:
            selected = get_random_cast()
            if selected:
                world, window, text = selected
                post_to_farcaster(text, world, window)
                asyncio.run(post_to_threads(text, world, window))
            time.sleep(60)
        else:
            print("+checked at:", now)
            time.sleep(10)
except KeyboardInterrupt:
    print("\n🛑 Auto-caster stopped manually.")
