"""Base classes for HTML report components."""


from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod
import attrs

from ..utils.fileIO._handling import copy_file
from ..utils.string import indent


@attrs.define
class HTMLStringContent():
    header: Optional[str] = attrs.field(
        default=None,
        validator=[attrs.validators.optional(attrs.validators.instance_of(str))])
    body: Optional[str] = attrs.field(
        default=None,
        validator=attrs.validators.instance_of(str))
    footer: Optional[str] = attrs.field(
        default=None,
        validator=[attrs.validators.optional(attrs.validators.instance_of(str))])


class HTMLExtraFile(ABC):
    """ Base class for additional files to be included in the output directory."""
    @abstractmethod
    def export(self, output_dir: Path):
        """export method to be implemented by the subclass"""

@attrs.define
class HTMLAdditionalFile(HTMLExtraFile):
    """
    Represents an additional HTML file to be included in the output directory.

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
        default=None,
        validator=[attrs.validators.optional(attrs.validators.instance_of(str))],
        kw_only=True,
        metadata={
            'description': 'The name of the directory in which the file' +
                ' will be copied with in the target directory.'}
        )

    def post_init(self):
        #check if the original file exists
        if not self.original_file.exists():
            raise FileNotFoundError(f"The file {self.original_file} does not exist.")

    def export(self, output_dir: Path):

        # Create the target directory if it does not exist
        target_dir = output_dir / self.directory_name if self.directory_name else output_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy the file
        target_file = target_dir / self.filename

        copy_file(
            source_path=self.original_file,
            destination_path=target_file)


class HTMLComponent(ABC):
    _DEFAULT_INDENT_LEVEL = 4
    _DEFAULT_INDENT_CHAR = ' '

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def get_additional_files(self) -> list[HTMLExtraFile]:
        pass
    
    @abstractmethod
    def get_tag(self) -> str:
        pass