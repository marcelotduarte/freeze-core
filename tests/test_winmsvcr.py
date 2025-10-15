"""Test winmsvcr."""

from __future__ import annotations

import sys

import pytest

from freeze_core._compat import IS_LINUX, IS_WINDOWS
from freeze_core.winmsvcr import MSVC_FILES, UCRT_FILES

# This test is really necessary on Windows, but it runs in other environments,
# so I let it be tested on Python 3.12 Linux, which is used on Ubuntu 24.04.
# On other systems, it is disabled, including mingw.

MSVC_EXPECTED = (
    # VC 2015 and 2017
    "concrt140.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "vcamp140.dll",
    "vccorlib140.dll",
    "vcomp140.dll",
    "vcruntime140.dll",
    # VS 2019
    "msvcp140_atomic_wait.dll",
    "msvcp140_codecvt_ids.dll",
    "vcruntime140_1.dll",
    # VS 2022
    "vcruntime140_threads.dll",
)

UCRT_EXPECTED = (
    "api-ms-win-*.dll",
    "ucrtbase.dll",
)


@pytest.mark.skipif(
    not (IS_WINDOWS or (IS_LINUX and sys.version_info[:2] == (3, 12))),
    reason="Windows tests",
)
def test_files() -> None:
    """Test MSVC files."""
    assert MSVC_EXPECTED == MSVC_FILES
    assert UCRT_EXPECTED == UCRT_FILES
