"""Tools for creating the header of an HTML document."""
import attrs
from ..base import HTMLComponent, HTMLExtraFile

__all__ = ["Header"]

#TODO : define a validation function to validate the children of the header

@attrs.define
class HTMLHeader(HTMLComponent):
    """
    Represents the header of an HTML document.

    Attributes:
        children (list[HTMLComponent]): List of HTML components that are children of the header.
    """

    children: list[HTMLComponent] = attrs.field(
        default=[],
        validator=attrs.validators.instance_of(list),
        metadata={'description': 'List of HTML components that are children of the header'},
        kw_only=True)

    def render(self) -> str:
        """
        Render the header and return it as a string.

        Returns:
            str: The rendered header as a string.
        """
        return self._create_string_block(
            prefix='<header>',
            content=''.join([child.render() for child in self.children]),
            suffix='</header>',
            inline=False
        )

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the header.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = []
        if self.children:
            for child in self.children:
                additional_files.extend(child.get_additional_files())
        return additional_files

def Header(*children: HTMLComponent) -> HTMLHeader: # pylint: disable=invalid-name
    """
    Create a new HTML header with the given children.

    Args:
        children (HTMLComponent): The children of the header.
    """
    return HTMLHeader(children=list(children))