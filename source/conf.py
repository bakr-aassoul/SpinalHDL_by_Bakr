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
    # Keep code frames + soft wrapping in PDF
    'sphinxsetup': 'verbatimwithframe=true, verbatimwrapslines=true',

    'preamble': r'''
        % --- basics / fonts ---
        \usepackage{lmodern}
        % If you prefer system fonts with XeLaTeX, uncomment:
        % \usepackage{fontspec}
        % \setmainfont{Noto Serif}[Scale=MatchLowercase]
        % \setmonofont{DejaVu Sans Mono}[Scale=MatchLowercase]

        \usepackage{graphicx}
        \usepackage{fancyhdr}

        % --- verbatim handling (soft wrapping, no splits) ---
        \usepackage{fvextra}   % better verbatim
        \fvset{
          breaklines=true,
          breakanywhere=true
        }

        % Ask LaTeX to move whole code blocks to next page if not enough space
        \usepackage{needspace}
        \usepackage{etoolbox}
        \makeatletter
        % Inject Needspace at the start of Sphinx's verbatim environment
        \pretocmd{\sphinxVerbatim}{\Needspace{12\baselineskip}}{}{}
        \makeatother

        % --- unicode niceties (optional but quiets warnings) ---
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
