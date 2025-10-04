# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'SpinalHDL Dokumentation'
copyright = '2025, Bakr Aassoul'
author = 'Bakr Aassoul'

# -- General Configuration ---------------------------------------------------
extensions = ['myst_parser']  # Markdown via MyST
# Enable MyST directive fences like ```{code-block} and ```{literalinclude}
myst_enable_extensions = ["colon_fence"]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

exclude_patterns = []

# -- Options for HTML Output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# -- LaTeX Configurations ----------------------------------------------------
latex_engine = 'xelatex'
# Ensure the logo image is available to LaTeX build
latex_additional_files = ['spinalhdl-logo.png']

latex_elements = {
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',

    'preamble': r'''
        % --- fonts & headers ---
        \usepackage{fontspec}
        \setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]
        \setmainfont{Noto Serif}[Scale=MatchLowercase]

        \usepackage{fancyhdr}
        \usepackage{graphicx}

        % --- verbatim handling ---
        \usepackage{fvextra}
        % Remove "samepage" which can hide code content
        \fvset{
          breaklines=true,
          breakanywhere=true
        }

        % Unicode safety
        \usepackage{newunicodechar}
        \newunicodechar{^^^^202f}{\,}
        \newunicodechar{│}{|}
        \newunicodechar{├}{+}
        \newunicodechar{└}{+}
        \newunicodechar{─}{-}

        \makeatletter
        \fancypagestyle{normal}{
            \fancyhf{}
            \fancyfoot[LE,RO]{\py@HeaderFamily\thepage}
            \fancyfoot[LO,RE]{\py@HeaderFamily\nouppercase{\leftmark}}
            \renewcommand{\headrulewidth}{0.4pt}
            \renewcommand{\footrulewidth}{0.4pt}
        }
        \makeatother
    ''',

    'maketitle': r'''
    \begin{titlepage}
        \centering
        \vspace*{3cm}
        \includegraphics[width=0.5\textwidth]{spinalhdl-logo.png}\par
        \vspace{2cm}
        {\Huge \bfseries SpinalHDL Dokumentation \par}
        \vspace{1cm}
        {\Large Bakr Aassoul \par}
        \vfill
        {\large \today \par}
    \end{titlepage}

    \clearpage
    \null
    \thispagestyle{empty}
    \clearpage
''',
}

language = 'de'

latex_documents = [
    ('index',
     'SpinalHDL.tex',
     'SpinalHDL Dokumentation',
     'Bakr Aassoul',
     'manual'),
]
