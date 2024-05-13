"""Collection of tools for formatting text in Markdown syntax."""

# Reference : https://www.markdownguide.org/basic-syntax/

__all__ = [
    'MDFormat'
]

from typing import Literal

from beartype import beartype

# constants

HTML_COLORS = ["aqua", "black", "blue", "fuchsia", "gray", "green", "lime",
               "maroon", "navy", "olive", "purple", "red", "silver", "teal",
               "white", "yellow"]
Color = Literal[*HTML_COLORS] # type: ignore


class MDFormat:
    """
    A class that provides methods for formatting text in Markdown syntax.
    """

    @staticmethod
    def bold(text:str) -> str:
        """
        Formats the given text as bold in Markdown syntax.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text.
        """
        return f"**{text}**"

    @staticmethod
    def italic(text:str) -> str:
        """
        Formats the given text as italic in Markdown syntax.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text.
        """
        return f"*{text}*"

    @staticmethod
    def code(text:str) -> str:
        """
        Formats the given text as inline code in Markdown syntax.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text.
        """
        return f"`{text}`"

    @staticmethod
    def code_block(text:str) -> str:
        """
        Formats the given text as a code block in Markdown syntax.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text.
        """
        return f"```\n{text}\n```"

    @staticmethod
    def link(text:str, url:str) -> str:
        """
        Creates a hyperlink with the given text and URL in Markdown syntax.

        Args:
            text (str): The text of the link.
            url (str): The URL to link to.

        Returns:
            str: The formatted link.
        """
        return f"[{text}]({url})"

    @staticmethod
    def unordered_list(items:list[str]) -> str:
        """
        Formats a list of items as an unordered list in Markdown syntax.

        Args:
            items (list[str]): The items to be formatted as a list.

        Returns:
            str: The formatted list.
        """
        return "\n".join([f"- {item}" for item in items])

    @staticmethod
    def ordered_list(items:list[str]) -> str:
        """
        Formats a list of items as an ordered list in Markdown syntax.

        Args:
            items (list[str]): The items to be formatted as a list.

        Returns:
            str: The formatted list.
        """
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])

    @staticmethod
    def blockquote(text:str) -> str:
        """
        Formats the given text as a blockquote in Markdown syntax.

        Args:
            text (str): The text to be formatted.

        Returns:
            str: The formatted text.
        """
        return f"> {text}"

    @staticmethod
    def horizontal_rule() -> str:
        """
        Generates a horizontal rule in Markdown syntax.

        Returns:
            str: The horizontal rule.
        """
        return "---"

    @staticmethod
    def heading(text:str, level:int) -> str:
        """
        Formats the given text as a heading in Markdown syntax.
        Equivalent to HTML heading tags (h1-h6).

        Args:
            text (str): The text to be formatted as a heading.
            level (int): The level of the heading (1-6).

        Returns:
            str: The formatted heading.
        """
        # Ensure level is within 1-6
        level = max(1, min(6, level))

        return f"{'#'*(level)} {text}\n"

    @staticmethod
    def line_break() -> str:
        """
        Generates a line break in Markdown syntax.

        Returns:
            str: The line break.
        """
        return "  \n"

    @beartype
    @staticmethod
    def text_style(
        text: str,
        *,
        align: Literal['center','right','left','justify'] = "left",
        bold: bool = False,
        italic: bool = False,
        text_color: Color = "black",  # color name or RGB code
        background_color: Color = "black",  # color name or RGB code
        font_size: int = 0,  # positive integer
    ) -> str:
        """
        Apply text styling to the given text and return the styled HTML string.
        Equivalent to inline CSS styling with HTML <span> tag.

        Args:
            text (str): The text to be styled.
            align (Literal['center','right','left','justify'], optional):
             The alignment of the text. Defaults to "left".
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            text_color (Color, optional): The color of the text. Can be a HTML color name.
             Defaults to "black".
            background_color (Color, optional): The background color of the text.
             Can be a HTML color name. Defaults to "black".
            font_size (int, optional): The font size of the text in pixels.
             Defaults to html default.

        Returns:
            str: The styled HTML string.

        """
        # Dictionary to hold CSS properties
        style_options = {
            "text-align": align,
            "font-weight": "bold" if bold else None,
            "font-style": "italic" if italic else None,
            "color": text_color or None,
            "background-color": background_color or None,
            "font-size": f"{font_size}px" if font_size > 0 else None,
        }

        # Filter out None values
        style_options = {k: v for k, v in style_options.items() if v is not None}

        style_str = "; ".join(f"{k}: {v}" for k, v in style_options.items())

        return f"<span style='{style_str}'>{text}</span>"
