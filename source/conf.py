# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'SpinalHDL Dokumentation'
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
        \usepackage{fancyhdr}

        % Redefine the 'normal' pagestyle used by Sphinx
        \fancypagestyle{normal}{
            \fancyhf{} % clear all header/footer fields
            % Page number on outer edge
            \fancyfoot[LE,RO]{\py@HeaderFamily\thepage}
            % Chapter title on inner edge of footer
            \fancyfoot[LO,RE]{\py@HeaderFamily\nouppercase{\leftmark}}
            \renewcommand{\headrulewidth}{0.4pt}
            \renewcommand{\footrulewidth}{0.4pt}
        }
    ''',
}
language = 'de'   # German
latex_documents = [
    ('index',               # Your master .rst/.md file (no extension)
     'SpinalHDL.tex',       # Name of the LaTeX file Sphinx should create
     'SpinalHDL Dokumentation',  # Document title
     'Bakr Aassoul',        # Author
     'manual'),             # 'manual' or 'howto'
]
