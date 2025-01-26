import pytest
from excel_in_python import xlookup, MatchMode, SearchMode

# Define a fixture for the numeric lookup array
@pytest.fixture
def numeric_lookup_array():
    """Fixture to provide a numeric lookup array."""
    return [133, 306, 533, 273, 657, 671, 751, 893, 956, 504, 11, 
            767, 170, 27, 433, 826, 427, 209, 645, 136, 362, 582, 
            862, 313, 197, 1, 715, 54, 397, 178]

# Parametrize test cases with combinations of inputs
@pytest.mark.parametrize(
    "lookup_value, match_mode, search_mode, expected_result, should_sort",
    [
        (27, MatchMode.EXACT, SearchMode.FROM_FIRST, 27, False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, 11, False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, 1, False),
        (27, MatchMode.EXACT, SearchMode.FROM_LAST, 27, False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, 11, False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, 1, False),
        (27, MatchMode.EXACT, SearchMode.BINARY_FROM_FIRST, 27, True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, 11, True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, 1, True),
        (27, MatchMode.EXACT, SearchMode.BINARY_FROM_LAST, 27, True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, 11, True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, 1, True),
    ]
)

def test_xlookup(numeric_lookup_array, lookup_value, match_mode, 
                 search_mode, expected_result, should_sort):
    """Test xlookup with multiple combinations of match and search modes."""
    # Use the fixture-provided array
    lookup_array = sorted(numeric_lookup_array) if should_sort else numeric_lookup_array
    return_array = sorted(numeric_lookup_array) if should_sort else numeric_lookup_array

    # Perform the test
    assert xlookup(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        return_array=return_array,
        match_mode=match_mode,
        search_mode=search_mode
    ) == expected_result
