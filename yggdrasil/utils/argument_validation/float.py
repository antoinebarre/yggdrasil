"""Collection of tools to validate float values."""

from typing import Any


def validate_float(value: Any) -> float:
    """
    Validates if the given object is a float.

    Args:
        object (Any): The object to be validated.

    Returns:
        float: The validated float value.

    Raises:
        TypeError: If the object is not a float.

    """
    try:
        return float(value)
    except Exception as e:
        raise TypeError(f"Expected a float, but got {type(object).__name__}.") from e

def validate_strictly_positive_float(value: Any) -> float:
    """
    Validates if the given object is a positive float.

    Args:
        object (Any): The object to be validated.

    Returns:
        float: The validated positive float value.

    Raises:
        ValueError: If the object is not a positive float.

    """
    if validate_float(value) <= 0:
        raise ValueError(f"Expected a strictly positive float, but got {value}.")
    return value

def validate_positive_float(value: Any) -> float:
    """
    Validates if the given object is a positive float.

    Args:
        object (Any): The object to be validated.

    Returns:
        float: The validated positive float value.

    Raises:
        ValueError: If the object is not a positive float.

    """
    if validate_float(value) < 0:
        raise ValueError(f"Expected a positive float, but got {value}.")
    return value