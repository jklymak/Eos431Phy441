# Physical Oceanography

Physical Oceanography

## Usage

### Building the book

If you'd like to develop and/or build the Physical Oceanography book, you should:

1. Clone this repository
2. Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
3. (Optional) Edit the books source files located in the `site/` directory
4. Run `jupyter-book clean site/` to remove any existing builds
5. Run `jupyter-book build site/`

A fully-rendered HTML version of the book will be built in `site/_build/html/`.

### Hosting the book

This uses an action to push to https://jklymak.github.io/Eos431Phy441/

OK, action doesn't work because the raw data for answer keys to make it work can't be stored on Github.  SO instead, build locally as above, and then use `ghp-import -n -p -f _build/html`.  Note that this needs to be pip installed.  See https://jupyterbook.org/en/stable/publish/gh-pages.html



## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
