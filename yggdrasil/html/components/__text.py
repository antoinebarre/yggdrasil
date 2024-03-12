

import attrs
from ..base import HTMLComponent, HTMLExtraFile

__all__ = ["Text"]

@attrs.define
class HTMLText(HTMLComponent):
    """
    Represents a simple text component in an HTML document without any tags.

    Attributes:
        text (str): The text to be rendered.
    """

    text: str = attrs.field(
        validator=attrs.validators.instance_of(str),
        metadata={'description': 'The text to be rendered'},
        kw_only=False)

    def render(self) -> str:
        """
        Renders the text component and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """
        return self.text

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the text component.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        return []

    def get_tag(self) -> str:
        """
        Returns the tag of the text component.

        Returns:
            str: The tag of the text component.
        """
        return "text"

def Text(text: str) -> HTMLText: # pylint: disable=invalid-name
    """
    Factory function to create a text component.

    Args:
        text (str): The text to be rendered.

    Returns:
        HTMLText: The created text component.
    """
    return HTMLText(text=text)
