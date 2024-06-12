"""Test cases for the sha256_checksum function in the yggdrasil.utils.files module."""

from pathlib import Path
import hashlib
from unittest.mock import patch
import pytest
# Assuming the sha256_checksum function and validate_existing_file are defined in the same module
from yggdrasil.utils.files import sha256_checksum

# Mock the validate_existing_file to simply return the file_path for testing purposes
@pytest.fixture
def mock_validate_existing_file():
    """
    Mocks the 'validate_existing_file' function and returns the input argument as is.

    Returns:
        MagicMock: The mock object that can be used to assert the behavior of the
        'validate_existing_file' function.

    Example:
        with mock_validate_existing_file() as mock:
            # Perform test actions
            pass
    """
    with patch('yggdrasil.validation.files.validate_existing_file') as mock:
        mock.side_effect = lambda x: x
        yield mock

def test_sha256_checksum_valid_file(mock_validate_existing_file, tmp_path):  #pylint: disable=redefined-outer-name, unused-argument
    """
    Test case to verify the correctness of the sha256_checksum function when provided
    with a valid file.

    Args:
        mock_validate_existing_file: A mock object for the validate_existing_file function.
        tmp_path: A temporary directory path provided by pytest.

    Returns:
        None

    Raises:
        AssertionError: If the calculated SHA-256 checksum does not match the expected value.
    """
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    with open(test_file, "wb") as f:
        f.write(content)

    # Calculate the expected SHA-256 checksum
    expected_sha256 = hashlib.sha256(content).hexdigest()

    # Call the function and assert the result
    result = sha256_checksum(test_file)
    assert result == expected_sha256

def test_sha256_checksum_empty_file(mock_validate_existing_file, tmp_path):  #pylint: disable=redefined-outer-name, unused-argument
    """
    Test the SHA-256 checksum calculation for an empty file.

    Args:
        mock_validate_existing_file: A mock object for validating an existing file.
        tmp_path: A temporary directory path provided by pytest.

    Returns:
        None
    """

    # Create an empty temporary file
    test_file = tmp_path / "empty_file.txt"
    test_file.touch()

    # Calculate the expected SHA-256 checksum for an empty file
    expected_sha256 = hashlib.sha256(b"").hexdigest()

    # Call the function and assert the result
    result = sha256_checksum(test_file)
    assert result == expected_sha256

def test_sha256_checksum_non_existent_file(): #pylint: disable=redefined-outer-name, unused-argument
    """
    Test case to verify that the sha256_checksum function raises a FileNotFoundError
    when given a non-existent file.

    Args:
        mock_validate_existing_file: A mock object for the validate_existing_file function.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    # Create a Path object for a non-existent file
    non_existent_file = Path("/non/existent/file.txt")

    # Expect the function to raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        sha256_checksum(non_existent_file)
