"""Test cases for the xlookup function."""
import pytest
from excel_in_python import xlookup, MatchMode, SearchMode
import numpy as np

# Define a fixture for the numeric lookup array
@pytest.fixture
def data():
    """Fixture to provide a numeric lookup array."""
    lookup = [133, 306, 533, 273, 657, 671, 751, 893, 956, 504, 11,
        767, 170, 27, 433, 826, 427, 209, 645, 136, 362, 582,
        862, 313, 197, 1, 715, 54, 397, 178, 209]

    # create a list called text_values from a cycler of greek letter spelled out
    text_values = [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
        "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho",
        "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega", "alpha", "beta",
        "gamma", "delta", "epsilon", "zeta", "eta"
    ]
    return list(zip(lookup, text_values))


# Parametrize test cases with combinations of inputs
@pytest.mark.parametrize(
    "lookup_value, match_mode, search_mode, expected_result, should_sort",
    [
        (209, MatchMode.EXACT, SearchMode.FROM_FIRST, 'sigma', False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, 'lambda', False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, 'beta', False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, 'sigma', False), # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, 'sigma', False), # exact if exists
        (209, MatchMode.EXACT, SearchMode.FROM_LAST, 'eta', False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, 'lambda', False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, 'beta', False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, 'eta', False), # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, 'eta', False), # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_FIRST, 'sigma', True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, 'lambda', True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, 'beta', True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, 'sigma', True), # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, 'sigma', True), # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_LAST, 'eta', True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, 'lambda', True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, 'beta', True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, 'eta', True), # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, 'eta', True), # exact if exists
    ]
)

def test_xlookup(data, lookup_value, match_mode,
                 search_mode, expected_result, should_sort):
    """Test xlookup with multiple combinations of match and search modes."""
    # Use the fixture-provided array
    # TODO: Ensure this handles horizontal orientation
    numeric_lookup_array = np.array([i for i, _ in data])
    text_return_array = np.array([t for _, t in data])
    sort_indices = np.argsort(numeric_lookup_array,None)
    lookup_array = numeric_lookup_array[sort_indices] if should_sort else numeric_lookup_array
    return_array = text_return_array[sort_indices] if should_sort else text_return_array

    # Perform the test
    assert xlookup(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        return_array=return_array,
        match_mode=match_mode,
        search_mode=search_mode
    ) == expected_result
