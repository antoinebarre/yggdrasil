

import attrs
from ..base import HTMLComponent, HTMLExtraFile

__all__ = ["Footer"]

#TODO : define a validation function to validate the children of the footer


@attrs.define
class HTMLFooter(HTMLComponent):
    """
    Represents the footer of an HTML document.

    Attributes:
        children (list[HTMLComponent]): List of HTML components that are children of the footer.
    """

    children: list[HTMLComponent] = attrs.field(
        default=[],
        validator=attrs.validators.instance_of(list),
        metadata={'description': 'List of HTML components that are children of the footer'},
        kw_only=True)

    def render(self) -> str:
        """
        Render the footer and return it as a string.

        Returns:
            str: The rendered footer as a string.
        """
        return self._create_string_block(
            prefix='<footer>',
            content=''.join([child.render() for child in self.children]),
            suffix='</footer>',
            inline=False
        )

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the footer.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = []
        if self.children:
            for child in self.children:
                additional_files.extend(child.get_additional_files())
        return additional_files

def Footer(*children: HTMLComponent) -> HTMLFooter: # pylint: disable=invalid-name
    """
    Create a new HTML footer with the given children.

    Args:
        children (HTMLComponent): The children of the footer.
    """
    return HTMLFooter(children=list(children))