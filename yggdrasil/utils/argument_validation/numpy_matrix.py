

from beartype import beartype
import numpy as np
from numpy.typing import NDArray
from .numpy_array import is_numerical_array

@beartype
def is_3x3_numerical_matrix(matrix: NDArray[np.number]) -> bool:
    """
    Checks if the input is a 3x3 numerical matrix.

    Parameters:
        matrix (NDArray[np.number]): The matrix to check.

    Returns:
        bool: True if the matrix is a 3x3 numerical matrix, False otherwise.
    """
    return is_numerical_array and matrix.shape == (3, 3)

def assert_3x3_numerical_matrix(matrix: NDArray[np.number]) -> None:
    """
    Assert that the input is a 3x3 numerical matrix.

    Parameters:
        matrix (NDArray[np.number]): The matrix to check.
    """
    try:
        assert is_3x3_numerical_matrix(matrix)
    except AssertionError as exc:
        raise AssertionError(
            f"Expected a 3x3 numerical matrix, but got {matrix}",
            f"with shape {matrix.shape}."
        ) from exc
    except Exception as e:
        raise AssertionError(
            f"An unexpected error occurred: {e}"
        ) from e