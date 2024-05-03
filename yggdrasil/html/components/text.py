"""Basic text component for HTML documents."""

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

    bold: bool = attrs.field(
        validator=attrs.validators.instance_of(bool),
        metadata={'description': 'Whether the text should be bold.'},
        kw_only=True)

    @staticmethod
    def add_bold(text: str, is_bold: bool) -> str:
        """
        Adds bold formatting to the given text if `is_bold` is True.

        Args:
            text (str): The text to be formatted.
            is_bold (bool): A flag indicating whether the text should be bold or not.

        Returns:
            str: The formatted text.

        Example:
            >>> add_bold("Hello, world!", True)
            '<b>Hello, world!</b>'
            >>> add_bold("Hello, world!", False)
            'Hello, world!'
        """
        return f"<b>{text}</b>" if is_bold else text

    def render(self) -> str:
        """
        Renders the text component and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """
        return self.add_bold(self.text, self.bold)

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
    
    def get_id(self) -> str:
        """
        Returns the ID of the text component, i.e., an empty string.
        """
        return ""

def Text(text: str, bold: bool = False) -> HTMLText: # pylint: disable=invalid-name
    """
    Factory function to create a text component.

    Args:
        text (str): The text to be rendered.

    Returns:
        HTMLText: The created text component.
    """
    return HTMLText(text=text,bold=bold)
