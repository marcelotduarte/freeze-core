"""Freeze modules and regenerate C code for them.

This tool was based on:
    https://github.com/python/cpython/blob/main/Tools/freeze/regen_frozen.py

More references:
    https://github.com/python/cpython/blob/main/Python/frozen.c
    https://github.com/python/cpython/blob/main/Tools/build/freeze_modules.py
"""

from __future__ import annotations

import _imp
import json
import marshal
import sys
from importlib import import_module
from importlib.machinery import FrozenImporter, PathFinder
from pathlib import Path
from sysconfig import get_config_var, get_platform
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from io import TextIOWrapper

PLATFORM = get_platform()
SOABI = get_config_var("SOABI")
if SOABI is None:
    # Python <= 3.12 on Windows
    platform_nodot = PLATFORM.replace(".", "").replace("-", "_")
    SOABI = f"{sys.implementation.cache_tag}-{platform_nodot}"
THIS = Path(__file__)

FROZEN_SOURCE: list[tuple[str, list[str] | str | None]] = [
    # module, filename | search_path | None
    ("__startup__", "src/freeze_core/initscripts/__startup__.py"),
    ("__future__", None),  # for __startup__
    ("collections", None),  # and collections.abc in Python < 3.13
    ("string", None),  # for __startup__
    # already frozen, some of them partially frozen
    ("abc", None),  # 3.11+
    ("codecs", None),  # 3.11+
    ("_collections_abc", None),  # 3.11+
    ("encodings", None),  # 3.15+ partially frozen
    ("genericpath", None),  # 3.11+
    ("importlib", None),  # 3.11+ partially frozen
    ("io", None),  # 3.11+
    ("ntpath", None),  # 3.11+
    ("os", None),  # 3.11+
    ("posixpath", None),  # 3.11+
    ("stat", None),  # 3.11+
]
frozen_module_names = cast(
    "list[str]",
    _imp._frozen_module_names(),  # ty: ignore # noqa: SLF001
)


def get_module_code(filename: Path) -> bytes:
    """Compile 'filename' and return a marshalled byte code."""
    src = filename.read_bytes()
    co = compile(src, filename.as_posix(), "exec")
    return marshal.dumps(co)


def gen_c_code(name: str, src: Path, fp: TextIOWrapper) -> tuple[str, str]:
    """Generate C code for the source module, write it to 'fp'."""
    co_bytes = get_module_code(src)

    symbol = f"M_{name.replace('.', '_')}"
    fp.write(f"static unsigned char {symbol}[] = {{")
    bytes_per_row = 15
    for i, opcode in enumerate(co_bytes):
        if (i % bytes_per_row) == 0:
            # start a new row
            fp.write("\n    ")
        fp.write(f"{opcode:d}, ")
    fp.write("\n};\n\n")
    return name, symbol


def gen_symbols(fp: TextIOWrapper) -> list[tuple[str, str, bool]]:
    """Generate C code for all required modules, write it to 'fp'."""
    table = []
    todo = FROZEN_SOURCE[:]
    while todo:
        name, source = todo.pop()
        if isinstance(source, str):
            src = Path(source)
        else:
            spec = PathFinder.find_spec(name, path=source)
            if not spec or spec.origin in (None, "buit-in", "frozen"):
                continue
            src = Path(spec.origin)
            if src.stem == "__init__":
                for file in src.parent.iterdir():
                    if file.name not in ("__init__.py", "__pycache__") and (
                        file.suffix == ".py" or file.is_dir()
                    ):
                        search_path = spec.submodule_search_locations
                        todo.append((f"{name}.{file.stem}", search_path))
            # Check if name is already frozen after processing the directory
            # because packages may have been partially frozen.
            spec = FrozenImporter.find_spec(name)
            if spec:
                continue
            # Check if it is frozen using an alias.
            module = sys.modules.get(name)
            if module is None:
                try:
                    module = import_module(name)
                except ImportError:
                    module = None
            if module is not None:
                spec = module.__spec__
                if spec and spec.origin in (None, "buit-in", "frozen"):
                    continue
        _name, symbol = gen_c_code(name, src, fp)
        table.append((name, symbol, bool(src.stem == "__init__")))
    return table


def gen_source_file(filename: Path) -> Path:
    """Generate C code for all required modules, write it to 'filename'.

    A JSON file containing all built-in and frozen modules is also
    generated.
    """
    with filename.open("w") as fp:
        fp.write(f"/* Generated with {THIS.name} */\n\n")
        fp.write("#define PY_SSIZE_T_CLEAN\n")
        fp.write("#include <Python.h>\n\n")

        table = gen_symbols(fp)

        fp.write("const struct _frozen CoreFrozenModules[] = {\n")
        for name, symbol, is_package in sorted(table):
            fp.write(f'    {{"{name}", {symbol}, (int)sizeof({symbol}), ')
            fp.write(f"{1 if is_package else 0}}},\n")
        fp.write("    {0, 0, 0},\n")  # sentinel
        fp.write("};\n")

    internal = {"__version__": sys.version}
    for name in sys.builtin_module_names:
        internal[name] = "built-in"
    for name in frozen_module_names:
        internal[name] = "frozen"
    for name, _symbol, _is_package in sorted(table):
        internal[name] = "core"

    filename2 = filename.with_suffix(".json")
    with filename2.open("w") as fp:
        json.dump(internal, fp, indent=1)

    return filename


if __name__ == "__main__":
    frozen_dir = Path("src/freeze_core/frozen")
    frozen_dir.mkdir(exist_ok=True)
    frozen_dir.joinpath(".gitignore").write_bytes(b"*")
    filename = frozen_dir / f"frozen-{SOABI}.c"
    filename = gen_source_file(filename)
    print(f"{filename} generated!")
    print(f"{filename.with_suffix('.json')} generated!")
