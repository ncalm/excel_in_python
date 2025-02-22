"""Tests for the date function in the excel_in_python module."""
from datetime import datetime
import pytest
import numpy as np
from excel_in_python.date import date  # Replace with actual module name

@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        # All scalars
        (2023, 5, 20, datetime(2023, 5, 20)),

        # Year as array
        (np.array([2000, 2001, 2002]), 5, 20,
         [datetime(2000, 5, 20), datetime(2001, 5, 20), datetime(2002, 5, 20)]),

        # Month as array
        (2023, np.array([1, 2, 3]), 15,
         [datetime(2023, 1, 15), datetime(2023, 2, 15), datetime(2023, 3, 15)]),

        # Day as array
        (2023, 5, np.array([10, 20, 30]),
         [datetime(2023, 5, 10), datetime(2023, 5, 20), datetime(2023, 5, 30)]),
    ]
)
def test_date_valid_cases(year, month, day, expected):
    """Test the date function with valid inputs."""
    result = date(year, month, day)
    if isinstance(result, np.ndarray):
        result = result.tolist()  # Convert NumPy array to list for comparison
    assert result == expected


@pytest.mark.parametrize(
    "year, month, day, expected_exception, expected_message",
    [
        # More than one array input
        (np.array([2020, 2021]), np.array([5, 6]), 10, ValueError,
         "Only one of year, month, or day may be an array."),
        (np.array([2020, 2021]), 5, np.array([10, 15]), ValueError,
         "Only one of year, month, or day may be an array."),
        (2023, np.array([5, 6]), np.array([10, 15]), ValueError,
         "Only one of year, month, or day may be an array."),

        # More than 2D arrays
        (np.array([[[2023]]]), 5, 20, ValueError,
         "year, month, and day must be scalars or 1D or 2D arrays."),
        (2023, np.array([[[5]]]), 20, ValueError,
         "year, month, and day must be scalars or 1D or 2D arrays."),
        (2023, 5, np.array([[[20]]]), ValueError,
         "year, month, and day must be scalars or 1D or 2D arrays."),
    ]
)
def test_date_invalid_cases(year, month, day, expected_exception, expected_message):
    """Test the date function with invalid inputs."""
    with pytest.raises(expected_exception, match=expected_message):
        date(year, month, day)
