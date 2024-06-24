''' This module contains the tests for the integer validation functions. '''
import pytest
from yggdrasil.utils.argument_validation.int import validate_integer, validate_positive_integer

# Test validate_integer function
def test_validate_integer():
    """
    Test the validate_integer function.

    This function tests the behavior of the validate_integer function by passing
    different types of values as input.

    - Test with an integer value: The function should return the same integer value.
    - Test with a non-integer value: The function should raise a TypeError.

    """
    assert validate_integer(123) == 123

    with pytest.raises(TypeError):
        validate_integer(3.14) # type: ignore

# Test validate_positive_integer function
def test_validate_positive_integer():
    """
    Test the validate_positive_integer function.

    This function tests the behavior of the validate_positive_integer function by passing
    different types of values as input.

    - Test with a positive integer value: The function should return the same
      positive integer value.
    - Test with a zero value: The function should return 0.
    - Test with a negative integer value: The function should raise a ValueError.

    """
    assert validate_positive_integer(123) == 123

    assert validate_positive_integer(0) == 0

    with pytest.raises(ValueError):
        validate_positive_integer(-123)
