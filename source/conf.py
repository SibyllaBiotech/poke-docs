# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Poké'
copyright = ''          # no copyright line in the page footer; the licence is in LICENSE
html_show_copyright = False
author = 'Erika Primavera, Emilia Cassese and Sibylla Biotech'
import pathlib
from importlib.metadata import PackageNotFoundError, version as _installed_version

# Distribution name of the Poké package these docs are built against.
# The version shown on the site is read from the installed package, never typed by hand.
DIST_NAME = "poke"

try:
    release = _installed_version(DIST_NAME)      # full version, e.g. "0.1.0"
except PackageNotFoundError as exc:
    raise SystemExit(
        f"The '{DIST_NAME}' package is not installed in this environment. "
        "The docs read their version from it: run `pip install -e ../poke` first."
    ) from exc
version = ".".join(release.split(".")[:2])       # short version, e.g. "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinxcontrib.bibtex",
    "sphinx.ext.doctest",      # `sphinx-build -b doctest` runs the code examples in the guide
]
# Code examples run inside source/_static/md, where the sample structure lives, so they can
# refer to it simply as structure.pdb.
doctest_global_setup = f"import os; os.chdir({str(pathlib.Path(__file__).parent / '_static' / 'md')!r})"
bibtex_bibfiles = ["refs.bib"]
bibtex_default_style = "unsrt"
bibtex_reference_style = "super"
templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['poke.css']
html_logo = 'img/compress_light.png'
html_favicon = '_static/favicon.ico'

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'searchbox.html',
    ]
}

master_doc = 'index' 
