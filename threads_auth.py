from dotenv import load_dotenv
from pythreads.threads import Threads  # ✅ Updated import path

load_dotenv()

auth_url, state_key = Threads.authorization_url()
print(f"Visit this URL in your browser:\n{auth_url}")
print(f"\nStore this state key securely:\n{state_key}")
