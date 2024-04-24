"""Base classes for HTML report components."""


from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod
import attrs

from ..utils.fileIO._handling import copy_file


class HTMLExtraFile(ABC):
    """ Base class for additional files to be included in the output directory."""
    @abstractmethod
    def export(self, output_dir: Path):
        """export method to be implemented by the subclass"""

    @abstractmethod
    def get_status(self) -> str:
        """Returns the status of the file"""

@attrs.define
class HTMLAdditionalFile(HTMLExtraFile):
    """
    Represents an additional file to be included in the output directory.

    Attributes:
        original_file (Path): The original file to be copied to the output directory.
        filename (str): The name of the file with extension in the output directory.
        directory_name (Optional[str]): The name of the directory in which the file will
        be copied within the target directory.
    """

    original_file: Path = attrs.field(
        validator=attrs.validators.instance_of(Path),
        kw_only=True,
        metadata={
            'description': 'The original file to be copied to the output directory.'})

    filename : str = attrs.field(
        validator=attrs.validators.instance_of(str),
        kw_only=True,
        metadata={
            'description': 'The name of the file with extension in the output directory.'})

    directory_name: Optional[str] = attrs.field(
        factory=None,
        validator=[attrs.validators.optional(attrs.validators.instance_of(str))],
        kw_only=True,
        metadata={
            'description': 'The name of the directory in which the file' +
                ' will be copied with in the target directory.'}
        )

    def post_init(self):
        """
        Performs post-initialization tasks.

        This method checks if the original file exists. If it doesn't,
         it raises a FileNotFoundError.

        Raises:
            FileNotFoundError: If the original file does not exist.
        """
        #check if the original file exists
        if not self.original_file.exists():
            raise FileNotFoundError(f"The file {self.original_file} does not exist.")

    def export(self, output_dir: Path) -> None:

        # Create the target directory if it does not exist
        target_dir = output_dir / self.directory_name if self.directory_name else output_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy the file
        target_file = target_dir / self.filename

        copy_file(
            source_path=self.original_file,
            destination_path=target_file)

    def get_status(self) -> str:
        return f"File {self.original_file} has been copied to {self.directory_name}/{self.filename}."


class HTMLComponent(ABC):
    """
    Base class for HTML components.

    This class defines the interface for HTML components, which includes the `render`,
     `get_additional_files`, and `get_tag` methods.
    Subclasses of `HTMLComponent` should implement these methods to provide the
     desired functionality.
    """

    @abstractmethod
    def render(self) -> str:
        """
        Renders the HTML representation of the object.

        Returns:
            A string containing the HTML representation.
        """

    @abstractmethod
    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Returns a list of additional HTML files that should be included in the output.

        :return: A list of HTMLExtraFile objects representing the additional files.
        """

    @abstractmethod
    def get_tag(self) -> str:
        """
        Returns the tag associated with the HTML element.

        :return: The tag of the HTML element.
        :rtype: str
        """
