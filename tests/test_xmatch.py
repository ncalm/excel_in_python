"""Test cases for the xmatch function."""
import pytest
import numpy as np
from excel_in_python import xmatch
from excel_in_python.enums import MatchMode, SearchMode


@pytest.fixture
def data():
    """Fixture to provide a numeric lookup array with a text return array."""
    lookup = [133, 306, 533, 273, 657, 671, 751, 893, 956, 504, 11,
              767, 170, 27, 433, 826, 427, 209, 645, 136, 362, 582,
              862, 313, 197, 1, 715, 54, 397, 178, 209]

    return lookup


# Parametrize test cases with combinations of inputs
@pytest.mark.parametrize(
    "lookup_value, match_mode, search_mode, expected_result, should_sort",
    [
        (209, MatchMode.EXACT, SearchMode.FROM_FIRST, 17, False),

        # to test integers instead of enum values
        (209, 0, 1, 17, False),

        # test exact match with a number not in the array
        (1000, MatchMode.EXACT, SearchMode.FROM_FIRST, None, False),

        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, 10, False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, 25, False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_FIRST, 17, False),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_FIRST, 17, False),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.FROM_LAST, 30, False),
        (10, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, 10, False),
        (10, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, 25, False),
        (209, MatchMode.NEXT_LARGER, SearchMode.FROM_LAST, 30, False),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.FROM_LAST, 30, False),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_FIRST, 17, True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, 10, True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, 25, True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_FIRST, 17, True),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_FIRST, 17, True),  # exact if exists
        (209, MatchMode.EXACT, SearchMode.BINARY_FROM_LAST, 30, True),
        (10, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, 10, True),
        (10, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, 25, True),
        (209, MatchMode.NEXT_LARGER, SearchMode.BINARY_FROM_LAST, 30, True),  # exact if exists
        (209, MatchMode.NEXT_SMALLER, SearchMode.BINARY_FROM_LAST, 30, True),  # exact if exists
    ]
)
def test_xmatch(data, lookup_value, match_mode,
                 search_mode, expected_result, should_sort):
    """Test xmatch with multiple combinations of match and search modes."""
    # the return array is always the text return array
    # transpose the return array if the orientation is horizontal
    # (this makes text_return array 5 rows and 31 columns, while lookup_array is 1D and 31 elements)

    # add the original indices to the lookup array
    numeric_lookup_array = np.array(data)

    # Sort only if binary search mode is used
    if should_sort:
        sort_indices = np.argsort(numeric_lookup_array)  # Indices after sorting
        lookup_array = numeric_lookup_array[sort_indices]  # Sorted lookup array
        expected_result = sort_indices[expected_result]  # Map expected index to sorted position
    else:
        lookup_array = numeric_lookup_array


    # if should_sort is true, sort the numeric_lookup_array by the first column
    # lookup_array = (np.sort(numeric_lookup_array[:, 1]) 
                    # if should_sort else numeric_lookup_array[:, 1])

    # Perform the test
    assert np.all(xmatch(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        match_mode=match_mode,
        search_mode=search_mode
    ) == expected_result)


@pytest.fixture
def text_lookup_data():
    """Fixture to provide a text lookup array and a text return array for regex and wildcard."""
    # define an array of 30 fake addresses. Each address should be a tuple of 3 elements
    # (street, city, state)
    # there should be various cities and states
    # the streets should be suitable for regex matching

    addresses = [
        ("777 Aspen Ct", "Hilltop", "IL"),
        ("753 Summer Rd", "Lakeside", "TX"),
        ("555 Birch Blvd", "Brookfield", "IL"),
        ("101 Pine Rd", "Rivertown", "CA"),
        ("123 Main St", "Brookfield", "TX"),
        ("369 Mountain Ave", "Springfield", "PA"),
        ("2468 Lexington Rd", "Lakeside", "FL"),
        ("34 Second Ave", "Hilltop", "NY"),
        ("5678 Sunset Blvd", "Rivertown", "OH"),
        ("999 Willow Ter", "Pinecrest", "WA"),
        ("456 Elm St", "Fairview", "TX"),
        ("789 Oak Ave", "Brookfield", "CA"),
        ("12 First St", "Meadowvale", "PA"),
        ("4321 Park Ave", "Hilltop", "FL"),
        ("101 Pine Rd", "Springfield", "NY"),
        ("56 Third Blvd", "Brookfield", "WA"),
        ("753 Summer Rd", "Meadowvale", "IL"),
        ("357 Winter Cir", "Fairview", "TX"),
        ("1357 Madison Ln", "Lakeside", "OH"),
        ("951 Fall Ave", "Meadowvale", "FL"),
        ("852 Riverside Dr", "Brookfield", "CA"),
        ("741 Lakeview Rd", "Springfield", "TX"),
        ("2468 Lexington Rd", "Fairview", "IL"),
        ("159 Spring St", "Pinecrest", "WA"),
        ("258 Ocean Blvd", "Springfield", "NY"),
        ("369 Valley Cir", "Lakeside", "CA"),
        ("147 Hillside Ln", "Meadowvale", "OH"),
        ("9101 Broadway St", "Hilltop", "PA"),
        ("5678 Sunset Blvd", "Pinecrest", "FL"),
        ("78 Fourth Dr", "Rivertown", "IL")
    ]

    return addresses

