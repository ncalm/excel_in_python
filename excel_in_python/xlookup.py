""" This module provides a Python implementation of the XLOOKUP function in Excel. """
from enum import Enum
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
            raise ValueError(f"return_array dimensions {
                             shape_return} do not match lookup_array length {len_lookup}")
    else:
        if shape_return[0] == len_lookup:
            orientation = LookupOrientation.VERTICAL
        elif shape_return[1] == len_lookup:
            orientation = LookupOrientation.HORIZONTAL
        else:
            raise ValueError(
                "One dimension of return_array must have the same length as lookup_array")

    if search_mode == SearchMode.FROM_LAST:
        lookup_array = lookup_array[::-1]  # lookup_array is always 1D
        return_array = (
            return_array[:, ::-1]
            if orientation == LookupOrientation.HORIZONTAL
            else return_array[::-1]
        )

    match match_mode:
        case MatchMode.EXACT:
            indices = np.flatnonzero(lookup_array == lookup_value)
            if indices.size > 0:
                idx = indices[0]
                result = extract_result(return_array, idx, orientation)
            else:
                result = default
        case MatchMode.NEXT_LARGER | MatchMode.NEXT_SMALLER:
            # Either find the exact match or find the item that is next in the array if the array
            # were sorted
            # for FROM_FIRST, the array is sorted in ascending order
            # for FROM_LAST, the array is sorted in descending order
            # for BINARY_FROM_FIRST, the array is assumed to be sorted in ascending order
            # for BINARY_FROM_LAST, the array is assumed to be sorted in descending order
            match search_mode:
                case SearchMode.FROM_FIRST | SearchMode.FROM_LAST:
                    # the program sorts the data
                    sort_indices = (
                        np.argsort(lookup_array)
                        if search_mode == SearchMode.FROM_FIRST
                        else np.argsort(lookup_array)[::-1]
                    )
                    sorted_lookup_array = lookup_array[sort_indices]
                    sorted_return_array = extract_result(
                        return_array, sort_indices, orientation)
                    print(f"{sorted_lookup_array=}")
                    # print(f"{sorted_return_array=}")
                case SearchMode.BINARY_FROM_FIRST:
                    # the data are already sorted
                    sorted_lookup_array = lookup_array
                    sorted_return_array = return_array
                case SearchMode.BINARY_FROM_LAST:
                    # the data are already sorted, but we reverse it in it's current state
                    sorted_lookup_array = lookup_array[::-1]
                    sorted_return_array = (
                        return_array[:, ::-1]
                        if orientation == LookupOrientation.HORIZONTAL
                        else return_array[::-1]
                    )
                case _:
                    raise ValueError(f"Invalid search_mode: {search_mode}")

            # finds the position at which the lookup_value would be inserted in the lookup_array
            # TODO: This doesn't work for arrays sorted in descending order, so we need to fix it
            pos = (np.searchsorted(sorted_lookup_array, lookup_value, side="left")
                   if match_mode == MatchMode.NEXT_LARGER
                   else np.searchsorted(sorted_lookup_array, lookup_value, side="right") - 1)
            
            print(f"{pos=}")

            # providing the position found is a valid position in the lookup_array
            if 0 <= pos < len(sorted_lookup_array):
                # return the value from the return_array at the position found
                result = extract_result(sorted_return_array, pos, orientation)
            else:
                # if the position is not valid, return the default value
                result = default

        case MatchMode.REGEX | MatchMode.WILDCARD:
            # For both of these match modes, Excel's XLOOKUP returns a #VALUE! error if either of
            # the binary search modes are used
            if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.BINARY_FROM_LAST):
                raise ValueError(
                    "BINARY search modes are not supported for WILDCARD or REGEX match modes")

            # For WILDCARD and REGEX match modes, lookup_value is treated as a string
            lookup_value = str(lookup_value)

            # if the value is not in the array, return the default value

            # if the match mode is WILDCARD, we convert the lookup_value to a valid regex pattern
            regex_pattern = (re.escape(str(lookup_value)).replace(r'\*', '.*').replace(r'\?', '.')
                             if match_mode == MatchMode.WILDCARD else str(lookup_value))
            regex = re.compile(f'^{regex_pattern}$', re.IGNORECASE)

            matches = pd.Series(lookup_array).str.match(
                regex.pattern, na=False)
            if matches.any():
                idx = matches.idxmax()
                result = extract_result(return_array, idx, orientation)
            else:
                result = default
        case _:
            raise ValueError(f"Invalid match_mode: {match_mode}")

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
