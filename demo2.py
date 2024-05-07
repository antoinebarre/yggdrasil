from bs4 import BeautifulSoup

# Create a new BeautifulSoup object
html = BeautifulSoup()

# Create the HTML structure
html_tag = html.new_tag('html')
head_tag = html.new_tag('head')
title_tag = html.new_tag('title')
title_tag.string = 'My HTML Page'
body_tag = html.new_tag('body')
h1_tag = html.new_tag('h1')
h1_tag.string = 'Welcome to my HTML Page!'

# Append the tags to the HTML structure
html_tag.append(head_tag)
head_tag.append(title_tag)
html_tag.append(body_tag)
body_tag.append(h1_tag)

# Save the HTML structure to a file
with open('output.html', 'w') as file:
    file.write(str(html_tag))