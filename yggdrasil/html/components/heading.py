"""Function to create a heading component."""

from typing import Optional

from .text import Text
from ._blocks import InlineHTMLBlock
from .__validate_attributes import validate_html_attribute
from ...utils.string import generate_unique_id


__all__ = ['h']

ALLOWED_ATTRIBUTES = ['class']

def h(
    *,
    level: int,
    title: str,
    attributes: Optional[dict[str, str]] = None,
    ) -> InlineHTMLBlock:
    """
    Create an HTML heading element.

    Args:
        level (int): The level of the heading (between 1 and 6).
        title (str): The title or content of the heading.
        attributes (Optional[dict[str, str]]): Optional attributes for the heading element.

    Returns:
        InlineHTMLBlock: An instance of the InlineHTMLBlock class representing the heading element.

    Raises:
        TypeError: If the level is not an integer between 1 and 6.

    """

    # validate the level
    if not isinstance(level, int) and ( level < 1 or level > 6):
        raise TypeError("The level must be an integer between 1 and 6.")

    # validate attributes
    final_attributes = validate_html_attribute(attributes, ALLOWED_ATTRIBUTES)

    # add unique id to the heading element
    final_attributes["id"] = f"h{level}_{title.lower().replace(' ', '_')}_{generate_unique_id()}"

    return InlineHTMLBlock(  #pylint: disable=unexpected-keyword-arg
        tag_name=f"h{level}",
        component=Text(title),
        attributes=final_attributes
    )
