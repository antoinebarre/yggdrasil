""" Class for the body of an HTML report."""

import attrs

from ..base import HTMLExtraFile, HTMLComponent

__all__ = ["Body"]

VALID_BODY_CHILDREN = (HTMLComponent, HTMLExtraFile)

#TODO : define a validation function to validate the children of the body

@attrs.define
class HTMLBody(HTMLComponent):
    """
    Represents the body of an HTML document.

    Attributes:
        children (list[HTMLComponent]): List of HTML components that are children of the body.
    """

    children: list[HTMLComponent] = attrs.field(
        default=[],
        validator=attrs.validators.instance_of(list),
        metadata={'description': 'List of HTML components that are children of the body'},
        kw_only=True)

    def render(self) -> str:
        """
        Render the body and return it as a string.

        Returns:
            str: The rendered body as a string.
        """
        return self._create_string_block(
            prefix='<body>',
            content=''.join([child.render() for child in self.children]),
            suffix='</body>',
            inline=False
        )

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the body.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = []
        if self.children:
            for child in self.children:
                additional_files.extend(child.get_additional_files())
        return additional_files
    
    def add_components(self, *components: HTMLComponent):
        """
        Adds a component to the body of the HTML document at the last position.

        Args:
            component (HTMLComponent): The component to be added.

        Returns:
            None
        """
        for component in components:
            self.children.append(component)


def Body(*children: HTMLComponent) -> HTMLBody: # pylint: disable=invalid-name
    """
    Create a new HTML body with the given children.

    Args:
        children (HTMLComponent): The children of the body.

    Returns:
        HTMLBody: The new HTML body.
    """
    return HTMLBody(children=list(children))
