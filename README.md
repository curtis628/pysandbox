# Example for Python Packaging, Testing and Running

[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This repo can be a helpful example for how to package, test and run a collection
of python files. It requires `python3.10+` and `tox`.

Run the following to clone, build, test and package everything.

```shell
git clone https://github.com/curtis628/pysandbox.git
cd pysandbox
tox
```

If you want to run some of the scripts from the command line after building,
run:

```shell
source .tox/py310/bin/activate.fish
```

## Included Scripts

* `spelling-bee`: solves the New York Times' [spelling-bee game](https://www.nytimes.com/puzzles/spelling-bee)
* `nflpicker-gen`: recommends picks for [my NFL pickem league](https://www.runyourpool.com/nfl/pickem/), using [the-odds-api](https://the-odds-api.com/)

## Libraries Used

* [tox](https://tox.wiki/en/latest/index.html) - automates and standardizes 
  packaging, testing and release process for Python software
* [pytest](https://pytest.org) - a mature full-featured Python testing tool that
  helps you write better programs
* [isort](https://github.com/PyCQA/isort) - sorts import statements
* [black](https://github.com/psf/black) - the uncompromising Python code formatter
* [flake8](https://github.com/PyCQA/flake8) - checks Python code style and quality
* [mypy](https://mypy.readthedocs.io/en/stable/) - static type checker for Python code
