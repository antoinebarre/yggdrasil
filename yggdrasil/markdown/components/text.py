"""Simple text components for markdown documents."""

import attrs

from .format import MDFormat
from .basic import MDComponent, MDExtraFile

__all__ = ['Text']

@attrs.define
class Text(MDComponent):
    """A simple text component for markdown documents."""
    text: str = attrs.field(
        metadata={'description': 'The text content of the component'},
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        kw_only=False)

    def render(self) -> str:
        """
        Render the component to a string.

        Returns:
            str: The text content of the component.
        """
        return replace_breakline(self.text) + MDFormat.line_break()

    def get_additional_files(self) -> list[MDExtraFile]:
        """
        Get additional files required by the component.

        Returns:
            list[MDExtraFile]: An empty list.
        """
        return []

def replace_breakline(text: str) -> str:
    """
    Replace breaklines with the markdown line break.

    Args:
        text (str): The text to be processed.

    Returns:
        str: The processed text.
    """
    return text.replace('\n', MDFormat.line_break())