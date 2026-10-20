# Poké user guide

Source of the Poké documentation site, built with [Sphinx](https://www.sphinx-doc.org/).
The code lives in its own repository: https://github.com/SibyllaBiotech/poke

## Build the site on your computer

1. Create a Python environment and install the build tools:

   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Install Poké itself. The build reads the version and the command-line help from the
   installed package. Until the first PyPI release, install it from a clone of the code
   repository placed next to this one:

   ```
   pip install -e ../poke
   ```

3. Build and open the site:

   ```
   sphinx-build -W --keep-going -b html source build/html
   open build/html/index.html       # Linux: xdg-open, Windows: start
   ```

4. Run the code examples in the guide (they execute against the installed Poké):

   ```
   sphinx-build -b doctest source build/doctest
   ```

   `-W` turns warnings into errors, so a broken link or a page missing from the index fails
   the build instead of going unnoticed.

## Publishing

GitHub Actions builds the site on every push and pull request (`.github/workflows/docs.yml`)
and publishes it from `main` to https://sibyllabiotech.github.io/poke-docs/. This needs a
one-time setting in the repository: *Settings → Pages → Build and deployment → Source:
GitHub Actions*. A second workflow (`.github/workflows/linkcheck.yml`) follows every
external link once a week and fails when one is dead.

The workflows install Poké from PyPI, so they fail until the first release there.

## Editing

- Pages are reStructuredText files in `source/`. Images and tutorial data are in `source/_static/`.
- `build/` is generated output and is not tracked by git.

## Licence

The text, figures and tutorial data in this repository are © Sibylla Biotech and are
released under the [Creative Commons Attribution 4.0 International licence](LICENSE)
(CC BY 4.0): you may copy, adapt and redistribute them, including commercially, as long as
you credit Sibylla Biotech. Code snippets shown in the documentation may also be used under
the MIT licence of [Poké](https://github.com/SibyllaBiotech/poke), so no attribution is
needed to paste an example into your own script.

The interactive viewers in the tutorial use the [NGL](https://github.com/nglviewer/ngl)
library, bundled in `source/_static/` under its own MIT licence (see
`ngl-2.5.0-LICENSE.txt` next to it).
