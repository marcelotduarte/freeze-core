"""Test to validate the fixes in PR #208."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15


SOURCE_TEST_CTYPES = """
test_ctypes.py
    import ctypes

    print("Hello from cx_Freeze")
    print("Hello", ctypes.__name__)
pyproject.toml
    [project]
    name = "test_ctypes"
    version = "0.1.2.3"
    dependencies = [
        "cx_Freeze>=8.7.0",
    ]

    [tool.cxfreeze]
    executables = ["test_ctypes.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter"]
    silent = true
"""


@pytest.mark.venv
def test_ctypes(tmp_package: TempPackage) -> None:
    """Test if ctypes hook is working correctly."""
    tmp_package.create(SOURCE_TEST_CTYPES)
    # force upgrade of freeze-core
    tmp_package.install_system_dependencies()  # ty: ignore
    tmp_package.freeze()
    executable = tmp_package.executable("test_ctypes")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "Hello ctypes*"])
