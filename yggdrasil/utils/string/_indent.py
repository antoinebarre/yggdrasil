
"""
This module provides a function for indenting text.
"""

import textwrap


def indent(
    text:str,
    amount:int,
    ch: str =' '):
    """
    Indents the given text by the specified amount using the specified character.

    Args:
        text (str): The text to be indented.
        amount (int): The number of times the character should be repeated for
            each indentation level.
        ch (str, optional): The character used for indentation. Defaults to a space (' ').

    Returns:
        str: The indented text.
    """
    return textwrap.indent(text, amount * ch)