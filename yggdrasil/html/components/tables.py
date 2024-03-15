"""Collection of tools to create HTML table"""
# see https://github.com/sbi-rviot/ph_table
# https://www.youtube.com/watch?v=biI9OFH6Nmg&t=113s
# https://tympanus.net/codrops/2012/11/02/heading-set-styling-with-css/


from dataclasses import dataclass
from typing import Literal, Optional
import attrs


from ..base import  HTMLComponent, HTMLExtraFile
from .__extrafiles import collect_additional_files
from .text import Text
from ._blocks import HTMLBlock
from .__childrenUtils import get_children

__all__=[
    "TableColumn",
    "Table"
]

# ============================ TABLE COMPONENTS ============================ #

ALLOWED_TAGS = ["text", "span", "a", "ul", "ol","p"]

@dataclass
class TableColumn():
    """
    Represents a column in a table.

    Attributes:
        header (str): The header text of the column.
        data (list[HTMLComponent | str]): The data elements in the column.
        alignment (Optional[Literal["left", "center", "right"]]): The alignment of
            the column (left, center, or right).
        width_percent (Optional[int]): The width of the column as a percentage.

    Methods:
        length() -> int: Returns the number of data elements in the column.
        get_data() -> list[HTMLComponent]: Returns the data elements in the column
            as a list of HTMLComponents.
    """
    header: str
    data: list[HTMLComponent | str]
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

    #TODO : change this class to ATTRS
    
    # TODO : create a table from dataframe
    
    # TODO : add class for horizontal table

    def length(self) -> int:
        """
        Returns the length of the data in the table.

        Returns:
            int: The length of the data.
        """
        return len(self.data)

    def get_data(self) -> list[HTMLComponent]:
        """
        Returns the data of the table as a list of HTMLComponent objects.
        If the data is a string, it is converted to a Text object before being added to the list.
        """
        data = get_children(self.data)

        # Check allowed tags
        if any(component.get_tag() not in ALLOWED_TAGS for component in data):
            raise ValueError(f"Only the following tags are allowed: {ALLOWED_TAGS}")
        return data

@dataclass
class Cells():
    """
    Represents a collection of cells in a table.

    Attributes:
        data (HTMLComponent): The HTML component representing the data in the cells.
        alignment (Optional[Literal["left", "center", "right"]]): The alignment of
            the cells (left, center, or right).
        width_percent (Optional[int]): The width of the cells as a percentage.
    """
    data: HTMLComponent
    alignment: Optional[Literal["left", "center", "right"]] = None
    width_percent: Optional[int] = None

def create_HTML_table_row(  # pylint: disable=invalid-name
    row_elements: list[Cells],
    balise: Literal["th", "td"] = "td",
) -> HTMLBlock:
    """
    Create an HTML table row (`tr`) based on the provided `row_elements`.

    Args:
        row_elements (list[Cells]): A list of `Cells` objects representing the elements in the row.
        balise (Literal["th", "td"], optional): The HTML tag name for the cells 
        in the row. Defaults to "td".

    Returns:
        HTMLBlock: An HTMLBlock object representing the table row.

    Note:
        This function is stateless. It generates a new row each time it's called,
        based on the provided `row_elements`. Ensure `row_elements` is constructed
        freshly for each row to avoid unintended accumulation of data.
    """

    # Create an initial HTML block for the table row (`tr`)
    tr = HTMLBlock(
        tag_name="tr",
        attributes={},
    )

    # Iterate through each cell in the row to create its HTML representation
    for element in row_elements:
        # Manage cell attributes, such as alignment and width
        attributes = {}
        if element.alignment:
            attributes["align"] = element.alignment
        if element.width_percent:
            attributes["style"] = f"width:{element.width_percent}%"

        # Create the HTML block for the cell (`td` or `th`)
        t_cell = HTMLBlock(
            tag_name=balise,
            attributes=attributes,
            children=[element.data]
        )

        # Add the cell to the row
        tr.add_components(t_cell)

    # Render and return the HTML string representation of the row
    return tr


def validate_table_columns(columns: list[TableColumn]) -> list[TableColumn]:
    """
    Validate the table columns.

    Args:
        columns (list[TableColumn]): The list of table columns to validate.

    Returns:
        list[TableColumn]: The validated list of table columns.

    Raises:
        ValueError: If the table has no columns, if any column is not of type TableColumn,
        or if the columns have different lengths.
    """
    if not columns:
        raise ValueError("The table must have at least one column.")
    if not all(isinstance(column, TableColumn) for column in columns):
        raise ValueError("All columns must be of type TableColumn.")

    # check if all columns have the same length
    if len({column.length() for column in columns}) > 1:
        raise ValueError("All columns must have the same length.")

    return columns

def extract_headers(columns: list[TableColumn]) -> list[Cells]:
    """
    Extracts the headers from the given list of TableColumn objects and returns
    a list of Cells objects.

    Args:
        columns (list[TableColumn]): The list of TableColumn objects.

    Returns:
        list[Cells]: The list of Cells objects representing the extracted headers.
    """
    return [Cells(
        data=column.header if isinstance(column.header, HTMLComponent) else Text(column.header),
        alignment= column.alignment,
        width_percent= column.width_percent
        )
            for column in columns]

