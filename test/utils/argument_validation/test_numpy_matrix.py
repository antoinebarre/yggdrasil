import pytest
import numpy as np
from numpy.typing import NDArray
from yggdrasil.utils.argument_validation.numpy_matrix import (
    is_3x3_numerical_matrix,
    assert_3x3_numerical_matrix)

def mock_is_numerical_array(arr: NDArray[np.number]) -> bool:
    """
    Mock implementation of is_numerical_array for testing purposes.

    Parameters:
        arr (NDArray[np.number]): The array to check.

    Returns:
        bool: True if arr is a numerical numpy array, False otherwise.
    """
    return isinstance(arr, np.ndarray) and np.issubdtype(arr.dtype, np.number)

@pytest.fixture(autouse=True)
def patch_is_numerical_array(monkeypatch) -> None:
    """
    Fixture to patch is_numerical_array with a mock implementation.

    Parameters:
        monkeypatch: pytest's monkeypatch fixture.
    """
    monkeypatch.setattr(
        'yggdrasil.utils.argument_validation.numpy_array.is_numerical_array',
        mock_is_numerical_array)

def test_is_3x3_numerical_matrix_valid() -> None:
    """
    Test is_3x3_numerical_matrix with a valid 3x3 numerical matrix.
    """
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert is_3x3_numerical_matrix(matrix) is True


def test_is_3x3_numerical_matrix_wrong_shape() -> None:
    """
    Test is_3x3_numerical_matrix with a matrix that is not 3x3.
    """
    matrix = np.array([[1, 2], [3, 4]])
    assert is_3x3_numerical_matrix(matrix) is False


def test_assert_3x3_numerical_matrix_valid() -> None:
    """
    Test assert_3x3_numerical_matrix with a valid 3x3 numerical matrix.
    """
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert_3x3_numerical_matrix(matrix)  # Should not raise

def test_assert_3x3_numerical_matrix_non_numerical() -> None:
    """
    Test assert_3x3_numerical_matrix with a 3x3 non-numerical matrix and expect AssertionError.
    """
    matrix = np.array([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']], dtype=object)
    with pytest.raises(AssertionError, match=r"An unexpected error occurred"):
        assert_3x3_numerical_matrix(matrix)

def test_assert_3x3_numerical_matrix_wrong_shape() -> None:
    """
    Test assert_3x3_numerical_matrix with a matrix that is not 3x3 and expect AssertionError.
    """
    matrix = np.array([[1, 2], [3, 4]])
    with pytest.raises(AssertionError, match=r"Expected a 3x3 numerical matrix"):
        assert_3x3_numerical_matrix(matrix)

def test_assert_3x3_numerical_matrix_invalid_input() -> None:
    """
    Test assert_3x3_numerical_matrix with an invalid input (not a numpy array) and expect TypeError.
    """
    with pytest.raises(AssertionError):
        assert_3x3_numerical_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
