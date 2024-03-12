


from yggdrasil.html.components import Paragraph, Link, h
from yggdrasil.html.components._blocks import InlineHTMLBlock
from yggdrasil.html.components.article import Article
from yggdrasil.html.components.lists import OrderedList, UnorderedList
from yggdrasil.html.components.span import Span,CSS_Style
from yggdrasil.html.components.tables import Table, TableColumn

# 1. Create a paragraph HTML component.
# 2. Render the paragraph HTML component.

# 1. Create a paragraph HTML component.
# a = Paragraph("Hello, World!")
# print(a)



a = Paragraph("Hello, World!")
print(a.render())

b = Link(link="https://www.google.com", component="Google")
print(b.render())


s = Span("Hello, World!", style=CSS_Style(color="red",font_family="arial"), attributes={"class": "highlight"})
print(s.render())

h3 = h(level=3, title="Hello, World!", attributes={"class": "highlight"})

print(h3.render())

ul = UnorderedList("Hello", "World", attributes={"class": "highlight"})
print(ul.render())

ol = OrderedList("Hello", "World", attributes={"class": "highlight"})
print(ol.render())

article = Article(title="Hello, World!")
p1 = Paragraph("Hello, World!" ,
          Span("Hello, World!", style=CSS_Style(color="red",font_family="arial"), attributes={"class": "highlight"}))
article.add_components("Hello, World!")
article.add_components(p1)
article.add_components(ul)

a2 = Article(title="Hello, World!")
a2.add_components("Hello, World!")
a2.add_components(p1)
a2.add_components(ul)

article.add_components(a2)

print(article.render())


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

print(tt.render())
