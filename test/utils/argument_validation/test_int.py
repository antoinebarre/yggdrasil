''' This module contains the tests for the integer validation functions. '''
import pytest
from yggdrasil.utils.argument_validation.int import (
  validate_integer, validate_positive_integer,
  assert_integer, assert_positive_integer)

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


# Test cases for assert_integer
@pytest.mark.parametrize("value", [0, 1, -1, 100, -100])
def test_assert_integer_valid(value):
    """
    Test the assert_integer function with valid input.

    This function tests the behavior of the assert_integer function by passing
    valid integer values as input. The function should not raise any exception.

    """
    assert_integer(value)  # Should not raise any exception

@pytest.mark.parametrize("value", [0.5, "string", None, [], {}, set(), (1, 2)])
def test_assert_integer_invalid(value):
    """
    Test the assert_integer function with invalid input.

    This function tests the behavior of the assert_integer function by passing
    invalid values (non-integer) as input. The function should raise a TypeError.

    """
    with pytest.raises(TypeError):
        assert_integer(value)

# Test cases for assert_positive_integer
@pytest.mark.parametrize("value", [0, 1, 100])
def test_assert_positive_integer_valid(value):
    """
    Test the assert_positive_integer function with valid input.

    This function tests the behavior of the assert_positive_integer function by passing
    valid positive integer values as input. The function should not raise any exception.

    """
    assert_positive_integer(value)  # Should not raise any exception

@pytest.mark.parametrize("value", [-1, -100])
def test_assert_positive_integer_negative(value):
    """
    Test the assert_positive_integer function with negative input.

    This function tests the behavior of the assert_positive_integer function by passing
    negative integer values as input. The function should raise a ValueError.

    """
    with pytest.raises(ValueError):
        assert_positive_integer(value)

@pytest.mark.parametrize("value", [0.5, "string", None, [], {}, set(), (1, 2)])
def test_assert_positive_integer_invalid(value):
  """
  Test the assert_positive_integer function with invalid input.

  This function tests the behavior of the assert_positive_integer function by passing
  invalid values (non-integer) as input. The function should raise a TypeError.

  """
  with pytest.raises(TypeError):
    assert_positive_integer(value)
