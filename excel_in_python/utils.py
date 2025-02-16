"""Utility functions for the Excel in Python series."""
import numpy as np

def ensure_numpy_array(obj):
    """Converts the input to a NumPy array if it isn't one already."""
    return obj if isinstance(obj, np.ndarray) else np.array(obj)
