"""Python implementation of Excel's SEQUENCE function

Any missing optional arguments will default to 1. If you omit the rows argument, you must provide 
at least one other argument.

An array can be thought of as a row of values, a column of values, or a combination of rows 
and columns of values. In the example above, the array for our SEQUENCE formula is range C1:G4.

The SEQUENCE function will return an array, which will spill if it's the final result of a formula. 
This means that Excel will dynamically create the appropriate sized array range when you press 
ENTER. If your supporting data is in an Excel table, then the array will automatically resize as 
you add or remove data from your array range if you're using structured references. For more 
details, see this article on spilled array behavior.

Excel has limited support for dynamic arrays between workbooks, and this scenario is only 
supported when both workbooks are open. If you close the source workbook, any linked dynamic 
array formulas will return a #REF! error when they are refreshed.
"""
import numpy as np

MAX_ELEMENTS = 10**7  # Safety limit to prevent excessive memory usage

def sequence(rows=1, columns=1, start=1, step=1):
    """Return a 2D array of sequential numbers, mimicking Excel's SEQUENCE behavior."""


    if not all(isinstance(arg, (int, float)) for arg in (rows, columns, start, step)):
        raise ValueError("All arguments must be numeric")

    if rows < 1 or columns < 1:
        raise ValueError("rows and columns must be at least 1")

    rows, columns = int(np.floor(rows)), int(np.floor(columns))
    total_elements = rows * columns

    if total_elements > MAX_ELEMENTS:
        raise MemoryError("Requested array is too large")

    if step == 0:
        values = np.full(total_elements, start)  # Fill with `start` if step is 0
    else:
        values = start + step * np.arange(total_elements)

    return values.reshape((rows, columns))
