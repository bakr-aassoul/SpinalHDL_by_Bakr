# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'SpinalHDL'
copyright = '2025, Bakr Aassoul'
author = 'Bakr Aassoul'

# -- General Configuration ---------------------------------------------------
extensions = ['myst_parser']  # Add extensions here

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',  # Enable Markdown support
}

exclude_patterns = []  # List of patterns to ignore

# -- Options for HTML Output -------------------------------------------------
html_theme = 'alabaster'  # Replace with your desired theme
html_static_path = ['_static']

# -- LaTeX Configurations (Optional) -----------------------------------------
latex_engine = 'xelatex'  # Use xelatex for better Unicode support
latex_elements = {
    'preamble': r'''
        \usepackage[utf8]{inputenc}
        \usepackage[T1]{fontenc}
        \usepackage{lmodern}
    ''',
}
