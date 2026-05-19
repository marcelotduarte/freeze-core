# ruff: noqa: PYI021
"""Compiled functions in freeze_core.util."""

from os import PathLike
from typing import NewType, TypeAlias

HANDLE = NewType("HANDLE", int)
StrPath: TypeAlias = str | PathLike[str]

class BindError(Exception):
    """BindError Exception."""

def AddIcon(target_path: StrPath, exe_icon: StrPath) -> None:
    """Add the icon as a resource to the specified file."""

def BeginUpdateResource(
    path: StrPath, delete_existing_resources: bool = True
) -> HANDLE:
    """BeginUpdateResource wrapper."""

def UpdateResource(
    handle: HANDLE, resource_type: int, resource_id: int, resource_data: bytes
) -> None:
    """UpdateResource wrapper."""

def EndUpdateResource(handle: HANDLE, discard_changes: bool) -> None:
    """EndUpdateResource wrapper."""

def UpdateCheckSum(target_path: StrPath) -> None:
    """Update the CheckSum into the specified executable."""

def GetSystemDir() -> str:
    r"""Return the Windows system directory (C:\Windows\system for example)."""

def GetWindowsDir() -> str:
    r"""Return the Windows directory (C:\Windows for example)."""

def GetDependentFiles(path: StrPath) -> list[str]:
    """Return a list of files that this file depends on."""
