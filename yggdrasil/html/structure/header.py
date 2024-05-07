"""Tools for creating the header of an HTML document."""
import attrs
from ..base import HTMLComponent, HTMLExtraFile
from ..components.blocks import HTMLBlock

__all__ = ["Header"]

#TODO : define a validation function to validate the children of the header


def Header(*children: HTMLComponent) -> HTMLBlock: # pylint: disable=invalid-name
    """
    Create a new HTML header with the given children.

    Args:
        children (HTMLComponent): The children of the header.
    """
    return HTMLBlock(
        tag_name="header",
        children=list(children))