# content-mgmt

A Python-based toolkit for managing and analyzing social content performance.  
Currently supports **Farcaster** posting, logging, and analytics, with **Threads integration** in progress.

## Features

- Post automation and scheduling for Farcaster  
- Engagement tracking (likes, recasts, replies)  
- SQLite-based data storage  
- Analytics merging and CSV export  
- Duplicate protection for posted casts  
- `.env` integration for API keys and credentials  
- Threads integration (WIP)  

## Project Structure

```

content-mgmt/
├── data/                 # SQLite databases and CSV exports
│   ├── farcaster.db
│   └── threads.db
├── db/                   # Database helper modules
│   ├── farcaster_db.py
│   └── threads_db.py
├── posters/              # Platform-specific posting scripts
│   ├── farcaster_poster.py
│   └── threads_poster.py
├── utils/                # Config, helper utilities, etc.
│   └── config.py
├── main.py               # Entry point for running the auto-poster
├── gather_analytics.py   # Script for pulling post metrics
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/yourusername/content-mgmt.git
cd content-mgmt
python -m venv venv
venv\Scripts\activate   # (Windows)
source venv/bin/activate  # (Mac/Linux)
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```
FARCASTER_MNEMONIC="your_wallet_seed_phrase"
FARCASTER_USERNAME="your_username"
INSTAGRAM_USERNAME="your_threads_username"     # (Threads WIP)
INSTAGRAM_PASSWORD="your_threads_password"     # (Threads WIP)
```

## Usage

### Run the poster:

```bash
python main.py
```

### Gather and analyze engagement:

```bash
python gather_analytics.py
```


## Output Files

| File                      | Description                               |
| ------------------------- | ----------------------------------------- |
| `data/farcaster.db`       | Main database storing posts and metrics   |
| `data/threads.db`         | Separate database for Threads posts (WIP) |
| `data/cast_analytics.csv` | Exported engagement report                |
| `data/used_casts.json`    | Prevents duplicate posting                |

## Roadmap

* ✅ Farcaster posting + analytics
* 🟨 Threads integration (auth & publishing)
* ⏳ Scheduling and multi-platform sync
* ⏳ Dashboard for visual analytics

## License

MIT License © 2025 Brian Felix