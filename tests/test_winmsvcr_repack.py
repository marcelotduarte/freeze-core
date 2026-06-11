"""Test winmsvcr_repack."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from freeze_core._compat import IS_LINUX, IS_UCRT
from freeze_core.winmsvcr import MSVC_FILES, UCRT_FILES
from freeze_core.winmsvcr_repack import copy_msvcr_files, main_test

if TYPE_CHECKING:
    from .conftest import TempPackage
# This test is really necessary on Windows, but it runs in other environments,
# so I let it be tested on Python 3.12 Linux, which is used on Ubuntu 24.04.

TEST_ENABLED = IS_UCRT or (IS_LINUX and sys.version_info[:2] == (3, 12))


@pytest.mark.skipif(not TEST_ENABLED, reason="Windows tests")
@pytest.mark.parametrize(
    ("version", "platform", "no_cache"),
    [
        ("15", "win32", False),
        ("15", "win-amd64", False),
        ("15", "win-arm64", False),
        ("16", "win32", False),
        ("16", "win-amd64", False),
        ("16", "win-arm64", False),
        ("17", "win32", False),
        ("17", "win-amd64", True),  # just one no_cache is enough
        ("17", "win-arm64", False),
        (17, "win-arm64", False),  # one test using int
    ],
)
def test_versions(
    tmp_package: TempPackage, version: int | str, platform: str, no_cache: bool
) -> None:
    """Test the downloads of all versions of msvcr."""
    copy_msvcr_files(tmp_package.path, platform, version, no_cache=no_cache)
    expected = [*MSVC_FILES]
    if version == "15":
        expected.extend(UCRT_FILES)
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, expected))
    ]
    assert names != []


@pytest.mark.skipif(not TEST_ENABLED, reason="Windows tests")
@pytest.mark.parametrize(
    ("version", "platform", "expected_exception", "expected_match"),
    [
        ("18", "win-amd64", RuntimeError, "Version is not expected"),
        ("17", "", RuntimeError, "Architecture not supported"),
        ("17", "win64", RuntimeError, "Architecture not supported"),
    ],
)
def test_invalid(
    tmp_package: TempPackage,
    version: str,
    platform: str,
    expected_exception: type[BaseException],
    expected_match: str,
) -> None:
    """Test invalid values to use with copy_msvcr_files function."""
    with pytest.raises(expected_exception, match=expected_match):
        copy_msvcr_files(tmp_package.path, platform, version)


@pytest.mark.skipif(not TEST_ENABLED, reason="Windows tests")
def test_repack_main(tmp_package: TempPackage) -> None:
    """Test the freeze_core.winmsvcr_repack __main_ entry point with args."""
    main_test(
        args=[
            f"--target-dir={tmp_package.path}",
            "--target-platform=win-amd64",
            "--version=17",
        ]
    )
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("*.dll")
        if any(filter(file.match, MSVC_FILES))
    ]
    assert names != []


@pytest.mark.skipif(not TEST_ENABLED, reason="Windows tests")
def test_repack_main_no_option(tmp_package: TempPackage) -> None:
    """Test the freeze_core.winmsvcr_repack 'main' entry point without args."""
    main_test(args=[])
    names = [
        file.name.lower()
        for file in tmp_package.path.glob("dist/*.dll")
        if any(filter(file.match, MSVC_FILES))
    ]
    assert names != []
