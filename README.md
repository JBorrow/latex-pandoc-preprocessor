Latex to Markdown Preprocessor
==============================

Annoyed that Pandoc doesn't correctly handle figure labels? Well, this module
is just for you!

```ltmd``` uses regex to extract figures, references, and mathematics, and 
processes them separately to Pandoc so that the figure references, etc. are
preserved.

Usage
-----

Use:
```
python3 preprocess.py <input> <output>
```
for example to generate the test markdown, we use
```
python3 preprocess.py test.tex test.md
```

The module can also be used through an API, through the two objects that are given.

One should use:

```python
pre_processed = ltmd.PreProcess(input_text)
pandocced = ltmd.run_pandoc(pre_processed.parsed_text)
post_processed = ltmd.PostProcess(pandocced, pre_processed.parsed_data)
```

The final output string can then be extracted by using ```post_processed.parsed_text```.

Requirements
------------

+ ```python3``` (no ```python2``` version will *ever* be made available)
+ ```pandoc``` somewhere in your path.
+ ```pypandoc```

