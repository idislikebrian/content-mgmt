import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

import datetime

import pandas as pd
import streamlit as st

from db.farcaster_db import get_connection as get_farcaster_db
from db.bluesky_db import get_connection as get_bluesky_db


def get_fc_conn():
    return get_farcaster_db()

def get_bs_conn():
    return get_bluesky_db()


# -----------------------------
# Date helpers
# -----------------------------
def get_week_range(mode: str = "this") -> tuple[datetime.datetime, datetime.datetime]:
    """
    Return (start, end) datetimes for:
    - 'this':  Sunday–Saturday week containing today
    - 'last':  previous Sunday–Saturday week
    """
    today = datetime.date.today()

    # weekday(): Mon=0..Sun=6 → convert to "days since Sunday"
    days_since_sunday = (today.weekday() + 1) % 7
    this_sunday = today - datetime.timedelta(days=days_since_sunday)

    if mode == "last":
        start_date = this_sunday - datetime.timedelta(days=7)
    else:  # "this"
        start_date = this_sunday

    end_date = start_date + datetime.timedelta(days=7)

    start_dt = datetime.datetime.combine(start_date, datetime.time.min)
    end_dt = datetime.datetime.combine(end_date, datetime.time.min)
    return start_dt, end_dt


def to_iso(dt: datetime.datetime) -> str:
    return dt.isoformat()


# -----------------------------
# Data loaders
# -----------------------------
def load_farcaster_week(start_dt: datetime.datetime, end_dt: datetime.datetime) -> pd.DataFrame:
    conn = get_fc_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.timestamp,
            c.text,
            c.world,
            c.window,
            COALESCE(a.likes,   0) AS likes,
            COALESCE(a.recasts, 0) AS recasts,
            COALESCE(a.replies, 0) AS replies
        FROM casts c
        LEFT JOIN analytics a ON c.cast_hash = a.cast_hash
        WHERE c.timestamp >= ? AND c.timestamp < ?
        ORDER BY c.timestamp ASC
        """,
        (to_iso(start_dt), to_iso(end_dt)),
    )

    rows = cur.fetchall()
    conn.close()

    cols = ["timestamp", "text", "world", "window", "likes", "recasts", "replies"]
    df = pd.DataFrame(rows, columns=cols)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def load_bluesky_week(start_dt: datetime.datetime, end_dt: datetime.datetime) -> pd.DataFrame:
    conn = get_bs_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            p.timestamp,
            p.text,
            p.world,
            p.window,
            COALESCE(a.likes,   0) AS likes,
            COALESCE(a.reposts, 0) AS reposts,
            COALESCE(a.replies, 0) AS replies,
            COALESCE(a.quotes,  0) AS quotes
        FROM posts p
        LEFT JOIN analytics a ON p.post_uri = a.post_uri
        WHERE p.timestamp >= ? AND p.timestamp < ?
        ORDER BY p.timestamp ASC
        """,
        (to_iso(start_dt), to_iso(end_dt)),
    )

    rows = cur.fetchall()
    conn.close()

    cols = ["timestamp", "text", "world", "window", "likes", "reposts", "replies", "quotes"]
    df = pd.DataFrame(rows, columns=cols)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


# -----------------------------
# Streamlit app
# -----------------------------
st.set_page_config(page_title="Content Analytics Dashboard", layout="wide")

st.title("📈 Content Analytics Dashboard")

# Week selection
with st.sidebar:
    st.header("Week & Export")

    week_mode = st.radio(
        "Week range",
        options=["this", "last"],
        format_func=lambda x: "This week (Sun–Sat)" if x == "this" else "Last week (Sun–Sat)",
    )

    start_dt, end_dt = get_week_range(week_mode)
    st.write(f"**From:** {start_dt.date()}  \n**To:** {end_dt.date()}")

    st.markdown("---")

    st.header("Farcaster scoring")
    fc_like_w = st.slider("Likes weight (Farcaster)", 0.0, 5.0, 1.0, 0.5)
    fc_recast_w = st.slider("Recasts weight (Farcaster)", 0.0, 5.0, 2.0, 0.5)
    fc_reply_w = st.slider("Replies weight (Farcaster)", 0.0, 5.0, 3.0, 0.5)

    st.markdown("---")

    st.header("Bluesky scoring")
    bs_like_w = st.slider("Likes weight (Bluesky)", 0.0, 5.0, 1.0, 0.5)
    bs_repost_w = st.slider("Reposts weight (Bluesky)", 0.0, 5.0, 2.0, 0.5)
    bs_reply_w = st.slider("Replies weight (Bluesky)", 0.0, 5.0, 3.0, 0.5)
    bs_quote_w = st.slider("Quotes weight (Bluesky)", 0.0, 5.0, 4.0, 0.5)

