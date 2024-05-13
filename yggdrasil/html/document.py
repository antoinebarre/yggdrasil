
"""Collections of Classes and Functions to work with HTML documents."""


from pathlib import Path

import attrs

from ..utils.files import write_string_to_file
from ..utils.string import remove_blank_lines

from .base import HTMLExtraFile
from .components.blocks import HTMLBlock
from .structure.header import Header
from .structure.footer import Footer
from .structure.body import Body

__all__ = [
    "HTMLDocument",
    ]

# allowed file extensions
ALLOWED_HTML_EXTENSIONS = ['.html', '.htm']

# Contents of document
ALLOWED_TAG_4_HEADER = [
    "text","link","style","script","meta",
    "title","h1","div","nav","style",'script']
ALLOWED_TAG_4_BODY = None
ALLOWED_TAG_4_FOOTER = ["text","script"]

@attrs.define
class HTMLDocument:
    """
    Represents an HTML document.

    Attributes:
        header (HTMLBlock): The header of the HTML document.
        body (HTMLBlock): The body of the HTML document.
        footer (HTMLBlock): The footer of the HTML document.

    Methods:
        __attrs_post_init__(): Initializes the header, body, and footer of the HTML document.
        add2header(*components): Adds the specified components to the header of the document.
        add2body(*components): Adds the specified components to the body of the document.
        add2footer(*components): Adds the specified components to the footer of the document.
        get_html(): Returns the HTML content of the document as a string.
        get_all_additional_files(): Returns a list of all additional files associated
         with the document.
        publish(html_file_path, exist_ok): Publishes the HTML content to the specified file path.
    """

    header : HTMLBlock = attrs.field(
        metadata={'description': 'The header of the HTML document'},
        validator=attrs.validators.optional(
            attrs.validators.instance_of(HTMLBlock)), # type: ignore
        init=False)

    body : HTMLBlock = attrs.field(
        metadata={'description': 'The body of the HTML document'},
        validator=attrs.validators.instance_of(HTMLBlock),
        init=False)

    footer: HTMLBlock = attrs.field(
        metadata={'description': 'The footer of the HTML document'},
        validator=attrs.validators.optional(
            attrs.validators.instance_of(HTMLBlock)), # type: ignore
        init=False)

    def __attrs_post_init__(self):
        self.header = Header()
        self.body = Body()
        self.footer = Footer()

    def add2header(self, *components):
        """
        Adds the specified components to the header of the document.

        Parameters:
        - components: The components to be added to the header.

        Returns:
        None
        """
        self.header.add_components(
            *components,
            allowed_tag=ALLOWED_TAG_4_HEADER
        )

    def add2body(self, *components):
        """
        Adds the specified components to the body of the document.

        Parameters:
        - components: The components to be added to the body.

        Returns:
        None
        """
        self.body.add_components(
            *components,
            allowed_tag=ALLOWED_TAG_4_BODY
        )

    def add2footer(self, *components):
        """
        Adds the specified components to the footer of the document.

        Parameters:
        - components: The components to be added to the footer.

        Returns:
        None
        """
        self.footer.add_components(
            *components,
            allowed_tag=ALLOWED_TAG_4_FOOTER
        )

    def get_html(self) -> str:
        """
        Returns the HTML content of the document as a string.

        Returns:
            str: The HTML content of the document as a string.
        """
        header = self.header.render()
        body = self.body.render()
        footer = self.footer.render()

        # Combine the header, body, and footer
        html_text = f"{header}\n{body}\n{footer}"

        # clean up the HTML content
        html_text = html_text.strip()
        html_text = remove_blank_lines(html_text)

        return html_text

    def get_all_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of all additional files associated with the document.

        Returns:
            list[HTMLExtraFile]: List of additional files.
        """
        additional_files = []
        additional_files.extend(self.header.get_additional_files())
        additional_files.extend(self.body.get_additional_files())
        additional_files.extend(self.footer.get_additional_files())

        return additional_files

    def publish(
        self,
        html_file_path: Path,
        exist_ok: bool = False
    ) -> list[Path]:
        """
        Publishes the HTML content to the specified file path.

        Args:
            htlm_file_path (Path): The file path where the HTML content will be published.
            exist_ok (bool, optional): If True, allows overwriting an existing file.
             Defaults to False.

        Raises:
            FileExistsError: If the file already exists at the specified file path.
        """
        if not exist_ok and html_file_path.exists():
            raise FileExistsError(
                f"The file already exists at the specified file path: {html_file_path}")
        # initiate the list of exported files with the HTML file
        exported_files: list[Path] = [
            write_string_to_file(
                file_path=html_file_path,
                content=self.get_html(),
                exist_ok=exist_ok,
            )
        ]

        exported_files.extend(
            extra_file.export(html_file_path.parent)
            for extra_file in self.get_all_additional_files()
        )

        return exported_files
