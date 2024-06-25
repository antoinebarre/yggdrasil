import pytest
import numpy as np
from yggdrasil.utils.argument_validation import is_numerical_array

@pytest.mark.parametrize("array, expected", [
    (np.array([1, 2, 3]), True),                       # Integer array
    (np.array([1.0, 2.0, 3.0]), True),                 # Float array
    (np.array(['a', 'b', 'c']), False),                # String array
    (np.array([[1, 2], [3, 4]]), True),                # 2D numerical array
    (np.array([1, 2, 'a']), False),                    # Mixed type array
    (np.array([]), True),                              # Empty array, still numerical type
    (np.array([True, False, True]), False),            # Boolean array
])
def test_is_numerical_array(array, expected):
    """
    Test the is_numerical_array function.

    Args:
        array: The input array to be tested.
        expected: The expected result of the is_numerical_array function.

    Returns:
        None
    """
    assert is_numerical_array(array) == expected
