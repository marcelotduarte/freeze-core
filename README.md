# freeze-core

Core dependency for cx_Freeze.

[![PyPI version](https://img.shields.io/pypi/v/freeze-core)](https://pypi.org/project/freeze-core/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/freeze-core)](https://pypistats.org/packages/freeze-core)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/freeze-core.svg)](https://anaconda.org/conda-forge/freeze-core)
[![Conda Downloads](https://anaconda.org/conda-forge/freeze-core/badges/downloads.svg)](https://anaconda.org/conda-forge/freeze-core)
[![Python](https://img.shields.io/pypi/pyversions/freeze-core)](https://www.python.org/)
[![Coverage](https://raw.githubusercontent.com/marcelotduarte/freeze-core/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/marcelotduarte/freeze-core/blob/python-coverage-comment-action-data/htmlcov/index.html)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Installation

Choose the Python package manager according to your system. See how the
installation works with the most common ones, which are pip and conda.

To install the latest version of `freeze-core` into a virtual environment:

```
uv pip install --upgrade freeze-core
```

If using pip:

```
pip install --upgrade freeze-core
```

From the conda-forge channel:

```
conda install conda-forge::freeze-core
```

> [!WARNING]
> It is not recommended to use `pip` in conda environment. See why in
> [Using Pip in a Conda Environment](https://www.anaconda.com/blog/using-pip-in-a-conda-environment).

To install the latest development build:

```
uv pip uninstall freeze-core
uv pip install --extra-index-url https://test.pypi.org/simple/ freeze-core --prerelease=allow --index-strategy=unsafe-best-match
```

If using pip:

```
pip uninstall freeze-core
pip install --extra-index-url https://test.pypi.org/simple/ freeze-core --pre --no-cache
```

## Development

**freeze-core** is a volunteer-maintained open source project, and we welcome
contributions of all forms. The sections below will help you get started with
development and testing. We’re pleased that you are interested in working on
`freeze-core` and/or `cx_Freeze`. This document is meant to get you set up to
work on `freeze-core` and to act as a guide and reference to the development
setup.
If you face any issues during this process, please open an issue about it on
the issue tracker.

The source code can be found on
[Github](https://github.com/marcelotduarte/freeze-core).

You can use `git` to clone the repository:

```
git clone https://github.com/marcelotduarte/freeze-core
cd freeze-core
make install
```

If you don't have make installed, run:

```
python -m pip install --upgrade pip
pip install -e.[dev,tests]
pre-commit install --install-hooks --overwrite -t pre-commit
```

### Building redistributable binary wheels

When `python -m build` or `pip wheel` is used to build a `freeze-core` wheel,
that wheel will rely on external shared libraries. Such wheels therefore will
only run on the system on which they are built. See
[Building and installing or uploading artifacts](https://pypackaging-native.github.io/meta-topics/build_steps_conceptual/#building-and-installing-or-uploading-artifacts) for more context on that.

A wheel like that is therefore an intermediate stage to producing a binary that
can be distributed. That final binary may be a wheel - in that case, run
`auditwheel` (Linux) or `delocate` (macOS) to vendor the required shared
libraries into the wheel.

To reach this, `freeze-core` binary wheels are built using `cibuildwheel`, via
the following command:

```
make wheel
```

To run a Linux build on your development machine, Docker or Podman should be
installed.

## See also:

[Changelog](https://github.com/marcelotduarte/freeze-core/releases)

[Documentation](https://cx-freeze.readthedocs.io).

[Discussion](https://github.com/marcelotduarte/cx_Freeze/discussions).

[License](https://github.com/marcelotduarte/freeze-core/blob/main/LICENSE).
