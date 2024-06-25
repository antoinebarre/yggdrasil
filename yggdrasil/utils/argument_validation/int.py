"""Collection of functions for validating integer values."""

import warnings

__all__ = [
    'validate_integer',
    'validate_positive_integer',
]

def validate_integer(value: int) -> int:
    """
    Validates if the given value is an integer.

    Args:
        value (int): The value to be validated.

    Returns:
        int: The validated integer value.

    Raises:
        TypeError: If the value is not an integer.

    """
    if not isinstance(value, int):
        raise TypeError(f'Expected an integer, but got {type(value).__name__}.')

    # warning deprecated
    warnings.warn("This function is deprecated. Use assert function instead.")

    return value

def validate_positive_integer(value: int) -> int:
    """
    Validate if the given value is a positive integer or zero.

    Args:
        value (int): The value to be validated.

    Returns:
        int: The validated positive integer.

    Raises:
        ValueError: If the value is not a positive integer.

    """
    value = validate_integer(value)

    if value < 0:
        raise ValueError('Expected a positive integer.')
    
    # warning deprecated
    warnings.warn("This function is deprecated. Use assert function instead.")

    return value


def assert_integer(value: int) -> None:
    """
    Asserts if the given value is an integer.

    Args:
        value (int): The value to be asserted.

    Returns:
        None

    Raises:
        TypeError: If the value is not an integer.

    """
    if not isinstance(value, int):
        raise TypeError(f'Expected an integer, but got {type(value).__name__}.')


def assert_positive_integer(value: int) -> None:
    """
    Asserts if the given value is a positive integer or zero.

    Args:
        value (int): The value to be asserted.

    Returns:
        None

    Raises:
        ValueError: If the value is not a positive integer.

    """
    assert_integer(value)

    if value < 0:
        raise ValueError('Expected a positive integer.')
