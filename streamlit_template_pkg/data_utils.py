"""Module for reading and manipulating awards data from CSV files."""

from pathlib import Path

import pandas as pd
import streamlit as st


# Column names with meaningful labels
FISCAL_YEAR_COL = "FISCAL_YEAR"
FISCAL_YEAR_LABEL = "Fiscal year degree was granted"

AWARDS_CONFERRED_COL = "AWARDS_CONFERRED"
AWARDS_LABEL = "Number of degrees awarded"

SEGMENT_COL = "SEGMENT"
SEGMENT_LABEL = "Type of institution"

INSTITUTION_COL = "INSTITUTION"
INSTITUTION_LABEL = "Name of institution"

AWARD_TYPE_COL = "AWARD_TYPE"
AWARD_TYPE_LABEL = "Type of degree"

AWARD_TYPE_ORDER_COL = "AWARD_TYPE_ORDER"
AWARD_TYPE_ORDER_LABEL = "Ordered rank of degree"

GENDER_COL = "GENDER"
GENDER_LABEL = "Gender of degree awardee"

RACE_ETHNICITY_COL = "RACE_ETHNICITY"
RACE_ETHNICITY_LABEL = "Race or ethnicity of degree awardee"

# Meaningful labels for columns
DISPLAY_LABELS = {
    FISCAL_YEAR_COL: FISCAL_YEAR_LABEL,
    AWARDS_CONFERRED_COL: AWARDS_LABEL,
    SEGMENT_COL: SEGMENT_LABEL,
    INSTITUTION_COL: INSTITUTION_LABEL,
    AWARD_TYPE_COL: AWARD_TYPE_LABEL,
    AWARD_TYPE_ORDER_COL: AWARD_TYPE_ORDER_LABEL,
    GENDER_COL: GENDER_LABEL,
    RACE_ETHNICITY_COL: RACE_ETHNICITY_LABEL,
}


@st.cache_data
def load_awards_data(csv_path: Path) -> pd.DataFrame:
    """
    Load the public postsecondary awards data from CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the awards data with columns:
            - FISCAL_YEAR: Year the awards were conferred (int)
            - AWARDS_CONFERRED: Count of awards (int)
            - SEGMENT: Institution segment (e.g., Community Colleges)
            - INSTITUTION: Name of the institution
            - AWARD_TYPE: Type of award (Certificate, Associate, etc.)
            - AWARD_TYPE_ORDER: Numeric order for award type (int)
            - GENDER: Gender category
            - RACE_ETHNICITY: Race/ethnicity category

    Raises:
        FileNotFoundError: If the CSV file does not exist
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    # Cast numeric columns to appropriate types
    df[FISCAL_YEAR_COL] = pd.to_numeric(df[FISCAL_YEAR_COL], errors="coerce", downcast="integer")
    df[AWARDS_CONFERRED_COL] = pd.to_numeric(df[AWARDS_CONFERRED_COL], errors="coerce", downcast="integer")
    df[AWARD_TYPE_ORDER_COL] = pd.to_numeric(df[AWARD_TYPE_ORDER_COL], errors="coerce", downcast="integer")

    return df


@st.cache_data
def filter_awards_data(
    df: pd.DataFrame, year_min: int | None = None, year_max: int | None = None, institution: str | None = None
) -> pd.DataFrame:
    """
    Filter awards DataFrame by year range and/or institution.

    Args:
        df: DataFrame containing awards data
        year_min: Minimum fiscal year (inclusive). If None, no lower bound.
        year_max: Maximum fiscal year (exclusive). If None, no upper bound.
        institution: Institution name to filter by. If None, no institution filtering.

    Returns:
        pd.DataFrame: Filtered DataFrame based on the provided criteria.
            If all parameters are None, returns a copy of the original DataFrame.

    Examples:
        >>> df = load_awards_data()
        >>> # Filter by year range
        >>> filtered = filter_awards_data(df, year_min=2020, year_max=2025)
        >>> # Filter by minimum year only
        >>> filtered = filter_awards_data(df, year_min=2020)
        >>> # Filter by institution only
        >>> filtered = filter_awards_data(df, institution="Berkshire Community College")
        >>> # Filter by both year range and institution
        >>> filtered = filter_awards_data(df, year_min=2020, year_max=2025,
        ...                              institution="Berkshire Community College")
    """
    filtered_df = df.copy()

    if year_min is not None:
        filtered_df = filtered_df[filtered_df[FISCAL_YEAR_COL] >= year_min]

    if year_max is not None:
        filtered_df = filtered_df[filtered_df[FISCAL_YEAR_COL] < year_max]

    if institution is not None:
        filtered_df = filtered_df[filtered_df[INSTITUTION_COL] == institution]

    return filtered_df
