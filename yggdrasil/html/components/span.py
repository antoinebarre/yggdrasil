"""Create a span element."""

from typing import Optional
import attrs
from ._blocks import InlineHTMLBlock
from .__text import Text
from .__validate_attributes import validate_html_attribute

@attrs.define
class CSS_Style:  # pylint: disable=too-few-public-methods, invalid-name
    """
    Represents the CSS style for an HTML object.

    Attributes:
        color (Optional[str]): The color of the text following CSS rules.
        font_family (Optional[str]): The font family of the text.
        font_size (Optional[str]): The font size of the text.
        font_weight (Optional[str]): The font weight of the text.
        font_style (Optional[str]): The font style of the text.
    """

    #TODO : add background color

    color: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The color of the text.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    font_family: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The font family of the text.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    font_size: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The font size of the text.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    font_weight: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The font weight of the text.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)
    font_style: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The font style of the text.'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)


    def render(self):
        """
        Renders the CSS style as a string.

        Returns:
            str: The CSS style string.
        """
        style_components = []
        for field in attrs.fields(self.__class__):
            attribute_name: str = field.name
            if attribute_value := getattr(self, attribute_name):
                # Convert field names to CSS property names if they are different
                css_property_name = attribute_name.replace('_', '-')
                style_components.append(f"{css_property_name}:{attribute_value}")
        return '; '.join(style_components)


ALLOWED_ATTRIBUTES = ['class']

def Span(  # pylint: disable=invalid-name
    text: str,
    style: CSS_Style = CSS_Style(),
    attributes: Optional[dict[str, str]] = None) -> InlineHTMLBlock:
    """
    Create a span element with the given text, style, and attributes.

    Args:
        text (str): The text content of the span.
        style (CSS_Style, optional): The CSS style to apply to the span. Defaults to CSS_Style().
        attributes (Optional[dict[str, str]], optional): Additional attributes for the span element.
        Defaults to None.

    Returns:
        InlineHTMLBlock: The span element as an InlineHTMLBlock.

    """
    final_attributes = validate_html_attribute(attributes, ALLOWED_ATTRIBUTES)

    # render the style
    if style_string := style.render():
        final_attributes['style'] = style_string

    return InlineHTMLBlock( #pylint: disable=unexpected-keyword-arg
        tag_name='span',
        component=Text(text),
        attributes=final_attributes)
