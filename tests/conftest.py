"""Conftest.py is a feature provided by pytest to let you reuse data structures across unit tests."""

import os
from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir():
    """A folder storing example file inputs for unit tests"""
    return Path(os.path.dirname(os.path.realpath(__file__))) / "test_data"


@pytest.fixture
def sample_csv(test_data_dir):
    """A CSV file structured like the original Public Postseconday Awards (Degrees) detailed
    from the Massachusetts Education-toCareer Research and Data Hub. This CSV file is available to all unit tests"""
    return test_data_dir / "sample_data.csv"
