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

# Year Range Slider
min_year = int(df[FISCAL_YEAR_COL].min())
max_year = int(df[FISCAL_YEAR_COL].max())
selected_years = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year) # Default to full range
)

# Filter the dataframe based on the slider selection
filtered_df = df[
    (df[FISCAL_YEAR_COL] >= selected_years[0]) & 
    (df[FISCAL_YEAR_COL] <= selected_years[1])
]

color_by = st.sidebar.radio(
    "Color lines by:",
    options=[SEGMENT_COL, AWARD_TYPE_COL],
    format_func=DISPLAY_LABELS.get,
    help="Choose how to group and color the lines in the plot",
)

# Create and display the chart USING the filtered_df
fig = create_degrees_over_time_chart(filtered_df, color_by)
st.plotly_chart(fig, width="stretch")

# Display summary statistics (also updated to use filtered_df)
st.subheader("Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    total_awards = int(filtered_df[AWARDS_CONFERRED_COL].sum())
    st.metric("Total Awards", f"{total_awards:,}")

with col2:
    year_range = f"{filtered_df[FISCAL_YEAR_COL].min()} - {filtered_df[FISCAL_YEAR_COL].max()}"
    st.metric("Year Range", year_range)

with col3:
    num_institutions = filtered_df[INSTITUTION_COL].nunique()
    st.metric("Number of Institutions", num_institutions)