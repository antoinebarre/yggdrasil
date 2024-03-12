
"""Collections of Classes and Functions to work with HTML documents."""


from pathlib import Path
from typing import Optional

import attrs

# from firefly.tools.files import copy_file
# from firefly.validation.fileIO import validate_file_extension

# from .components import AdditionalFile
# from .components._render_tools import create_block
# from .components.header import  HTMLHeader

from .base import HTMLExtraFile, HTMLComponent
from .structure.header import HTMLHeader
from .structure.footer import HTMLFooter
from .structure.body import HTMLBody

__all__ = ["HTMLDocument","HTMLComponent"]

# allowed file extensions
ALLOWED_HTML_EXTENSIONS = ['.html', '.htm']

@attrs.define
class HTMLDocument:
    header : Optional[HTMLHeader] = attrs.field(
        default=None,  # type: ignore
        metadata={'description': 'The header of the HTML document'},
        validator=attrs.validators.optional(
            attrs.validators.instance_of(HTMLHeader)), # type: ignore
        kw_only=True)

    body : HTMLBody = attrs.field(
        default=HTMLBody(), # type: ignore
        metadata={'description': 'The body of the HTML document'},
        validator=attrs.validators.instance_of(HTMLBody),
        kw_only=True)

    footer: HTMLFooter = attrs.field(
        default=None, # type: ignore
        metadata={'description': 'The footer of the HTML document'},
        validator=attrs.validators.optional(
            attrs.validators.instance_of(HTMLFooter)), # type: ignore
        kw_only=True)

    additional_files : list[HTMLExtraFile] = attrs.field(
        default=[],
        metadata={'description': 'List of additional files to be published'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(HTMLExtraFile)),
        kw_only=True)

    def add_component(self, *components: HTMLComponent):
        """
        Adds a component to the body of the HTML document at the last position.

        Args:
            component (HTMLComponent): The component to be added.

        Returns:
            None
        """
        for component in components:
            self.body.add_components(component)


    def get_html(self) -> str:
        """
        Returns the HTML content of the document as a string.

        Returns:
            str: The HTML content of the document as a string.
        """
        header = self.header.render() if self.header else ''
        body = self.body.render()
        footer = self.footer.render() if self.footer else ''

        return header + body + footer
        
    def get_all_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of all additional files associated with the document.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = []
        if self.header:
            additional_files.extend(self.header.get_additional_files())
        additional_files.extend(self.body.get_additional_files())
        if self.footer:
            additional_files.extend(self.footer.get_additional_files())
        additional_files.extend(self.additional_files)
        return additional_files

    def publish(self, htlm_file_path: Path, exist_ok: bool = False):
        """
        Publishes the HTML content to the specified file path.

        Args:
            htlm_file_path (Path): The file path where the HTML content will be published.
            exist_ok (bool, optional): If True, allows overwriting an existing file. Defaults to False.

        Raises:
            FileExistsError: If the file already exists at the specified file path.
        """
        return ""