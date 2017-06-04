"""
Comamnd-line access for ltmd.

Use:

    python3 preprocess.py <INPUT> <OUTPUT>

Takes an input of a LaTeX file, outputs a Pandoc Markdown file.
"""

import argparse
import ltmd
import os


# deal with command line options

Parser = argparse.ArgumentParser()

Parser.add_argument("input", type=str, help='Filename of the input .tex file.')
Parser.add_argument('output', type=str, help='Output markdown filename.')

Args = Parser.parse_args()


InputFilename = Args.input
OutputFilename = Args.output


# now need to run ltmd options

InputText = ltmd.GetTex(InputFilename)

PreProcessed = ltmd.PreProcess(InputText)
Pandocced = ltmd.RunPandoc(PreProcessed.ParsedText)
PostProcessed = ltmd.PostProcess(Pandocced, PreProcessed.ParsedData)

ltmd.OutputMD(OutputFilename, PostProcessed.ParsedText)
