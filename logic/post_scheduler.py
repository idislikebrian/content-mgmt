import datetime
from db.master_casts_db import get_random_cast_for_window
from db.farcaster_db import has_been_posted as farcaster_posted
from db.bluesky_db import has_been_posted as bluesky_posted


def pick_fresh_cast_for_platform(window, platform):
    """
    Generic selector:
        platform = "farcaster" or "bluesky"
    """

    checker = {
        "farcaster": farcaster_posted,
        "bluesky": bluesky_posted
    }[platform]

    max_attempts = 30

    for attempt in range(max_attempts):
        row = get_random_cast_for_window(window)
        if not row:
            return None

        master_cast_id, world, win, text = row

        if not checker(master_cast_id, text):
            return row  # fresh for this platform

    return None


def pick_cast_for_farcaster(window):
    return pick_fresh_cast_for_platform(window, "farcaster")


def pick_cast_for_bluesky(window):
    return pick_fresh_cast_for_platform(window, "bluesky")
