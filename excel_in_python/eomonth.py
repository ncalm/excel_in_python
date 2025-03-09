"""Implements the EOMONTH function in Python.

Returns the serial number for the last day of the month that is the 
indicated number of months before or after start_date. 
Use EOMONTH to calculate maturity dates or due dates that fall on the 
last day of the month.

Syntax
EOMONTH(start_date, months)

The EOMONTH function syntax has the following arguments:

Start_date    Required. A date that represents the starting date. 
    Dates should be entered by using the DATE function, 
    or as results of other formulas or functions. 
    For example, use DATE(2008,5,23) for the 23rd day of May, 2008. 
    Problems can occur if dates are entered as text.

Months    Required. The number of months before or after start_date. 
    A positive value for months yields a future date; a negative value yields a past date.


"""
from datetime import datetime
import math  # For NaN
from collections.abc import Iterable
from dateutil.relativedelta import relativedelta

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
