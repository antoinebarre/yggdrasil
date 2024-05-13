"""Markdown table generator."""


from dataclasses import KW_ONLY, dataclass
from typing import Literal

from beartype import beartype

from .basic import MDComponent, MDExtraFile

__all__ = [
    'MD_table_from_dict',
    ]

@dataclass
class MarkdownColumnTable():
    """
    Represents a column-based table in Markdown format.

    Args:
        name (str): The name of the column.
        values (list[str]): The values in the column.
        align (Literal["left", "center", "right"], optional): The alignment of
            the column. Defaults to "left".
    """
    _: KW_ONLY
    name: str
    values: list[str]
    align: Literal["left", "center", "right"] = "left"


def create_markdown_table(table_columns: list[MarkdownColumnTable]) -> str:
    """
    Create a Markdown table based on the provided table columns.

    Args:
        table_columns (list[MarkdownColumnTable]): The list of table columns.

    Returns:
        str: The generated Markdown table.

    """
    # Define the alignment symbols for Markdown
    align_symbols = {
        "left": ":--",
        "center": ":-:",
        "right": "--:"
    }

    # Construct the header row
    header_row = "| " + " | ".join(column.name for column in table_columns) + " |"

    # Construct the alignment row
    alignment_row = "| " + " | ".join(align_symbols[column.align] \
        for column in table_columns) + " |"

    data_rows = [
        "| " + " | ".join(row_values) + " |"
        for row_values in zip(*[column.values for column in table_columns])
    ]
    return "\n".join([header_row, alignment_row] + data_rows)

@dataclass
class MarkdownTable(MDComponent):
    """
    Represents a Markdown table.

    Attributes:
        columns (list[MarkdownColumnTable]): The list of table columns.

    Methods:
        publish(directory_path: Path) -> MarkdownContent:
            Publishes the Markdown table.
    """
    columns: list[MarkdownColumnTable]

    def render(self) -> str:
        """
        Publishes the Markdown table.

        Args:
            directory_path (Path): The directory path where the table will be published.

        Returns:
            MarkdownContent: The content of the published table.
        """
        return f"  \n\n{create_markdown_table(self.columns)}  \n"

    def get_additional_files(self) -> list[MDExtraFile]:
        """
        Retrieves any additional files associated with the table component.

        Returns:
            list[MDExtraFile]: A list of additional files required for rendering.
        """

        return []

@beartype
def MD_table_from_dict( # pylint: disable=invalid-name
    data: dict[str, list[str]],
    alignement: Literal["left", "center", "right"] = "center" ) -> MarkdownTable:
    """
    Create a Markdown table from a dictionary.

    Args:
        data (dict[str, list[str]]): The dictionary containing the data for the table.

    Returns:
        MarkdownTable: The Markdown table.
    """

    #check if all the columns have the same number of rows
    num_rows = len(data[list(data.keys())[0]])
    for values in data.values():
        if len(values) != num_rows:
            raise ValueError("All columns must have the same number of rows.")

    # check if the dict values are lists of strings
    for values in data.values():
        for value in values:
            if not isinstance(value, str):
                raise ValueError("All values must be strings.")

    columns = [
        MarkdownColumnTable(name=key, values=values, align=alignement)
        for key, values in data.items()
    ]
    return MarkdownTable(columns=columns)

# TODO : add other import functon for table