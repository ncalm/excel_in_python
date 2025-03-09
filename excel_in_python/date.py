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


# def eomonth(start_date, months):
#     """Returns the last day of the month that is the indicated number of
#     months before or after start_date.

#     If start_date is an iterable, applies the function to each element.
#     If an element is not a datetime object, returns NaN for that element.
#     """

#     def compute_eomonth(date_scalar):
#         if isinstance(date_scalar, datetime):
#             return (date_scalar + relativedelta(months=months, day=31)).date()
#         return math.nan  # Return NaN for invalid elements

#     if isinstance(start_date, Iterable) and not isinstance(start_date, (str, datetime)):
#         return [compute_eomonth(date) for date in start_date]

#     if not isinstance(start_date, datetime):
#         raise ValueError("start_date must be a datetime object.")
#     if not isinstance(months, int):
#         raise ValueError("months must be an integer.")

#     return compute_eomonth(start_date)


def _adjust_date(start_date, months, day=None):
    """Generalized function to adjust a date by a given number of months.

    If `day` is specified (e.g., 31), it moves to the last day of the target month (EOMONTH).
    If `day` is None, it keeps the same day of the month if possible (EDATE).
    """
    if isinstance(start_date, datetime):
        if day is None:
            return (start_date + relativedelta(months=months)).date()
        return (start_date + relativedelta(months=months, day=31)).date()
    return math.nan  # Return NaN for invalid elements

def _adjust_month(start_date, months, day=None):
    """Adjusts the date by a given number of months.

    - If `day=None`, it behaves like `EDATE`.
    - If `day=31`, it behaves like `EOMONTH`.

    If `start_date` is an iterable, applies the function to each element.
    Returns NaN for invalid elements in iterables.
    """

    if isinstance(start_date, Iterable) and not isinstance(start_date, (str, datetime)):
        return [_adjust_date(date, months, day) for date in start_date]

    if not isinstance(start_date, datetime):
        raise ValueError("start_date must be a datetime object.")
    if not isinstance(months, int):
        raise ValueError("months must be an integer.")

    return _adjust_date(start_date, months, day)

# Define EDATE and EOMONTH using the helper function
def edate(start_date, months):
    """Returns the date that is the indicated number of months before or after start_date."""
    return _adjust_month(start_date, months, day=None)

def eomonth(start_date, months):
    """Returns the last day of the month that is the indicated number of months before or
    after start_date."""
    return _adjust_month(start_date, months, day=31)
