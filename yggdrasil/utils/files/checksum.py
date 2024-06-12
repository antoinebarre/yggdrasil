"""Class to analyze and manage files in a safe way"""

import hashlib
from dataclasses import KW_ONLY, dataclass, field
from pathlib import Path
from typing import Callable

from ...validation.files import validate_existing_file

__all__ = ["SafeFile", "md5_checksum", "sha256_checksum","File"]

def md5_checksum(file_path: Path) -> str:
    """
    Calculate the MD5 checksum of a existing file.

    Args:
        file_path (Path): The path of the file to calculate the checksum.

    Returns:
        str: The MD5 checksum.
    """

    # Validate the file path
    file_path = validate_existing_file(file_path)

    # Open the file
    with open(file_path, "rb") as file_content:
        # Read the file in chunks
        chunk = 0
        md5 = hashlib.md5()
        while chunk := file_content.read(8192):
            md5.update(chunk)
    # Return the checksum
    return md5.hexdigest()

def sha256_checksum(file_path: Path) -> str:
    """
    Calculate the SHA-256 checksum of a existing file.

    Args:
        file_path (Path): The path of the file to calculate the checksum.

    Returns:
        str: The SHA-256 checksum.
    """
    # Validate the file path
    file_path = validate_existing_file(file_path)

    # Open the file
    with open(file_path, "rb") as file_content:
        # Read the file in chunks
        chunk = 0
        sha256 = hashlib.sha256()
        while chunk := file_content.read(8192):
            sha256.update(chunk)
    # Return the checksum
    return sha256.hexdigest()

@dataclass(frozen=True)
class SafeFile:
    """
    Represents a safe file with a file path and checksum.

    Attributes:
        file_path (Path): The path to the file.
        checksum_method (Callable[[Path], str]): The method used to calculate
        the checksum. Default is md5_checksum.
        checksum (str): The calculated checksum of the file.

    Methods:
        __post_init__(): Validates the file path and calculates the checksum.
        __repr__(): Returns a string representation of the SafeFile object.
        __str__(): Returns a string representation of the SafeFile object.
    """
    file_path: Path
    _ : KW_ONLY
    checksum_method: Callable[[Path], str] = md5_checksum
    checksum: str = field(init=False)

    def __post_init__(self):
        # Calculate and set the checksum
        checksum_value = self.checksum_method(self.file_path)
        object.__setattr__(self, 'checksum', checksum_value)

    def __repr__(self) -> str:
        return (
            f"SafeFile(file_path={self.file_path!r},"
            f" checksum={self.checksum!r},"
            f" checksum_method={self.checksum_method.__name__!r})")

    def __str__(self) -> str:
        return (
            f"SafeFile: {self.file_path}"
            f" with checksum {self.checksum}"
            f" (method: {self.checksum_method.__name__})")

    @classmethod
    def from_list(cls, file_list: list[Path]) -> list['SafeFile']:
        """
        Creates a list of SafeFile objects from a list of file paths.

        Args:
            file_list (list): A list of file paths.

        Returns:
            list: A list of SafeFile objects.
        """
        return [cls(file_path=Path(file_path)) for file_path in file_list]

@dataclass(frozen=True)
class File:
    """
    Represents a file with its path, checksum, size, and checksum method.

    Attributes:
        path (Path): The path to the file.
        checksum (str): The checksum value of the file.
        size (int): The size of the file in bytes.
        checksum_method (Callable[[Path], str]): The method used to calculate the checksum.

    Methods:
        __post_init__(): Calculates and sets the checksum and size of the file.
        __repr__(): Returns a string representation of the File object.
        __str__(): Returns a string representation of the File object.
        from_list(file_list, checksum_method): Creates a list of File objects from a list of file paths.
        __eq__(value): Checks if two File objects are equal.
        name(): Returns the name of the file.
        parent(): Returns the parent directory of the file.
        extension(): Returns the file extension.

    """

    path: Path
    _ : KW_ONLY
    checksum: str = field(init=False)
    size: int = field(init=False)
    checksum_method: Callable[[Path], str] = md5_checksum

    def __post_init__(self):
        """
        Calculates and sets the checksum and size of the file.
        """
        checksum_value = self.checksum_method(self.path)
        object.__setattr__(self, 'checksum', checksum_value)

        size = self.path.stat().st_size
        object.__setattr__(self, 'size', size)

    def __repr__(self) -> str:
        """
        Returns a string representation of the File object.
        """
        return (
            f"File(path={self.path!r},"
            f" checksum={self.checksum!r},"
            f" size={self.size!r},"
            f" checksum_method={self.checksum_method.__name__!r})")

    def __str__(self) -> str:
        """
        Returns a string representation of the File object.
        """
        return (
            f"File: {self.path}"
            f" with checksum {self.checksum}"
            f" (method: {self.checksum_method.__name__})"
            f" and size {self.size} bytes")

    @classmethod
    def from_list(
        cls,
        file_list: list[Path],
        checksum_method:Callable[[Path], str] = md5_checksum
        ) -> list['File']:
        """
        Creates a list of File objects from a list of file paths.

        Args:
            file_list (list): A list of file paths.

        Returns:
            list: A list of File objects.
        """
        return [cls(
            path=Path(file_path),
            checksum_method=checksum_method) for file_path in file_list]

    def __eq__(self, value: object) -> bool:
        """
        Checks if two File objects are equal.

        Args:
            value (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(value, File):
            return False
        return (
            self.checksum == value.checksum
            and self.checksum_method == value.checksum_method)

    @property
    def name(self) -> str:
        """
        Returns the name of the file.
        """
        return self.path.name

    @property
    def parent(self) -> Path:
        """
        Returns the parent directory of the file.
        """
        return self.path.parent

    @property
    def extension(self) -> str:
        """
        Returns the file extension.
        """
        return self.path.suffix