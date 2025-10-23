# content-mgmt

A Python-based toolkit for managing and analyzing content and engagement data.

## Features
- Fetches and logs analytics (likes, recasts, replies)
- Tracks used casts to avoid duplicates
- Generates CSV reports for insights
- Simple `.env` integration for API keys

## Project Structure
```
content-mgmt/
├── farcast/            # Core logic and scripts
├── data/               # CSV and JSON outputs
├── main.py             # Entry point for running scripts
└── requirements.txt
```

## Setup
```bash
git clone https://github.com/yourusername/content-mgmt.git
cd content-mgmt
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```
FARCAST_API_KEY=your_api_key_here
```

## Usage

Run the main script:

```bash
python main.py
```

## Output

* `data/cast_analytics.csv` — engagement metrics
* `data/used_casts.json` — record of processed casts

## License

MIT License © Brian Felix