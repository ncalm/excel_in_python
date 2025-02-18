"""Tests for the sequence module."""
import pytest
import numpy as np
from excel_in_python.sequence import sequence, MAX_ELEMENTS


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
        # tests with multiple rows and decimal step
        (3, 2, 1, 0.5, [[1, 1.5], [2, 2.5], [3, 3.5]]),
        (3, 2, 1.5, 0.5, [[1.5, 2], [2.5, 3], [3.5, 4]]),
        (3, 2, 1, 0.1, [[1, 1.1], [1.2, 1.3], [1.4, 1.5]]),
        (3, 2, 1.5, 0.1, [[1.5, 1.6], [1.7, 1.8], [1.9, 2]]),
        # tests with one row, multiple columns, and decimal step
        (1, 3, 1, 0.5, [[1, 1.5, 2]]),
        (1, 3, 1.5, 0.5, [[1.5, 2, 2.5]]),
        (1, 3, 1, 0.1, [[1, 1.1, 1.2]]),
        (1, 3, 1.5, 0.1, [[1.5, 1.6, 1.7]]),
        # tests with multiple rows, one column, decimal start and negative decimal step
        (3, 1, 1.5, -0.5, [[1.5], [1], [0.5]]),
        (3, 1, 1.5, -0.1, [[1.5], [1.4], [1.3]]),
        (3, 1, 1.5, -0.01, [[1.5], [1.49], [1.48]]),
        # tests with multiple rows, multiple columns, negative start and negative decimal step
        (3, 2, -1, -0.5, [[-1, -1.5], [-2, -2.5], [-3, -3.5]]),
        (3, 2, -1.5, -0.5, [[-1.5, -2], [-2.5, -3], [-3.5, -4]]),
        (3, 2, -1, -0.1, [[-1, -1.1], [-1.2, -1.3], [-1.4, -1.5]]),
        (3, 2, -1.5, -0.1, [[-1.5, -1.6], [-1.7, -1.8], [-1.9, -2]]),
        # test where rows is omitted
        (None, 2, 1, 1, [[1, 2]]),
        # tests where columns is omitted
        (2, None, 1, 1, [[1], [2]]),
        # tests where start is omitted
        (2, 2, None, 1, [[1, 2], [3, 4]]),
        # tests where step is omitted
        (2, 2, 1, None, [[1, 2], [3, 4]]),
        # tests where all arguments are omitted
        (None, None, None, None, [[1]]),
    ],
)
def test_sequence(rows, columns, start, step, expected):
    """Test the sequence function."""
    args = {k: v
            for k, v
            in zip(["rows", "columns", "start", "step"], (rows, columns, start, step))
            if v is not None}
    result = sequence(**args)

    assert result.tolist() == expected
    assert result.shape == (np.floor(rows or 1), np.floor(columns or 1))


# test for invalid inputs
def test_invalid_sequence():
    """Test the sequence function with invalid inputs."""

    # test with negative rows
    with pytest.raises(ValueError):
        sequence(-1, 1, 1, 1)

    # test with negative columns
    with pytest.raises(ValueError):
        sequence(1, -1, 1, 1)

    # test with non-numeric arguments
    with pytest.raises(ValueError):
        sequence("a", 1, 1, 1)

    # test with non-numeric arguments
    with pytest.raises(ValueError):
        sequence(1, "a", 1, 1)

    # test with non-numeric arguments
    with pytest.raises(ValueError):
        sequence(1, 1, "a", 1)

    # test with non-numeric arguments
    with pytest.raises(ValueError):
        sequence(1, 1, 1, "a")

def test_sequence_max_elements():
    """Test that sequence raises MemoryError when exceeding MAX_ELEMENTS."""
    max_rows = MAX_ELEMENTS // 10  # Ensure product exceeds MAX_ELEMENTS
    max_cols = 11

    with pytest.raises(MemoryError, match="Requested array is too large"):
        sequence(max_rows, max_cols)

def test_large_sequence():
    """Test large but valid sequence generation does not fail."""
    large_seq = sequence(1000, 1000)  # 1 million elements (should work)
    assert large_seq.shape == (1000, 1000)
    assert large_seq[0, 0] == 1  # Start value
    assert large_seq[-1, -1] == 1 + (1000 * 1000 - 1)  # Last value

def test_sequence_step_zero():
    """Test sequence with step=0 returns a constant array."""
    result = sequence(3, 3, start=5, step=0)
    assert np.all(result == 5)
    assert result.shape == (3, 3)

@pytest.mark.parametrize("rows, columns", [(-1, 3), (3, -1), (-2, -2)])
def test_sequence_negative_rows_columns(rows, columns):
    """Test that sequence raises ValueError for negative row or column values."""
    with pytest.raises(ValueError, match="rows and columns must be at least 1"):
        sequence(rows, columns)
