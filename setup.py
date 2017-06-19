from distutils.core import setup

setup(name='ltmd',
      version='1.1',
      description='A preprocessor for pandoc allowing LaTeX cross-references to be correctly ranslated',
      author='Josh Borrow',
      author_email='joshua.borrow@durham.ac.uk',
      url='https://github.com/JBorrow/latex-pandoc-preprocessor',
      packages=['ltmd'],
      license='MIT',
      scripts=['preprocess.py'],
)
