"""collection of paragraph components"""

from typing import Optional
from .blocks import HTMLBlock
from ..base import HTMLComponent
from .__childrenUtils import get_children

ALLOWED_ATTRIBUTES = ['class']

def Paragraph(  # pylint: disable=invalid-name
    *children: HTMLComponent | str,
    attributes: Optional[dict[str, str]] = None) -> HTMLBlock:
    """
    Create a paragraph HTML component.

    Args:
        *children (HTMLComponent | str): The children components or strings to be
        included in the paragraph.
        attributes (Optional[dict[str, str]]): Optional attributes for the paragraph.

    Returns:
        HTMLBlock: The paragraph HTML component.

    Raises:
        ValueError: If an invalid attribute is provided.

    """
    if attributes is None:
        attributes = {}
    # validate attributes
    for key in attributes:
        if key not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Invalid attribute '{key}' " +
                f"for paragraph. Allowed attributes are {ALLOWED_ATTRIBUTES}"
                )
    # get the children as HTML components
    components = get_children(children)

    return HTMLBlock(  #pylint: disable=unexpected-keyword-arg
        tag_name='p',
        children=components,
        attributes=attributes
    )
