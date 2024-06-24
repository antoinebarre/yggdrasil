"""Contains functions for validating NumPy vectors."""

import numpy as np
from beartype import beartype

from .numpy_array import is_numerical_array

__all__ = [
    "is_3d_numpy_vector",
    "assert_3d_numpy_vector"
]

@beartype
def is_3d_numpy_vector(vector: np.ndarray):
    """
    Checks if the input is a 3-dimensional numerical vector represented as a NumPy array.

    Parameters:
    vector (np.ndarray): The vector to check.

    Returns:
    bool: True if the vector is a 3-dimensional NumPy array, False otherwise.
    """
    return is_numerical_array(vector) and vector.ndim == 1 and vector.shape[0] == 3

def assert_3d_numpy_vector(vector:np.ndarray):
    """
    Assert that the input is a 3-dimensional numerical vector represented as a NumPy array.

    Parameters:
    vector (np.ndarray): The vector to validate.

    Raises:
    AssertionError : If the input is not a 3-dimensional NumPy array.
    """
    try:
        assert is_3d_numpy_vector(vector)
    except AssertionError as exc:
        raise AssertionError(
            f"Expected a 3-dimensional NumPy vector, but got {vector} ",
            f"with shape {vector.shape}."
        ) from exc
    except Exception as e:
        raise AssertionError(
            f"An unexpected error occurred: {e}"
        ) from e
