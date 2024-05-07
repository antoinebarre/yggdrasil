"""Tools to generate a script tag."""

from .blocks import HTMLBlock
from .text import Text

def Script(  # pylint: disable=invalid-name
    source_code: str
    ) -> HTMLBlock:
    """
    Create a script tag with the specified source code.

    Args:
        source_code (str): The source code of the script.

    Returns:
        HTMLBlock: The script tag.
    """
    return HTMLBlock(
        tag_name='script',
        children=[Text(source_code)]
    )