# Parametrize test cases for regex and wildcard using the text_lookup_data fixture.
# the lookup_value should be "Blvd$" for regex and "* Blvd" for wildcard
@pytest.mark.parametrize(
    "lookup_value, match_mode, search_mode, expected_result, should_sort",
    [
        (".*Blvd$", MatchMode.REGEX, SearchMode.FROM_FIRST, 2, False),
        (".*Blvd$", MatchMode.REGEX, SearchMode.FROM_LAST, 10, False),
        ("* Blvd", MatchMode.WILDCARD, SearchMode.FROM_FIRST, 2, False),
        ("* Blvd", MatchMode.WILDCARD, SearchMode.FROM_LAST, 10, False),

        # regex match that has no matches
        (".*Boulvd$", MatchMode.REGEX, SearchMode.FROM_FIRST, [], False),
    ]
)
def test_xmatch_text(text_lookup_data, lookup_value, match_mode,
                      search_mode, expected_result, should_sort):
    """Test xmatch with multiple combinations of match and search modes for text."""

    # create a lookup array that is the street names
    lookup_array = np.array([street for street, _, _ in text_lookup_data])
    sort_indices = np.argsort(lookup_array, None)
    lookup_array = lookup_array[sort_indices] if should_sort else lookup_array

    # Perform the test
    assert np.all(xmatch(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        match_mode=match_mode,
        search_mode=search_mode
    ) == expected_result)

def test_xmatch_empty_arrays():
    """Test that xmatch raises ValueError when lookup_array is empty."""
    empty_array = np.array([])

    with pytest.raises(ValueError, match="lookup_array must not be empty"):
        xmatch(1, empty_array)

# test where lookup_array is not 1 dimensional
def test_xmatch_2d_array():
    """Test that xmatch raises ValueError when lookup_array is not 1D."""
    lookup_array = np.array([[1, 2], [3, 4]])

    with pytest.raises(ValueError, match="lookup_array must be 1D"):
        xmatch(1, lookup_array)

# test for invalid search_mode
def test_xmatch_invalid_search_mode():
    """Test that xmatch raises ValueError when an invalid search_mode is provided."""
    lookup_array = np.array([1, 2, 3])

    with pytest.raises(ValueError, match="Invalid search_mode"):
        xmatch(1, lookup_array, search_mode=5)

# test for invalid match_mode
def test_xmatch_invalid_match_mode():
    """Test that xmatch raises ValueError when an invalid match_mode is provided."""
    lookup_array = np.array([1, 2, 3])

    with pytest.raises(ValueError, match="Invalid match_mode"):
        xmatch(1, lookup_array, match_mode=5)

# test for regex and binary search modes
def test_xmatch_regex_and_binary():
    """Test that xmatch raises ValueError when regex is used with binary search mode."""
    lookup_array = np.array([1, 2, 3])

    with pytest.raises(
        ValueError,
        match="BINARY search modes are not supported for WILDCARD or REGEX match modes"):
        xmatch(4, lookup_array,
               match_mode=MatchMode.REGEX, search_mode=SearchMode.BINARY_FROM_FIRST)

# test for wildcard and binary search modes
def test_xmatch_wildcard_and_binary():
    """Test that xmatch raises ValueError when wildcard is used with binary search mode."""
    lookup_array = np.array([1, 2, 3])

    with pytest.raises(
        ValueError,
        match="BINARY search modes are not supported for WILDCARD or REGEX match modes"):
        xmatch(4, lookup_array,
               match_mode=MatchMode.WILDCARD, search_mode=SearchMode.BINARY_FROM_FIRST)

# test that lookup_array must be iterable
def test_xmatch_lookup_array_not_iterable():
    """Test that xmatch raises TypeError when lookup_array is not iterable."""
    lookup_array = 1

    with pytest.raises(TypeError, match="lookup_array and return_array must be iterable"):
        xmatch(1, lookup_array)
