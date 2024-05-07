from pathlib import Path
from typing import List
import importlib.resources as pkg_resources

from yggdrasil.html import Article, HTMLBlock, Division, Hyperlink
from yggdrasil.html.components.nav import Navigation
from yggdrasil.html.components.script import Script
from ..base import HTMLComponent
from .generic_html_tag import Generic_block_HTML, Generic_inline_HTML
from .span import Span
from .link import CSSStyleSheet
from .style import Style
from .button import Button


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
    toc = Division(attributes={"class": "sidebar","id":"mySidebar"})


    toc.add_components(
        Hyperlink(component="X",
                  link="javascript:void(0)",
                  attributes={
                      "onclick": "closeNav()",
                      'class':'closebtn'})
    )
    for element in collect_toc_elements(body_elements, ["article"]):
        toc.add_components(create_link4toc(element))

    return toc

def toc_style() -> HTMLBlock:
    """
    Create the style for the table of contents.

    Returns:
        CSSStyleSheet: The style for the table of contents.
    """

    code = """
.sidebar {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  transition: 0.5s;
  padding-top: 60px;
}

.sidebar a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

.sidebar a:hover {
  color: #f1f1f1;
}

.sidebar .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

.openbtn {
  font-size: 20px;
  cursor: pointer;
  background-color: #111;
  color: white;
  padding: 10px 15px;
  border: none;
}

.openbtn:hover {
  background-color: #444;
}

#main {
  transition: margin-left .5s;
  padding: 16px;
}

/* On smaller screens, where height is less than 450px, change the style of the sidenav (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidebar {padding-top: 15px;}
  .sidebar a {font-size: 18px;}
}"""

    return Style(source_code=code)

def toc_script() -> HTMLBlock:
    """
    Create the script for the table of contents.

    Returns:
        HTMLBlock: The script for the table of contents.
    """

    code = """
    function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}"""
    return Script(source_code=code)

def toc_button() -> HTMLBlock:
    """
    Create the button to open the table of contents.

    Returns:
        Button: The button to open the table of contents.
    """
    return Button(
        text="☰ Open Sidebar",
        onclick="openNav()",
        attributes={
            "class": "openbtn",
        }
    )