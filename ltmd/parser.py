"""
Holds the PreProcess class. This class contains functions that populate the

    PreProcess.parsed_data

dictionary - this contains the objects defined in types.py and parses the data.

It takes in the initial .tex string, replaces with uids and leaves you with
the above array and PreeProcess.parsed_text which should be written to a
temporary file and ran through pandoc to markdown.

It also contains the PostProcess class. This should be given the markdown
string so that it can replace the unique ids generated by PreProcess with
the generated text.

Extract the final string with:

    PostProcess.parsed_text

Author: Josh Borrow
Date Created: 2016-09-09.
"""

import uuid
import re
import copy
from ltmd.parsetypes import *


class PreProcess(object):
    def __init__(self, input_text, img_prepend="", debug=False):
        self.input_text = input_text
        self.parsed_text = copy.deepcopy(self.input_text)
        self.img_prepend = img_prepend
        self.debug = debug

        self.parsed_ref = {}
        self.parsed_cite = {}
        self.parsed_math = {}
        self.parsed_fig = {}
        self.parsed_inline_fig = {}  # e.g. just \includegraphics{}
        self.parsed_wrap_fig = {}
        self.parsed_tables = {}

        self.ref_extract()
        self.replace_all(self.parsed_ref)

        self.cite_extract()
        self.replace_all(self.parsed_cite)

        self.math_extract()
        self.replace_all(self.parsed_math)

        self.wrap_fig_extract()
        self.replace_all(self.parsed_wrap_fig)

        self.fig_extract()
        self.replace_all(self.parsed_fig)

        self.inline_extract()
        self.replace_all(self.parsed_inline_fig)

        self.table_extract()
        self.replace_all(self.parsed_tables)

        self.parsed_data = {
            'ref': self.parsed_ref,
            'cite': self.parsed_cite,
            'math': self.parsed_math,
            'fig': self.parsed_fig,
            'wfig': self.parsed_wrap_fig,
            'ifig': self.parsed_inline_fig,
            'tab': self.parsed_tables,
        }


    def generate_uid(self):
        r""" Generates a Unique Identifier - checks if it is already in
        self.parsed_data.keys() - if not it gets returned for use elsewhere."""

        return "{}".format(uuid.uuid4())


    def ref_extract(self):
        r""" Finds all references in the text, generates uids and places
        the text in a Ref instance. """
        regex = r"\\ref\{.*?\}"
        self.ref_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        ref_extracted = self.ref_regex.findall(self.parsed_text)

        for reference in ref_extracted:
            this_uid = self.generate_uid()
            self.parsed_ref[this_uid] = Ref(reference, this_uid)


    def cite_extract(self):
        r""" Finds all cites in the text. This is a passthrough. """

        regex = r"\\cite\{.*?\}"
        self.cite_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        cite_extracted = self.cite_regex.findall(self.parsed_text)

        for citation in cite_extracted:
            this_uid = self.generate_uid()
            self.parsed_cite[this_uid] = Cite(citation, this_uid)


    def math_extract(self):
        r""" Finds all equations in the text, generates uids and places
        the text in a Math instance. """

        regex = r"\\begin\{equation\}.*?\\end\{equation\}"
        self.math_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        math_extracted = self.math_regex.findall(self.parsed_text)

        for mathematics in math_extracted:
            this_uid = self.generate_uid()
            self.parsed_math[this_uid] = Math(mathematics, this_uid)


    def fig_extract(self):
        r""" Finds all figures in the text, generates uids and places
        the text in a Fig instance. """

        regex = r"\\begin\{figure\}.*?\\end\{figure\}"
        self.fig_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        fig_extracted = self.fig_regex.findall(self.parsed_text)

        for figure_text in fig_extracted:
            this_uid = self.generate_uid()
            self.parsed_fig[this_uid] = Figure(figure_text, this_uid, self.img_prepend)


    def wrap_fig_extract(self):
        r""" Same as above but looks for wrapfigures """

        regex = r"\\begin\{wrapfigure\}.*?\\end\{wrapfigure\}"
        self.wrap_fig_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        fig_extracted = self.wrap_fig_regex.findall(self.parsed_text)

        for figure_text in fig_extracted:
            this_uid = self.generate_uid()
            self.parsed_wrap_fig[this_uid] = Figure(figure_text, this_uid, self.img_prepend)


    def inline_extract(self):
        r""" Looks for inline figures that aren't wrapped inside any kind of
             Figure environment. """

        regex = r"(\\includegraphics.*\{.*?\})"
        self.inline_fig_regex = re.compile(regex, re.VERBOSE)

        fig_extracted = self.inline_fig_regex.findall(self.parsed_text)

        for figure_text in fig_extracted:
            this_uid = self.generate_uid()
            self.parsed_inline_fig[this_uid] = Figure(figure_text, this_uid, self.img_prepend)


    def table_extract(self):
        r""" Looks for tables and processes them using regex """

        regex = r"\\begin\{table\}.*?\\end\{table\}"  # no closing brace on purpose --
                                                      # this is so that table* is included
        self.table_regex = re.compile(regex, re.VERBOSE|re.DOTALL)
        regex = r"\\begin\{table\*\}.*?\\end\{table\*}"
        self.table_star_regex = re.compile(regex, re.VERBOSE|re.DOTALL)

        table_extracted = self.table_regex.findall(self.parsed_text)
        table_star_extracted = self.table_star_regex.findall(self.parsed_text)

        for table_text in table_extracted + table_star_extracted:
            this_uid = self.generate_uid()
            self.parsed_tables[this_uid] = Table(table_text, this_uid)


    def replace_all(self, to_parse):
        """ Replaces all of the original_content from the objects in parsed_data
        with their respective Unique Identifiers. """

        for uid, instance in to_parse.items():
            if self.debug:
                print("[Debug  ] Found {} item {}".format(
                    instance.__class__.__name__,
                    instance.original_content,
                ))

            self.parsed_text = self.parsed_text.replace(instance.original_content, uid)


class PostProcess(object):
    def __init__(self, input_text, parsed_data):
        self.input_text = input_text
        self.parsed_text = copy.deepcopy(self.input_text)

        self.replace_all(parsed_data['wfig'])
        self.replace_all(parsed_data['fig'])
        self.replace_all(parsed_data['math'])
        self.replace_all(parsed_data['cite'])
        self.replace_all(parsed_data['ref'])
        self.replace_all(parsed_data['ifig'])
        self.replace_all(parsed_data['tab'])

    def replace_all(self, to_parse):
        """ Replaces all of the Unique Identifiers from parsed_data with their
        markdown-ified expressions from parsed_data. """

        for uid, instance in to_parse.items():
            self.parsed_text = self.parsed_text.replace(uid, instance.output_content)

