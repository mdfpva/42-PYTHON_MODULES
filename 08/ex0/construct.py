#!/usr/bin/env python3

# sys  - access to interpreter internals: sys.prefix, sys.executable, sys.version_info
# os   - access to environment variables (os.environ) and path utilities (os.path)
# site - access to package installation paths (site.getsitepackages)
import sys
import os
import site


def is_virtual_env() -> bool:
    """Detect if currently running inside a virtual environment."""

    # os.environ.get("VIRTUAL_ENV") reads the VIRTUAL_ENV shell variable,
    # which is automatically set by 'source activate' when entering a venv.
    # Returns None if the variable doesn't exist (i.e. no venv is active).
    has_venv_var = os.environ.get("VIRTUAL_ENV") is not None

    # sys.prefix  → path to the active Python environment (venv dir when inside one)
    # sys.base_prefix → path to the original system Python (never changes)
    # getattr(..., sys.prefix) provides a safe fallback for Python < 3.3,
    # where base_prefix didn't exist yet. If they differ, we're in a venv.
    has_prefix_diff = sys.prefix != getattr(sys, "base_prefix", sys.prefix)

    # hasattr(sys, "real_prefix") catches older virtualenv (pre-3.3) setups,
    # which stored the original prefix in sys.real_prefix instead of base_prefix.
    has_real_prefix = hasattr(sys, "real_prefix")

    # Any single True is enough to confirm we're inside a virtual environment.
    return has_venv_var or has_prefix_diff or has_real_prefix


def get_venv_name() -> str:
    """Get the name of the current virtual environment."""

    # Prefer VIRTUAL_ENV because it is always set to the venv root by activate.
    virtual_env = os.environ.get("VIRTUAL_ENV")
    if virtual_env:
        # os.path.basename extracts the last component of the path,
        # e.g. "/home/user/projects/matrix_env" → "matrix_env"
        return os.path.basename(virtual_env)

    # Fallback: sys.prefix also points to the venv root when inside one.
    return os.path.basename(sys.prefix)


def get_venv_path() -> str:
    """Get the root path of the current virtual environment."""

    # VIRTUAL_ENV holds the absolute path set on activation.
    # sys.prefix is used as a fallback in case the env was not activated
    # through a shell (e.g. called directly via the venv's Python binary).
    return os.environ.get("VIRTUAL_ENV", sys.prefix)


def get_site_packages() -> str:
    """Get the primary site-packages path for the current environment."""

    # site.getsitepackages() returns a list of directories where pip installs
    # packages. The first entry is the main one (e.g. lib/python3.x/site-packages).
    # hasattr guards against environments where this function is unavailable.
    if hasattr(site, "getsitepackages"):
        packages = site.getsitepackages()
        if packages:
            return packages[0]  # pick the primary site-packages directory

    # Fallback: build the path manually using the version numbers from sys.version_info.
    # sys.version_info.major → 3, sys.version_info.minor → 11 (for Python 3.11)
    python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"

    # os.path.join assembles the path safely for any OS:
    # e.g. /path/to/matrix_env/lib/python3.11/site-packages
    return os.path.join(sys.prefix, "lib", python_version, "site-packages")


def show_outside() -> None:
    """Display info and instructions when outside a virtual environment."""

    # sys.executable is the absolute path to the Python interpreter currently running.
    print("MATRIX STATUS: You're still plugged in")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()  # blank line for readability
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")

    # 'python -m venv matrix_env' creates a new isolated environment in ./matrix_env/
    print("    python -m venv matrix_env")

    # 'source activate' modifies the current shell session to use the venv's Python.
    print("    source matrix_env/bin/activate  # On Unix")

    # Raw string r"..." prevents Python from interpreting the backslash as an escape.
    print(r"    matrix_env\Scripts\activate     # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    """Display environment details when inside a virtual environment."""

    print("MATRIX STATUS: Welcome to the construct")

    # sys.executable now points to the venv's own Python binary, not the system one.
    print(f"Current Python: {sys.executable}")

    # Display the folder name of the active venv (e.g. "matrix_env").
    print(f"Virtual Environment: {get_venv_name()}")

    # Display the full root path of the active venv.
    print(f"Environment Path: {get_venv_path()}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()

    # Show where pip will install packages inside this venv.
    print(f"Package installation path: {get_site_packages()}")


def main() -> None:
    # Branch on whether a venv is active and call the appropriate display function.
    if is_virtual_env():
        show_inside()   # venv detected: show environment details
    else:
        show_outside()  # no venv: warn user and provide setup instructions


# Standard Python entry-point guard:
# __name__ is "__main__" only when this file is run directly (python construct.py).
# If it were imported as a module, __name__ would be "construct" and main() would
# not be called automatically.
if __name__ == "__main__":
    main()
