from dataclasses import dataclass, field
import warnings

from .text import Text
from .basic import MDComponent, MDExtraFile
from .format import MDFormat


@dataclass
class Paragraph(MDComponent):
    """
    Represents a paragraph in a Markdown document.

    Attributes:
        title (str): The title of the paragraph.
        components (list[MDComponent]): The list of child components.
        _level (int): The level of the paragraph structure.

    Methods:
        get_additional_files() -> list[MDExtraFile]: Get a list of additional files required by the article.
        add_components(*component: MDComponent) -> None: Add a component to the document.
        render() -> str: Render the paragraph.
    """

    title: str
    components: list[MDComponent] = field(default_factory=list)
    _level: int = field(init=False, default=1)

    def set_level(self, level: int) -> None:
        """
        Set the level of the structure.

        Args:
            level (int): The level to set.

        Returns:
            None
        """
        self._level = level

    def __set__children_level(self) -> None:
        """
        Set the level of the child articles.
        """
        if self.components:
            for component in self.components:
                if isinstance(component, Paragraph):
                    # check maximum level
                    if self._level < 6:
                        component.set_level(self._level + 1)
                    else:
                        component.set_level(6)
                        warnings.warn(
                            "The maximum level of heading is 6.")

    def set_title(self) -> str:
        """
        Get the title of the article.

        Returns:
            str: The title of the article.
        """
        return MDFormat.heading(text=self.title, level=self._level)

    def get_additional_files(self) -> list[MDExtraFile]:
        """
        Get a list of additional files required by the article.

        Returns:
            list[MDExtraFile]: List of additional files.
        """
        additional_files = []
        if self.components:
            for component in self.components:
                additional_files.extend(component.get_additional_files())
        return additional_files

    def add_components(self, *component: MDComponent) -> None:
        """
        Add a component to the document.

        Parameters:
            component: The component to be added to the document.

        Returns:
            None
        """
        self.components.extend(component)
        
    def add_text(self, text: str) -> None:
        """
        Add a text component to the document.

        Parameters:
            text: The text to be added to the document.

        Returns:
            None
        """
        self.components.append(Text(text))

    def render(self) -> str:
        """
        Render the paragraph.

        Returns:
            str: The rendered paragraph.
        """

        self.__set__children_level()
        return (
            self.set_title() + "\n" +
            ("\n").join([c.render() for c in self.components])
        )
