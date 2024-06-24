"""Test functions for the yggdrasil.validation.files module."""

from pathlib import Path
import pytest
from yggdrasil.utils.argument_validation.files import (
    validate_path,
    validate_file_extension,
    validate_existing_file)

# Test validate_path function
def test_validate_path():
    """
    Test the validate_path function.

    This function tests the behavior of the validate_path function by passing
    different types of paths as input.

    - Test with a valid string path
    - Test with a valid Path object
    - Test with an invalid file path

    The function asserts that the output of the validate_path function matches
    the expected output for each test case.
    If the output does not match the expected output, an AssertionError is raised.

    Raises:
        TypeError: If an invalid file path is passed as input.

    """
    assert validate_path("/path/to/file.txt") == Path("/path/to/file.txt")

    assert validate_path(Path("/path/to/file.txt")) == Path("/path/to/file.txt")

    with pytest.raises(TypeError):
        validate_path(123) # type: ignore

# Test validate_file_extension function
def test_validate_file_extension():
    """
    Test the validate_file_extension function.

    This function tests the behavior of the validate_file_extension function by providing
    a file path with both valid and invalid file extensions.

    - Test with a valid file extension: The function should return the same file path if the
        file extension is in the list of valid extensions.
    - Test with an invalid file extension: The function should raise a ValueError if the
        file extension is not in the list of valid extensions.
    """
    assert validate_file_extension(
        Path("/path/to/file.txt"),
        [".txt", ".csv"]) == Path("/path/to/file.txt")

    with pytest.raises(ValueError):
        validate_file_extension(Path("/path/to/file.jpg"), [".txt", ".csv"])

# Test validate_existing_file function
def test_validate_existing_file(tmp_path: Path):
    """
    Test the validate_existing_file function with an existing file and a non-existing file.

    Args:
        tmp_path (Path): The temporary directory path provided by pytest.

    Raises:
        FileNotFoundError: If the file does not exist.

    Returns:
        None
    """
    # Create a temporary file
    file_path = tmp_path / "test.txt"
    file_path.touch()

    # Test with an existing file
    assert validate_existing_file(file_path) == file_path

    # Test with a non-existing file
    with pytest.raises(FileNotFoundError):
        validate_existing_file(tmp_path / "non_existing.txt")
