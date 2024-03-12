
from ..base import HTMLComponent, HTMLExtraFile

def collect_additional_files(components: list[HTMLComponent]) -> list[HTMLExtraFile]:
    """
    Collects additional files required by a list of HTML components.

    Args:
        components (list[HTMLComponent]): The list of HTML components.

    Returns:
        list[AdditionalFile]: A list of additional files required by the components.
    """
    additional_files = []
    for component in components:
        additional_files += component.get_additional_files()
    return additional_files