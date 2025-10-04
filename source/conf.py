# Configuration file for the Sphinx documentation builder.

# -- Project Information -----------------------------------------------------
project = 'SpinalHDL Dokumentation'
copyright = '2025, Bakr Aassoul'
author = 'Bakr Aassoul'

# -- General Configuration ---------------------------------------------------
extensions = ['myst_parser']  # Markdown via MyST

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

exclude_patterns = []  # Nothing excluded

# -- Options for HTML Output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

# -- LaTeX Configurations ----------------------------------------------------
latex_engine = 'xelatex'

# Tell Sphinx to copy the logo into the LaTeX build dir
latex_additional_files = ['spinalhdl-logo.png']

latex_elements = {
    # keep the nice frame and soft wrapping Sphinx provides
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',

    'preamble': r'''
        % XeLaTeX + fonts
        \usepackage{lmodern}
        \usepackage{fontspec} % (optional; comment out if you prefer lmodern only)
        % \setmainfont{Noto Serif}[Scale=MatchLowercase]
        % \setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

        \usepackage{fancyhdr}
        \usepackage{graphicx}

        % Verbatim handling + soft wrapping
        \usepackage{fvextra}     % extends fancyvrb
        \fvset{
          breaklines=true,
          breakanywhere=true
        }

        % NEW: avoid splitting code blocks across pages
        \usepackage{needspace}
        % Ask LaTeX to keep at least N lines together; adjust N if you like
        \AtBeginEnvironment{Verbatim}{\Needspace{10\baselineskip}}
        \AtBeginEnvironment{sphinxVerbatim}{\Needspace{10\baselineskip}}

        % (Optional) Unicode niceties; safe to leave in
        \usepackage{newunicodechar}
        \newunicodechar{^^^^202f}{\,} % map U+202F narrow NBSP to thin space

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
