

import attrs
from ..base import HTMLComponent, HTMLExtraFile
from ..components._blocks import HTMLBlock

__all__ = ["Footer"]

#TODO : define a validation function to validate the children of the footer


def Footer(*children: HTMLComponent) -> HTMLBlock: # pylint: disable=invalid-name
    """
    Create a new HTML footer with the given children.

    Args:
        children (HTMLComponent): The children of the footer.
    """
    return HTMLBlock(
        tag_name="footer",
        children=list(children))
