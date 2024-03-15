""" Tools for working with children of a component. """


from typing import Iterable
from ..base import HTMLComponent
from .text import Text

def get_children(children : Iterable[HTMLComponent | str ]) -> list[HTMLComponent]:
    """
    Get the HTML components from an iterable of children of HTMLComponent or string type.

    Args:
        children (Iterable[HTMLComponent | str]): Iterable of children.

    Returns:
        list[HTMLComponent]: List of HTML components.
    """
    return [
        child if isinstance(child, HTMLComponent) else Text(child)
        for child in children
    ]

def validate_children(children: Iterable[HTMLComponent | str]) -> None:
    """
    Validate that the children are valid HTML components.

    Args:
        children (Iterable[HTMLComponent | str]): Iterable of children.

    Raises:
        ValueError: If a child is not a valid HTML component.
    """
    for child in children:
        if not isinstance(child, HTMLComponent) and not isinstance(child, str):
            raise ValueError(f"Invalid child {child}. Must be an HTML component or a string.")

def validate_tag(
    children: Iterable[HTMLComponent],
    allowed_tags: list[str]) -> None:
    """
    Validate that the children are valid HTML components.

    Args:
        children (Iterable[HTMLComponent]): Iterable of children.
        allowed_tags (list[str]): List of allowed tags.

    Raises:
        ValueError: If a child is not a valid HTML component.
    """

    for child in children:
        if child.get_tag() not in allowed_tags:
            raise ValueError(
                f"Invalid tag '{child.get_tag()}' " +
                f"for {child}. Allowed tags are {allowed_tags}"
)