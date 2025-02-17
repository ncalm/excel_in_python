"""Tests for the sequence module."""
import pytest
from excel_in_python.sequence import sequence


# create parameterized inputs for sequence with expected results
@pytest.mark.parametrize(
    "rows, columns, start, step, expected", 
    [
        (1, 1, 1, 1, [[1]]),
        (2, 3, 1, 1, [[1, 2, 3], [4, 5, 6]]),
        (3, 2, 1, 2, [[1, 3], [5, 7], [9, 11]]),
        (1, 1, 2, 1, [[2]]),
        (1, 1, 1, 2, [[1]]),
        (1, 1, 2, 2, [[2]]),
        (1, 1, 1, 1.5, [[1]]),
        (1, 1, 1.5, 1, [[1.5]]),
        (1, 1, 1.5, 1.5, [[1.5]]),
        (1.5, 1, 1, 1, [[1]]),
        (1, 1.5, 1, 1, [[1]]),
        (1.5, 2.5, 1, 1, [[1, 2]]),
    ],
)
def test_sequence(rows, columns, start, step, expected):
    """Test the sequence function."""

    result = sequence(rows, columns, start, step)
    assert result.tolist() == expected