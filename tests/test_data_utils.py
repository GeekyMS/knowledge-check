"""Tests for data_utils module."""

import pytest
import pandas as pd

from streamlit_template_pkg.data_utils import (
    load_awards_data,
    filter_awards_data,
    FISCAL_YEAR_COL,
    AWARDS_CONFERRED_COL,
    SEGMENT_COL,
    INSTITUTION_COL,
    AWARD_TYPE_COL,
    AWARD_TYPE_ORDER_COL,
    GENDER_COL,
    RACE_ETHNICITY_COL,
)


class TestLoadAwardsData:
    """Tests for load_awards_data function."""

    def test_load_awards_data_returns_dataframe(self, sample_csv):
        """Test that load_awards_data returns a pandas DataFrame."""
        df = load_awards_data(sample_csv)
        assert isinstance(df, pd.DataFrame)

    def test_load_awards_data_has_expected_columns(self, sample_csv):
        """Test that the loaded DataFrame has all expected columns."""
        df = load_awards_data(sample_csv)
        expected_columns = [
            FISCAL_YEAR_COL,
            AWARDS_CONFERRED_COL,
            SEGMENT_COL,
            INSTITUTION_COL,
            AWARD_TYPE_COL,
            AWARD_TYPE_ORDER_COL,
            GENDER_COL,
            RACE_ETHNICITY_COL,
        ]
        assert all(col in df.columns for col in expected_columns)

    def test_load_awards_data_not_empty(self, sample_csv):
        """Test that the loaded DataFrame is not empty."""
        df = load_awards_data(sample_csv)
        assert len(df) > 0

    def test_load_awards_data_numeric_types(self, sample_csv):
        """Test that numeric columns are cast to Int64."""
        df = load_awards_data(sample_csv)
        assert pd.api.types.is_integer_dtype(df[FISCAL_YEAR_COL])
        assert pd.api.types.is_integer_dtype(df[AWARDS_CONFERRED_COL])
        assert pd.api.types.is_integer_dtype(df[AWARD_TYPE_ORDER_COL])


class TestFilterAwardsData:
    """Tests for filter_awards_data function."""

    @pytest.fixture
    def sample_df(self):
        """A sample DataFrame for testing."""
        return pd.DataFrame(
            {
                FISCAL_YEAR_COL: pd.array([2023, 2024, 2024, 2025, 2025], dtype="Int64"),
                AWARDS_CONFERRED_COL: pd.array([5, 10, 20, 15, 25], dtype="Int64"),
                SEGMENT_COL: [
                    "Community Colleges",
                    "Community Colleges",
                    "State Universities",
                    "Community Colleges",
                    "State Universities",
                ],
                INSTITUTION_COL: ["College A", "College A", "University B", "College A", "University B"],
                AWARD_TYPE_COL: ["Certificate", "Certificate", "Associate", "Certificate", "Bachelor"],
                AWARD_TYPE_ORDER_COL: pd.array([1, 1, 2, 1, 3], dtype="Int64"),
                GENDER_COL: ["Female", "Female", "Male", "Female", "Male"],
                RACE_ETHNICITY_COL: ["White", "White", "Hispanic or Latino", "Asian or Pacific Islander", "White"],
            }
        )

    def test_filter_by_year_range(self, sample_df):
        """Test filtering by year range."""
        filtered = filter_awards_data(sample_df, year_min=2024, year_max=2025)
        assert len(filtered) == 2
        assert all(filtered[FISCAL_YEAR_COL] >= 2024)
        assert all(filtered[FISCAL_YEAR_COL] < 2025)

    def test_filter_by_year_min_only(self, sample_df):
        """Test filtering by minimum year only."""
        filtered = filter_awards_data(sample_df, year_min=2024)
        assert len(filtered) == 4
        assert all(filtered[FISCAL_YEAR_COL] >= 2024)

    def test_filter_by_year_max_only(self, sample_df):
        """Test filtering by maximum year only."""
        filtered = filter_awards_data(sample_df, year_max=2024)
        assert len(filtered) == 1
        assert all(filtered[FISCAL_YEAR_COL] < 2024)

    def test_filter_by_exact_year(self, sample_df):
        """Test filtering by exact year using both min and max."""
        filtered = filter_awards_data(sample_df, year_min=2024, year_max=2025)
        assert len(filtered) == 2
        assert all(filtered[FISCAL_YEAR_COL] == 2024)

    def test_filter_by_institution_only(self, sample_df):
        """Test filtering by institution only."""
        filtered = filter_awards_data(sample_df, institution="College A")
        assert len(filtered) == 3
        assert all(filtered[INSTITUTION_COL] == "College A")

    def test_filter_by_year_range_and_institution(self, sample_df):
        """Test filtering by both year range and institution."""
        filtered = filter_awards_data(sample_df, year_min=2024, year_max=2025, institution="University B")
        assert len(filtered) == 1
        assert all(filtered[FISCAL_YEAR_COL] >= 2024)
        assert all(filtered[FISCAL_YEAR_COL] < 2025)
        assert all(filtered[INSTITUTION_COL] == "University B")

    def test_filter_with_no_parameters_returns_copy(self, sample_df):
        """Test that calling filter with no parameters returns a copy of the original."""
        filtered = filter_awards_data(sample_df)
        assert len(filtered) == len(sample_df)
        assert filtered.equals(sample_df)
        # Verify it's a copy, not the same object
        assert filtered is not sample_df

    def test_filter_with_nonexistent_year_range(self, sample_df):
        """Test filtering with a year range that doesn't exist in the data."""
        filtered = filter_awards_data(sample_df, year_min=2099, year_max=2100)
        assert len(filtered) == 0

    def test_filter_with_nonexistent_institution(self, sample_df):
        """Test filtering with an institution that doesn't exist in the data."""
        filtered = filter_awards_data(sample_df, institution="Nonexistent College")
        assert len(filtered) == 0
