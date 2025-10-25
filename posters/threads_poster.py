import asyncio
import datetime
import os
from dotenv import load_dotenv
from threads_api.src.threads_api import ThreadsAPI
from db.threads_db import add_post_entry

load_dotenv()

async def test_login():
    """Verify login and show basic user info before posting."""
    from threads_api.src.threads_api import ThreadsAPI
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api = ThreadsAPI()

    print("🔑 Logging into Threads via Instagram...")
    await api.login(
        os.getenv("INSTAGRAM_USERNAME"),
        os.getenv("INSTAGRAM_PASSWORD"),
        cached_token_path=".threads_token"
    )

    me = await api.get_user_id_from_username(os.getenv("INSTAGRAM_USERNAME"))
    print(f"✅ Logged in successfully. Your user ID: {me}")

    await api.close_gracefully()

async def post_to_threads(text, world, window, image_path=None):
    """Posts a cast to Threads."""
    try:
        api = ThreadsAPI()
        await api.login(
            os.getenv("INSTAGRAM_USERNAME"),
            os.getenv("INSTAGRAM_PASSWORD"),
            cached_token_path=".threads_token"
        )

        result = await api.post(caption=text, image_path=image_path)

        timestamp = datetime.datetime.now().isoformat()

        if result:
            post_id = getattr(result, "id", None)
            print(f"\n✅ Posted to Threads [{world}] → [{window}]")
            print(f"📝 {text}")
            print(f"⏰ {timestamp}")
            print(f"🔗 Post ID: {post_id}")

            # Save to database (threads can share same structure)
            add_post_entry(post_id=post_id, text=text, world=world, window=window)

        else:
            print(f"❌ Unable to post [{world}] → [{window}]")

        await api.close_gracefully()

    except Exception as e:
        print(f"⚠️ Threads posting failed: {e}")
