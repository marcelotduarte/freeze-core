"""Initialization script for cx_Freeze.

Sets the attribute sys.frozen so that modules that expect it behave as they
should.
"""

from __future__ import annotations

import importlib.util
import sys
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from importlib.machinery import SourcelessFileLoader

sys.frozen = True  # ty: ignore[unresolved-attribute]

ERROR_MSG = "Error: main script {name!r} {msg}"


def run(name) -> None:
    """Execute the main script of the frozen application."""
    spec = importlib.util.find_spec(name)
    if spec is None:
        msg = ERROR_MSG.format(name=name, msg="not found")
        raise RuntimeError(msg)
    loader = cast("SourcelessFileLoader", spec.loader)
    if loader is None:
        msg = ERROR_MSG.format(name=name, msg="loader error")
        raise RuntimeError(msg)
    code = loader.get_code(name)
    if code is None:
        msg = ERROR_MSG.format(name=name, msg="code error")
        raise RuntimeError(msg)
    main_module = sys.modules["__main__"]
    main_globals = main_module.__dict__
    main_globals.update(
        __cached__=spec.cached,
        __file__=spec.cached,
        __loader__=spec.loader,
        __spec__=spec,
    )
    exec(code, main_globals)
