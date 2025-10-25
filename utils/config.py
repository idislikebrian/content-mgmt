import os
from dotenv import load_dotenv
from farcaster import Warpcast

load_dotenv()

MNEMONIC = os.getenv("MNEMONIC_ENV_VAR")

def get_farcaster_client():
    return Warpcast(mnemonic=MNEMONIC)
