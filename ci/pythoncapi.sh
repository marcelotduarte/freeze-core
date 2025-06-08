#!/bin/bash

# Get script directory (without using /usr/bin/realpath)
_CI_DIR=$(dirname "${BASH_SOURCE[0]}")
CI_DIR=$(cd "$_CI_DIR" && pwd)
TOP_DIR=$(cd "$CI_DIR/.." && pwd)

CI_TMPDIR=$(python -c "import tempfile; print(tempfile.mkdtemp())")
pushd "$CI_TMPDIR" >/dev/null || exit
git clone -q https://github.com/python/pythoncapi-compat .
python upgrade_pythoncapi.py \
    "$TOP_DIR/src/" --download "$TOP_DIR/src/freeze_core/include/"
popd >/dev/null || exit
