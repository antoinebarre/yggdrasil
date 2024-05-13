"""
YGGDRASIL - A collection of tools for aerospace applications.

This module provides various functionalities for working with aerospace applications.
It includes modules for handling markdown, converting to HTML, and utility functions.

Modules:
- markdown: Provides functions for working with markdown files.
- html: Provides functions for converting markdown to HTML.
- utils: Provides utility functions for aerospace applications.

Note: This module is part of the Yggdrasil project.
"""

from sys import version_info

from . import markdown
from . import html
from . import utils


# check the python version
if version_info < (3, 9):
    raise ImportError("YGGDRASIL requires Python 3.9 or higher.")
