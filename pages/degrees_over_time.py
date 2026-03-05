"""Streamlit page that shows year-by-year numbers of degrees granted by all Massachusetts public institutions"""

import streamlit as st

from config import CSV_PATH
from streamlit_template_pkg.data_utils import (
    load_awards_data,
    FISCAL_YEAR_COL,
    AWARDS_CONFERRED_COL,
    SEGMENT_COL,
    INSTITUTION_COL,
    AWARD_TYPE_COL,
    DISPLAY_LABELS,
)
from streamlit_template_pkg.visualizations import create_degrees_over_time_chart

# Load cached data
df = load_awards_data(CSV_PATH)

# Headlines
st.title("Degrees Over Time")
st.write("Visualize the trend of postsecondary degrees conferred at Massachusetts public institutions over time.")

# Sidebar controls
st.sidebar.header("Visualization Options")
color_by = st.sidebar.radio(
    "Color lines by:",
    options=[SEGMENT_COL, AWARD_TYPE_COL],
    format_func=DISPLAY_LABELS.get,
    help="Choose how to group and color the lines in the plot",
)

# Create and display the chart
fig = create_degrees_over_time_chart(df, color_by)
st.plotly_chart(fig, width="stretch")

# Display summary statistics
st.subheader("Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    total_awards = int(df[AWARDS_CONFERRED_COL].sum())
    st.metric("Total Awards", f"{total_awards:,}")

with col2:
    year_range = f"{df[FISCAL_YEAR_COL].min()} - {df[FISCAL_YEAR_COL].max()}"
    st.metric("Year Range", year_range)

with col3:
    num_institutions = df[INSTITUTION_COL].nunique()
    st.metric("Number of Institutions", num_institutions)
