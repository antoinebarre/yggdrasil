""" Generic HTML tag Object """

from typing import Optional
from yggdrasil.html.components._blocks import InlineHTMLComponent, HTMLBlock
from yggdrasil.html.base import HTMLComponent, HTMLExtraFile


ALLOWED_INLINE_TAGS = [
    "input",
]
ALLOWED_BLOCK_TAG = [
    "label",
]

def Generic_inline_HTML(
    tag_name: str,
    attributes: dict,
) -> InlineHTMLComponent:

    # Check if the tag is allowed
    if tag_name not in ALLOWED_INLINE_TAGS:
        raise ValueError((
            f"Tag {tag_name} is not allowed in inline HTML.",
            f"Allowed tags are: {ALLOWED_INLINE_TAGS}"))
    return InlineHTMLComponent(
        tag_name=tag_name,
        attributes=attributes,)

def Generic_block_HTML(
    tag_name: str,
    attributes: dict,
    content: Optional[list[HTMLComponent]] = None,
) -> HTMLBlock:

    if content is None:
        content = []

    # Check if the tag is allowed
    if tag_name not in ALLOWED_BLOCK_TAG:
        raise ValueError((
            f"Tag {tag_name} is not allowed in block HTML.",
            f"Allowed tags are: {ALLOWED_BLOCK_TAG}"))

    return HTMLBlock(
        tag_name=tag_name,
        attributes=attributes,
        children=content)
