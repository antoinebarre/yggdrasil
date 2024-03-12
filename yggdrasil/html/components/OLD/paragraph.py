"""Collection of function and class for HTML Paragraph"""


from typing import Optional
import attrs

from .generic_component import HTMLGenericComponent # pylint: disable=import-error
from .components import AdditionalFile, HTMLComponent
from .html_tag import HTMLOptions, HTMLTag
from ._render_tools import create_block


__all__ = ["Text", "Paragraph", "Basic"]

@attrs.define
class Basic(HTMLComponent):
    """
    Represents a basic paragraph component without any formating or balise.

    Attributes:
        text (str): The text to be rendered.
    """

    text: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={'description': 'The text to be rendered'},
        kw_only=False)

    def render(self) -> str:
        return create_block(
            open_prefix="",
            content=self.text,
            close_suffix="",
            inline=True)

    def get_additional_files(self) -> list[AdditionalFile]:
        return []

def Text(  # pylint: disable=invalid-name
    *children: HTMLComponent | str,
) -> Basic:
    """
    Create a text component with the given children.

    Args:
        *children: The children components or strings to be included in the text.

    Returns:
        A Basic component representing the text.

    """
    components = validate_HTML_children(children)
    return Basic("".join([component.render() for component in components]))


def Paragraph(  # pylint: disable=invalid-name
    *children: HTMLComponent | str,
    options: Optional[HTMLOptions] = None) -> HTMLGenericComponent:
    """
    Create an advanced paragraph component.

    Args:
        *children (HTMLComponent | str): The child components or strings to be
            included in the paragraph.
        options (Optional[dict[str,str]]): Additional options for the paragraph.

    Returns:
        HTMLGenericComponent: The advanced paragraph component.
    """
    components = validate_HTML_children(children)

    tag = HTMLTag(
        tag_name="p",
        options=options)
    return HTMLGenericComponent(
        tag=tag,
        contents=components)


def validate_HTML_children(children: list | tuple) -> list[HTMLComponent]: # pylint: disable=invalid-name
    """
    Validate the children of an HTML component.
    childre shall be a iterable of HTMLComponent or str.

    Args:
        children (list or tuple): The children to validate.

    Returns:
        list[HTMLComponent]: The validated children.

    Raises:
        TypeError: If any child is not an instance of HTMLComponent or str.
    """
    if not all(isinstance(child, (HTMLComponent, str)) for child in children):

        # detect the first invalid child
        for child in children:
            if not isinstance(child, (HTMLComponent, str)):
                raise TypeError("All children must be instances of HTMLComponent or str" +
                                f"Got Invalid input: {child}, type: {type(child)}" +
                                f", Position: {children.index(child)}")

    return [
        Basic(child) if isinstance(child, str) else child for child in children
    ]
