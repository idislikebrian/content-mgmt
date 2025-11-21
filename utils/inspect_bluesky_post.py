import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from atproto import Client

load_dotenv()

TEST_URI = "at://did:plc:xv2khloarcziywapsdg5r2tn/app.bsky.feed.post/3m5z3nvhqol2m"

def get_bluesky_client():
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")

    client = Client()
    client.login(handle, password)
    return client

client = get_bluesky_client()

print("\n=== Fetching raw post ===")
res = client.get_posts(uris=[TEST_URI])

print("\n=== Raw response object ===")
print(res)

if not res.posts:
    print("\n⚠️ No posts returned")
    sys.exit()

post = res.posts[0]

print("\n=== DIR(post) ===")
print(dir(post))

print("\n=== post.record ===")
print(post.record)

print("\n=== DIR(post.record) ===")
print(dir(post.record))

print("\n=== post.record.__dict__ ===")
try:
    print(post.record.__dict__)
except:
    print("record.__dict__ not available (likely pydantic-like object)")

print("\n=== Viewer section if available ===")
try:
    print("viewer:", post.viewer)
    print("DIR(viewer):", dir(post.viewer))
except Exception as e:
    print("No viewer object:", e)
