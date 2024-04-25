from pathlib import Path
from PIL import Image
import numpy as np

from yggdrasil.validation.files import validate_file_extension

__all__ = ["create_random_png"]

def create_random_png(
        filename: Path,
        width=256,
        height=256,) -> Path:
    """
    Create a random PNG image with the specified dimensions and save it to the given filename.

    Args:
        filename (Path): The path to save the PNG image.
        width (int, optional): The width of the image in pixels. Defaults to 256.
        height (int, optional): The height of the image in pixels. Defaults to 256.

    Returns:
        Path: The path to the saved PNG image.
    """

    # validate the filename
    filename = validate_file_extension(filename, [".png"])

    # Generate an array of random colors
    random_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

    # Create an image from the array
    image = Image.fromarray(random_data)

    # Save the image
    image.save(filename)

    return filename
