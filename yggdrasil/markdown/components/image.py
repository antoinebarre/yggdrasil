""" Image component in Markdown. """

from dataclasses import KW_ONLY, dataclass
from pathlib import Path
from .basic import MDComponent, MDExtraFile
from ...utils.files import copy_file

ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg"}
DEFAULT_IMAGE_DIRECTORY = "images"

__all__ = ["Image"]

@dataclass
class ImageFile(MDExtraFile):
    """
    Represents an image file.

    Attributes:
        image_path (Path): The path to the image file.
    """

    _: KW_ONLY
    image_path: Path
    __destination_directory = DEFAULT_IMAGE_DIRECTORY

    def __post_init__(self):
        if not self.image_path.exists():
            raise FileNotFoundError(f"The file {self.image_path} does not exist.")
        if not self.image_path.is_file():
            raise FileNotFoundError(f"{self.image_path} is not a file.")
        if self.image_path.suffix not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(f"Invalid image extension: {self.image_path.suffix}")

    def get_file_name(self) -> str:
        """
        Get the name of the file.

        Returns:
            str: The name of the file.
        """
        return self.image_path.name

    def get_relative_path(self) -> Path:
        """
        Get the relative path to the image.

        Returns:
            Path: The relative path to the image.
        """
        return Path(self.__destination_directory) / self.get_file_name()

    def export(self, output_dir: Path) -> Path:
        """
        Export the image to the specified output directory.

        Args:
            output_dir (Path): The directory where the image will be exported.

        Returns:
            Path: The path to the exported image file.
        """
        # create the destination directory
        destination_dir = output_dir / self.__destination_directory
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination_path = destination_dir / self.image_path.name

        # copy the file
        return copy_file(
            source_path=self.image_path,
            destination_path=destination_path)

    def __str__(self) -> str:
        return f"ImageFile({self.image_path})"

    def __repr__(self) -> str:
        return f"ImageFile(image_path={self.image_path})"

class Image(MDComponent):
    """
    Represents an image component in Markdown.

    Attributes:
        original_image_path (Path): The path to the original image file.
        replacement_text (str): The text to be displayed as the image's alternative text.
    """

    def __init__(self, original_image_path: Path, replacement_text: str):
        """
        Initializes an image component.

        Args:
            original_image_path (Path): The path to the original image file.
            replacement_text (str): The text to be displayed as the image's alternative text.
        """
        self.replacement_text = replacement_text
        self.image_file = ImageFile(image_path=original_image_path)

    def render(self) -> str:
        """
        Renders the image component as a Markdown string.

        Returns:
            str: The Markdown representation of the image component.
        """
        return f"![{self.replacement_text}]({self.image_file.get_relative_path()})"

    def get_additional_files(self) -> list[MDExtraFile]:
        """
        Retrieves any additional files associated with the image component.

        Returns:
            list[MDExtraFile]: A list of additional files.
        """
        return [self.image_file]
