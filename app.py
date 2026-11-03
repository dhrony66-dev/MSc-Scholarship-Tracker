import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="MSc Scholarship Tracker",
    page_icon="🎓",
    layout="wide"
)

# Load Data
DATA_PATH = Path(__file__).parent / "data" / "scholarships.csv"

df = pd.read_csv(DATA_PATH)

# Sidebar
st.sidebar.title("🎓 Scholarship Tracker")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Scholarship Explorer", "About"]
)

# Dashboard
if menu == "Dashboard":

    st.title("🎓 MSc Scholarship Dashboard")

    st.markdown(
        "Explore fully funded Master's opportunities worldwide."
    )

    st.markdown("---")

    # Statistics
    total = len(df)

    funded = len(
        df[df["funding"] == "Fully Funded"]
    )

    countries = df["country"].nunique()

    deadlines = pd.to_datetime(
        df["deadline"], errors="coerce"
    )

    upcoming = (
        deadlines.notna() &
        (deadlines >= pd.Timestamp.today().normalize())
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Scholarships", total)
    col2.metric("Fully Funded", funded)
    col3.metric("Countries", countries)
    col4.metric("Upcoming Deadlines", int(upcoming))

    st.markdown("---")

    # Charts
    left, right = st.columns(2)

    with left:

        st.subheader("Scholarships by Country")

        country_data = (
            df.groupby("country")
            .size()
            .reset_index(name="Scholarships")
        )

        fig = px.bar(
            country_data,
            x="country",
            y="Scholarships",
            title="Country-wise Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Scholarships by Field")

        field_data = (
            df.groupby("field")
            .size()
            .reset_index(name="Scholarships")
        )

        fig2 = px.pie(
            field_data,
            names="field",
            values="Scholarships",
            hole=0.4
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("Recent Scholarship Opportunities")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# Scholarship Explorer
elif menu == "Scholarship Explorer":

    st.title("🔍 Scholarship Explorer")

    selected_country = st.selectbox(
        "Select Country",
        ["All"] + sorted(df["country"].unique().tolist())
    )

    selected_field = st.selectbox(
        "Select Study Field",
        ["All"] + sorted(df["field"].unique().tolist())
    )

    filtered = df.copy()

    if selected_country != "All":
        filtered = filtered[
            filtered["country"] == selected_country
        ]

    if selected_field != "All":
        filtered = filtered[
            filtered["field"] == selected_field
        ]

    st.write(f"Found {len(filtered)} scholarships")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# About
else:

    st.title("About This Project")

    st.write("""
    MSc Scholarship Tracker is an academic portfolio project.

    Its objective is to help students explore international
    fully funded Master's scholarships.

    Developed using:

    - Python
    - Streamlit
    - Pandas
    - Plotly
    """)

