from atproto import Client

c = Client()

print("\n=== DIR(Client) ===")
print(dir(c))

print("\n=== DIR(Client.app) ===")
print(dir(c.app))

print("\n=== DIR(Client.app.bsky) ===")
print(dir(c.app.bsky))

print("\n=== DIR(Client.app.bsky.feed) ===")
print(dir(c.app.bsky.feed))

print("\n=== DIR(Client.app.bsky.feed.get_post) ===")
try:
    print(c.app.bsky.feed.get_post)
except:
    print("get_post doesn't exist here")
