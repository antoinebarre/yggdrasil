""" Create a style tag with the specified source code."""

from .text import Text
from .blocks import HTMLBlock

def Style(  # pylint: disable=invalid-name
    source_code: str
    ) -> HTMLBlock:
    """
    Create a style tag with the specified source code.

    Args:
        source_code (str): The source code of the style.

    Returns:
        HTMLBlock: The style tag.
    """
    return HTMLBlock(
        tag_name='style',
        children=[Text(source_code)]
    )
