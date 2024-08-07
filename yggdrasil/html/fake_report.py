"""Example of a fake HTML report created with YGGDRASIL."""
from pathlib import Path
import tempfile
from matplotlib import pyplot as plt

from yggdrasil.html.components.breakline import Breakline
from yggdrasil.html.components.plot import Plot
from yggdrasil.html.components.text import Text
from yggdrasil.html.components.tables import HorizontalTable, HorizontalTableComponent
from yggdrasil.html.components.toc2 import collect_toc_elements, create_toc, toc_button, toc_script, toc_style
from yggdrasil.utils.files.checksum import SafeFile

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

    section3 = Article(
        title="Section 3 with Plot")

    section3.add_components(LoremIpsum.generate_paragraph())
    section3.add_components(Breakline())
    section3.add_components(Hyperlink(component="GO TO GOOGLE",link="https://www.google.com"))

    # create a fake plot

    fig, ax = plt.subplots()
    ax.plot([1,2,3,4],[1,4,9,16])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Fake Plot")
    plot = Plot(figure_name="fake_plot", figure=fig, legend="This is a fake plot.")
    section3.add_components(plot)

    # create a horizontal table
    h1 = HorizontalTableComponent(
        title="info1",
        component=Text(LoremIpsum.generate_sentence()),
    )
    h2 = HorizontalTableComponent(
        title="info2",
        component=Text(LoremIpsum.generate_sentence()),
    )
    h3 = HorizontalTableComponent(
        title="info3",
        component=Text(LoremIpsum.generate_sentence()),
    )

    ht = HorizontalTable(
        components=[h1,h2,h3],
        legend="This is a fake horizontal table."
    )

    section3.add_components(ht)

    md.add2body(section1,section2,section3)

    print("###########################")

    list_article = collect_toc_elements(md.body.children,["article"])
    print(len(list_article))

    for article in list_article:
        print(article.title)
        print(article.get_level())
        print(article.get_id())


    # add the table of contents div
    md.add2header(create_toc(md.body.children))

    # add the header
    md.add2header(toc_style())
    # create the footer
    md.add2header(toc_script())
    
    md.add2body(toc_button())



    print("###########################")
    # publish the fake report
    a = md.publish(html_file_path)

    print(a)


    chk = SafeFile.from_list(a)

    print(chk)

    # close the temporary directory
    temp_dir.cleanup()

    return md
