"""Implementation of the XMATCH function in Python."""
import bisect
import re
import numpy as np
import pandas as pd
from excel_in_python.enums import MatchMode, SearchMode
from excel_in_python.utils import ensure_numpy_array

def xmatch(
    lookup_value, lookup_array, match_mode=MatchMode.EXACT, search_mode=SearchMode.FROM_FIRST
):
    """
    Performs an XMATCH operation, returning the index of the found match.
    """
    if isinstance(search_mode, int):
        try:
            search_mode = SearchMode(search_mode)
        except ValueError as e:
            raise ValueError(f"Invalid search_mode: {search_mode}") from e

    if isinstance(match_mode, int):
        try:
            match_mode = MatchMode(match_mode)
        except ValueError as e:
            raise ValueError(f"Invalid match_mode: {match_mode}") from e

    if not hasattr(lookup_array, "__iter__"):
        raise TypeError("lookup_array must be iterable")

    lookup_array = ensure_numpy_array(lookup_array)

    if lookup_array.size == 0:
        raise ValueError("lookup_array must not be empty")

    if lookup_array.ndim != 1:
        raise ValueError("lookup_array must be 1D")

    # exact_match_indices = np.flatnonzero(lookup_array == lookup_value)
    # if exact_match_indices.size > 0:
    #     match search_mode:
    #         case SearchMode.FROM_FIRST | SearchMode.BINARY_FROM_FIRST:
    #             return exact_match_indices[0]
    #         case SearchMode.FROM_LAST | SearchMode.BINARY_FROM_LAST:
    #             return exact_match_indices[-1]

    match match_mode:
        case MatchMode.EXACT:
            # if from first or from last, use flatnonzero to find the first or last match
            match search_mode:
                case SearchMode.FROM_FIRST:
                    exact_match_indices = np.flatnonzero(lookup_array == lookup_value)
                    if exact_match_indices.size > 0:
                        return exact_match_indices[0]
                case SearchMode.FROM_LAST:
                    exact_match_indices = np.flatnonzero(lookup_array == lookup_value)
                    if exact_match_indices.size > 0:
                        return exact_match_indices[-1]
                case SearchMode.BINARY_FROM_FIRST:
                    # Binary search for the first occurrence
                    idx = np.searchsorted(lookup_array, lookup_value, side='left')
                    if idx < len(lookup_array) and lookup_array[idx] == lookup_value:
                        return idx
                case SearchMode.BINARY_FROM_LAST:
                    # Binary search for the last occurrence
                    idx = np.searchsorted(lookup_array, lookup_value, side='right') - 1
                    if idx >= 0 and lookup_array[idx] == lookup_value:
                        return idx

            return None

        case MatchMode.NEXT_LARGER | MatchMode.NEXT_SMALLER:
            # Store original indices before sorting
            if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.BINARY_FROM_LAST):
                # the data are assumed to be already sorted, so don't sort
                sorted_indices = np.arange(len(lookup_array))  # Identity mapping
                sorted_lookup_array = lookup_array
            else:
                sorted_indices = np.argsort(lookup_array)  # Indices of lookup_array after sorting
                sorted_lookup_array = lookup_array[sorted_indices]  # Sorted values

            # Find the position in the sorted array
            idx = (
                bisect.bisect_left(sorted_lookup_array, lookup_value)
                if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.FROM_FIRST)
                else bisect.bisect_right(sorted_lookup_array, lookup_value)
            )

            # Ensure index stays within valid range
            if match_mode == MatchMode.NEXT_LARGER:
                check_exact_idx = max(idx - 1, 0)
                idx = (check_exact_idx
                       if sorted_lookup_array[check_exact_idx] == lookup_value
                       else min(idx, len(lookup_array) - 1))
            else:  # NEXT_SMALLER
                check_exact_idx = min(idx, len(lookup_array) - 1)
                idx = (check_exact_idx
                       if sorted_lookup_array[check_exact_idx] == lookup_value
                       else max(idx - 1, 0))

            # Map back to original index
            return int(sorted_indices[idx])

        case MatchMode.REGEX | MatchMode.WILDCARD:
            if search_mode in (SearchMode.BINARY_FROM_FIRST, SearchMode.BINARY_FROM_LAST):
                raise ValueError(
                    "BINARY search modes are not supported for WILDCARD or REGEX match modes"
                )

            print(re.escape(str(lookup_value)).replace(r'\\*', '.*').replace(r'\\?', '.'))

            pattern = (
                re.escape(str(lookup_value)).replace(r'\*', '.*').replace(r'\?', '.')
                if match_mode == MatchMode.WILDCARD
                else str(lookup_value)
            )

            regex = re.compile(f'^{pattern}$', re.IGNORECASE)

            matches = pd.Series(lookup_array).str.match(regex.pattern, na=False)
            if matches.any():
                return (matches.idxmax()
                        if search_mode == SearchMode.FROM_FIRST
                        else matches[::-1].idxmax())

    return None
