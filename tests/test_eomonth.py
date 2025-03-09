"""Unit tests for the eomonth function."""
from datetime import datetime
import math
import pytest
from excel_in_python.date import eomonth  # Update with the actual module name

@pytest.mark.parametrize(
    "start_date, months, expected",
    [
        # Basic forward cases
        (datetime(2023, 1, 15), 2, datetime(2023, 3, 31).date()),  # Normal case, forward
        (datetime(2023, 1, 31), 1, datetime(2023, 2, 28).date()),  # End of month, Feb non-leap
        (datetime(2024, 1, 31), 1, datetime(2024, 2, 29).date()),  # End of month, Feb leap year

        # Basic backward cases
        (datetime(2023, 3, 10), -1, datetime(2023, 2, 28).date()),  # Backward to Feb non-leap
        (datetime(2024, 3, 10), -1, datetime(2024, 2, 29).date()),  # Backward to Feb leap year
        (datetime(2023, 3, 31), -2, datetime(2023, 1, 31).date()),  # Backward multiple months

        # Edge cases
        (datetime(2023, 12, 15), 1, datetime(2024, 1, 31).date()),  # Year transition forward
        (datetime(2024, 1, 15), -1, datetime(2023, 12, 31).date()), # Year transition backward

        # Same month cases
        (datetime(2023, 5, 10), 0, datetime(2023, 5, 31).date()),  # Stay in the same month
        (datetime(2023, 7, 31), 0, datetime(2023, 7, 31).date()),  # Already last day

        # Large jumps
        (datetime(2000, 1, 1), 240, datetime(2020, 1, 31).date()),  # Large forward jump
        (datetime(2023, 8, 15), -100, datetime(2015, 4, 30).date()), # Large backward jump
    ]
)
def test_eomonth(start_date, months, expected):
    """Test the eomonth function with various inputs."""
    assert eomonth(start_date, months) == expected

# Test vectorized behavior with iterables
@pytest.mark.parametrize(
    "start_dates, months, expected",
    [
        # List of valid dates
        ([datetime(2023, 1, 15), datetime(2023, 6, 20), datetime(2024, 2, 29)], 2,
         [datetime(2023, 3, 31).date(), datetime(2023, 8, 31).date(),
          datetime(2024, 4, 30).date()]),

        # List with invalid elements
        ([datetime(2023, 1, 15), "invalid", datetime(2024, 2, 29), 42, None], 2,
         [datetime(2023, 3, 31).date(), math.nan, datetime(2024, 4, 30).date(),
          math.nan, math.nan]),

        # Empty list should return empty list
        ([], 2, []),

        # All invalid values
        (["not a date", 123, None], 2, [math.nan, math.nan, math.nan]),
    ]
)
def test_eomonth_vectorized(start_dates, months, expected):
    """Test eomonth function with iterables and invalid values."""
    result = eomonth(start_dates, months)

    # Handle NaN comparison correctly
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        if isinstance(e, float) and math.isnan(e):
            assert math.isnan(r)
        else:
            assert r == e

# Exception handling tests for invalid single inputs
def test_eomonth_invalid_inputs():
    """Test the eomonth function with invalid inputs."""
    with pytest.raises(ValueError, match="start_date must be a datetime object."):
        eomonth("2023-01-15", 2)  # Invalid date type

    with pytest.raises(ValueError, match="months must be an integer."):
        eomonth(datetime(2023, 1, 15), "2")  # Invalid months type
