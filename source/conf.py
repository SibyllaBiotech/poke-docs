# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'poké'
copyright = '2025, Sibylla Biotech'
author = 'Sibylla Biotech'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib.bibtex",
]
bibtex_bibfiles = ["refs.bib"]
bibtex_default_style = "unsrt"
bibtex_reference_style = "super"
templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = 'img/compress_light.png'
html_favicon = '_static/favicon.ico'
html_css_files = [
               'custom.css',
               ]

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'searchbox.html',
    ]
}

master_doc = 'index' 
