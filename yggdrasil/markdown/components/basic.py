

from abc import ABC, abstractmethod
from pathlib import Path

class MDExtraFile(ABC):
    """ Base class for additional files to be included in the output directory."""
    @abstractmethod
    def export(self, output_dir: Path) -> Path:
        """export method to be implemented by the subclass"""

class MDComponent(ABC):
    """Abstract base class for Markdown components."""

    @abstractmethod
    def render(self) -> str:
        """Render the component to a string."""

    @abstractmethod
    def get_additional_files(self) -> list[MDExtraFile]:
        """Get additional files required by the component."""
