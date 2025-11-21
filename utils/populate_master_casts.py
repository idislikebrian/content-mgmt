import os
import sys

# Get the absolute path to the project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from db.master_casts_db import init_db, insert_cast
from utils.helpers import casts


def main():
    init_db()
    total = 0

    for world, windows in casts.items():
        for window, entries in windows.items():
            for text in entries:
                insert_cast(world, window, text)
                total += 1

    print(f"✅ Populated master_casts.db with {total} rows.")


if __name__ == "__main__":
    main()