# Load data
fc_df = load_farcaster_week(start_dt, end_dt)
bs_df = load_bluesky_week(start_dt, end_dt)

# Compute custom scores per platform
if not fc_df.empty:
    fc_df["score_custom"] = (
        fc_like_w * fc_df["likes"]
        + fc_recast_w * fc_df["recasts"]
        + fc_reply_w * fc_df["replies"]
    )

if not bs_df.empty:
    bs_df["score_custom"] = (
        bs_like_w * bs_df["likes"]
        + bs_repost_w * bs_df["reposts"]
        + bs_reply_w * bs_df["replies"]
        + bs_quote_w * bs_df["quotes"]
    )

# Top row: summary
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Farcaster posts (week)", 0 if fc_df.empty else len(fc_df))
with col2:
    st.metric("Bluesky posts (week)", 0 if bs_df.empty else len(bs_df))
with col3:
    st.metric(
        "Top Farcaster score",
        0 if fc_df.empty else int(fc_df["score_custom"].max()),
    )
with col4:
    st.metric(
        "Top Bluesky score",
        0 if bs_df.empty else int(bs_df["score_custom"].max()),
    )

st.markdown("---")

# Leaderboards
fc_col, bs_col = st.columns(2)

with fc_col:
    st.subheader("🏁 Farcaster – Top posts this week")

    if fc_df.empty:
        st.info("No Farcaster posts in this week range.")
    else:
        fc_top = (
            fc_df.sort_values("score_custom", ascending=False)
            .copy()
        )
        fc_top["text_preview"] = fc_top["text"].str.slice(0, 140)
        display_cols = [
            "timestamp",
            "world",
            "window",
            "text_preview",
            "likes",
            "recasts",
            "replies",
            "score_custom",
        ]
        st.dataframe(
            fc_top[display_cols].rename(
                columns={
                    "timestamp": "time",
                    "world": "world",
                    "window": "window",
                    "text_preview": "text",
                    "score_custom": "score",
                }
            ),
            use_container_width=True,
        )

with bs_col:
    st.subheader("🌐 Bluesky – Top posts this week")

    if bs_df.empty:
        st.info("No Bluesky posts in this week range.")
    else:
        bs_top = (
            bs_df.sort_values("score_custom", ascending=False)
            .copy()
        )
        bs_top["text_preview"] = bs_top["text"].str.slice(0, 140)
        display_cols = [
            "timestamp",
            "world",
            "window",
            "text_preview",
            "likes",
            "reposts",
            "replies",
            "quotes",
            "score_custom",
        ]
        st.dataframe(
            bs_top[display_cols].rename(
                columns={
                    "timestamp": "time",
                    "world": "world",
                    "window": "window",
                    "text_preview": "text",
                    "score_custom": "score",
                }
            ),
            use_container_width=True,
        )

st.markdown("---")

# CSV export (combined)
st.subheader("📤 Export weekly CSV (Sunday–Saturday)")

if fc_df.empty and bs_df.empty:
    st.info("No posts found for this week. Nothing to export.")
else:
    export_frames = []

    if not fc_df.empty:
        fc_export = fc_df.copy()
        fc_export["platform"] = "farcaster"
        export_frames.append(fc_export)

    if not bs_df.empty:
        bs_export = bs_df.copy()
        bs_export["platform"] = "bluesky"
        export_frames.append(bs_export)

    combined = pd.concat(export_frames, ignore_index=True)

    # Keep export columns clean
    export_cols = [
        "timestamp",
        "platform",
        "world",
        "window",
        "text",
        "likes",
    ]
    if "recasts" in combined.columns:
        export_cols.append("recasts")
    if "replies" in combined.columns:
        export_cols.append("replies")
    if "reposts" in combined.columns:
        export_cols.append("reposts")
    if "quotes" in combined.columns:
        export_cols.append("quotes")
    if "score_custom" in combined.columns:
        export_cols.append("score_custom")

    combined = combined[export_cols].sort_values("timestamp")

    csv_bytes = combined.to_csv(index=False).encode("utf-8")
    filename = f"weekly_report_{start_dt.date()}_{end_dt.date()}.csv"

    st.download_button(
        label="⬇️ Download weekly CSV",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
    )
