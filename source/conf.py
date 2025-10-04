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
    # Wrap long lines in verbatim, draw a frame around code blocks
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',

    'preamble': r'''
        % --- Fonts & headers ---
        \usepackage{fontspec} % XeLaTeX: allow system fonts
        % Fonts that include box-drawing characters and U+202F
        \setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]
        \setmainfont{Noto Serif}[Scale=MatchLowercase]

        \usepackage{fancyhdr}
        \usepackage{graphicx}

        % --- Verbatim handling (code blocks) ---
        \usepackage{fvextra}
        \fvset{
          breaklines=true,      % wrap long lines
          breakanywhere=true,   % allow breaks anywhere if needed
          samepage=true         % try to keep each code block on one page
        }

        % Map U+202F NARROW NO-BREAK SPACE to a thin space to avoid "Missing character"
        \usepackage{newunicodechar}
        \newunicodechar{^^^^202f}{\,} % U+202F → \, (thin space)

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
