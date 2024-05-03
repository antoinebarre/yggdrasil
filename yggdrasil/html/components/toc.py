"""Tools to generate a table of contents for a page."""

from pathlib import Path
from typing import List
import importlib.resources as pkg_resources

from yggdrasil.html import Article, HTMLBlock, Division, Hyperlink
from ..base import HTMLComponent
from .generic_html_tag import Generic_block_HTML, Generic_inline_HTML
from .span import Span
from .link import CSSStyleSheet


def collect_toc_elements(
    body_elements: List[HTMLComponent],
    tags2search: list[str],
) -> List[Article]:
    """
    Collect the elements that will be included in the table of contents.

    Args:
        body_elements (List[HTMLComponent]): The elements of the body.
        tags2search (list[str]): The tags to search for.

    Returns:
        List[HTMLComponent]: The elements that will be included in the table of contents.
    """
    toc_elements = []
    for element in body_elements:
        if element.get_tag() in tags2search:
            toc_elements.append(element)
            if isinstance(element, Article):
                toc_elements += collect_toc_elements(element.get_content(), tags2search)
    return toc_elements

def create_link4toc(
    element: Article
) -> HTMLBlock:
    """
    Create a link to an element.

    Args:
        element (Article): The element to link to.

    Returns:
        HTMLBlock: The link to the element.
    """
    return Hyperlink(
        component=element.title,
        link=f"#{element.get_id()}",
        attributes={"class": f"toc_item{element.get_level()-1}"}
    )

def create_toc(
    body_elements: List[HTMLComponent]
) -> HTMLBlock:
    """
    Create the table of contents.

    Args:
        body_elements (List[Union[Article, HTMLBlock]]): The body of the page.

    Returns:
        HTMLBlock: The table of contents.
    """
    toc = Division(
        attributes={"class": "hamburger-menu"}
    )

    # add buttan and label
    toc.add_components(
        Generic_inline_HTML(
            tag_name="input",
            attributes={
                "type": "checkbox",
                "id": "menu_toggle",
                "class": "menu_toggle"
            }
        ),
        Generic_block_HTML(
            tag_name="label",
            attributes={
                "class": "menu_btn",
                "for": "menu_toggle"
            },
            content=[
                Span(
                    text="",
                )
            ]
        ))
    # add the list
    for element in collect_toc_elements(body_elements, ["article"]):
        toc.add_components(create_link4toc(element))

    return toc

def hamburger_css_stylesheet():
    with pkg_resources.path("yggdrasil.html.templates", "toc.css") as css_path:
        # css_path is a Path object that can be used within this block
        return CSSStyleSheet(Path(css_path))



# def create_link(
#     element: Union[Article, HTMLBlock]
# ) -> HTMLBlock:
#     """
#     Create a link to an element.

#     Args:
#         element (Union[Article, HTMLBlock]): The element to link to.

#     Returns:
#         HTMLBlock: The link to the element.
#     """
#     if isinstance(element, HTMLBlock):
#         return HTMLBlock(
#             tag_name="a",
#             children=[element],
#             attributes={"href": f"#{element.attributes['id']}"}
#         )
#     return element

# def create_toc(
#     body: List[Union[Article, HTMLBlock]]
# ) -> Article:
#     """
#     Create the table of contents.

#     Args:
#         body (List[Union[Article, HTMLBlock]]): The body of the page.

#     Returns:
#         Article: The table of contents.
#     """
#     toc = Division()
#     toc.add_components("Table of Contents")
#     toc.add_components(
#         [
#             element
#             for element in collect_toc_elements(body)
#             if isinstance(element, HTMLBlock)
#         ]
#     )
#     return toc