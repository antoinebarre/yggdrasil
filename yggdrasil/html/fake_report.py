"""Example of a fake HTML report created with YGGDRASIL."""
from pathlib import Path
import tempfile

from ..utils.string import LoremIpsum
from ..utils.images import create_random_png
from .document import HTMLDocument
from .components import (Title,h, default_css_stylesheet, Article,
                         Table,TableColumn,Image, UnorderedList, Hyperlink, OrderedList)



def create_fake_report(html_file_path: Path) -> HTMLDocument:
    """
    Creates a fake report in HTML format.

    Args:
        html_file_path (Path): The file path where the HTML report will be saved.

    Returns:
        HTMLDocument: The generated HTML document.

    """

    # create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir_path = Path(temp_dir.name)


    # create the HTML document
    md = HTMLDocument()

    # create the header
    md.add2header(
        Title("Fake Report"),
        h(level=1, title="Fake Report"),
        default_css_stylesheet()
    )


    # create the body based on article
    intro = Article(
        title="Introduction")

    intro.add_components("This is a fake report created with YGGDRASIL.")

    md.add2body(intro)

    # create sections
    section1 = Article(
        title="Section 1")
    section1.add_components(LoremIpsum.generate_paragraph())

    section11 = Article(
        title="Section 1.1")
    section11.add_components(LoremIpsum.generate_paragraph())

    # create a table
    tt = Table(
        legend="The Beatles",
        columns=[
            TableColumn(
            header= "Name",
            data=["John","Paul","George","Ringo"]),
            TableColumn(
            header= "Instrument",
            data=["Guitar","Bass","Guitar","Drums"]),
            TableColumn(
            header= "Vocals",
            data=["Yes","Yes","Yes","Yes"]),
        ]
        )
    section11.add_components(tt)

    section1.add_components(section11)



    section12 = Article(
        title="Section 1.2")
    section12.add_components(LoremIpsum.generate_paragraph())

    # create a fake image png
    image_path = create_random_png(temp_dir_path / "fake_image.png")

    im = Image(
        src_path=image_path,
        alt_text="Fake Image",
        width=400,
        height=300,
        legend="This is a fake image.",
        )

    section12.add_components(im)

    section1.add_components(section12)

    section2 = Article(
        title="Section 2")
    section2.add_components(LoremIpsum.generate_paragraph())

    section21 = Article(
        title="Section 2.1")
    section21.add_components(LoremIpsum.generate_paragraph())

    l = UnorderedList(
    "Hello, World!",
    "Hello, World!",
    "Hello, World!",
    )

    l2 = UnorderedList(
        "titi",
        "sdfsdfsdfsdf",
        "dflkdlfkdlfk",
        "dlsfjldsfjk")

    l3 = OrderedList(
        "Hello, World!1",
        "Hello, World!2",
        "Hello, World!3",
        type_="A",)
    section21.add_components(l,l2,l3)

    section2.add_components(section21)

    section22 = Article(
        title="Section 2.2")
    section22.add_components(LoremIpsum.generate_paragraph())
    section22.add_components(Hyperlink(component="GO TO GOOGLE",link="https://www.google.com"))

    section2.add_components(section22)

    md.add2body(section1,section2)

    # publish the fake report
    md.publish(html_file_path)

    # close the temporary directory
    temp_dir.cleanup()

    return md
