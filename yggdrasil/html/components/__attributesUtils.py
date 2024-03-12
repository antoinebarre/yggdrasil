

from typing import Optional


def validate_attributes(
        allowed_attributes: list[str],
        attributes: Optional[dict[str, str]] = None) -> dict[str, str]:
    """
    Validate that the attributes are valid.

    Args:
        allowed_attributes (list[str]): List of allowed attributes.
        attributes (Optional[dict[str, str]]): Dictionary of attributes.

    Returns:
        dict[str, str]: The validated attributes.

    Raises:
        ValueError: If an attribute is not in the list of allowed attributes.

    Example:
        >>> allowed = ['class', 'id', 'src']
        >>> attrs = {'class': 'container', 'data': '123'}
        >>> validate_attributes(allowed, attrs)
        ValueError: Invalid attribute 'data'. Allowed attributes are ['class', 'id', 'src']
    """
    if attributes is None:
        return {}

    for key in attributes:
        if key not in allowed_attributes:
            raise ValueError(
                f"Invalid attribute '{key}'. Allowed attributes are {allowed_attributes}"
            )
    return attributes
