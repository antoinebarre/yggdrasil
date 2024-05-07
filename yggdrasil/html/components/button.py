"""Tools to generate a button."""

from typing import Optional
from .blocks import HTMLBlock
from .text import Text

# TODO: improve the check for the allowed attributes


def Button(  # pylint: disable=invalid-name
    text: str,
    onclick: str,
    attributes: Optional[dict[str, str]] = None
    ) -> HTMLBlock:
    # manage attibutes
    if attributes is None:
        attributes = {'onclick': onclick}
    else:
        attributes['onclick'] = onclick

    return HTMLBlock(
        tag_name='button',
        children=[Text(text)],
        attributes=attributes
    )
