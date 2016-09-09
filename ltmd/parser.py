import random
import re
import copy
from types import Ref, Math, Figure

class PreProcess(object):
    def __init__(self, InputText):
        self.InputText = InputText
        self.ParsedData = {}
        self.RefExtract()
        self.MathExtract()
        self.FigExtract()


    def GenerateUID(self):
        r""" Generates a Unique Identifier - checks if it is already in
        self.ParsedData.keys() - if not it gets returned for use elsewhere."""

        UID = random.randint(0, 1e10)
        
        while UID is not in self.ParsedData.keys():
            UID = random.randint()

        return UID


    def RefExtract(self):
        r""" Finds all references in the text, generates UIDs and places
        the text in a Ref instance. """
        Regex = r"\\ref\{(.*?)\}"
        self.RefRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        RefExtracted = self.RefRegex.findall()

        for Reference in RefExtracted:
            ThisUID = GenerateUID()
            self.ParsedData[ThisUID] = Ref(Reference, ThisUID)


    def MathExtract(self):
        r""" Finds all equations in the text, generates UIDs and places
        the text in a Math instance. """

        Regex = r"\\begin\{equation\}(.*?)\\end\{equation\}"
        self.MathRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        MathExtracted = self.MathRegex.findall()

        for Mathematics in MathExtracted:
            ThisUID = GenerateUID()
            self.ParsedData[ThisUID] = Math(Mathematics, ThisUID)


    def FigExtract(self):
        r""" Finds all figures in the text, generates UIDs and places
        the text in a Fig instance. """

        Regex = r"\\begin\{figure\}(.*?)\\end\{figure\}"
        self.FigRegex = re.compile(Regex, re.VERBOSE|re.DOTALL)

        FigExtracted = self.FigRegex.findall()

        for FigureText in FigExtracted:
            ThisUID = GenerateUID()
            self.ParsedData[ThisUID] = Figure(FigureText, ThisUID)


    def ReplaceAll(self):
        """ Replaces all of the OriginalContent from the objects in ParsedData
        with their respective Unique Identifiers. """
        self.ParsedText = copy.deepcopy(self.InputText)

        for UID, Instance in self.ParsedData.iteritems():
            self.ParsedText = self.ParsedText.replace(UID, Instance.OriginalContent)





