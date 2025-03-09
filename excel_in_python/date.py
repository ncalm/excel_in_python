"""Date related Excel functions"""
from datetime import datetime
import math  # For NaN
from collections.abc import Iterable
import numpy as np
from dateutil.relativedelta import relativedelta

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


def eomonth(start_date, months):
    """Returns the last day of the month that is the indicated number of 
    months before or after start_date.

    If start_date is an iterable, applies the function to each element.
    If an element is not a datetime object, returns NaN for that element.
    """

    def compute_eomonth(date):
        if isinstance(date, datetime):
            return (date + relativedelta(months=months, day=31)).date()
        return math.nan  # Return NaN for invalid elements

    if isinstance(start_date, Iterable) and not isinstance(start_date, (str, datetime)):
        return [compute_eomonth(date) for date in start_date]

    if not isinstance(start_date, datetime):
        raise ValueError("start_date must be a datetime object.")
    if not isinstance(months, int):
        raise ValueError("months must be an integer.")

    return compute_eomonth(start_date)
