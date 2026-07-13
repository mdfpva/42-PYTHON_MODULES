#!/usr/bin/env python3

import sys
import os
import site


def is_virtual_env() -> bool:
    """Detect if currently running inside a virtual environment."""

    has_venv_var = os.environ.get("VIRTUAL_ENV") is not None

    has_prefix_diff = sys.prefix != getattr(sys, "base_prefix", sys.prefix)

    has_real_prefix = hasattr(sys, "real_prefix")

    return has_venv_var or has_prefix_diff or has_real_prefix


def get_venv_name() -> str:
    """Get the name of the current virtual environment."""

    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        return os.path.basename(virtual_env)

    return os.path.basename(sys.prefix)


def get_venv_path() -> str:
    """Get the root path of the current virtual environment."""

    return os.environ.get("VIRTUAL_ENV", sys.prefix)


def get_site_packages() -> str:
    """Get the primary site-packages path for the current environment."""

    if hasattr(site, "getsitepackages"):
        packages = site.getsitepackages()
        if packages:
            return packages[0]

    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"

    return os.path.join(sys.prefix, "lib", python_version, "site-packages")


def show_outside() -> None:
    """Display info and instructions when outside a virtual environment."""

    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")

    print("    python -m venv matrix_env")

    print("    source matrix_env/bin/activate  # On Unix")

    print(r"    matrix_env\Scripts\activate     # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    """Display environment details when inside a virtual environment."""

    print("MATRIX STATUS: Welcome to the construct")

    print(f"Current Python: {sys.executable}")

    print(f"Virtual Environment: {get_venv_name()}")

    print(f"Environment Path: {get_venv_path()}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()

    print(f"Package installation path: {get_site_packages()}")


def main() -> None:
    if is_virtual_env():
        show_inside()
    else:
        show_outside()


if __name__ == "__main__":
    main()
