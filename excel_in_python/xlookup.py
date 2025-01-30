""" This module provides a Python implementation of the XLOOKUP function in Excel. """
from enum import Enum
import bisect
import re
import numpy as np
import pandas as pd


class MatchMode(Enum):
    """ Enumeration of the different match modes for XLOOKUP. """
    EXACT = 0
    NEXT_LARGER = 1
    NEXT_SMALLER = -1
    WILDCARD = 2
    REGEX = 3


class SearchMode(Enum):
    """ Enumeration of the different search modes for XLOOKUP. """
    FROM_FIRST = 1
    FROM_LAST = -1
    BINARY_FROM_FIRST = 2
    BINARY_FROM_LAST = -2


class LookupOrientation(Enum):
    """ Enumeration of the different orientations for XLOOKUP. """
    HORIZONTAL = 1
    VERTICAL = -1


def extract_result(return_array, selector, orientation):
    """
    Helper function to extract results from return_array based on orientation.

    Args:
        return_array (np.ndarray): The array to extract results from.
        selector: The mask or position index for slicing.
        orientation (LookupOrientation): The orientation of lookup (HORIZONTAL or VERTICAL).

    Returns:
        np.ndarray: The extracted results.
    """
    if orientation == LookupOrientation.HORIZONTAL:
        return return_array[:, selector]  # Slice columns
    else:  # VERTICAL
        return return_array[selector]  # Slice rows


def ensure_numpy_array(obj):
    """
    Converts the input to a NumPy array if it isn't one already.
    """
    return obj if isinstance(obj, np.ndarray) else np.array(obj)

def exact_match(lookup_array, lookup_value, return_array, orientation):
    """ Returns the index of the first exact match in the lookup_array. """
    indices = np.flatnonzero(lookup_array == lookup_value)
    if indices.size > 0:
        idx = indices[0]
        result = extract_result(return_array, idx, orientation)
    else:
        result = None

    return result

def xlookup_single(
        lookup_value,
        lookup_array,
        return_array,
        default=None,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.FROM_FIRST
):
    """ Performs an XLOOKUP operation for a single lookup value. 
    """
    if isinstance(search_mode, int):
        search_mode = SearchMode(search_mode)

    if isinstance(match_mode, int):
        match_mode = MatchMode(match_mode)

    if not hasattr(lookup_array, "__iter__") or not hasattr(return_array, "__iter__"):
        raise TypeError("lookup_array and return_array must be iterable")

    lookup_array = ensure_numpy_array(lookup_array)
    return_array = ensure_numpy_array(return_array)

    if lookup_array.size == 0 or return_array.size == 0:
        raise ValueError("lookup_array and return_array must not be empty")


    if lookup_array.ndim != 1:
        raise ValueError("lookup_array must be 1D")

    len_lookup = len(lookup_array)
    shape_return = return_array.shape
    if len(shape_return) == 1:
        orientation = LookupOrientation.VERTICAL
        if shape_return[0] != len_lookup:
            raise ValueError(
                f"return_array dim. {shape_return} do not match lookup_array length {len_lookup}"
                )
    else:
        if shape_return[0] == len_lookup:
            orientation = LookupOrientation.VERTICAL
        elif shape_return[1] == len_lookup:
            orientation = LookupOrientation.HORIZONTAL
        else:
            raise ValueError(
                "One dimension of return_array must have the same length as lookup_array")

    # if search_mode == SearchMode.FROM_LAST:
    #     lookup_array = lookup_array[::-1]  # lookup_array is always 1D
    #     return_array = (
    #         return_array[:, ::-1]
    #         if orientation == LookupOrientation.HORIZONTAL
    #         else return_array[::-1]
    #     )

    # first we're only concerned with finding the index of the position to extract
    # If there's a match, it doesn't matter what the MatchMode is
    exact_match_indices = np.flatnonzero(lookup_array == lookup_value)
    if exact_match_indices.size == 0:
        exact_match_indices = None

    if exact_match_indices is not None:
        sorted_return_array = return_array
        match search_mode:
            case SearchMode.FROM_FIRST | SearchMode.BINARY_FROM_FIRST:
                idx = exact_match_indices[0]
            case SearchMode.FROM_LAST | SearchMode.BINARY_FROM_LAST:
                idx = exact_match_indices[-1]
            case _:
                idx = exact_match_indices[0]
    else: # No exact match found
        match match_mode:
            case MatchMode.EXACT:
                idx = None
            case MatchMode.NEXT_LARGER | MatchMode.NEXT_SMALLER:
                if search_mode in (SearchMode.FROM_FIRST, SearchMode.FROM_LAST):
                    sorted_lookup_array = np.sort(lookup_array)
                    if orientation == LookupOrientation.HORIZONTAL:
                        sorted_return_array = return_array[:, np.argsort(lookup_array)]
                    else:
                        sorted_return_array = return_array[np.argsort(lookup_array)]
                else:
                    sorted_lookup_array = lookup_array
                    sorted_return_array = return_array


                # For BINARY search modes, the arrays are assumed to be sorted

                if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.FROM_FIRST):
                    # If there's an exact match, return it, otherwise bisect left and find the index
                    # of the first element that is less than lookup_value
                    idx = bisect.bisect_left(sorted_lookup_array, lookup_value)
                else:
                    # If there's an exact match, return it, otherwise bisect right and find the
                    # index of the first element that is greater than lookup_value
                    idx = bisect.bisect_right(sorted_lookup_array, lookup_value)

                if match_mode == MatchMode.NEXT_LARGER:
                    idx = min(idx, len_lookup - 1)
                else:
                    idx = max(idx - 1, 0)

                # result = extract_result(sorted_return_array, idx, orientation)

            case MatchMode.REGEX | MatchMode.WILDCARD:
                sorted_return_array = return_array
                # For both of these match modes, Excel's XLOOKUP returns a #VALUE! error if either
                # of the binary search modes are used
                if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.BINARY_FROM_LAST):
                    raise ValueError(
                        "BINARY search modes are not supported for WILDCARD or REGEX match modes")

                # For WILDCARD and REGEX match modes, lookup_value is treated as a string
                lookup_value = str(lookup_value)

                # if the value is not in the array, return the default value

                # if the match mode is WILDCARD, convert the lookup_value to a valid regex pattern
                pattern = (re.escape(str(lookup_value)).replace(r'\*', '.*').replace(r'\?', '.')
                                if match_mode == MatchMode.WILDCARD
                                else str(lookup_value))
                regex = re.compile(f'^{pattern}$', re.IGNORECASE)

                matches = pd.Series(lookup_array).str.match(regex.pattern, na=False)
                if matches.any():
                    idx = matches.idxmax()
                    # result = extract_result(return_array, idx, orientation)
                else:
                    idx = None
                    # result = default
            case _:
                raise ValueError(f"Invalid match_mode: {match_mode}")

    if idx is not None:
        result = extract_result(sorted_return_array, idx, orientation)
    else:
        result = default

    return result


def xlookup(
        lookup_value,
        lookup_array,
        return_array,
        default=None,
        match_mode=MatchMode.EXACT,
        search_mode=SearchMode.FROM_FIRST
        ):
    """ Performs an XLOOKUP operation for multiple lookup values. """
    if not isinstance(lookup_value, list):
        lookup_value = [lookup_value]

    output = [
        xlookup_single(v, lookup_array, return_array,
                       default, match_mode, search_mode)
        for v in lookup_value
    ]
    return np.array(output)
