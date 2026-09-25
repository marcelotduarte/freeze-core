"""Test to validate the fixes in PR #244.

Before the fix, the code:
    import concurrent.interpreters
Produced the following error on Linux:
    undefined symbol: _PyInterpreterConfig_UpdateFromDict
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

SOURCE = """
test_interpreters.py
    import concurrent.interpreters

    print(concurrent.interpreters)
pyproject.toml
    [project]
    name = "test_interpreters"
    version = "0.1.2.3"
    dependencies = [
        "cx_Freeze>=8.7.0",
    ]

    [tool.cxfreeze]
    executables = ["test_interpreters.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


@pytest.mark.skipif(
    sys.version_info < (3, 14), reason="Module of Python 3.14+"
)
def test_interpreters(tmp_package: TempPackage) -> None:
    """Test if concurrent.interpreters is correctly imported."""
    tmp_package.create(SOURCE)
    tmp_package.freeze()
    executable = tmp_package.executable("test_interpreters")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["<module 'concurrent.interpreters' from *"])
