import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(
    page_title="Application Tracker",
    page_icon="📋",
    layout="wide"
)

# Database
DB_PATH = (
    Path(__file__).parent.parent
    / "database"
    / "scholarship.db"
)

DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

# Create Table
with get_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scholarship TEXT,
            country TEXT,
            deadline TEXT,
            status TEXT,
            notes TEXT
        )
    """)

st.title("📋 Scholarship Application Tracker")

st.write("Track and manage your scholarship applications.")

# Add Application
st.subheader("Add New Application")

with st.form("application_form"):

    scholarship = st.text_input("Scholarship Name")

    country = st.text_input("Country")

    deadline = st.date_input("Application Deadline")

    status = st.selectbox(
        "Application Status",
        [
            "Not Started",
            "Preparing Documents",
            "In Progress",
            "Submitted",
            "Accepted",
            "Rejected"
        ]
    )

    notes = st.text_area("Additional Notes")

    submitted = st.form_submit_button(
        "Save Application"
    )

    if submitted:

        if scholarship.strip():

            with get_connection() as conn:

                conn.execute(
                    """
                    INSERT INTO applications
                    (scholarship, country, deadline, status, notes)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        scholarship,
                        country,
                        str(deadline),
                        status,
                        notes
                    )
                )

            st.success("Application saved successfully!")

        else:

            st.error("Please enter scholarship name.")

# Display Applications
st.markdown("---")

st.subheader("My Applications")

with get_connection() as conn:

    df = pd.read_sql_query(
        "SELECT * FROM applications",
        conn
    )

if not df.empty:

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Applications", len(df))

    col2.metric(
        "Submitted",
        (df["status"] == "Submitted").sum()
    )

    col3.metric(
        "Accepted",
        (df["status"] == "Accepted").sum()
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Update Status
    st.markdown("---")

    st.subheader("Update Application Status")

    selected_id = st.selectbox(
        "Select Application ID",
        df["id"].tolist()
    )

    new_status = st.selectbox(
        "New Status",
        [
            "Not Started",
            "Preparing Documents",
            "In Progress",
            "Submitted",
            "Accepted",
            "Rejected"
        ]
    )

    if st.button("Update Status"):

        with get_connection() as conn:

            conn.execute(
                """
                UPDATE applications
                SET status = ?
                WHERE id = ?
                """,
                (new_status, selected_id)
            )

        st.success("Status updated successfully!")

        st.rerun()

else:

    st.info("No applications added yet.")

