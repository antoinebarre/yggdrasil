"""Contains classes for HTML blocks and inline HTML blocks."""



from typing import Optional
import attrs
from ...utils.string import indent
from ..base import HTMLComponent, HTMLExtraFile
from .__childrenUtils import validate_tag, get_children


__all__ = [
    'HTMLBlock',
    'InlineHTMLComponent'
]
DEFAULT_INDENT_LEVEL = 4
DEFAULT_INDENT_CHAR = ' '

def _create_string_block(
    prefix: str,
    content: str,
    suffix: str,
    inline: bool) -> str:
    """
    Create a string block with the given prefix, content, and suffix.

    Args:
        prefix (str): The prefix of the string block.
        content (str): The content of the string block.
        suffix (str): The suffix of the string block.
        inline (bool): Whether the string block should be inline or not.

    Returns:
        str: The created string block.
    """
    if inline:
        return f'{prefix}{content}{suffix}'
    else:
        return (
            f"{prefix}\n" +
            f"{indent(
                text=content,
                amount=DEFAULT_INDENT_LEVEL,
                ch=DEFAULT_INDENT_CHAR)}\n" +
                f"{suffix}")

@attrs.define
class InlineHTMLComponent(HTMLComponent):
    """
    Represents a generic inline HTML block in an HTML document.

    Exemple of HTML block:
    '''<img src="img src" alt="img alt" width="500" height="600"/>'''


    Attributes:
        content (str): The content of the block.
    """
    tag_name: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={'description': 'The tag name of the block'},
        kw_only=True)

    additional_file:HTMLExtraFile = attrs.field(
        factory=None,
        metadata={'description': 'additional file to be published'},
        validator=attrs.validators.instance_of(HTMLExtraFile),
        kw_only=True)

    attributes: dict[str, str] = attrs.field(
        factory=dict,
        metadata={'description': 'The attributes of the block'},
        validator=attrs.validators.deep_mapping(
            key_validator=attrs.validators.instance_of(str),
            value_validator=attrs.validators.instance_of(str)),
        kw_only=True)

    def add_attribute(self, key: str, value: str):
        """
        Adds an attribute to the block.

        Args:
            key (str): The key of the attribute.
            value (str): The value of the attribute.

        Returns:
            None
        """
        self.attributes[key] = value

    def render_attributes(self) -> str:
        """
        Renders the attributes of the block and returns them as a string.

        Returns:
            str: The rendered attributes as a string.
        """
        return ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

    def render(self) -> str:
        """
        Renders the block and returns the generated HTML string.

        Returns:
            str: The generated HTML string.
        """
        return f'<{self.tag_name} {self.render_attributes()}/>'

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the block.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        return [self.additional_file]

    def get_tag(self) -> str:
        """
        Returns the tag name of the HTML component.

        :return: The tag name as a string.
        """
        return self.tag_name


@attrs.define
class HTMLBlock(HTMLComponent):
    """
    Represents an HTML block component.

    Attributes:
        tag_name (str): The tag name of the block.
        children (list[HTMLComponent]): List of HTML components that are children of the block.
        additional_files (list[HTMLExtraFile]): List of additional files to be published.
        attributes (dict[str, str]): Dictionary of attributes for the block.
    """
    tag_name: str = attrs.field(
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        metadata={'description': 'The tag name of the block'},
        kw_only=True)

    children: list[HTMLComponent] = attrs.field(
        factory=list,
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLComponent)),
        metadata={'description': 'List of HTML components that are children of the block'},
        kw_only=True)

    additional_file:HTMLExtraFile = attrs.field(
        default=None,
        metadata={'description': 'List of additional files to be published'},
        validator=attrs.validators.optional(attrs.validators.instance_of(HTMLExtraFile)),
        kw_only=True)

    attributes: dict[str, str] = attrs.field(
        factory=dict,
        metadata={'description': 'Dictionary of attributes for the block'},
        validator=attrs.validators.deep_mapping(
            key_validator=attrs.validators.instance_of(str),
            value_validator=attrs.validators.instance_of(str)),
        kw_only=True)

    def add_components(
            self,
            *components: HTMLComponent | str,
            allowed_tag: Optional[list[str]] = None):
        """
        Adds a component to the block at the last position.

        Args:
            component (HTMLComponent): The component to be added.

        Returns:
            None
        """
        # change all string to text component
        children = get_children(list(components))

        # If allowed_tag is not None, check that the tag of the component is in the allowed list
        if allowed_tag:
            validate_tag(
                children=children,
                allowed_tags=allowed_tag
            )

        for component in children:
            self.children.append(component)

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional files associated with the block.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = [self.additional_file] if self.additional_file else []

        if self.children:
            for child in self.children:
                additional_files.extend(child.get_additional_files())
        return additional_files

    def add_attribute(self, key: str, value: str):
        """
        Adds an attribute to the block.

        Args:
            key (str): The key of the attribute.
            value (str): The value of the attribute.

        Returns:
            None
        """
        self.attributes[key] = value

    def render_attributes(self) -> str:
        """
        Renders the attributes of the block and returns them as a string.

        Returns:
            str: The rendered attributes as a string.
        """
        return ' '.join([f'{key}="{value}"' for key, value in self.attributes.items()])

    def render(self) -> str:
        """
        Render the block and return it as a string.

        Returns:
            str: The rendered block as a string.
        """
        return _create_string_block(
            prefix=f'<{self.tag_name} {self.render_attributes()}>',
            content='\n'.join([child.render() for child in self.children]),
            suffix=f'</{self.tag_name}>',
            inline=False
        )

    def get_extra_files_info(self)-> str:
        return '\n'.join([file.get_status() for file in self.get_additional_files()])

    def get_tag(self) -> str:
        """
        Returns the tag name of the HTML component.

        :return: The tag name as a string.
        """
        return self.tag_name
