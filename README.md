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

   `-W` turns warnings into errors, so a broken link or a page missing from the index fails
   the build instead of going unnoticed.

## Editing

- Pages are reStructuredText files in `source/`. Images and tutorial data are in `source/_static/`.
- `build/` is generated output and is not tracked by git.
- Commit with your GitHub no-reply address (GitHub → Settings → Emails) so personal addresses
  do not end up in the public history:
  `git config user.email "ID+username@users.noreply.github.com"`
