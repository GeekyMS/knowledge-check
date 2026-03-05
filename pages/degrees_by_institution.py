"""Streamlit page that lets the user select an institution and see a year-by-year breakdown
of the degrees granted by that institution.
"""

import streamlit as st

from config import CSV_PATH
from streamlit_template_pkg.data_utils import (
    load_awards_data,
    DISPLAY_LABELS,
    FISCAL_YEAR_COL,
    AWARDS_CONFERRED_COL,
    INSTITUTION_COL,
    AWARD_TYPE_COL,
    GENDER_COL,
    RACE_ETHNICITY_COL,
)
from streamlit_template_pkg.visualizations import create_institution_bar_chart

# Load cached data
df = load_awards_data(CSV_PATH)

st.title("Degrees by Institution")
st.write("See details about degrees awarded at a specific Massachusetts public higher education institution.")

# Sidebar controls
st.sidebar.header("Visualization Options")

# Institution dropdown
institutions = sorted(df[INSTITUTION_COL].unique())
selected_institution = st.sidebar.selectbox(
    "Select Institution:",
    options=institutions,
    help="Choose an institution to view its award data",
)

# Breakdown option
breakdown_by = st.sidebar.radio(
    "Detailed breakdown by:",
    options=[GENDER_COL, AWARD_TYPE_COL, RACE_ETHNICITY_COL],
    format_func=DISPLAY_LABELS.get,
    help="Choose how to break down and color the bars in the chart",
)

# Create and display the bar chart
fig = create_institution_bar_chart(df, selected_institution, breakdown_by)
st.plotly_chart(fig, width="stretch")

# Display summary statistics for the selected institution in columns at the bottom of the page
st.subheader(f"Summary Statistics for {selected_institution}")
institution_df = df[df[INSTITUTION_COL] == selected_institution]

col1, col2, col3 = st.columns(3)

with col1:
    total_awards = int(institution_df[AWARDS_CONFERRED_COL].sum())
    st.metric("Total Awards", f"{total_awards:,}")

with col2:
    year_range = f"{institution_df[FISCAL_YEAR_COL].min()} - {institution_df[FISCAL_YEAR_COL].max()}"
    st.metric("Year Range", year_range)

with col3:
    num_award_types = institution_df[AWARD_TYPE_COL].nunique()
    st.metric("Award Types Offered", num_award_types)
