"""
Contains basic IO operations for running pandoc.

Author: Josh Borrow
Date Created: 2016-09-09
"""

import pypandoc


def get_tex(filename):
    """ Get the content of the tex file """

    print("Reading {}...".format(filename))
    with open(filename, 'r') as file:
        return file.read()


def output_md(filename, content):
    """ Output the final markdown to file """

    print("Writing {}...".format(filename))
    with open(filename, 'w') as file:
        file.write(content)


def run_pandoc(content, extra=[]):
    """ Creates a temporary file, runs pandoc TeX->MD on it (with content)
    and then reopens and returns the string. """
    print("Running Pandoc (LT -> MD)")
    output = pypandoc.convert_text(content, "md", format="latex", extra_args=extra)

    return output

