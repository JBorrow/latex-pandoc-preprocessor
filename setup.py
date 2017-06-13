from distutils.core import setup

setup(name='ltmd',
      version='1.0',
      description='A preprocessor for pandoc allowing LaTeX syntax to be correctly translated (notably cross-references',
      author='Josh Borrow',
      author_email='joshua.borrow@durham.ac.uk',
      url='https://github.com/JBorrow/latex-pandoc-preprocessor',
      packages=['ltmd'],
      license='MIT',
      scripts=['preprocess.py'],
)
