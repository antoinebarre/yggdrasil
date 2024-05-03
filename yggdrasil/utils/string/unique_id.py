"""All Unique ID generation functions."""


from abc import ABC, abstractmethod
import uuid

__all__ = ["UniqueID", "NoUniqueID", "UUID4"]

class UniqueID(ABC):
    """Abstract class for generating unique IDs."""

    @abstractmethod
    def generate_unique_id(self) -> str:
        """Generate a unique ID.

        Returns:
            str: The generated unique ID.
        """

class NoUniqueID(UniqueID):
    """Class for generating no unique IDs."""

    def generate_unique_id(self) -> str:
        """Generate a unique ID.

        Returns:
            str: The generated unique ID.
        """
        return ""

class UUID4(UniqueID):
    """Class for generating UUID4 unique IDs."""

    def generate_unique_id(self) -> str:
        """Generate a unique ID.

        Returns:
            str: The generated unique ID.
        """
        return str(uuid.uuid4())
