"""Tests for the utility functions in the excel_in_python module."""
import numpy as np
import pytest
from excel_in_python.utils import ensure_numpy_array

@pytest.mark.parametrize("input_value, expected", [
    ([1, 2, 3], np.array([1, 2, 3])),
    (np.array([1, 2, 3]), np.array([1, 2, 3])),
    ((1, 2, 3), np.array([1, 2, 3])),
    (5, np.array(5))
])
def test_ensure_numpy_array(input_value, expected):
    """Test ensure_numpy_array with various input types."""
    result = ensure_numpy_array(input_value)
    assert isinstance(result, np.ndarray)
    assert np.array_equal(result, expected)
    if isinstance(input_value, np.ndarray):
        assert result is input_value  # Should return the same object if already a NumPy array
