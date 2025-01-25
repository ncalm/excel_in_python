""" Test xlookup function"""
# import pytest
from excel_in_python import xlookup, MatchMode, SearchMode

# create a constant called NUMERIC_LOOKUP_ARRAY which is an array
# of 30 random integers between 1 and 1000. Use a random sort order
# to make the array unique.
NUMERIC_LOOKUP_ARRAY = [133,
                        306,
                        533,
                        273,
                        657,
                        671,
                        751,
                        893,
                        956,
                        504,
                        11,
                        767,
                        170,
                        27,
                        433,
                        826,
                        427,
                        209,
                        645,
                        136,
                        362,
                        582,
                        862,
                        313,
                        197,
                        1,
                        715,
                        54,
                        397,
                        178]


def helper_xlookup(lookup_value, match_mode, search_mode, expected_result):
    """ Test xlookup function with different match and search modes """
    # If using either binary search mode, the arrays must be sorted
    if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.BINARY_FROM_LAST):
        lookup_array = sorted(NUMERIC_LOOKUP_ARRAY)
        return_array = sorted(NUMERIC_LOOKUP_ARRAY)
    else:
        lookup_array = NUMERIC_LOOKUP_ARRAY
        return_array = NUMERIC_LOOKUP_ARRAY

    assert xlookup(
        lookup_value=lookup_value,
        lookup_array=lookup_array,
        return_array=return_array,
        match_mode=match_mode,
        search_mode=search_mode
        ) == expected_result

def test_xlookup_exact_match_from_first():
    """ Test xlookup function with exact match from first """
    lookup_value = 27
    helper_xlookup(
        lookup_value=lookup_value,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.FROM_FIRST,
        expected_result=lookup_value
        )

def test_xlookup_next_larger_from_first():
    """ Test xlookup function with next larger match from first """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_LARGER,
        search_mode=SearchMode.FROM_FIRST,
        expected_result=11
    )

def test_xlookup_next_smaller_from_first():
    """ Test xlookup function with next smaller match from first """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_SMALLER,
        search_mode=SearchMode.FROM_FIRST,
        expected_result=1
    )

# FROM_LAST

def test_xlookup_exact_match_from_last():
    """ Test xlookup function with exact match from last """
    lookup_value = 27
    helper_xlookup(
        lookup_value=lookup_value,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.FROM_LAST,
        expected_result=lookup_value
        )
    
def test_xlookup_next_larger_from_last():
    """ Test xlookup function with next larger match from last """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_LARGER,
        search_mode=SearchMode.FROM_LAST,
        expected_result=11
    )

def test_xlookup_next_smaller_from_last():
    """ Test xlookup function with next smaller match from last """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_SMALLER,
        search_mode=SearchMode.FROM_LAST,
        expected_result=1
    )

# BINARY_FROM_LAST

def test_xlookup_exact_match_binary_from_last():
    """ Test xlookup function with exact match binary from last """
    lookup_value = 27
    helper_xlookup(
        lookup_value=lookup_value,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.BINARY_FROM_LAST,
        expected_result=lookup_value
        )
    
def test_xlookup_next_larger_binary_from_last():
    """ Test xlookup function with next larger match binary from last """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_LARGER,
        search_mode=SearchMode.BINARY_FROM_LAST,
        expected_result=11
    )

def test_xlookup_next_smaller_binary_from_last():
    """ Test xlookup function with next smaller match from last """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_SMALLER,
        search_mode=SearchMode.BINARY_FROM_LAST,
        expected_result=1
    )

# BINARY_FROM_FIRST

def test_xlookup_exact_match_binary_from_first():
    """ Test xlookup function with exact match from first """
    lookup_value = 27
    helper_xlookup(
        lookup_value=lookup_value,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.BINARY_FROM_FIRST,
        expected_result=lookup_value
        )

def test_xlookup_next_larger_binary_from_first():
    """ Test xlookup function with next larger match from first """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_LARGER,
        search_mode=SearchMode.BINARY_FROM_FIRST,
        expected_result=11
    )

def test_xlookup_next_smaller_binary_from_first():
    """ Test xlookup function with next smaller match from first """
    helper_xlookup(
        lookup_value=10, # doesn't exist in the numeric lookup array
        match_mode=MatchMode.NEXT_SMALLER,
        search_mode=SearchMode.BINARY_FROM_FIRST,
        expected_result=1
    )