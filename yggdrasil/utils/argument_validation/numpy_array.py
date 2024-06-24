"""Collection of functions for validating NumPy arrays."""

from beartype import beartype
import numpy as np

__all__ = [
    "is_numerical_array"
]
@beartype
def is_numerical_array(array: np.ndarray):
    """
    Checks if the input is a numerical NumPy array.

    Parameters:
    array (np.ndarray): The array to check.

    Returns:
    bool: True if the array is a numerical NumPy array, False otherwise.
    """
    return isinstance(array, np.ndarray) and np.issubdtype(array.dtype, np.number)
