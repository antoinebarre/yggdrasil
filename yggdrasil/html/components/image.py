"""Image component for the HTML report."""

from pathlib import Path
from typing import Optional
from beartype import beartype

from yggdrasil.validation.files import validate_file_extension
from .blocks import InlineHTMLComponent, HTMLBlock
from ..base import HTMLAdditionalFile

__all__ = ["Image"]

ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
IMAGE_HTML_DIRECTORY = 'images'
IMAGE_HTML_TAG = 'img'

@beartype
def Image(  # pylint: disable=invalid-name
    *,
    src_path: Path,
    alt_text: str,
    width: Optional[int]    = None,
    height: Optional[int]   = None,
    legend: Optional[str]   = None
    ) -> HTMLBlock:
    """
    Create an image component with the specified source path, alt text, width, and height.

    Args:
        src_path (Path): The path to the image file.
        alt (str): The alternative text for the image.
        width (Optional[int]): The width of the image (default: None).
        height (Optional[int]): The height of the image (default: None).

    Returns:
        InlineHTMLComponent: The image component.

    Raises:
        FileNotFoundError: If the image file does not exist.
    """
    # validate the file extension
    src_path= validate_file_extension(src_path, ALLOWED_IMAGE_EXTENSIONS)

    # check if the file exists
    if not src_path.is_file():
        raise FileNotFoundError(f"The file {src_path} does not exist.")
    # create the figure component
    fig = HTMLBlock(tag_name='figure')

    # add the image component
    fig.add_components(__create_img(src_path, alt_text, width, height))

    # add the legend component if specified
    if legend:
        caption = HTMLBlock(tag_name='figcaption')
        caption.add_components(legend)
        fig.add_components(caption)

    return fig


def __create_img(
    src_path: Path,
    alt_text: str,
    width: Optional[int],
    height: Optional[int]
) -> InlineHTMLComponent:
    """
    Create an image component with the specified source path, alt text, width, and height.

    Args:
        src_path (Path): The path to the image file.
        alt (str): The alternative text for the image.
        width (Optional[int]): The width of the image (default: None).
        height (Optional[int]): The height of the image (default: None).

    Returns:
        InlineHTMLComponent: The image component.

    Raises:
        FileNotFoundError: If the image file does not exist.
    """

    # instantiate the image component
    img = InlineHTMLComponent(  # pylint: disable=unexpected-keyword-arg
        tag_name=IMAGE_HTML_TAG,
        additional_file=HTMLAdditionalFile(
            original_file=src_path,
            filename=src_path.name,
            directory_name=IMAGE_HTML_DIRECTORY
            )
        )

    # add the alt attribute
    img.add_attribute('alt', alt_text)

    # add the src attribute
    img.add_attribute('src', f"{IMAGE_HTML_DIRECTORY}/{src_path.name}")

    # add the width attribute
    if width:
        img.add_attribute('width', str(width))

    # add the height attribute
    if height:
        img.add_attribute('height', str(height))
    return img
