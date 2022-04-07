"""To install the package with rez."""

import os
import shutil
import sys


def build(source_path, build_path, install_path, targets):
    """Build the package by copying it to the install_path."""

    # copy the src folder to the installation path
    _source_path = os.path.join(source_path, "src")
    _install_path = os.path.join(install_path, "src")
    if os.path.exists(_install_path):
        shutil.rmtree(_install_path)
    shutil.copytree(_source_path, _install_path)


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:],
    )
