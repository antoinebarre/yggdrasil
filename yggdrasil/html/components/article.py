"""Collection of structure components for HTML"""

from dataclasses import dataclass, field
from typing import Optional
import warnings

from ...utils.string.unique_id import UUID4, UniqueID, NoUniqueID

from ...utils.string import generate_unique_id
from .blocks import _create_string_block
from ..base import HTMLComponent, HTMLExtraFile
from .__childrenUtils import get_children
from .heading import h

# TODO : change to attrs and add validators

# TODO : limit the nature of the components that can be added to the article

@dataclass
class Article(HTMLComponent):
    """
    Represents an HTML article component with title and content.

    Articles are used to structure the content of an HTML document. an article can contain
    other articles, tables, images, lists, and other HTML components. The title of the article
    is rendered as a heading with a level that depends on the level of the article in the structure.

    Attributes:
        title (str): The title of the article.
        _content (list[HTMLComponent]): The list of HTML components that
        make up the content of the article.
        _level (int): The level of the article structure.
        class_ (Optional[str]): The CSS class of the article.

    Methods:
        set_level: Set the level of the structure.
        __set_children_level: Set the level of the child articles.
        __get_title: Get the title of the article.
        get_additional_files: Get a list of additional files required by the article.
        add_components: Add HTML or string components to the structure.
        render: Render the structure component as an HTML article.
        get_tag: Get the tag of the structure component.
    """

    title: str
    _content: list[HTMLComponent] = field(default_factory=list, init=False)
    _level: int = field(init=False, default=2)
    class_: Optional[str] = field(default=None, init=True)
    id_method:UniqueID = UUID4()
    id_: str = field(init=False)

    def __post_init__(self):
        """Initialize the article."""
        self.id_ = self.id_method.generate_unique_id()

    def set_level(self, level: int) -> None:
        """
        Set the level of the structure.

        Args:
            level (int): The level to set.

        Returns:
            None
        """
        self._level = level

    def __set_children_level(self) -> None:
        """
        Set the level of the child articles.
        """
        if self._content:
            for component in self._content:
                if isinstance(component, Article):
                    # check maximum level
                    if self._level < 6:
                        component.set_level(self._level + 1)
                    else:
                        component.set_level(6)
                        warnings.warn(
                            "The maximum level of heading is 6.")

    def __get_title(self) -> str:
        """
        Get the title of the article.

        Returns:
            str: The title of the article.
        """
        return h(level=self._level, title=self.title,id_=self.id_).render()

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Get a list of additional files required by the article.

        This method recursively collects additional files from the content components
        of the article and returns them as a list.

        Returns:
            A list of HTMLExtraFile objects representing the additional files required
            by the article.
        """
        additional_files = []
        if self._content:
            for component in self._content:
                additional_files.extend(component.get_additional_files())
        return additional_files

    def add_components(
                self,
                *component: HTMLComponent | str,
                ) -> None :
        """
        Add HTML or string components to the structure.

        Args:
            *component (HTMLComponent | str): The HTML components or strings to be added.

        Returns:
            None
        """
        # change all strings to Text components
        components = get_children(component)

        self._content += components

    def render(self) -> str:
        """
        Render the structure component as an HTML article.

        Returns:
            str: The rendered HTML article.
        """
        # set the children article level to the current level + 1
        self.__set_children_level()

        if self._content:
            content_str =  (self.__get_title() + "\n" +
                            "\n".join([component.render() for component in self._content]))
        else:
            content_str = self.__get_title()

        # create the class attribute
        class_attr = f' class="{self.class_}"' if self.class_ else ''

        return _create_string_block(
            prefix=f"<article{class_attr}>",
            suffix="</article>",
            content = content_str,
            inline=False
        )

    def get_tag(self) -> str:
        """
        Get the tag of the structure component.

        Returns:
            str: The tag of the structure component.
        """
        return "article"

    def get_id(self) -> str:
        """
        Returns the ID of the article.

        Returns:
            str: The ID of the article.
        """
        return self.id_

    def get_content(self) -> list[HTMLComponent]:
        """
        Returns the content of the article.

        Returns:
            list[HTMLComponent]: The content of the article.
        """
        return self._content

    def get_level(self) -> int:
        """
        Returns the level of the article.

        Returns:
            int: The level of the article.
        """

        # update the level of the children
        self.__set_children_level()

        return self._level