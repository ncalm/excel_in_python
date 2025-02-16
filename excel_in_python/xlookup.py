"""Implementation of the XLOOKUP function in Python."""
import numpy as np
from excel_in_python.xmatch import xmatch
from excel_in_python.enums import MatchMode, SearchMode
from excel_in_python.utils import ensure_numpy_array


def extract_result(return_array, selector, orientation):
    """
    Helper function to extract results from return_array based on the index selector.
    """

    return return_array[selector] if orientation == "vertical" else return_array[:, selector]



def xlookup(
    lookup_value,
    lookup_array,
    return_array,
    default=None,
    match_mode=MatchMode.EXACT,
    search_mode=SearchMode.FROM_FIRST,
):
    """
    Performs an XLOOKUP operation using xmatch to find the index.
    """
    lookup_array = ensure_numpy_array(lookup_array)
    return_array = ensure_numpy_array(return_array)

    if lookup_array.size == 0 or return_array.size == 0:
        raise ValueError("lookup_array and return_array must not be empty")

    if lookup_array.ndim != 1:
        raise ValueError("lookup_array must be 1D")

    if (
        return_array.ndim > 1
        and return_array.shape[0] != lookup_array.shape[0]
        and return_array.shape[1] != lookup_array.shape[0]
    ):
        raise ValueError(
            "One dimension of return_array must have the same length as lookup_array"
        )
    
    # if return_array is 1D, it must be the same length as lookup_array
    if return_array.ndim == 1 and return_array.size != lookup_array.size:
        raise ValueError("1D return_array must have the same length as lookup_array")

    # If len lookup_array is the same as the first dimension of return_array
    # then the orientation is vertical, otherwise it is horizontal
    orientation = "vertical" if return_array.shape[0] == lookup_array.size else "horizontal"

    indices = np.array([
        xmatch(val, lookup_array, match_mode, search_mode)
        for val in np.atleast_1d(lookup_value)
    ])

    results = np.array([
        extract_result(return_array, idx, orientation) if idx is not None else default for idx in indices
    ])

    return results if isinstance(lookup_value, list) else results[0]
