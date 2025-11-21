import os
from dotenv import load_dotenv
from atproto import Client
from db.bluesky_db import save_post

load_dotenv()


def get_bluesky_client():
    """Return an authenticated Bluesky client."""
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")

    if not handle or not password:
        raise ValueError("Missing BLUESKY_HANDLE or BLUESKY_PASSWORD in .env")

    client = Client()
    client.login(handle, password)
    return client


def post_to_bluesky(master_cast_id, text, world, window):
    """
    Posts content to Bluesky and logs it into bluesky.db.
    """

    client = get_bluesky_client()

    try:
        post = client.send_post(text.strip())

        post_uri = post.uri
        post_cid = post.cid

        print(f"🌐 Bluesky posted: {post_uri}")

        # Save to the DB
        save_post(
            master_cast_id=master_cast_id,
            post_uri=post_uri,
            cid=post_cid,
            text=text,
            world=world,
            window=window,
        )

        return post_uri, post_cid

    except Exception as e:
        print(f"❌ Bluesky post failed:", e)
        return None, None
