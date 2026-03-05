"""Configuration constants for the Streamlit application."""

from pathlib import Path

# Data file path - defined relative to this config file location
DATA_PATH = Path(__file__).parent / "data"
CSV_PATH = DATA_PATH / "public_postsecondary_awards_conferred_by_institution_20260125.csv"
