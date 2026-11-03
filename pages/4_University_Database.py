import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="University Database",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ International University Database")

st.write(
    "Explore international universities and "
    "Master's programs in your preferred fields."
)

# Load Data
DATA_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "universities.csv"
)

df = pd.read_csv(DATA_PATH)

# Search Filters
st.subheader("Find Your University")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox(
        "Select Country",
        ["All"] + sorted(df["country"].unique().tolist())
    )

with col2:
    field = st.selectbox(
        "Select Field",
        ["All"] + sorted(df["field"].unique().tolist())
    )

# Filtering
filtered = df.copy()

if country != "All":
    filtered = filtered[filtered["country"] == country]

if field != "All":
    filtered = filtered[filtered["field"] == field]

st.markdown("---")

st.subheader(
    f"Available Universities: {len(filtered)}"
)

# University Cards
for _, row in filtered.iterrows():

    with st.container(border=True):

        st.subheader(row["university"])

        col1, col2, col3 = st.columns(3)

        col1.write(f"🌍 {row['country']}")
        col2.write(f"📚 {row['program']}")
        col3.write(f"🎓 {row['funding']}")

        st.write(f"Study Field: {row['field']}")

        st.write(f"IELTS: {row['ielts']}")

        st.link_button(
            "Visit Official Website",
            row["official_website"]
        )

# Download Database
st.markdown("---")

st.subheader("Download University Database")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="university_database.csv",
    mime="text/csv"
)

