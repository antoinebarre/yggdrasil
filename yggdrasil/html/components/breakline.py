
from .text import HTMLText

__all__ = ["Breakline"]

def Breakline() -> HTMLText: # pylint: disable=invalid-name
    """
    Factory function to create a breakline component.

    Returns:
        HTMLText: The created breakline component.
    """
    return HTMLText(text="<br>")