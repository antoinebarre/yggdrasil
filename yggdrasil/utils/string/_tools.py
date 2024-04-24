"""Collection of tools for string manipulation."""


import re

__all__ = [
    "remove_blank_lines"]

def remove_blank_lines(text:str)->str:
    """
    Remove all blank lines from the given string.

    Args:
    text (str): The input string from which blank lines should be removed.

    Returns:
    str: A new string with all blank lines removed.

    Nota:
    Explanation of the regex pattern:
    - ^ asserts position at the start of a line.
    - \s* matches any whitespace character (equal to [\r\n\t\f\v ])
      - * Quantifier — Matches between zero and unlimited times, as many
      times as possible, giving back as needed (greedy).
    - $ asserts position at the end of a line.

    - The re.MULTILINE flag allows the ^ and $ anchors to match at the start and end of each line.

    - \n+ matches a newline character (equal to \r\n|\r|\n) one or more times.
    - \n matches a newline character (equal to \r\n|\r|\n).
    - The re.sub() function replaces all occurrences of the pattern with the specified replacement.
    - The re.sub() function is used to remove extra newlines left after removing blank lines.
    - The .strip() method is used to remove leading and trailing whitespace from the string.
    """
    # Regex to match any line that contains only whitespace
    clean_text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
    # Removing any extra newlines left after removing blank lines
    clean_text = re.sub(r'\n+', '\n', clean_text).strip()
    return clean_text
