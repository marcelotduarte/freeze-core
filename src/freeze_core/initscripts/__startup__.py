"""First script that is run when cx_Freeze starts up.

It determines the name of the initscript that is to be executed after a basic
initialization.
"""

from __future__ import annotations

import os
import sys
from _frozen_importlib import ModuleSpec
from _frozen_importlib_external import (
    EXTENSION_SUFFIXES,
    ExtensionFileLoader,
    PathFinder,
)


class ExtensionFinder(PathFinder):
    """A Finder for extension modules of packages in zip files."""

    @classmethod
    def find_spec(
        cls,
        fullname: str,
        path=None,  # noqa: ANN001 # Sequence[str]
        target=None,  # noqa: ARG003,ANN001 # ModuleType
    ) -> ModuleSpec | None:
        """Finder for extension modules only.

        The extension modules found within packages that are included in the
        zip file (instead of as files on disk) cannot be found within zip files
        but are stored in the lib subdirectory; if the extension module is
        found in a package, however, its name has been altered so this finder
        is needed.
        """
        if path is None:
            return None
        suffixes = EXTENSION_SUFFIXES
        for entry in sys.path:
            if not isinstance(entry, str):
                continue
            if ".zip" in entry:
                continue
            for ext in suffixes:
                location = os.path.join(entry, fullname + ext)
                if os.path.isfile(location):
                    loader = ExtensionFileLoader(fullname, location)
                    return ModuleSpec(fullname, loader, origin=location)
        return None


def get_name(executable: str) -> str:
    """Get the module basename to search for init and main scripts."""
    name = os.path.normcase(os.path.basename(executable))
    if sys.platform.startswith("win"):
        name, _ = os.path.splitext(name)
    name = name.partition(".")[0]
    if not name.isidentifier():
        import string  # noqa: PLC0415

        invalid = string.whitespace + string.punctuation
        idtable = str.maketrans(invalid, "_" * len(invalid))
        return name.translate(idtable)
    return name


def init() -> None:
    """Initialize the startup script."""
    # fix prefix if using console_legacy
    if not sys.prefix:
        sys.prefix = os.path.dirname(sys.executable)
        sys.base_prefix = sys.base_exec_prefix = sys.exec_prefix = sys.prefix

    # enable ExtensionFinder only if uses a zip file
    library_zip = None
    for path in sys.path:
        if path.endswith(".zip"):
            library_zip = path
            break
    if library_zip:
        sys.meta_path.append(ExtensionFinder)

    _fix_init()


def _fix_init() -> None:
    if not sys.platform.startswith("win"):
        return
    import BUILD_CONSTANTS  # noqa: PLC0415 # ty: ignore[unresolved-import]

    # to avoid bugs, especially in MSYS2, normalize sys.argv and sys.path
    # (preserving the reference)
    for j, path in enumerate(sys.path):
        sys.path[j] = os.path.normpath(path)
    sys.argv[0] = os.path.normpath(sys.argv[0])
    # the search path for dependencies
    search_path: list[str] = [
        entry for entry in sys.path if os.path.isdir(entry)
    ]
    # add to dll search path (or to path)
    env_path: list[str] = [
        os.path.normpath(entry) for entry in os.get_exec_path()
    ]
    for directory in search_path:
        try:  # noqa: SIM105
            os.add_dll_directory(directory)
        except OSError:
            pass
        # we need to add to path for packages like 'gi' in MSYS2
        if directory not in env_path:
            env_path.insert(0, directory)
    env_path = [entry.replace(os.sep, "\\") for entry in env_path]
    os.environ["PATH"] = os.pathsep.join(env_path)
    # add extra "module.libs"
    libs_dirs = getattr(BUILD_CONSTANTS, "__LIBS__", None)
    if libs_dirs:
        for entry in libs_dirs.split(os.pathsep):
            directory = os.path.normpath(
                os.path.join(sys.prefix, "lib", entry)
            )
            if os.path.isdir(directory):
                os.add_dll_directory(directory)


def run() -> None:
    """Determine the name of the initscript and execute it."""
    name = get_name(sys.executable)
    try:
        # basically is __init__ plus the basename of the executable
        module_init = __import__(f"__init__{name}")
    except ModuleNotFoundError:
        import BUILD_CONSTANTS  # noqa: PLC0415 # ty: ignore[unresolved-import]

        # but can be renamed when only one executable exists
        executables = BUILD_CONSTANTS.__EXECUTABLES__.split(os.pathsep)
        num = len(executables)
        if num > 1:
            msg = (
                "Apparently, the original executable has been renamed to "
                f"{name!r}. When multiple executables are frozen, "
                "renaming is not allowed."
            )
            raise RuntimeError(msg) from None
        name = get_name(executables[0])
        module_init = __import__(f"__init__{name}")
    module_init.run(f"__main__{name}")
