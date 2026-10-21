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
import sys
from importlib.metadata import PackageNotFoundError, version as _installed_version

sys.path.insert(0, str(pathlib.Path(__file__).parent / "_ext"))   # extensions local to this guide

# Distribution name of the Poké package these docs are built against: the name used on PyPI
# and by pip. The import name and the command are still "poke".
# The version shown on the site is read from the installed package, never typed by hand.
DIST_NAME = "poke-scouter"

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
    "myst_parser",             # Markdown support, for the README sections included below
    "poke_cli",                # the CLI Reference tables, built from the installed poke's parser
    "sphinx.ext.githubpages",  # adds .nojekyll, so GitHub Pages serves the _static folder as is
]
# Code examples run inside source/_static/md, where the sample structure lives, so they can
# refer to it simply as structure.pdb.
doctest_global_setup = f"import os; os.chdir({str(pathlib.Path(__file__).parent / '_static' / 'md')!r})"
bibtex_bibfiles = ["refs.bib"]
bibtex_default_style = "unsrt"
bibtex_reference_style = "super"
templates_path = ['_templates']

# -- Link check (sphinx-build -b linkcheck, run weekly by GitHub Actions) ------------------
# A DOI is meant to redirect to the publisher's page, so that redirect is not a problem.
linkcheck_allowed_redirects = {r"https://doi\.org/.*": r".*"}
# Wiley answers every automated request with "403 Forbidden", whatever the link's state.
linkcheck_ignore = [r"https://doi\.org/10\.1002/med\.70001"]
exclude_patterns = ['_generated']   # the README sections below are included by pages, never built alone

# -- README sections pulled from the installed package -----------------------
# The reference pages of this guide (Descriptors, Filters, ...) are not typed a second time
# here: they include sections of the poke README, which ships inside the package metadata and
# marks each reusable section with <!-- docs:start NAME --> ... <!-- docs:end NAME -->.
# Every build rewrites those sections as source/_generated/NAME.md (git-ignored), with two
# adjustments for Sphinx: GitHub alert boxes (> [!NOTE] ...) become MyST admonitions, and
# the headings are promoted so that each file starts at H1, as the include directive expects.
import re
from importlib.metadata import metadata as _package_metadata

_ALERTS = {"NOTE": "note", "TIP": "tip", "IMPORTANT": "important", "WARNING": "warning", "CAUTION": "caution"}


def _convert_alerts(lines):
    """Turn GitHub alert boxes (a "> [!NOTE]" line followed by quoted lines) into MyST admonitions."""
    out, i = [], 0
    while i < len(lines):
        match = re.match(r"^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$", lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        body, i = [], i + 1
        while i < len(lines) and lines[i].startswith(">"):
            body.append(lines[i][1:].lstrip(" "))
            i += 1
        out += ["```{" + _ALERTS[match.group(1)] + "}", *body, "```"]
    return out


def _promote_headings(lines):
    """Shift the headings so that the highest level present becomes H1. Code fences are skipped."""
    levels, in_fence = [], False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and (match := re.match(r"^(#+)\s", line)):
            levels.append(len(match.group(1)))
    if not levels:
        return lines
    shift = min(levels) - 1
    out, in_fence = [], False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and (match := re.match(r"^(#+)(\s.*)$", line)):
            line = "#" * (len(match.group(1)) - shift) + match.group(2)
        out.append(line)
    return out


def _write_readme_sections():
    """Write every marked README section to _generated/NAME.md and return the section names."""
    meta = _package_metadata(DIST_NAME)
    text = meta.get_payload() or meta.get("Description") or ""
    starts = re.findall(r"<!-- docs:start ([\w-]+) -->", text)
    ends = re.findall(r"<!-- docs:end ([\w-]+) -->", text)
    if not starts:
        raise SystemExit(
            f"The README of the installed '{DIST_NAME}' package has no docs:start markers. "
            "The guide includes sections of it: run `pip install -e ../poke` with a current poke."
        )
    if starts != ends or len(starts) != len(set(starts)):
        raise SystemExit(f"The README docs markers are not paired: start {starts}, end {ends}")
    out_dir = pathlib.Path(__file__).parent / "_generated"
    out_dir.mkdir(exist_ok=True)
    for name in starts:
        body = text.split(f"<!-- docs:start {name} -->", 1)[1].split(f"<!-- docs:end {name} -->", 1)[0]
        lines = _promote_headings(_convert_alerts(body.strip("\n").split("\n")))
        content = "\n".join(lines) + "\n"
        path = out_dir / f"{name}.md"
        if not path.exists() or path.read_text() != content:   # keep the mtime when nothing changed
            path.write_text(content)
    return starts


readme_sections = _write_readme_sections()


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['poke.css']
html_logo = 'img/sidebar-logo.svg'
html_favicon = '_static/favicon.ico'

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',
        'searchbox.html',
    ]
}

master_doc = 'index' 
