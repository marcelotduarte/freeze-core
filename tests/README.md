## Test Execution

To Execute the tests in this folder, do the following steps in the parent
directory:

Note: Use a virtual environment.

```
make tests
```

Alternatively, to run coverage:

```
make cov
```

Of course, if needed, you can use pytest directly:

```
uv pip install --upgrade -r pyproject.toml --group tests
uv pip install -e. --no-deps
pytest tests
```
