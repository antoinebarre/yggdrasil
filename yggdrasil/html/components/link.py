"""Function to create a link component."""

from typing import Literal, Optional
from ._blocks import InlineHTMLBlock, InlineHTMLComponent
from .__childrenUtils import get_children


ALLOWED_ATTRIBUTES = ['class']

allowedComponentsType = str | InlineHTMLComponent | InlineHTMLBlock

def Link(  # pylint: disable=invalid-name
        *,
        component: allowedComponentsType,
        link: str,
        target: Optional[Literal['_blank', '_self', '_parent', '_top']] = None,
        attributes: Optional[dict[str, str]] = None) -> InlineHTMLBlock:
    """
    Create an HTML link element.

    Args:
        component (allowedComponentsType): The component to be linked.
        link (str): The URL of the link.
        target (Optional[Literal['_blank', '_self', '_parent', '_top']]): The target
        attribute of the link.
        attribustes (Optional[dict[str, str]]): Additional attributes for the link.

    Returns:
        HTMLBlock: The HTML link element.

    Raises:
        ValueError: If an invalid attribute is provided in `attribustes`.

    """
    # manage the nature of the component
    component_as_list = get_children([component])

    # create attributes
    block_attributes = {'href': link}

    if target:
        block_attributes['target'] = target

    if attributes:
        for key in attributes:
            if key not in ALLOWED_ATTRIBUTES:
                raise ValueError(
                    f"Invalid attribute '{key}' " +
                    f"for link. Allowed attributes are {ALLOWED_ATTRIBUTES}"
                    )
            block_attributes[key] = attributes[key]

    return InlineHTMLBlock(  #pylint: disable=unexpected-keyword-arg
        tag_name='a',
        component=component_as_list[0],
        attributes=block_attributes
    )
