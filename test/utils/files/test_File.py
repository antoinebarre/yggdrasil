
from pathlib import Path
from unittest.mock import patch


import pytest

from yggdrasil.utils.files import File, md5_checksum

# create a fake and simple checksum function

def fake_checksum(file_path: Path) -> str:  #pylint: disable=unused-argument
    """
    Calculate the fake checksum for a given file.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The fake checksum of the file.
    """
    return "fake_checksum"

@pytest.fixture
def mock_validate_existing_file():
    with patch('yggdrasil.utils.argument_validation.files.validate_existing_file') as mock:
        mock.side_effect = lambda x: x
        yield mock

def test_file_initialization_with_default(mock_validate_existing_file, tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    with open(test_file, "wb") as f:
        f.write(content)

    # Calculate the expected MD5 checksum
    expected_md5 = md5_checksum(test_file)
    expected_size = len(content)

    # Initialize the File object
    file_obj = File(path=test_file)

    # Assert the attributes
    assert file_obj.path == test_file
    assert file_obj.checksum == expected_md5
    assert file_obj.size == expected_size
    assert file_obj.checksum_method == md5_checksum

def test_file_initialization_with_other_method(mock_validate_existing_file, tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    content = b"Hello, World!"
    with open(test_file, "wb") as f:
        f.write(content)

    # Calculate the expected SHA-256 checksum
    expected_chk = "fake_checksum"
    expected_size = len(content)

    # Initialize the File object with SHA-256 checksum method
    file_obj = File(path=test_file, checksum_method=fake_checksum)

    # Assert the attributes
    assert file_obj.path == test_file
    assert file_obj.checksum == expected_chk
    assert file_obj.size == expected_size
    assert file_obj.checksum_method == fake_checksum

def test_file_initialization_non_existent_file(mock_validate_existing_file):
    # Create a Path object for a non-existent file
    non_existent_file = Path("/non/existent/file.txt")

    # Expect the initialization to raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        File(path=non_existent_file)

def test_file_from_list(mock_validate_existing_file, tmp_path):
    # Create temporary files with some content
    file_paths = []
    for i in range(3):
        file = tmp_path / f"test_file_{i}.txt"
        with open(file, "wb") as f:
            f.write(b"Content")
        file_paths.append(file)

    # Initialize the File objects from the list
    file_list = File.from_list(file_paths)

    # Assert the length and types
    assert len(file_list) == 3
    for file_obj, file_path in zip(file_list, file_paths):
        assert isinstance(file_obj, File)
        assert file_obj.path == file_path

def test_file_properties(mock_validate_existing_file, tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    with open(test_file, "wb") as f:
        f.write(b"Content")

    # Initialize the File object
    file_obj = File(path=test_file)

    # Assert the properties
    assert file_obj.name == test_file.name
    assert file_obj.parent == test_file.parent
    assert file_obj.extension == test_file.suffix
    
def test_file_eq(mock_validate_existing_file, tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test_file.txt"
    with open(test_file, "wb") as f:
        f.write(b"Content")

    # Initialize the File objects
    file_obj1 = File(path=test_file)
    file_obj2 = File(path=test_file)

    # Assert the equality
    assert file_obj1 == file_obj2

def test_file_not_eq(mock_validate_existing_file, tmp_path):
    # Create temporary files with some content
    file1 = tmp_path / "test_file1.txt"

    with open(file1, "wb") as f:
        f.write(b"Content")
    file2 = tmp_path / "test_file2.txt"
    with open(file2, "wb") as f:
        f.write(b"Content2")

    # Initialize the File objects
    file_obj1 = File(path=file1)
    file_obj2 = File(path=file2)

    # Assert the inequality
    assert file_obj1 != file_obj2
