"""Collection of functions for creating list components."""

from typing import Literal, Optional

from ..base import HTMLComponent
from ._blocks import HTMLBlock
from .__childrenUtils import get_children, validate_children,validate_tag
from .__attributesUtils import validate_attributes

__all__ = ["UnorderedList", "OrderedList"]

ALLOWED_ATTRIBUTES_UNORDERED = ['class']
ALLOWED_TAG_UNORDERED = ["text","span",'a']


# TODO : allow nested unordered list


def UnorderedList(  # pylint: disable=invalid-name
    *children: HTMLComponent | str,
    attributes: Optional[dict[str, str]] = None) -> HTMLBlock:
    """
    Create an unordered list component.

    Args:
        *children: Variable-length argument list of child components or strings.
        attributes: Optional dictionary of attributes for the unordered list.

    Returns:
        An HTMLBlock representing the unordered list component.

    Raises:
        ValueError: If the children are not valid components.
    """

    # validate the children
    validate_children(children)
    components = get_children(list(children))
    validate_tag(components, ALLOWED_TAG_UNORDERED)

    # manage the attributes
    attributes = validate_attributes(ALLOWED_ATTRIBUTES_UNORDERED, attributes)

    # create the list component
    list_component = HTMLBlock(  #pylint: disable=abstract-class-instantiated, unexpected-keyword-arg
        children=[],
        tag_name="ul",
        attributes=attributes,
    )

    # change components to list members
    for component in components:
        member = HTMLBlock(
            children=[component],
            tag_name="li",
        )
        list_component.add_components(member)

    return list_component

ALLOWED_ATTRIBUTES_ORDERED = ['class']
ALLOWED_TAG_ORDERED = ["text","span",'a']

def OrderedList( # pylint: disable=invalid-name
    *children: HTMLComponent | str,
    type_: Optional[Literal["A", "a", "I", "i", "1"]] = None,
    attributes: Optional[dict[str, str]] = None) -> HTMLBlock:
    """
    Create an ordered list component.

    Args:
        *children: Variable-length argument list of child components or strings.
        attributes: Optional dictionary of attributes for the ordered list.

    Returns:
        An HTMLBlock representing the ordered list component.

    Raises:
        ValueError: If the children are not valid components.
    """

    # validate the children
    validate_children(children)
    components = get_children(list(children))
    validate_tag(components, ALLOWED_TAG_ORDERED)

    # manage the attributes
    attributes = validate_attributes(ALLOWED_ATTRIBUTES_ORDERED, attributes)

    # manage the type attribute
    if type_:
        if type_ not in ["A", "a", "I", "i", "1"]:
            raise ValueError(f"Invalid value for the type attribute: {type_}." +
                             " Allowed values are 'A', 'a', 'I', 'i', '1'.")
        attributes["type"] = type_

    # create the list component
    list_component = HTMLBlock(  #pylint: disable=abstract-class-instantiated, unexpected-keyword-arg
        children=[],
        tag_name="ol",
        attributes=attributes,
    )

    # change components to list members
    for component in components:
        member = HTMLBlock(
            children=[component],
            tag_name="li",
        )
        list_component.add_components(member)

    return list_component
