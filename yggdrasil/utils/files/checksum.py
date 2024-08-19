"""Class to analyze and manage files in a safe way"""

import hashlib
from dataclasses import KW_ONLY, dataclass, field
from pathlib import Path
from typing import Callable
from datetime import datetime, timezone

import attrs

from ..argument_validation.files import validate_existing_file

__all__ = [ "md5_checksum", "sha256_checksum","File", "FileProperties"]

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

    @property
    def last_modified(self) -> str:
        """
        Returns the last modified time (UTC) of the file.
        """
        return datetime.fromtimestamp(
            self.path.stat().st_mtime,
            tz=timezone.utc
            ).isoformat()


@attrs.define(slots=True, frozen=True)
class FileProperties:
    """Represents properties of a file.

    Attributes:
        filepath (Path): The path to the file.
        checksum_method (Callable[[Path], str]): The method used to calculate the checksum.

    Properties:
        checksum (str): The checksum of the file.
        size (int): The size of the file in bytes.
        name (str): The name of the file.
        parent (Path): The parent directory of the file.
        extension (str): The file extension.
        last_modified (str): The last modified time (UTC) of the file.

    Methods:
        __str__(): Returns a string representation of the FileProperties object.
        __repr__(): Returns a string representation of the FileProperties object that can be used to recreate the object.
        __eq__(value: object) -> bool: Checks if two FileProperties objects are equal.
    """

    filepath : Path = attrs.field(
        metadata={'description': 'The path to the file'},
        converter=Path,
        )
    checksum_method:Callable[[Path], str] = attrs.field(
        metadata={'description': 'The method used to calculate the checksum'},
        default=md5_checksum,
        )

    @filepath.validator
    def _validate_path(self, attribute, value:Path):
        if not value.is_file():
            raise ValueError(
                f"The path {value} does not represent an existing file.")

    @checksum_method.validator
    def _validate_checksum_method(
        self,
        attribute,
        value:Callable[[Path], str]):
        if not callable(value):
            raise ValueError(
                "The checksum method must be a callable function.")


    @property
    def checksum(self) -> str:
        """
        Returns the checksum of the file.
        """
        return self.checksum_method(self.filepath)

    @property
    def size(self) -> int:
        """
        Returns the size of the file in bytes.
        """
        return self.filepath.stat().st_size

    @property
    def name(self) -> str:
        """
        Returns the name of the file.
        """
        return self.filepath.name

    @property
    def parent(self) -> Path:
        """
        Returns the parent directory of the file.
        """
        return self.filepath.parent

    @property
    def extension(self) -> str:
        """
        Returns the file extension.
        """
        return self.filepath.suffix

    @property
    def last_modified(self) -> str:
        """
        Returns the last modified time (UTC) of the file.
        """
        return datetime.fromtimestamp(
            self.filepath.stat().st_mtime,
            tz=timezone.utc
            ).isoformat()

    def __str__(self) -> str:
        return (
            f"File: {self.filepath}\n"
            f" - checksum: {self.checksum} (method: {self.checksum_method.__name__})\n"
            f" - size: {self.size} bytes\n"
            f" - last modified: {self.last_modified}\n"
            )

    def __repr__(self) -> str:
        return (
            f"FileProperties(filepath={self.filepath!r},"
            f" checksum_method={self.checksum_method.__name__!r})")

    def __eq__(self, value: object) -> bool:
        """
        Checks if two FileProperties objects are equal.

        Args:
            value (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(value, FileProperties):
            return False
        return (
            self.checksum == value.checksum
            and self.checksum_method == value.checksum_method)
