"""Test cases for the 'md5_checksum' function in the 'yggdrasil.utils.files' module."""

from pathlib import Path
import hashlib
from unittest.mock import patch
import pytest

# Assuming the md5_checksum function and validate_existing_file are defined in the same module
from yggdrasil.utils.files import md5_checksum

# Mock the validate_existing_file to simply return the file_path for testing purposes
@pytest.fixture
def mock_validate_existing_file():
    """
    Mocks the 'validate_existing_file' function and returns the input argument as is.

    Returns:
        MagicMock: The mock object that mocks the 'validate_existing_file' function.

    Example:
        with mock_validate_existing_file() as mock:
            mock.return_value = 'test_file.txt'
            result = validate_existing_file('test_file.txt')
            assert result == 'test_file.txt'
    """
    with patch('yggdrasil.utils.argument_validation.files.validate_existing_file') as mock:
        mock.side_effect = lambda x: x
        yield mock

def test_md5_checksum_valid_file(mock_validate_existing_file, tmp_path):  #pylint: disable=redefined-outer-name, unused-argument
    """
    Test case to verify the correctness of the MD5 checksum calculation for a valid file.

    Args:
        mock_validate_existing_file: A mock object for validating an existing file.
        tmp_path: A temporary directory path provided by pytest.

    Returns:
        None
    """
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    with open(test_file, "wb") as f:
        f.write(content)

    # Calculate the expected MD5 checksum
    expected_md5 = hashlib.md5(content).hexdigest()

    # Call the function and assert the result
    result = md5_checksum(test_file)
    assert result == expected_md5

def test_md5_checksum_empty_file(mock_validate_existing_file, tmp_path):  #pylint: disable=redefined-outer-name, unused-argument
    """
    Test case for calculating the MD5 checksum of an empty file.

    Args:
        mock_validate_existing_file: A mock object for validating an existing file.
        tmp_path: A temporary directory path provided by pytest.

    Returns:
        None
    """
    # Create an empty temporary file
    test_file = tmp_path / "empty_file.txt"
    test_file.touch()

    # Calculate the expected MD5 checksum for an empty file
    expected_md5 = hashlib.md5(b"").hexdigest()

    # Call the function and assert the result
    result = md5_checksum(test_file)
    assert result == expected_md5

def test_md5_checksum_non_existent_file():
    """
    Test case to verify that the md5_checksum function raises a FileNotFoundError
    when given a non-existent file.
    """
    # Create a Path object for a non-existent file
    non_existent_file = Path("/non/existent/file.txt")

    # Expect the function to raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        md5_checksum(non_existent_file)