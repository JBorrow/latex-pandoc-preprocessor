"""
This file contains all of the object definitions for the parser.

Use it wisely.

Author: Josh Borrow
Date Created: 2016-09-09.
"""

import re
import pypandoc

SHOW_ERRORS = False

class LatexObject(object):
    """ Generic LaTeX object that contains pattern matching functions """

    def __init__(self, original_content, uid):
        self.original_content = original_content
        self.uid = uid

        self.label_match = None
        self.label_text = ""

        self.caption_match = None
        self.caption_text = ""


    def get_label(self):
        r""" Returns the Match object (regex) for the original content's
        label.
        Searches for the regex:

                \\label\{(.*?)\}" """

        regex = r"\\label\{(.*?)\}"
        label_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        self.label_match = label_regex.search(self.original_content)

        try:
            self.label_text = self.label_match.group(1)
        except AttributeError:  # We didn't find any matches
            if SHOW_ERRORS:
                self.label_text = "@@@ERROR@@@"
            else:
                self.label_text = ""


    def get_caption(self):
        r""" Finds the caption inside the original_content. Looks for

            \caption{<TEXT>}.

        Does this by using the regex:

            \\caption\{(.*?)\}(?=\\label|\n),

        i.e. it expects that you follow your caption with either a \label
        *or* a newline and that you don't do something like this...

            \caption{test \ref{test}
            I'm a fool.} """

        regex = r"\\caption\{(.*?)\}(?=\\label|\n)"
        caption_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        self.caption_match = caption_regex.search(self.original_content)
        try:
            self.caption_text = self.caption_match.group(1)
        except AttributeError:
            self.caption_text = ""




class Math(LatexObject):
    """ Object for mathematics sections in the LaTeX document """

    def __init__(self, original_content, uid):
        self.original_content = original_content
        self.uid = uid
        self.get_label()
        self.get_math()
        self.convert_math()


    def get_math(self):
        r""" Finds the actual math inside an equation environment.

        Assumes that the only contents of the string are:

        +  math
        +  \label{.*}

        Uses the get_label method to find the place of the label and
        removes it.

        Assumes that self.label_match is already set."""

        label_string = "\\label{{{}}}".format(self.label_text)

        regex = r"\\begin\{equation\}(.*?)\\end\{equation\}"
        math_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        self.math_match = math_regex.search(self.original_content)

        self.math = self.math_match.group(1).replace(label_string, "")

        return self.math


    def convert_math(self):
        r""" Converts the math to the pandoc-crossref style:

            $$
                <math>
            $$ {#label}."""

        try:
            self.output_content = "$${}$$ {{#{}}}".format(
                self.math,
                self.label_text)
        except AttributeError:  # no Label
            self.output_content = "$${}$$".format(self.math)



class Ref(LatexObject):
    def __init__(self, original_content, uid):
        self.original_content = original_content
        self.uid = uid
        self.get_ref()
        self.convert_ref()


    def get_ref(self):
        r""" Returns the Match object (regex) for the original content's
        reference label.

        Searches for the regex:

                \\ref\{(.*?)\} """

        regex = r"\\ref\{(.*?)\}"
        ref_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        try:
            self.ref_match = ref_regex.search(self.original_content)
            self.ref_text = self.ref_match.group(1)
        except AttributeError:  # no match
            pass


    def convert_ref(self):
        r""" Converts the reference info the pandoc-crossref style:

            [@<REF>]."""

        try:
            self.output_content = "[@{}]".format(self.ref_text)
        except AttributeError:  # no match
            self.output_content = "[@ERROR]"


class Cite(LatexObject):
    def __init__(self, original_content, uid):
        self.original_content = original_content
        self.uid = uid

        self.get_cite()
        self.convert_cite()


    def get_cite(self):
        regex = r"\\cite\{(.*?)\}"
        cite_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        try:
            self.cite_match = cite_regex.search(self.original_content)
            self.cite_text = self.cite_match.group(1)
        except AttributeError:  # no match
            pass


    def convert_cite(self):
        try:
            self.output_content = "@{}".format(self.cite_text)
        except AttributeError:  # no match
            self.output_content = "@ERROR"


class Figure(LatexObject):
    def __init__(self, original_content, uid, img_prepend=""):
        self.original_content = original_content
        self.img_prepend = img_prepend
        self.uid = uid
        self.get_urls()
        self.get_label()
        self.get_caption()
        self.convert_figure()


    def get_urls(self):
        r""" Finds the URLs of the graphics files, found in:

            \includegraphics[options]{<FILENAME>}.

        Does this by using the regex:

            \\includegraphics.*?\{(.*?)\}. """

        regex = r"\\includegraphics.*?\{(.*?)\}"
        url_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        self.url_text = url_regex.findall(self.original_content)


    def convert_figure(self):
        r""" Outputs the figures as expected by pandoc-crossref:

            ![<CAPTION>](<URL>){#<LABEL>}."""

        if self.label_text:  # Deal with uncaptioned ones
            this_label = "{{#{}}}".format(self.label_text)
        else:
            this_label = ""

        if len(self.url_text) == 1:
            self.output_content = "![{}]({}){}".format(
                self.caption_text,
                self.img_prepend + self.url_text[0],
                this_label)
        else:
            self.output_content = "<div id=\"{}\">".format(self.label_text)
            width = 100/len(self.url_text)
            for index, img in enumerate(self.url_text):
                cap = '#{}{}'.format(self.label_text, index)
                formatted = "![]({}){{{} width={}%}}\n".format(self.img_prepend + img, cap, width)
                self.output_content = self.output_content + formatted

            self.output_content = self.output_content + "\n{}".format(self.caption_text)
            self.output_content = self.output_content + "\n</div>\n"


class Table(LatexObject):
    def __init__(self, original_content, uid):
        self.original_content = original_content
        self.uid = uid
        self.get_label()
        self.get_caption()
        self.get_table()
        self.convert_figure()


    def get_table(self):
        r""" The good thing here is that we wrap the actual table content
        inside \begin{tabular}, and all of the caption and label inside
        \begin{table}.
        """

        regex = r"\\begin{tabular}.*?\\end{tabular}"
        table_regex = re.compile(regex, re.DOTALL|re.VERBOSE)

        self.table_match = table_regex.search(self.original_content)

        try:
            self.table_text = self.table_match.group(0)
        except AttributeError:
            self.table_text = ""


    def convert_figure(self):
        r""" This uses pandoc to convert the explicit table text only. """

        pandoc_args = ["--mathjax"]

        try:
            converted_table = pypandoc.convert_text(
                self.table_text,
                to='markdown',
                format='latex',
                extra_args = pandoc_args)

        except AttributeError:
            # for pypandoc version before 1.2
            converted_table = pypandoc.convert(
                self.table_text,
                to='markdown',
                format='latex',
                extra_args=pandoc_args) 

        if self.label_text:
            this_label = self.label_text
        else:
            this_label = "tbl:" + self.uid

        converted_caption = ": {} {{#{}}}".format(self.caption_text.replace("\n", " "), this_label)

        self.output_content = "{}{}".format(converted_table, converted_caption)

