"""HTML components for creating a division element."""

from typing import Optional
from ._blocks import HTMLBlock, HTMLComponent

__all__ = ['Division']

def Division( # pylint: disable=invalid-name
    *children: HTMLComponent,
    attributes: Optional[dict[str, str]] = None,
    ) -> HTMLBlock:
    """
    Create a division (div) HTML element.

    Args:
        *children: Variable-length argument list of HTML components to be nested
         inside the division.
        attributes: Optional dictionary of attributes to be added to the division element.

    Returns:
        An HTMLBlock representing the division element.

    """
    if attributes is None:
        attributes = {}
    return HTMLBlock(
        tag_name="div",
        children=list(children),
        attributes=attributes)
