"""Compiled functions for cx_Freeze."""

from pathlib import Path

try:
    from typing import TypeAlias  # 3.10+
except ImportError:
    from typing import Any as TypeAlias

HANDLE: TypeAlias = ...

class BindError(Exception):
    """BindError Exception."""

# ruff: noqa: ARG001

def AddIcon(target_path: str | Path, exe_icon: str | Path) -> None:
    """Add the icon as a resource to the specified file."""

def BeginUpdateResource(
    path: str | Path, delete_existing_resources: bool = True
) -> HANDLE:
    """Wrapper for BeginUpdateResource."""

def UpdateResource(
    handle: HANDLE, resource_type: int, resource_id: int, resource_data: bytes
) -> None:
    """Wrapper for UpdateResource."""

def EndUpdateResource(handle: HANDLE, discard_changes: bool) -> None:
    """Wrapper for EndUpdateResource."""

def UpdateCheckSum(target_path: str | Path) -> None:
    """Update the CheckSum into the specified executable."""

def GetSystemDir() -> str:
    r"""Return the Windows system directory (C:\Windows\system for example)."""

def GetWindowsDir() -> str:
    r"""Return the Windows directory (C:\Windows for example)."""

def GetDependentFiles(path: str | Path) -> list[str]:
    """Return a list of files that this file depends on."""
