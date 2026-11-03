import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Scholarship Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Scholarship Analytics Dashboard")

st.write(
    "Explore global scholarship trends through "
    "interactive statistical visualizations."
)

# File Paths
BASE_DIR = Path(__file__).parent.parent

SCHOLARSHIP_PATH = BASE_DIR / "data" / "scholarships.csv"
UNIVERSITY_PATH = BASE_DIR / "data" / "universities.csv"

# Load Data
scholarships = pd.read_csv(SCHOLARSHIP_PATH)
universities = pd.read_csv(UNIVERSITY_PATH)

# Convert Deadline
scholarships["deadline"] = pd.to_datetime(
    scholarships["deadline"],
    errors="coerce"
)

# Summary Statistics
total_scholarships = len(scholarships)

total_countries = scholarships["country"].nunique()

fully_funded = (
    scholarships["funding"] == "Fully Funded"
).sum()

total_universities = len(universities)

# Metric Cards
st.subheader("Global Scholarship Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Scholarships", total_scholarships)

col2.metric("Countries", total_countries)

col3.metric("Fully Funded", int(fully_funded))

col4.metric("Universities", total_universities)

st.markdown("---")

# Country-wise Analysis
st.subheader("1. Country-wise Scholarship Distribution")

country_data = (
    scholarships.groupby("country")
    .size()
    .reset_index(name="Scholarships")
    .sort_values("Scholarships", ascending=False)
)

fig1 = px.bar(
    country_data,
    x="country",
    y="Scholarships",
    text="Scholarships",
    title="Scholarships by Country"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Field-wise Analysis
st.subheader("2. Study Field Distribution")

field_data = scholarships.assign(
    field=scholarships["field"].str.split("|")
).explode("field")

field_count = (
    field_data.groupby("field")
    .size()
    .reset_index(name="Scholarships")
)

fig2 = px.pie(
    field_count,
    names="field",
    values="Scholarships",
    hole=0.45,
    title="Scholarships by Study Field"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Funding Analysis
st.subheader("3. Funding Type Distribution")

funding_data = (
    scholarships.groupby("funding")
    .size()
    .reset_index(name="Count")
)

fig3 = px.pie(
    funding_data,
    names="funding",
    values="Count",
    title="Funding Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# CGPA Analysis
st.subheader("4. Minimum CGPA Requirements")

fig4 = px.histogram(
    scholarships,
    x="min_cgpa",
    nbins=10,
    title="Distribution of Minimum CGPA"
)

st.plotly_chart(fig4, use_container_width=True)

# IELTS Analysis
st.subheader("5. IELTS Requirement Analysis")

fig5 = px.histogram(
    scholarships,
    x="min_ielts",
    nbins=10,
    title="Distribution of Minimum IELTS Requirements"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# Deadline Analysis
st.subheader("6. Scholarship Deadline Analysis")

deadline_data = scholarships.dropna(
    subset=["deadline"]
).copy()

deadline_data["Month"] = (
    deadline_data["deadline"].dt.strftime("%Y-%m")
)

monthly_data = (
    deadline_data.groupby("Month")
    .size()
    .reset_index(name="Scholarships")
    .sort_values("Month")
)

fig6 = px.line(
    monthly_data,
    x="Month",
    y="Scholarships",
    markers=True,
    title="Monthly Scholarship Deadlines"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# University Analysis
st.subheader("7. University Distribution by Country")

university_data = (
    universities.groupby("country")
    .size()
    .reset_index(name="Universities")
)

fig7 = px.bar(
    university_data,
    x="country",
    y="Universities",
    color="Universities",
    title="Universities by Country"
)

st.plotly_chart(fig7, use_container_width=True)

# Download Report
st.markdown("---")

st.subheader("Download Analytical Dataset")

csv = scholarships.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Scholarship Dataset",
    data=csv,
    file_name="scholarship_analytics.csv",
    mime="text/csv"
)

st.success(
    "Scholarship Analytics Dashboard is Ready!"
)