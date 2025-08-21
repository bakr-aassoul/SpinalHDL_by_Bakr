# Configuration file for the Sphinx documentation builder.

# General project information
project = 'SpinalHDL Documentation'
copyright = '2023, Your Name'
author = 'Your Name'

# Extensions to load (enable Markdown support via MyST Parser)
extensions = ['myst_parser']

# Source file formats: Recognize Markdown (.md) and reStructuredText (.rst)
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# HTML theme to use for the documentation
html_theme = 'alabaster'
