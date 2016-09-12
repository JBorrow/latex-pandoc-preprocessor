"""
This file contains all of the object definitions for the parser.

Use it wisely.

Author: Josh Borrow
Date Created: 2016-09-09.
"""

import re

class LatexObject(object):
    def __init__(self, OriginalContent, UID):
        self.OriginalContent = OriginalContent
        self.UID = UID

    
    def GetLabel(self):
        r""" Returns the Match object (regex) for the original content's
        label.
        
        Searches for the regex:

                \\label\{(.*?)\}" """

        Regex = r"\\label\{(.*?)\}"
        LabelRegex = re.compile(Regex, re.DOTALL|re.VERBOSE)
        
        self.LabelMatch = LabelRegex.search(self.OriginalContent)
        self.LabelText = self.LabelMatch.group(1)


class Math(LatexObject):
    def __init__(self, OriginalContent, UID):
        self.OriginalContent = OriginalContent
        self.UID = UID
        self.GetLabel()
        self.GetMath()
        self.ConvertMath()
    
    
    def GetMath(self):
        r""" Finds the actual math inside an equation environment.
        
        Assumes that the only contents of the string are:
        
        +  Math
        +  \label{.*}
        
        Uses the GetLabel method to find the place of the label and
        removes it.
        
        Assumes that self.LabelMatch is already set."""

        LabelString = "\\label{{{}}}".format(self.LabelText)
        
        Regex = r"\\begin\{equation\}(.*?)\\end\{equation\}"
        MathRegex = re.compile(Regex, re.DOTALL|re.VERBOSE)

        self.MathMatch = MathRegex.search(self.OriginalContent)

        self.Math = self.MathMatch.group(1).replace(LabelString, "")

        return self.Math


    def ConvertMath(self):
        r""" Converts the math to the pandoc-crossref style:

            $$
                <MATH>
            $$ {#label}."""
        
        try:
            self.OutputContent =  "\n$$ {} $$ {{#{}}}\n".format(self.Math,
                                                              self.LabelText)
        except AttributeError:  # no Label
            self.OutputContent = "\n$$ {} $$\n".format(self.Math)



class Ref(LatexObject):
    def __init__(self, OriginalContent, UID):
        self.OriginalContent = OriginalContent
        self.UID = UID
        self.GetRef()
        self.ConvertRef()


    def GetRef(self):
        r""" Returns the Match object (regex) for the original content's
        reference label.
        
        Searches for the regex:

                \\ref\{(.*?)\} """

        Regex = r"\\ref\{(.*?)\}"
        RefRegex = re.compile(Regex, re.DOTALL|re.VERBOSE)
        
        try:
            self.RefMatch = RefRegex.search(self.OriginalContent)
            self.RefText = self.RefMatch.group(1)
        except AttributeError:  # no match
            pass


    def ConvertRef(self):
        r""" Converts the reference info the pandoc-crossref style:

            [@<REF>]."""
        
        try:
            self.OutputContent = "[@{}]".format(self.RefText)
        except AttributeError:  # no match
            self.OutputContent = "[@ERROR]"


class Figure(LatexObject):
    def __init__(self, OriginalContent, UID):
        self.OriginalContent = OriginalContent
        self.UID = UID
        self.GetUrls()
        self.GetLabel()
        self.GetCaption()
        self.ConvertFigure()

    def GetUrls(self):
        r""" Finds the URLs of the graphics files, found in:
        
            \includegraphics[options]{<FILENAME>}.

        Does this by using the regex:

            \\includegraphics.*?\{(.*?)\}. """

        Regex = r"\\includegraphics.*?\{(.*?)\}"
        UrlRegex = re.compile(Regex, re.DOTALL|re.VERBOSE)

        self.UrlMatch = UrlRegex.search(self.OriginalContent)
        self.UrlText = self.UrlMatch.group(1)


    def GetCaption(self):
        r""" Finds the caption inside the OriginalContent. Looks for
        
            \caption{<TEXT>}.

        Does this by using the regex:

            \\caption\{(.*?)\}(?=\\label|\n),
        
        i.e. it expects that you follow your caption with either a \label
        *or* a newline and that you don't do something like this...

            \caption{test \ref{test}
            I'm a fool.} """

        Regex = r"\\caption\{(.*?)\}(?=\\label|\n)"
        CaptionRegex = re.compile(Regex, re.DOTALL|re.VERBOSE)

        self.CaptionMatch = CaptionRegex.search(self.OriginalContent)
        self.CaptionText = self.CaptionMatch.group(1)


    def ConvertFigure(self):
        r""" Outputs the figures as expected by pandoc-crossref:

            ![<CAPTION>](<URL>){#<LABEL>}."""

        self.OutputContent = "\n![{}]({}){{#{}}}\n".format(
                                                self.CaptionText,
                                                self.UrlText,
                                                self.LabelText)


