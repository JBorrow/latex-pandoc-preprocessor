"""
This is a LaTeX -> Markdown preprocessor. It uses regex to extract certain
parts of the LaTeX that are not handled 'correctly' by John McFarlane's 
Pandoc, replaces them with a unique string and prcoesses them separately,
whilst the main body of text is converted with Pandoc.

For more information, view the README or check out the github page:

    https://www.github.com/jborrow/latex-pandoc-preprocessor.

Author: Josh Borrow.
"""

from ltmd.parser import *
from ltmd.inputoutput import *
