"""
Comamnd-line access for ltmd.

Use:

    python3 preprocess.py <INPUT> <OUTPUT>

Takes an input of a LaTeX file, outputs a Pandoc Markdown file.
"""

import argparse

import ltmd

if __name__ == "__main__":
    # deal with command line options

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("input", type=str, help='Filename of the input .tex file.')
    PARSER.add_argument('output', type=str, help='Output markdown filename.')

    ARGS = PARSER.parse_args()


    input_filename = ARGS.input
    output_filename = ARGS.output


    # now need to run ltmd options

    input_text = ltmd.get_tex(input_filename)

    pre_processed = ltmd.PreProcess(input_text)
    pandocced = ltmd.run_pandoc(pre_processed.parsed_text)
    post_processed = ltmd.PostProcess(pandocced, pre_processed.parsed_data)

    ltmd.output_md(output_filename, post_processed.parsed_text)
