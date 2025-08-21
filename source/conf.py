# Configuration file for the Sphinx documentation builder.
# Full documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project Information -----------------------------------------------------
project = "SpinalHDL Documentation"
copyright = "2023, Your Name"
author = "Your Name"

# -- General Configuration ---------------------------------------------------
extensions = [
    "myst_parser",  # Add MyST-Parser to support Markdown (.md) files
]

# Support both .rst and .md formats
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Paths to exclude from documentation build (if any)
exclude_patterns = []

# Template settings (if using custom HTML templates)
templates_path = ["_templates"]

# -- HTML Output Options -----------------------------------------------------
# The theme to use for HTML documentation. You can choose others like sphinx_rtd_theme or furo.
html_theme = "alabaster"  # Replace 'alabaster' with your desired theme, e.g., 'sphinx_rtd_theme'.

# Static files (e.g., custom CSS or JS, stored in the '_static' directory)
html_static_path = ["_static"]
