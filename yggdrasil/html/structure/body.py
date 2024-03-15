""" Class for the body of an HTML report."""

from ..components._blocks import HTMLBlock
from ..base import HTMLComponent

__all__ = ["Body"]


#TODO : define a validation function to validate the children of the body


def Body(*children: HTMLComponent) -> HTMLBlock: # pylint: disable=invalid-name
    """
    Create a new HTML body with the given children.

    Args:
        children (HTMLComponent): The children of the body.

    Returns:
        HTMLBody: The new HTML body.
    """
    return HTMLBlock(
        tag_name="body",
        children=list(children))
