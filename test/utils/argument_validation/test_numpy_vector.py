import pytest
import numpy as np

from yggdrasil.utils.argument_validation.numpy_vector import is_3d_numpy_vector, assert_3d_numpy_vector

def mock_is_numerical_array(arr: np.ndarray) -> bool:
    """
    Mock implementation of is_numerical_array for testing purposes.

    Parameters:
        arr (np.ndarray): The array to check.

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
        'yggdrasil.utils.argument_validation.numpy_array.is_numerical_array', mock_is_numerical_array)

def test_is_3d_numpy_vector_valid() -> None:
    """
    Test is_3d_numpy_vector with a valid 3-dimensional numerical vector.
    """
    vector = np.array([1, 2, 3])
    assert is_3d_numpy_vector(vector) == True

def test_is_3d_numpy_vector_non_numerical() -> None:
    """
    Test is_3d_numpy_vector with a non-numerical 3-dimensional vector.
    """
    vector = np.array(['a', 'b', 'c'], dtype=object)
    assert is_3d_numpy_vector(vector) == False

def test_is_3d_numpy_vector_wrong_shape() -> None:
    """
    Test is_3d_numpy_vector with a vector that is not 3-dimensional.
    """
    vector = np.array([1, 2])
    assert is_3d_numpy_vector(vector) == False

def test_assert_3d_numpy_vector_valid() -> None:
    """
    Test assert_3d_numpy_vector with a valid 3-dimensional numerical vector.
    """
    vector = np.array([1, 2, 3])
    assert_3d_numpy_vector(vector)  # Should not raise

def test_assert_3d_numpy_vector_non_numerical() -> None:
    """
    Test assert_3d_numpy_vector with a non-numerical 3-dimensional vector and expect AssertionError.
    """
    vector = np.array(['a', 'b', 'c'], dtype=object)
    with pytest.raises(AssertionError, match=r"Expected a 3-dimensional NumPy vector"):
        assert_3d_numpy_vector(vector)

def test_assert_3d_numpy_vector_wrong_shape() -> None:
    """
    Test assert_3d_numpy_vector with a vector that is not 3-dimensional and expect AssertionError.
    """
    vector = np.array([1, 2])
    with pytest.raises(AssertionError, match=r"Expected a 3-dimensional NumPy vector"):
        assert_3d_numpy_vector(vector)

def test_assert_3d_numpy_vector_invalid_input() -> None:
    """
    Test assert_3d_numpy_vector with an invalid input (not a numpy array) and expect TypeError.
    """
    with pytest.raises(AssertionError):
        assert_3d_numpy_vector([1, 2, 3])
