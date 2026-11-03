import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Smart Eligibility Checker",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Smart Scholarship Matching System")

st.write(
    "Find scholarships matching your academic profile."
)

# Student Profile
st.subheader("Academic Information")

col1, col2 = st.columns(2)

with col1:

    nationality = st.selectbox(
        "Nationality",
        ["Bangladesh", "India", "Pakistan", "Nepal", "Other"]
    )

    cgpa = st.number_input(
        "Your CGPA",
        0.0, 4.0, 3.50, 0.01
    )

    ielts = st.number_input(
        "IELTS Score",
        0.0, 9.0, 6.5, 0.5
    )

with col2:

    study_field = st.selectbox(
        "Study Field",
        [
            "Statistics",
            "Biostatistics",
            "Public Health",
            "Epidemiology",
            "Data Science",
            "Applied Statistics"
        ]
    )

    graduation_year = st.selectbox(
        "Graduation Year",
        list(range(2026, 2031)),
        index=1
    )

    target_degree = st.selectbox(
        "Target Degree",
        ["Masters"]
    )

st.markdown("---")

if st.button(
    "Find Matching Scholarships",
    use_container_width=True
):

    data_path = (
        Path(__file__).parent.parent
        / "data"
        / "scholarships.csv"
    )

    df = pd.read_csv(data_path)

    df["deadline"] = pd.to_datetime(
        df["deadline"], errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    results = []

    for _, row in df.iterrows():

        field_match = (
            study_field in str(row["field"]).split("|")
        )

        nationality_match = (
            nationality == row["nationality"]
            or row["nationality"] == "All"
        )

        cgpa_match = cgpa >= row["min_cgpa"]

        ielts_match = ielts >= row["min_ielts"]

        degree_match = (
            target_degree == row["degree"]
        )

        deadline_match = (
            pd.notna(row["deadline"])
            and row["deadline"] >= today
        )

        if all([
            field_match,
            nationality_match,
            cgpa_match,
            ielts_match,
            degree_match,
            deadline_match
        ]):

            results.append(row)

    st.subheader("Matching Results")

    if results:

        matched_df = pd.DataFrame(results)

        st.success(
            f"{len(matched_df)} potential scholarships found!"
        )

        st.dataframe(
            matched_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No matching scholarships found. "
            "Try changing your academic preferences."
        )

    st.caption(
        "This is a preliminary screening tool. "
        "Always verify eligibility through official "
        "scholarship websites."
    )