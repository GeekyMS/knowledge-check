"""Main entry point for the Streamlit application."""

import streamlit as st

from config import CSV_PATH
from streamlit_template_pkg.data_utils import (
    load_awards_data,
    FISCAL_YEAR_COL,
    AWARDS_CONFERRED_COL,
    INSTITUTION_COL,
)

# Page configuration
st.set_page_config(page_title="MA Public Higher Education Awards", layout="wide", initial_sidebar_state="expanded")

# Load and cache data at application startup
df = load_awards_data(CSV_PATH)

# Main page content
st.title("Massachusetts Public Higher Education Degrees Awarded")

st.markdown("""
## Welcome to the Massachusetts Public Postsecondary Degrees Data Explorer

This application provides interactive visualizations of certificates and degrees granted by public Massachusetts
institutions of higher education since 2014.
This application provides an example of multipage Streamlit application that reads and
displays data.

### About the Data

The dataset comes from the [Massachusetts Education-to-Career Research and Data Hub](https://educationtocareer.data.mass.gov/College-and-Career/Public-Postsecondary-Awards-Degrees-Conferred-by-I/5yjf-27fz/about_data) and contains detailed information about degrees granted by:
- **Community Colleges** - Two-year institutions offering certificates and associate degrees
- **State Universities** - Four-year public universities
- **University of Massachusetts System** - The flagship public university system

Awards are categorized by type (Certificate, Associate, Bachelor, Master, Doctoral, etc...),
institution, fiscal year and student demographics.

### How to Use This App

Use the **sidebar navigation** on the left to explore different visualizations:
- **Degrees Over Time** - View trends in degrees granted over the years
- **Degrees by Institution** - See details about degrees granted by a specific institutions

Each page offers interactive controls in the sidebar to customize the visualizations.
""")

# Data overview section
st.header("Data Overview")

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
