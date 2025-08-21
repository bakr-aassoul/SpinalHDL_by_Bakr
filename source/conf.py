# Configuration file for the Sphinx documentation builder.
   # This file only contains a selection of the most common options. For a full
   # list see the documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

   import os
   import sys
   # Path setup
   # Add any paths that contain custom modules to sys.path here.
   sys.path.insert(0, os.path.abspath('.'))

   # -- Project information -----------------------------------------------------
   project = 'SpinalHDL Documentation'
   copyright = '2025, Bakr Aassoul'
   author = 'Bakr Aassoul'

   # -- General configuration ---------------------------------------------------
   extensions = [
       'myst_parser',  # Add support for Markdown files
   ]

   # Markdown and reStructuredText support
   source_suffix = {
       '.rst': 'restructuredtext',
       '.md': 'markdown',
   }

   # Paths
   templates_path = ['_templates']
   exclude_patterns = []

   # -- Options for HTML output -------------------------------------------------
   html_theme = 'alabaster'  # You can change the theme (e.g., 'sphinx_rtd_theme')
   html_static_path = ['_static']
