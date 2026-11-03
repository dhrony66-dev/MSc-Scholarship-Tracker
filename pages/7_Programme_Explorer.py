import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Programme Explorer",
    page_icon="🎓",
    layout="wide"
)

# Locate project folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "programs.csv"

st.title("🎓 Master's Programme Explorer")

st.write(
    "Explore international Master's programmes "
    "related to Statistics and Public Health."
)

# Load programme data
@st.cache_data
def load_programmes():
    return pd.read_csv(DATA_FILE)

try:
    df = load_programmes()

except FileNotFoundError:
    st.error("programs.csv file not found in the data folder.")
    st.stop()

except Exception as e:
    st.error(f"Error loading programme data: {e}")
    st.stop()

# Dashboard metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Programmes", len(df))

with col2:
    st.metric("Scholarship Schemes", df["scholarship_name"].nunique())

with col3:
    st.metric("Degree Types", df["degree"].nunique())

st.divider()

# Search
st.subheader("🔍 Search Programmes")

search = st.text_input(
    "Search by programme or scholarship name"
)

# Field filter
all_fields = sorted({
    field.strip()
    for fields in df["study_area"].dropna()
    for field in fields.split("|")
})

selected_field = st.selectbox(
    "Select Study Area",
    ["All"] + all_fields
)

# Country filter
all_countries = sorted({
    country.strip()
    for countries in df["programme_countries"].dropna()
    for country in countries.split("|")
})

selected_country = st.selectbox(
    "Select Country",
    ["All"] + all_countries
)

# Apply filters
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["program_name"].str.contains(
            search, case=False, na=False
        )
        |
        filtered_df["scholarship_name"].str.contains(
            search, case=False, na=False
        )
    ]

if selected_field != "All":
    filtered_df = filtered_df[
        filtered_df["study_area"].apply(
            lambda x: selected_field in str(x).split("|")
        )
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["programme_countries"].apply(
            lambda x: selected_country in str(x).split("|")
        )
    ]

st.write(f"Found {len(filtered_df)} programme(s).")

# Display data
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "official_program_url": st.column_config.LinkColumn(
            "Official Programme Website"
        ),
        "scholarship_source_url": st.column_config.LinkColumn(
            "Scholarship Website"
        )
    }
)

# Programme details
st.divider()
st.subheader("📚 Programme Details")

if not filtered_df.empty:

    selected_program = st.selectbox(
        "Choose a Programme",
        filtered_df["program_name"].tolist()
    )

    programme = filtered_df[
        filtered_df["program_name"] == selected_program
    ].iloc[0]

    st.write(f"**Programme:** {programme['program_name']}")
    st.write(f"**Scholarship:** {programme['scholarship_name']}")
    st.write(f"**Degree:** {programme['degree']}")
    st.write(f"**Study Area:** {programme['study_area']}")
    st.write(f"**Countries:** {programme['programme_countries']}")
    st.write(f"**Intake:** {programme['intake']}")
    st.write(f"**Deadline:** {programme['application_deadline']}")
    st.write(f"**Funding Status:** {programme['scholarship_status']}")
    st.write(f"**English Requirement:** {programme['english_requirement']}")
    st.write(f"**Verification:** {programme['verification_status']}")

    st.markdown(
        f"[Visit Programme Website]({programme['official_program_url']})"
    )

    st.markdown(
        f"[Visit Scholarship Website]({programme['scholarship_source_url']})"
    )

else:
    st.warning("No programmes found.")

# Download filtered data
st.divider()

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Programme Data",
    data=csv,
    file_name="masters_programmes.csv",
    mime="text/csv"
)