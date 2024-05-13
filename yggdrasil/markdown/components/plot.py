"""Markdown component for rendering Matplotlib figures as images."""


from dataclasses import KW_ONLY, dataclass
from pathlib import Path
from matplotlib.figure import Figure

from .basic import MDComponent,MDExtraFile
from ...utils.string import normalize_string

__all__ = ['Plot']
# Constants
FILENAME_MAX_LENGTH = 50
DEFAULT_DPI = 100
DESTINATION_DIRECTORY = 'plots'
IMAGE_EXTENSION = 'png'

@dataclass
class MatplotlibFigure(MDExtraFile):
    """
    Represents a Matplotlib figure.

    Attributes:
        figure_name (str): The name of the figure.
        figure (Figure): The Matplotlib figure object.
        dpi (int): The resolution of the saved figure in dots per inch (default is 100).
    """

    _: KW_ONLY
    figure_name: str
    figure: Figure
    dpi: int = 100

    __destination_directory = DESTINATION_DIRECTORY

    def get_file_name(self) -> str:
        """
        Get the name of the file to save the figure as.

        Returns:
            str: The name of the file.
        """
        # get the name of the file
        title = normalize_string(self.figure_name).replace(' ', '_')

        # limit the length of the title to 50 characters
        title = title[:FILENAME_MAX_LENGTH]

        return f"{title}.{IMAGE_EXTENSION}"

    def get_relative_path(self) -> Path:
        """
        Get the relative path to the figure.

        Returns:
            Path: The relative path to the figure.
        """
        return Path(self.__destination_directory) / self.get_file_name()


    def export(self, output_dir: Path) -> Path:
        """
        Export the figure to a file.

        Args:
            output_dir (Path): The directory to save the figure in.

        Returns:
            Path: The path to the saved figure.
        """
        # Create the target directory if it does not exist
        target_dir = output_dir / DESTINATION_DIRECTORY
        target_dir.mkdir(parents=True, exist_ok=True)

        # Save the figure
        file_path = target_dir / self.get_file_name()
        self.figure.savefig(
            file_path,
            dpi=self.dpi,
            format=IMAGE_EXTENSION)

        return file_path


class Plot(MDComponent):
    """
    Represents a plot component that can be rendered in Markdown.

    Args:
        figure_name (str): The name of the figure.
        fig (Figure): The matplotlib figure object.
        dpi (int, optional): The resolution of the figure in dots per inch. Defaults to 100.

    Attributes:
        figure_name (str): The name of the figure.
        fig (MatplotlibFigure): The wrapped matplotlib figure object.

    Methods:
        render: Renders the plot component as a Markdown image.
        get_additional_files: Returns a list of additional files required for rendering.

    """

    def __init__(self, figure_name: str, fig: Figure, dpi: int = 100):
        # manage the figure name
        if not figure_name:
            raise ValueError("The figure name must be provided.")

        self.figure_name = figure_name

        # create the figure
        self.fig = MatplotlibFigure(
            figure_name=figure_name,
            figure=fig,
            dpi=dpi)

    def render(self) -> str:
        """
        Renders the plot component as a Markdown image.

        Returns:
            str: The Markdown image syntax for the plot component.

        """
        return f"![{self.figure_name}]({self.fig.get_relative_path()})"

    def get_additional_files(self) -> list[MDExtraFile]:
        """
        Returns a list of additional files required for rendering.

        Returns:
            list[MDExtraFile]: A list of additional files required for rendering.

        """
        return [self.fig]
