"""Markdown container components."""

from pathlib import Path
import attrs

from .components import MDComponent,MDExtraFile
from ..utils.files import write_string_to_file

ALLOWED_MARKDOWN_EXTENSIONS = {".md"}

__all__ = ["MarkdownDocument"]

@attrs.define
class MarkdownDocument():
    """
    Represents a Markdown document.

    Attributes:
        title (str): The title of the markdown document.
        components (list[MDComponent]): List of components in the document.

    Methods:
        add_component: Add a component to the document.
        get_markdown: Get the markdown representation of the document as a string.
        get_all_additional_files: Get all additional files associated with the document.
        publish: Publishes the document by exporting it to a Markdown file and any additional files.
    """

    title: str = attrs.field(
        metadata={'description': 'The title of the markdown document'},
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.min_len(1)],
        kw_only=True)
    components: list[MDComponent] = attrs.field(
        factory=list,
        metadata={'description': 'List of components in the document'},
        validator=attrs.validators.optional(attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(MDComponent))),
        kw_only=True)

    def add_component(self, *component: MDComponent) -> None:
        """
        Add a component to the document.

        Parameters:
            component: The component to be added to the document.

        Returns:
            None
        """
        self.components.extend(component)

    def get_markdown(self) -> str:
        """
        Get the markdown representation of the document as string.

        Returns:
            str: The markdown representation of the document.
        """
        return f"# {self.title}\n\n" + "".join([c.render() for c in self.components])

    def get_all_additional_files(self) -> list[MDExtraFile]:
        """
        Get all additional files associated with the document.

        Returns:
            list[MDExtraFile]: List of additional files.
        """
        additional_files = []
        for c in self.components:
            additional_files.extend(c.get_additional_files())
        return additional_files

    def publish(self,
                *,
                md_file_path: Path,
                exist_ok: bool = False
                ) -> list[Path]:
        """
        Publishes the document by exporting it to a Markdown file and any additional files.

        Args:
            md_file_path (Path): The path to the Markdown file to be exported.
            exist_ok (bool, optional): If False (default), raises an error if
             the Markdown file already exists.
             If True, overwrites the existing file. Defaults to False.

        Returns:
            list[Path]: A list of paths to the exported files.

        Raises:
            FileExistsError: If the Markdown file already exists and `exist_ok` is False.
        """

        # check the file extension
        if md_file_path.suffix not in ALLOWED_MARKDOWN_EXTENSIONS:
            raise ValueError((
                f"Invalid file extension: {md_file_path.suffix} - ",
                f"Allowed extensions: {ALLOWED_MARKDOWN_EXTENSIONS}"))

        if md_file_path.exists() and not exist_ok:
            raise FileExistsError(f"{md_file_path} already exists.")

        # export the md file
        exported_files = [write_string_to_file(
            file_path=md_file_path,
            content=self.get_markdown(),
            exist_ok=exist_ok)]

        # export additional files
        exported_files.extend([
            f.export(md_file_path.parent) for f in self.get_all_additional_files()])

        return exported_files


    def __str__(self):
        return self.get_markdown()

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title})"
