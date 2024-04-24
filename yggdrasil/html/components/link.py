

import importlib.resources as pkg_resources
from pathlib import Path


from ...validation.fileIO import validate_file_extension
from ..base import HTMLAdditionalFile
from ._blocks import InlineHTMLComponent


__all__ = ['CSSStyleSheet', 'default_css_stylesheet']

STYLE_DIRECTORY= 'styles'

def CSSStyleSheet(
    filepath: Path
    ) -> InlineHTMLComponent:
    """
    Create a CSS style sheet component with the specified file path.

    Args:
        filepath (Path): The path to the CSS file.

    Returns:
        InlineHTMLComponent: The CSS style sheet component.

    Raises:
        FileNotFoundError: If the CSS file does not exist.
    """
    # check if the file exists
    if not filepath.is_file():
        raise FileNotFoundError(f"The file {filepath} does not exist.")

    # validate the file extension
    filepath = validate_file_extension(filepath, ['.css'])

    # instantiate the CSS style sheet component
    css = InlineHTMLComponent(  # pylint: disable=unexpected-keyword-arg
        tag_name='link',
        additional_file=HTMLAdditionalFile(
            original_file = filepath,
            filename = filepath.name,
            directory_name = STYLE_DIRECTORY
            )
        )

    # add the rel attribute
    css.add_attribute('rel', 'stylesheet')

    # add the type attribute
    css.add_attribute('type', 'text/css')

    # add the href attribute
    css.add_attribute('href', f"{STYLE_DIRECTORY}/{filepath.name}")

    return css

def default_css_stylesheet():
    with pkg_resources.path("yggdrasil.html.templates", "report.css") as css_path:
        # css_path is a Path object that can be used within this block
        return CSSStyleSheet(Path(css_path))