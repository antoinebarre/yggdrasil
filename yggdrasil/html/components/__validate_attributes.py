"""internal tool to validate the attributes for an HTML component."""

from typing import Optional


def validate_html_attribute(
    attributes: Optional[dict[str, str]],
    allowed_attributes: list[str]
    ) -> dict[str, str]:
    """
    Validate the attributes for an HTML component.

    Args:
        attributes (Optional[dict[str, str]]): The attributes to be validated.
        allowed_attributes (list[str]): The allowed attributes.

    Returns:
        dict[str, str]: The validated attributes.

    Raises:
        ValueError: If an invalid attribute is provided.
    """
    if attributes is None:
        attributes = {}
    # validate attributes
    for key in attributes:
        if key not in allowed_attributes:
            raise ValueError(
                f"Invalid attribute '{key}' " +
                f"for HTML component. Allowed attributes are {allowed_attributes}"
                )
    return attributes
