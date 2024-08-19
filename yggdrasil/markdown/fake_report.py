"""Create a fake markdown report using YGGDRASIL."""

from pathlib import Path
import tempfile

from matplotlib import pyplot as plt

from yggdrasil.utils.files.checksum import File
from yggdrasil.utils.images.fake import create_random_png
from .document import MarkdownDocument
from . import components
from ..utils.string import LoremIpsum

__all__ = ["create_markdown_report"]

def create_markdown_report(md_file_path:Path) -> list[File]:
    """
    Creates a markdown report using YGGDRASIL.

    Args:
        md_file_path (Path): The file path where the markdown report will be saved.

    Returns:
        MarkdownDocument: The generated markdown document.

    """

    # create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)

    # create the markdown document
    md = MarkdownDocument(title="Fake Report")

    # create an introduction
    intro = components.Paragraph(
        title="Introduction",
        components=[components.Text("This is a fake report created with YGGDRASIL.")]
    )

    intro.add_text("this is a "+ components.MDFormat.bold("bold") + " text")
    intro.add_text("this is a "+ components.MDFormat.italic("italic") + " text")
    intro.add_text( components.MDFormat.code("this is a code") )
    intro.add_text(components.MDFormat.code_block("this is a fake code block"))
    intro.add_text(components.MDFormat.link("this is a link", "https://www.google.com"))
    intro.add_text(components.MDFormat.blockquote("this is a blockquote\nthis is a blockquote"))

    # add list
    intro.add_text(components.MDFormat.unordered_list(["item 1", "item 2", "item 3"]))
    intro.add_text(components.MDFormat.ordered_list(["item 1", "item 2", "item 3"]))

    # add horizontal rule
    intro.add_text(components.MDFormat.horizontal_rule())

    # add some color
    intro.add_text(components.MDFormat.text_style(
        "this is a red text",
        text_color="red",
        background_color="yellow"))

    # create paragraphs
    s1 = components.Paragraph(title="Section 1")
    s1.add_components(components.Text("This is the first section of the report."))
    s1.add_text(LoremIpsum.generate_paragraph())

    S11 = components.Paragraph(title="Section 1.1")
    S11.add_components(components.Text(LoremIpsum.generate_paragraph()))

    s12 = components.Paragraph(title="Section 1.2")
    s12.add_components(components.Text(LoremIpsum.generate_paragraph()))

    # add the sections to the document
    s1.add_components(S11)
    s1.add_components(s12)

    # create a second section
    s2 = components.Paragraph(title="Section 2")

    s21 = components.Paragraph(title="Section 2.1")
    # create a fake image png
    image_path = create_random_png(temp_dir_path / "fake_image.png")

    im = components.Image(
        original_image_path=image_path,
        replacement_text="A fake image"
        )
    s21.add_components(im)

    s22 = components.Paragraph(title="Section 2.2")
     # create a fake plot

    fig, ax = plt.subplots()
    ax.plot([1,2,3,4],[1,4,9,16])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Fake Plot")

    plot = components.Plot(figure_name="Fake Plot", fig=fig)
    s22.add_components(plot)

    s2.add_components(s21, s22)

    # create a third section
    s3 = components.Paragraph(title="Section 3")

    # create a table from a dict

    data = {
        "name": ["John", "Doe", "Jane"],
        "age": ["25", "30", "35"],
        "city": ["New York", "Paris", components.MDFormat.text_style("London",text_color="red")]
    }

    tb = components.MD_table_from_dict(data)

    s3.add_components(tb)

    # merge document
    md.add_component(intro, s1,s2,s3)

    # publish the document
    file_list = md.publish(md_file_path=md_file_path)

    # create the safe file list by collecting the checksums of the created files
    safe_file_list = SafeFile.from_list(file_list)

    # close the temporary directory
    temp_dir.cleanup()

    return safe_file_list
