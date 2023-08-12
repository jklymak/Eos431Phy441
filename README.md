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

template was created with a GitHub actions workflow file that, once pushed to GitHub, automatically renders and pushes your book to the `gh-pages` branch of your repo and hosts it on GitHub Pages when a push or pull request is made to the main branch.

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/jklymak/eos431phy441/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
