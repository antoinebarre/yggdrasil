"""HTML components for creating a navigation element."""

from typing import Optional
from .blocks import HTMLBlock, HTMLComponent

__all__ = ['Navigation']
ALLOWED_ATTRIBUTES = ['class','role']

def Navigation( # pylint: disable=invalid-name
    *children: HTMLComponent,
    attributes: Optional[dict[str, str]] = None,
    ) -> HTMLBlock:
    """
    Create a Navigation (nav) HTML element.

    Args:
        *children: Variable-length argument list of HTML components to be nested
         inside the division.
        attributes: Optional dictionary of attributes to be added to the division element.

    Returns:
        An HTMLBlock representing the division element.

    """
    if attributes is None:
        attributes = {}
        
    # validate attributes
    for key in attributes:
        if key not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Invalid attribute '{key}' " +
                f"for nav. Allowed attributes are {ALLOWED_ATTRIBUTES}"
                )
    # TODO : create a function to validate attributes
    return HTMLBlock(
        tag_name="nav",
        children=list(children),
        attributes=attributes)
