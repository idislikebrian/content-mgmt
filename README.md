# content-mgmt

A Python toolkit for posting, logging, and analyzing content across your social platforms.
Supports **Farcaster** + **Bluesky** with a full analytics pipeline and a **Streamlit dashboard** for weekly reporting.

## Features

* Farcaster + Bluesky posting (per-platform scripts)
* Analytics gathering for likes, recasts/reposts, replies, quotes
* SQLite databases for each platform
* Weekly analytics dashboard (Streamlit)
* Sunday–Saturday reporting logic
* Weighted scoring system (per platform)
* CSV export for cross-platform weekly reports
* Duplicate-post protection
* `.env` based credential loading

## Project Structure

```
content-mgmt/
├── analytics/
│   ├── gather_farcaster.py        # Fetch Farcaster engagement
│   ├── gather_bluesky.py          # Fetch Bluesky engagement
│   └── gather_all.py              # Optional combined runner
├── dashboard/
│   └── dashboard.py               # Streamlit analytics UI
├── data/
│   ├── farcaster.db
│   ├── bluesky.db
│   └── weekly_reports/            # CSV exports
├── db/
│   ├── farcaster_db.py            # Farcaster DB helpers
│   ├── bluesky_db.py              # Bluesky DB helpers
│   └── init_db.py                 # Migrations / table creation
├── posters/
│   ├── farcaster_poster.py
│   ├── bluesky_poster.py
│   └── shared/                    # Shared posting utils
├── utils/
│   ├── config.py
│   ├── inspect_bluesky_post.py    # Inspector tool
│   └── inspect_atproto.py         # Raw ATProto analysis tool
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/idislikebrian/content-mgmt.git
cd content-mgmt

python -m venv venv
venv/Scripts/activate      # Windows
source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

## Environment Variables

Create a `.env` in the root:

```
FARCASTER_MNEMONIC="your_mnemonic"
FARCASTER_FID="your_fid"
FARCASTER_USERNAME="your_username"

BLUESKY_HANDLE="you.bsky.social"
BLUESKY_APP_PASSWORD="your_app_password"
```

(Threads may be added later.)

## Usage

### Post to Farcaster

```bash
python posters/farcaster_poster.py
```

### Post to Bluesky

```bash
python posters/bluesky_poster.py
```

### Gather Farcaster analytics

```bash
python analytics/gather_farcaster.py
```

### Gather Bluesky analytics

```bash
python analytics/gather_bluesky.py
```

### Weekly dashboard (Streamlit)

```bash
streamlit run dashboard/dashboard.py
```

Includes:

* Weekly Farcaster + Bluesky breakdowns
* Weighted scoring sliders
* Leaderboards
* Combined CSV export (Sun–Sat)

## Output Files

| File/Folder                 | Description                        |
| --------------------------- | ---------------------------------- |
| `data/farcaster.db`         | All Farcaster posts + metrics      |
| `data/bluesky.db`           | All Bluesky posts + metrics        |
| `data/weekly_reports/*.csv` | Weekly combined exports            |
| `used_casts.json`           | Prevents duplicate Farcaster posts |

## Roadmap

* **Done:** Farcaster + Bluesky ingest + scoring
* **Done:** Streamlit weekly dashboard
* **Next:** Add manual-cast backfill (CLI tool)
* **Next:** Automatic Farcaster history sync
* **Later:** Threads integration
* **Later:** Scheduling + cross-platform posting

## License

MIT License © 2025 Brian Felix