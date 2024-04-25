"""Collection of tools to validate file paths."""

from pathlib import Path

__all__ = [
    "validate_path",
    "validate_file_extension",
    "validate_existing_file"]

def validate_path(file_path: Path | str ) -> Path:
    """
    Validate the given file path.

    Args:
        file_path (Path | str ): The file path to validate.

    Returns:
        Path: The validated file path.

    Raises:
        TypeError: If the file path is not a string or a Path object.
    """
    try:
        file_path = Path(file_path)
        return file_path
    except TypeError as e:
        raise TypeError(
            "The file path must be a string or a Path object.",
            f"Received: {file_path}, type {type(file_path)}"
        ) from e


def validate_file_extension(file_path: Path, extension: list[str]) -> Path:
    """
    Validates the file extension of a given file path.

    Args:
        file_path (Path): The path of the file to validate.
        extension (list[str]): A list of valid file extensions.

    Returns:
        Path: The validated file path.

    Raises:
        ValueError: If the file extension is not in the list of valid extensions.
    """

    # validate path
    file_path = validate_path(file_path)

    if file_path.suffix not in extension:
        raise ValueError(f"The file extension must be one of {extension}.")
    return file_path

def validate_existing_file(file_path: Path) -> Path:
    """
    Validates the existence of a file.

    Args:
        file_path (Path): The path of the file to validate.

    Returns:
        Path: The validated file path.

    Raises:
        FileNotFoundError: If the file does not exist.
    """

    # validate path
    file_path = validate_path(file_path)

    file_path.is_file()

    if file_path.is_file():
        return file_path
    raise FileNotFoundError(f"The file {file_path} does not exist.")
# Path: yggdrasil/utils/files/__init__.py
