"""Module for creating data visualizations using Plotly."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from streamlit_template_pkg.data_utils import FISCAL_YEAR_COL, AWARDS_CONFERRED_COL, INSTITUTION_COL, DISPLAY_LABELS


def create_degrees_over_time_chart(df: pd.DataFrame, color_by: str) -> go.Figure:
    """
    Create a line chart showing degrees conferred over time.

    Args:
        df: DataFrame containing degree count data
        color_by: Column name to use for grouping and coloring the lines
                  (e.g., SEGMENT_COL or AWARD_TYPE_COL)

    Returns:
        go.Figure: Plotly figure object with the line chart

    Examples:
        >>> from streamlit_template_pkg.data_utils import load_awards_data, SEGMENT_COL
        >>> df = load_awards_data()
        >>> fig = create_degrees_over_time_chart(df, SEGMENT_COL)
    """
    # Aggregate data by year and the selected grouping
    aggregated = df.groupby([FISCAL_YEAR_COL, color_by])[AWARDS_CONFERRED_COL].sum().reset_index()

    # Create Plotly line chart using year on x-axis, number of degrees on y-axis
    # Lines are colored by the unique values in the 'color_by' column
    fig = px.line(
        aggregated,
        x=FISCAL_YEAR_COL,
        y=AWARDS_CONFERRED_COL,
        color=color_by,
        markers=True,
        title=f"Degrees Granted Over Time by {DISPLAY_LABELS.get(color_by)}",
        # Dict maps original column names to labels that should be displayed
        labels=DISPLAY_LABELS,
    )

    fig.update_layout(
        # Display a single hovertext with all y values for each x trace
        hovermode="x unified",
        height=500,
        # Set x-axis title
        xaxis_title=DISPLAY_LABELS.get(FISCAL_YEAR_COL),
        # Set y-axis title
        yaxis_title=DISPLAY_LABELS.get(AWARDS_CONFERRED_COL),
    )

    return fig


def create_institution_bar_chart(df: pd.DataFrame, institution: str, color_by: str) -> go.Figure:
    """
    Create a bar chart showing awards by year for a specific institution.

    Args:
        df: DataFrame containing awards data
        institution: Institution name to filter by
        color_by: Column name to use for grouping and coloring the bars
                  (e.g., GENDER_COL, AWARD_TYPE_COL, RACE_ETHNICITY_COL)

    Returns:
        go.Figure: Plotly figure object with the bar chart

    Examples:
        >>> from streamlit_template_pkg.data_utils import load_awards_data, GENDER_COL
        >>> df = load_awards_data()
        >>> fig = create_institution_bar_chart(df, "Berkshire Community College", GENDER_COL)
    """
    # Filter data for the selected institution
    institution_df = df[df[INSTITUTION_COL] == institution].copy()

    # Aggregate data by year and the selected grouping
    aggregated = institution_df.groupby([FISCAL_YEAR_COL, color_by])[AWARDS_CONFERRED_COL].sum().reset_index()

    # Create stacked bar chart where each year gets a bar broken down by the counts of values in 'color_by'
    fig = px.bar(
        aggregated,
        x=FISCAL_YEAR_COL,
        y=AWARDS_CONFERRED_COL,
        color=color_by,
        title=f"Awards Conferred at {institution} by {DISPLAY_LABELS.get(color_by)}",
        # Dict maps original column names to labels that should be displayed
        labels=DISPLAY_LABELS,
        # Stack bars for each year, rather than displaying them side by side, to save space horizontally
        barmode="stack",
    )

    fig.update_layout(
        # Display a single hovertext with all y values for each x trace
        hovermode="x unified",
        height=500,
        # Set x-axis title
        xaxis_title=DISPLAY_LABELS.get(FISCAL_YEAR_COL),
        # Set y-axis title
        yaxis_title=DISPLAY_LABELS.get(AWARDS_CONFERRED_COL),
        # Forces a label on each year in the x-axis
        xaxis=dict(type="category"),
    )

    return fig
