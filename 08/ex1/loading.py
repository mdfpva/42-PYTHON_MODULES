#!/usr/bin/env python3

import sys
import importlib


class DepInfo:
    """Status of one dependency after an import probe."""

    def __init__(
        self,
        version:     str | None,
        ok:          bool,
        display:     str,
        description: str,
        required:    bool
    ) -> None:
        self.version     = version
        self.ok          = ok
        self.display     = display
        self.description = description
        self.required    = required


DEPENDENCIES: list[tuple[str, str, str, bool]] = [
    ("pandas",     "pandas",     "Data manipulation",     True),
    ("numpy",      "numpy",      "Numerical computation", True),
    ("requests",   "requests",   "Network access",        False),
    ("matplotlib", "matplotlib", "Visualization",         True),
]

N_POINTS:    int = 1000
OUTPUT_FILE: str = "matrix_analysis.png"


def check_dependencies() -> dict[str, DepInfo]:
    """
    Probe every package in DEPENDENCIES with importlib.import_module.
    Returns a dict[str, DepInfo] keyed by import name.
    """
    results: dict[str, DepInfo] = {}

    for import_name, display_name, description, required in DEPENDENCIES:
        try:
            mod = importlib.import_module(import_name)

            version: str | None = getattr(mod, "__version__", "unknown")

            results[import_name] = DepInfo(
                version=version, ok=True,
                display=display_name, description=description, required=required,
            )

        except ImportError:
            results[import_name] = DepInfo(
                version=None, ok=False,
                display=display_name, description=description, required=required,
            )

    return results


def print_dependency_status(results: dict[str, DepInfo]) -> None:
    """Print a formatted [OK] / [MISSING] line for each relevant package."""
    print("Checking dependencies:")

    for _import_name, info in results.items():
        if not info.required and not info.ok:
            continue

        if info.ok:
            label: str = f"[OK] {info.display} ({info.version})"
            print(f"  {label} - {info.description} ready")
        else:
            label = f"[MISSING] {info.display}"
            print(f"  {label:<30} - {info.description}")


def missing_required(results: dict[str, DepInfo]) -> list[str]:
    """Return import names of required packages that failed to load."""

    return [
        name for name, info in results.items()
        if info.required and not info.ok
    ]


def show_install_instructions() -> None:
    """Print pip and Poetry installation commands for the missing packages."""
    print()
    print("ERROR: Required packages are missing.")
    print()
    print("To install with pip:")
    print("    pip install -r requirements.txt")
    print("    python loading.py")
    print()
    print("To install with Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py")


def show_manager_comparison() -> None:
    """Explain the key differences between pip and Poetry."""
 
    in_venv:   bool = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    env_label: str  = sys.prefix if in_venv else "global (no venv active)"

    print()
    print("Dependency manager comparison:")
    print("  pip:    reads requirements.txt and installs into the active env")
    print("          no automatic lock file — versions may drift over time")
    print("  Poetry: reads pyproject.toml, resolves and pins all versions in")
    print("          poetry.lock, and manages its own venv automatically")
    print(f"  Python binary:      {sys.executable}")
    print(f"  Active environment: {env_label}")


def simulate_matrix_data() -> dict[str, object]:
    """
    Generate all dataset columns exclusively with numpy functions.

    Why a local import instead of a module parameter typed Any?
      'import numpy as np' here lets mypy resolve np's type from numpy's stubs.
      Passing the module as 'np: Any' would suppress all type checking on it.
      The local import is safe because check_dependencies() already confirmed
      numpy is installed before this function is ever called.

    Return type dict[str, object]:
      numpy.ndarray is only resolvable when numpy stubs are installed.
      object is the correct untyped upper bound — every ndarray IS an object.
    """
    import numpy as np
    np.random.seed(42)

    time = np.linspace(0, 4 * np.pi, N_POINTS)

    agent_activity = np.sin(time) + np.random.normal(0, 0.3, N_POINTS)

    signal_strength = np.random.normal(0, 1.5, N_POINTS)

    residual = 0.6 * agent_activity + np.random.normal(0, 0.5, N_POINTS)

    return {
        "time":            time,
        "agent_activity":  agent_activity,
        "signal_strength": signal_strength,
        "residual":        residual,
    }


