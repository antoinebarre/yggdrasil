

from yggdrasil.html.base import HTMLComponent
from .blocks import HTMLBlock
from .text import Text

__all__ = ["Title"]

def Title(  # pylint: disable=invalid-name
    title:str
) -> HTMLComponent:
    """
    Create a title component with the specified title.

    Args:
        title (str): The title of the document.

    Returns:
        HTMLComponent: The title component.
    """

    return HTMLBlock(
        tag_name="title",
        children=[Text(title.upper())]
    )