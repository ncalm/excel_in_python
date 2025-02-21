# Excel in Python

**Excel in Python** is a lightweight Python package that provides Excel-like functions for working with tabular data in Python. It aims to bring familiar Excel functions such as `XLOOKUP`, `XMATCH`, and `SEQUENCE` into a Python environment while maintaining efficiency and flexibility.

My intent with this library is to:

a) Offer an opportunity for users familiar with Excel functions to learn more about Python

b) Practice my own Python in implementing Excel functions

c) Offer powerful Excel functions to Python users in other environments by encapsulating the same logic outside of Excel

## Features

This package currently includes the following modules:

- **`xlookup.py`** – Implements Excel's `XLOOKUP` function in Python, allowing flexible lookups with exact, approximate, and wildcard matching.
- **`xmatch.py`** – Implements Excel's `XMATCH` function, providing flexible matching options, including binary search modes.
- **`sequence.py`** – Implements Excel’s `SEQUENCE` function, generating numeric sequences in a structured array format.
- **`utils.py`** – Contains utility functions such as `ensure_numpy_array` to assist with array conversions.
- **`enums.py`** – Defines enums (`MatchMode`, `SearchMode`) for lookup and match functions to improve readability and maintainability.

The package is designed for use cases such as:
- Data transformation and lookups in NumPy and Pandas arrays
- Excel-style formula operations in Python scripts
- Enhancing automation workflows by replacing Excel dependency

---

## Installation

To install `excel_in_python`, first ensure you have Python 3.x installed, then install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

### XLOOKUP

```Python
import numpy as np
from excel_in_python import xlookup
from excel_in_python.enums import MatchMode, SearchMode

lookup_array = np.array([10, 20, 30, 40])
return_array = np.array(["A", "B", "C", "D"])
lookup_value = 20

result = xlookup(lookup_value, lookup_array, return_array)
print(result)  # Output: "B"
```

For more details about how XLOOKUP works in Excel, read the documentation [here](https://support.microsoft.com/en-us/office/xlookup-function-b7fd680e-6d10-43e6-84f9-88eae8bf5929).


### XMATCH

```Python
from excel_in_python import xmatch

lookup_value = 30
match_index = xmatch(lookup_value, lookup_array, match_mode=MatchMode.EXACT)
print(match_index)  # Output: 2 (zero-based index)
```

For more details about how XMATCH works in Excel, read the documentation [here](https://support.microsoft.com/en-us/office/xmatch-function-d966da31-7a6b-4a13-a1c6-5a33ed6a0312).


### SEQUENCE

The `SEQUENCE` function generates an array of sequential numbers, similar to Excel’s `SEQUENCE` function.

```python
from excel_in_python import sequence

# Generate a 3-row by 4-column sequence starting at 1, with a step of 1
seq_array = sequence(3, 4, start=1, step=1)
print(seq_array)
# Output:
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]

# Generate a 2x3 sequence starting at 10, with a step of 5
seq_array = sequence(2, 3, start=10, step=5)
print(seq_array)
# Output:
# [[10 15 20]
#  [25 30 35]]
```

For more details about how SEQUENCE works in Excel, read the documentation [here](https://support.microsoft.com/en-us/office/sequence-function-57467a98-57e0-4817-9f14-2eb78519ca90).


## Contributing

Contributions are welcome! If you’d like to improve `excel_in_python`, feel free to fork the repository, make your changes, and submit a pull request. Issues and feature requests can be reported in the [GitHub Issues](https://github.com/ncalm/excel_in_python/issues) section.

## License

This project is licensed under the **MIT License**, meaning you’re free to use, modify, and distribute it with attribution. See the [`LICENSE`](LICENSE) file for details.
