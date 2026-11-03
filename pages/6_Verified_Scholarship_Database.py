import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Verified Scholarship Database",
    page_icon="🎓",
    layout="wide"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "verified_scholarships.csv"

st.title("🎓 Official-source Scholarship Database")

st.write(
    "Explore scholarship programmes using information "
    "from their official websites."
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()

except FileNotFoundError:
    st.error("Scholarship database file not found.")
    st.stop()

except Exception as e:
    st.error(f"Unable to load database: {e}")
    st.stop()

# Important information
st.info(
    "Note: This database contains programme-level information. "
    "Always check the official website for programme-specific "
    "eligibility, funding and deadlines."
)

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Programmes", len(df))

with col2:
    st.metric("Countries / Regions", df["country"].nunique())

with col3:
    st.metric("Fully Funded Entries", 
              (df["funding_status"] == "Fully Funded").sum())

st.divider()

# Search and filters
st.subheader("🔍 Find Scholarships")

search = st.text_input(
    "Search by scholarship name or provider"
)

countries = ["All"] + sorted(df["country"].dropna().unique().tolist())

selected_country = st.selectbox(
    "Select Country",
    countries
)

all_fields = sorted({
    field.strip()
    for fields in df["field"].dropna()
    for field in fields.split("|")
})

selected_field = st.selectbox(
    "Select Study Field",
    ["All"] + all_fields
)

# Apply filters
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["scholarship_name"].str.contains(
            search, case=False, na=False
        )
        |
        filtered_df["provider"].str.contains(
            search, case=False, na=False
        )
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ]

if selected_field != "All":
    filtered_df = filtered_df[
        filtered_df["field"].apply(
            lambda x: selected_field in str(x).split("|")
        )
    ]

# Display results
st.subheader("📚 Scholarship Results")

st.write(f"Found {len(filtered_df)} programme(s).")

display_columns = [
    "scholarship_name",
    "provider",
    "country",
    "degree",
    "field",
    "funding_status",
    "intake",
    "deadline",
    "application_status",
    "official_website",
    "last_verified",
    "data_status"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "official_website": st.column_config.LinkColumn(
            "Official Website"
        )
    }
)

# Download filtered data
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Scholarship Data",
    data=csv_data,
    file_name="scholarship_database.csv",
    mime="text/csv"
)

st.divider()

# Detailed information
st.subheader("🌐 Scholarship Details")

if not filtered_df.empty:

    selected_scholarship = st.selectbox(
        "Choose a Scholarship",
        filtered_df["scholarship_name"].tolist()
    )

    scholarship = filtered_df[
        filtered_df["scholarship_name"] == selected_scholarship
    ].iloc[0]

    st.write(f"**Provider:** {scholarship['provider']}")
    st.write(f"**Country:** {scholarship['country']}")
    st.write(f"**Degree:** {scholarship['degree']}")
    st.write(f"**Eligible Fields:** {scholarship['field']}")
    st.write(f"**Funding:** {scholarship['funding_status']}")
    st.write(f"**Intake:** {scholarship['intake']}")
    st.write(f"**Deadline:** {scholarship['deadline']}")
    st.write(f"**Application Status:** {scholarship['application_status']}")
    st.write(f"**Last Verified:** {scholarship['last_verified']}")

    st.markdown(
        f"[Visit Official Website]({scholarship['official_website']})"
    )

    st.markdown(
        f"[Check Eligibility Source]({scholarship['eligibility_source']})"
    )

else:
    st.warning("No scholarships match your selected filters.")