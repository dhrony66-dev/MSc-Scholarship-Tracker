import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Deadline Reminder",
    page_icon="📅",
    layout="wide"
)

# Database Path
DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "scholarship.db"
)

st.title("📅 Scholarship Deadline Reminder")

st.write(
    "Monitor upcoming scholarship deadlines "
    "and manage your application schedule."
)

# Connect Database
conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query(
    "SELECT * FROM applications",
    conn
)

conn.close()

if not df.empty:

    df["deadline"] = pd.to_datetime(
        df["deadline"],
        errors="coerce"
    )

    today = pd.Timestamp(date.today())

    df["days_remaining"] = (
        df["deadline"] - today
    ).dt.days

    # Summary Cards
    upcoming_7 = (
        (df["days_remaining"] >= 0) &
        (df["days_remaining"] <= 7)
    ).sum()

    upcoming_15 = (
        (df["days_remaining"] >= 0) &
        (df["days_remaining"] <= 15)
    ).sum()

    upcoming_30 = (
        (df["days_remaining"] >= 0) &
        (df["days_remaining"] <= 30)
    ).sum()

    expired = (
        df["days_remaining"] < 0
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Next 7 Days", int(upcoming_7))
    col2.metric("Next 15 Days", int(upcoming_15))
    col3.metric("Next 30 Days", int(upcoming_30))
    col4.metric("Expired", int(expired))

    st.markdown("---")

    # Upcoming Deadlines
    st.subheader("⏳ Upcoming Deadlines")

    upcoming = df[
        df["days_remaining"] >= 0
    ].sort_values("days_remaining")

    if not upcoming.empty:

        st.dataframe(
            upcoming[
                [
                    "scholarship",
                    "country",
                    "deadline",
                    "days_remaining",
                    "status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No upcoming deadlines.")

    st.markdown("---")

    # Urgent Notifications
    st.subheader("🚨 Urgent Reminders")

    urgent = df[
        (df["days_remaining"] >= 0) &
        (df["days_remaining"] <= 7)
    ]

    if not urgent.empty:

        for _, row in urgent.iterrows():

            st.warning(
                f"{row['scholarship']} deadline is "
                f"in {row['days_remaining']} days!"
            )

    else:

        st.success(
            "No scholarship deadlines within the next 7 days."
        )

    # Expired Applications
    st.subheader("❌ Expired Deadlines")

    expired_df = df[
        df["days_remaining"] < 0
    ]

    if not expired_df.empty:

        st.dataframe(
            expired_df[
                ["scholarship", "country", "deadline"]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No expired deadlines.")

else:

    st.info(
        "No scholarship applications found. "
        "Add applications through Application Tracker first."
    )

