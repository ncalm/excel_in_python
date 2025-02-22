"""Implements the DATE function in Python."""
from datetime import datetime
import numpy as np

def date(year, month, day):
    """Creates valid dates from year, month, and day inputs, handling overflows and sequences."""

    # Ensure only one argument is an array
    array_args = [isinstance(arg, np.ndarray) for arg in (year, month, day)]

    if sum(array_args) > 1:
        raise ValueError("Only one of year, month, or day may be an array.")

    # If an argument is an array, ensure it is at most 2D
    for arg in (year, month, day):
        if isinstance(arg, np.ndarray) and arg.ndim > 2:
            raise ValueError("year, month, and day must be scalars or 1D or 2D arrays.")

    # Convert the array argument to at least 1D, but leave scalars untouched
    if isinstance(year, np.ndarray):
        array_arg, fixed1, fixed2 = year, month, day
        def func(y):
            return datetime(y, fixed1, fixed2)
    elif isinstance(month, np.ndarray):
        array_arg, fixed1, fixed2 = month, year, day
        def func(m):
            return datetime(fixed1, m, fixed2)
    elif isinstance(day, np.ndarray):
        array_arg, fixed1, fixed2 = day, year, month
        def func(d):
            return datetime(fixed1, fixed2, d)
    else:
        # If all arguments are scalars, just return a single datetime object
        return datetime(year, month, day)

    # Vectorize the function for broadcasting
    vectorized_func = np.vectorize(func)

    return vectorized_func(array_arg)