def get_elements_at_index(
    columns: list[TableColumn],
    index: int
) -> list[Cells]:
    """
    Extracts specific elements from the given columns at the specified index.

    Args:
        columns (list[TableColumn]): The list of TableColumn objects.
        index (int): The index of the specific element to extract.

    Returns:
        list[Cells]: The list of extracted Cells objects.
    """
    return [Cells(
        data= column.get_data()[index]
            if isinstance(column.get_data()[index], HTMLComponent)
            else Text(column.get_data()[index]), # type: ignore
        alignment= column.alignment) for column in columns]

def get_additional_files(columns: list[TableColumn]) -> list[HTMLExtraFile]:
    """
    Get additional files from the given list of columns.

    Args:
        columns (list[TableColumn]): A list of TableColumn objects.

    Returns:
        list[HTMLExtraFile]: A list of HTMLExtraFile objects.

    """
    return sum((collect_additional_files(column.get_data()) for column in columns), [])


@attrs.define
class Table(HTMLComponent):
    """
    Represents an vertical HTML table.

    Attributes:
        columns (list[TableColumn]): The columns of the table.

        class_ (Optional[str]): The HTML class of the table for CSS.

        width_percent (Optional[int]): The width of the table as a percentage
        of page width.
    """
    columns: list[TableColumn] = attrs.field(
        metadata={'description': 'The columns of the table'},
        validator=attrs.validators.deep_iterable(
            member_validator=attrs.validators.instance_of(TableColumn)),
        kw_only=True)
    class_ : Optional[str] = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        metadata={'description': 'The class of the table'},
        kw_only=True)

    width_percent: Optional[int] = attrs.field(
        default=80, # type: ignore
        validator=[attrs.validators.optional(attrs.validators.instance_of(int)), # type: ignore
                   attrs.validators.optional(attrs.validators.in_(range(1, 101)))], # type: ignore
        metadata={'description': 'The width of the table as a percentage of page width'},
        kw_only=True)

    center: Optional[bool] = attrs.field(
        default=True,
        metadata={'description': 'Center the table'},
        kw_only=True)

    legend: Optional[str] = attrs.field(
        default=None,
        metadata={'description': 'The legend of the table'},
        validator=attrs.validators.optional(attrs.validators.instance_of(str)),
        kw_only=True)

    def __attrs_post_init__(self):
        self.columns = validate_table_columns(self.columns)

    @property
    def body(self) -> HTMLBlock:
        """
        Generates the body of the table.

        Returns:
            HTMLBlock: The generated HTML block representing the table body.
        """
        body = HTMLBlock(
            tag_name="tbody",
        )

        for idx in range(self.columns[0].length()):
            body.add_components(create_HTML_table_row(
                row_elements=get_elements_at_index(self.columns, idx)
            ))
        return body

    @property
    def header(self) -> HTMLBlock:
        """
        Generates the header of the table.

        Returns:
            HTMLBlock: The generated HTML block representing the table header.
        """
        header_row = create_HTML_table_row(
            row_elements=extract_headers(self.columns),
            balise="th")

        return HTMLBlock(tag_name="thead", attributes={}, children=[header_row])

    @property
    def caption(self) -> HTMLBlock | None:
        """
        Generates the legend of the table.

        Returns:
            HTMLBlock: The generated HTML block representing the table legend.
        """
        return HTMLBlock(
            tag_name="caption",
            attributes={},
            children=[Text(self.legend)]
        ) if self.legend else None

    def get_table(self) -> HTMLBlock:
        """
        Generates the table.

        Returns:
            HTMLBlock: The generated HTML block representing the table.
        """

        components = [self.header, self.body]

        if self.caption:
            components = [self.caption] + components


        return HTMLBlock(
            tag_name="table",
            attributes=self.get_table_attributes(),
            children=components # type: ignore
        )

    @property
    def table_style(self) -> str:
        """
        Returns the style attribute for the table.

        The style attribute is generated based on the properties of the table object.
        It includes margin properties for centering the table and width property if
        the width_percent property is set.

        Returns:
            str: The style attribute for the table.
        """
        #manage style
        style_attribute = ""

        if self.center:
            style_attribute += "margin-left:auto;margin-right:auto;"

        if self.width_percent:
            style_attribute += f"width:{self.width_percent}%;"

        return style_attribute

    def get_table_attributes(self) -> dict[str, str]:
        """
        Returns the attributes for the table.

        Returns:
            dict[str, str]: The attributes for the table.
        """
        attributes = {}
        if self.class_:
            attributes["class"] = self.class_
        if self.table_style:
            attributes["style"] = self.table_style
        return attributes

    def render(self) -> str:
        """
        Renders the HTML representation of the table.

        Returns:
            str: The HTML representation of the table.
        """
        return self.get_table().render()

    def get_additional_files(self) -> list[HTMLExtraFile]:
        """
        Gets the additional files associated with the table.

        Returns:
            list[AdditionalFile]: The additional files associated with the table.
        """
        return get_additional_files(self.columns)

    def get_tag(self) -> str:
        """
        Get the tag of the table component.

        Returns:
            str: The tag of the table component.
        """
        return "table"
