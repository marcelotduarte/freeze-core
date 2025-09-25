## Test Execution

To Execute the tests in this folder, do the following steps in the parent
directory:

```
make tests
```

Alternatively, to run coverage:

```
make cov
```

Of course, if needed, you can use pytest directly:

```
pip install -e.[test]
pytest -n0
```
