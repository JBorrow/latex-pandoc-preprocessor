"""
Contains basic IO operations for running pandoc.

Author: Josh Borrow
Date Created: 2016-09-09
"""

import os
import tempfile
import subprocess


def GetTex(filename):
    """ Get the content of the tex file """

    with open(filename, 'r') as file:
       return file.read()


def OutputMD(filename, content):
    """ Output the final markdown to file """

    with open(filename, 'w') as file:
        file.write(content)


def RunPandoc(content, extra=""):
    """ Creates a temporary file, runs pandoc TeX->MD on it (with content)
    and then reopens and returns the string. """

    TempFileTeX = tempfile.NamedTemporaryFile(mode='w+t', encoding='utf-8')
    TempFileMD = tempfile.NamedTemporaryFile(mode='w+t', encoding='utf-8')

    TempFileTeX.write(content)
    print(TempFileTeX.read())

    subprocess.call(['pandoc', '-f', 'latex', '-t', 'markdown', TempFileTeX.name, '-o', TempFileMD.name])

    OutputData = TempFileMD.read()

    TempFileTeX.close()
    TempFileMD.close()

    return OutputData

