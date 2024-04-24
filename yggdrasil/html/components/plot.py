"""Components used to integrate a Matplotlib figure in a HTML report"""

from dataclasses import KW_ONLY, dataclass
from pathlib import Path
from typing import Optional
from matplotlib.figure import Figure

from ..base import HTMLExtraFile
from ._blocks import HTMLBlock, InlineHTMLComponent
from ...utils.string import normalize_string

__all__ = ['Plot']

FILENAME_MAX_LENGTH = 50
IMAGE_HTML_DIRECTORY = 'plots'
IMAGE_HTML_TAG = 'img'

@dataclass
class AdditionalMatplotlibFigure(HTMLExtraFile):
    _: KW_ONLY
    figure_name : str
    figure : Figure
    directory_name: Optional[str] = None
    dpi : int = 100

    def get_file_name(self) -> str:
        # get the name of the file
        title = normalize_string(self.figure_name).replace(' ', '_')

        # limit the length of the title to 50 characters
        title = title[:FILENAME_MAX_LENGTH]

        return f"{title}.png"

    def export(self, output_dir: Path) -> None:

        # Create the target directory if it does not exist
        target_dir = output_dir / self.directory_name if self.directory_name else output_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        # get the target file path
        target_file = target_dir / self.get_file_name()

        # save the figure
        self.figure.savefig(target_file,dpi=self.dpi,format='png')

    def get_status(self) -> str:
        return "TO BE DONE"

def Plot(
    *,
    figure_name: str,
    figure: Figure,
    width: Optional[int]    = None,
    height: Optional[int]   = None,
    legend: Optional[str]   = None
    ) -> HTMLBlock:

    # create the figure component
    fig = HTMLBlock(tag_name='figure')

    # add the image component
    fig.add_components(__create_plot(figure, figure_name, width, height))

    # add the legend component if specified
    if legend:
        caption = HTMLBlock(tag_name='figcaption')
        caption.add_components(legend)
        fig.add_components(caption)

    return fig

def __create_plot(
    figure: Figure,
    figure_name: str,
    width: Optional[int],
    height: Optional[int]
) -> InlineHTMLComponent:

    # create additional file for the figure
    additional_file = AdditionalMatplotlibFigure(
        figure=figure,
        figure_name=figure_name,
        directory_name=IMAGE_HTML_DIRECTORY
        )

    # instantiate the image component
    img = InlineHTMLComponent(  # pylint: disable=unexpected-keyword-arg
        tag_name=IMAGE_HTML_TAG,
        additional_file=additional_file
        )

    # add the alt attribute
    img.add_attribute('alt', figure_name)

    # add the src attribute
    img.add_attribute('src', f"{IMAGE_HTML_DIRECTORY}/{additional_file.get_file_name()}")

    # add the width attribute
    if width:
        img.add_attribute('width', str(width))

    # add the height attribute
    if height:
        img.add_attribute('height', str(height))
    return img