def build_dataframe(data: dict[str, object]) -> object:
    """
    Wrap the numpy arrays in a pandas DataFrame.
    Local import for the same reason as simulate_matrix_data.
    Return type is object: pd.DataFrame is only known when pandas stubs are
    installed; object is the safe untyped upper bound.
    """
    import pandas as pd

    return pd.DataFrame({
        "time":            data["time"],
        "agent_activity":  data["agent_activity"],
        "signal_strength": data["signal_strength"],
        "residual":        data["residual"],
    })


def print_statistics(df: object) -> None:
    """
    Compute and display descriptive statistics using pandas Series methods.

    Why isinstance instead of a more specific parameter type?
      We cannot annotate df as pd.DataFrame at the top of the file because
      pandas may not be installed (and we have no 'typing.TYPE_CHECKING' block
      without 'typing'). Receiving df as object and narrowing with isinstance
      gives mypy the same information: after the guard, df is pd.DataFrame and
      all subscript and method-call types are fully verified.
    """
    import pandas as pd

    if not isinstance(df, pd.DataFrame):
        return

    aa = df["agent_activity"]
    ss = df["signal_strength"]

    print(f"    Agent activity  — "
          f"mean: {aa.mean():+.4f}  std: {aa.std():.4f}  "
          f"min/max: {aa.min():.3f} / {aa.max():.3f}")
    print(f"    Signal strength — "
          f"mean: {ss.mean():+.4f}  std: {ss.std():.4f}  "
          f"min/max: {ss.min():.3f} / {ss.max():.3f}")


def generate_visualization(df: object) -> None:
    """
    Build a 3-panel matplotlib figure and save it to OUTPUT_FILE.
    Both matplotlib.pyplot and pandas are imported locally — safe because
    check_dependencies() confirmed they are installed before this is called.
    The isinstance check narrows df to pd.DataFrame for mypy.
    """
    import matplotlib.pyplot as plt
    import pandas as pd

    if not isinstance(df, pd.DataFrame):
        return

    plt.style.use("dark_background")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Matrix Signal Analysis", color="#00ff41", fontsize=14)

    GREEN: str = "#00ff41"
 
    ax1.plot(df["time"], df["agent_activity"],
             color=GREEN, linewidth=0.8, alpha=0.9)
    ax1.set_title("Agent Activity", color=GREEN)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")

    ax2.hist(df["signal_strength"], bins=40,
             color=GREEN, alpha=0.8, edgecolor="black")
    ax2.set_title("Signal Distribution", color=GREEN)
    ax2.set_xlabel("Strength")
    ax2.set_ylabel("Frequency")

    ax3.scatter(df["agent_activity"], df["residual"],
                color=GREEN, alpha=0.3, s=4)
    ax3.set_title("Activity vs Residual", color=GREEN)
    ax3.set_xlabel("Agent Activity")
    ax3.set_ylabel("Residual")

    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")

    plt.close(fig)

def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()

    results: dict[str, DepInfo] = check_dependencies()
    print_dependency_status(results)

    missing: list[str] = missing_required(results)
    if missing:
        show_install_instructions()
        sys.exit(1)

    show_manager_comparison()

    print()
    print("Analyzing Matrix data...")
    print(f"  Generating {N_POINTS} data points with numpy...")
    data: dict[str, object] = simulate_matrix_data()

    print("  Loading into pandas DataFrame...")
    df: object = build_dataframe(data)

    print("  Computing statistics...")
    print_statistics(df)

    print()
    print("Generating visualization...")
    generate_visualization(df)

    print(f"Analysis complete! Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
