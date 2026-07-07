#!/usr/bin/env python3
# sys       - sys.prefix / sys.base_prefix (detect venv), sys.exit (abort on error)
# importlib - importlib.import_module: probe packages without crashing on ImportError
#
# No 'typing' import: Python 3.10+ built-in syntax replaces every typing construct:
#   X | None          instead of Optional[X]
#   X | Y             instead of Union[X, Y]
#   list[X]           instead of List[X]
#   dict[K, V]        instead of Dict[K, V]
#   tuple[X, ...]     instead of Tuple[X, ...]
#   plain class       instead of TypedDict
#   local imports     instead of Any  (mypy resolves types from in-scope imports)
import sys
import importlib


# ---------------------------------------------------------------------------
# DepInfo — plain class replaces TypedDict, no 'typing' needed.
#
# Why not TypedDict?
#   typing.TypedDict is the only option for typed dicts; without 'typing' we
#   use a regular class instead. The trade-off is attribute access (info.ok)
#   instead of key access (info["ok"]), but mypy understands both equally well.
#
# Why no 'module' field?
#   The previous version stored the module object here so it could be passed
#   as a parameter (typed Any). Without Any we instead import each package
#   locally inside the function that uses it — safer and fully typed.
# ---------------------------------------------------------------------------

class DepInfo:
    """Status of one dependency after an import probe."""

    def __init__(
        self,
        version:     str | None,  # __version__ string, or None when missing
        ok:          bool,        # True if importlib.import_module succeeded
        display:     str,         # human-readable name shown in output
        description: str,         # one-line role description
        required:    bool,        # True → absence causes sys.exit(1)
    ) -> None:
        # Each assignment inherits its type from the parameter annotation above.
        # mypy infers self.ok: bool, self.version: str | None, etc. automatically.
        self.version     = version
        self.ok          = ok
        self.display     = display
        self.description = description
        self.required    = required


# ---------------------------------------------------------------------------
# Dependency manifest
# Tuple layout: (import_name, display_name, description, required)
# required=False → a missing package is silently skipped, not an error.
# ---------------------------------------------------------------------------
DEPENDENCIES: list[tuple[str, str, str, bool]] = [
    ("pandas",     "pandas",     "Data manipulation",     True),
    ("numpy",      "numpy",      "Numerical computation", True),
    ("requests",   "requests",   "Network access",        False),
    ("matplotlib", "matplotlib", "Visualization",         True),
]

N_POINTS:    int = 1000                   # number of simulated Matrix data points
OUTPUT_FILE: str = "matrix_analysis.png"  # destination path for the saved figure


# ---------------------------------------------------------------------------
# 1. Dependency checking
# ---------------------------------------------------------------------------

def check_dependencies() -> dict[str, DepInfo]:
    """
    Probe every package in DEPENDENCIES with importlib.import_module.
    Returns a dict[str, DepInfo] keyed by import name.
    """
    results: dict[str, DepInfo] = {}

    for import_name, display_name, description, required in DEPENDENCIES:
        try:
            # importlib.import_module is the programmatic form of 'import X'.
            # Wrapping it in try/except lets us catch ImportError gracefully
            # instead of crashing the whole program on a missing package.
            mod = importlib.import_module(import_name)

            # __version__ is a PEP 396 convention; not every package defines it,
            # so getattr provides "unknown" as a safe fallback.
            # str | None without 'typing': Python 3.10+ union syntax.
            version: str | None = getattr(mod, "__version__", "unknown")

            results[import_name] = DepInfo(
                version=version, ok=True,
                display=display_name, description=description, required=required,
            )

        except ImportError:
            # Record the failure without re-raising so we can keep checking
            # the remaining packages and report all missing ones at once.
            results[import_name] = DepInfo(
                version=None, ok=False,
                display=display_name, description=description, required=required,
            )

    return results


def print_dependency_status(results: dict[str, DepInfo]) -> None:
    """Print a formatted [OK] / [MISSING] line for each relevant package."""
    print("Checking dependencies:")

    for _import_name, info in results.items():
        # Attribute access on the plain class: info.ok, info.required, etc.
        # mypy knows their types from DepInfo.__init__ annotations.
        if not info.required and not info.ok:
            # Silently skip optional packages that are not installed.
            continue

        if info.ok:
            # f-string embeds the version number inline in the label.
            label: str = f"[OK] {info.display} ({info.version})"
            print(f"  {label} - {info.description} ready")
        else:
            label = f"[MISSING] {info.display}"
            # :<30 left-aligns the label in a 30-character column.
            print(f"  {label:<30} - {info.description}")


def missing_required(results: dict[str, DepInfo]) -> list[str]:
    """Return import names of required packages that failed to load."""
    # list[str] without 'typing': built-in generic (Python 3.9+).
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


# ---------------------------------------------------------------------------
# 2. pip vs Poetry comparison
# ---------------------------------------------------------------------------

def show_manager_comparison() -> None:
    """Explain the key differences between pip and Poetry."""
    # sys.prefix  → root of the currently active Python environment.
    # sys.base_prefix → root of the original system Python (never changes).
    # When they differ, we are inside a virtual environment.
    in_venv:   bool = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    env_label: str  = sys.prefix if in_venv else "global (no venv active)"

    print()
    print("Dependency manager comparison:")
    print("  pip:    reads requirements.txt and installs into the active env")
    print("          no automatic lock file — versions may drift over time")
    print("  Poetry: reads pyproject.toml, resolves and pins all versions in")
    print("          poetry.lock, and manages its own venv automatically")
    # sys.executable is the absolute path to the Python binary running now.
    print(f"  Python binary:      {sys.executable}")
    print(f"  Active environment: {env_label}")


# ---------------------------------------------------------------------------
# 3. Matrix data simulation (numpy only — no hardcoded lists or range())
# ---------------------------------------------------------------------------

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
    import numpy as np  # local: avoids top-level ImportError when numpy is missing

    # np.random.seed: fix the RNG state so every run produces identical data.
    np.random.seed(42)

    # np.linspace(start, stop, num): N_POINTS evenly spaced floats from 0 to 4π.
    # 4π = two full sine cycles, giving a clear periodic pattern.
    time = np.linspace(0, 4 * np.pi, N_POINTS)

    # Periodic agent-activity signal: sine wave + Gaussian noise.
    # np.random.normal(mean, std, size) draws from a normal distribution.
    agent_activity = np.sin(time) + np.random.normal(0, 0.3, N_POINTS)

    # Independent signal-strength channel: zero-mean, std=1.5.
    signal_strength = np.random.normal(0, 1.5, N_POINTS)

    # Residual: 60 % correlated with agent_activity, plus its own noise.
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
    import pandas as pd  # local: avoids top-level ImportError when pandas is missing

    # pd.DataFrame accepts a dict of equal-length array-like values as columns.
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
    import pandas as pd  # local import for isinstance and type narrowing

    # isinstance narrows the type of df from object to pd.DataFrame.
    # mypy uses this to allow df["col"] subscript access and Series methods.
    if not isinstance(df, pd.DataFrame):
        return

    aa = df["agent_activity"]   # pd.Series — mypy knows this after narrowing
    ss = df["signal_strength"]  # pd.Series

    # :+.4f → always show sign (+/-) and 4 decimal places.
    # :.3f  → 3 decimal places for min/max (shorter, less noise).
    print(f"    Agent activity  — "
          f"mean: {aa.mean():+.4f}  std: {aa.std():.4f}  "
          f"min/max: {aa.min():.3f} / {aa.max():.3f}")
    print(f"    Signal strength — "
          f"mean: {ss.mean():+.4f}  std: {ss.std():.4f}  "
          f"min/max: {ss.min():.3f} / {ss.max():.3f}")


# ---------------------------------------------------------------------------
# 4. Visualization
# ---------------------------------------------------------------------------

def generate_visualization(df: object) -> None:
    """
    Build a 3-panel matplotlib figure and save it to OUTPUT_FILE.
    Both matplotlib.pyplot and pandas are imported locally — safe because
    check_dependencies() confirmed they are installed before this is called.
    The isinstance check narrows df to pd.DataFrame for mypy.
    """
    import matplotlib.pyplot as plt  # local: all drawing functions live here
    import pandas as pd              # local: needed for isinstance narrowing

    # isinstance narrows df from object to pd.DataFrame.
    # After this guard, mypy allows df["col"] subscript access.
    if not isinstance(df, pd.DataFrame):
        return

    # "dark_background" built-in style: white-on-black — Matrix terminal feel.
    plt.style.use("dark_background")

    # plt.subplots(rows, cols, figsize): returns a Figure and a tuple of Axes.
    # figsize=(15, 4): 15-inch wide by 4-inch tall canvas.
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Matrix Signal Analysis", color="#00ff41", fontsize=14)

    GREEN: str = "#00ff41"   # iconic Matrix terminal green

    # --- Panel 1: agent activity time series ---
    # linewidth=0.8 keeps the noisy signal readable without looking too thick.
    ax1.plot(df["time"], df["agent_activity"],
             color=GREEN, linewidth=0.8, alpha=0.9)
    ax1.set_title("Agent Activity", color=GREEN)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Amplitude")

    # --- Panel 2: signal-strength histogram ---
    # bins=40: divide the data range into 40 equal-width bars.
    # edgecolor="black" draws a thin border between bars for clarity.
    ax2.hist(df["signal_strength"], bins=40,
             color=GREEN, alpha=0.8, edgecolor="black")
    ax2.set_title("Signal Distribution", color=GREEN)
    ax2.set_xlabel("Strength")
    ax2.set_ylabel("Frequency")

    # --- Panel 3: scatter — agent activity vs residual ---
    # s=4: marker size in points²; alpha=0.3: semi-transparent to show density.
    ax3.scatter(df["agent_activity"], df["residual"],
                color=GREEN, alpha=0.3, s=4)
    ax3.set_title("Activity vs Residual", color=GREEN)
    ax3.set_xlabel("Agent Activity")
    ax3.set_ylabel("Residual")

    # tight_layout adjusts subplot spacing to prevent label overlap.
    plt.tight_layout()

    # savefig writes the figure to disk.
    # dpi=150 → 150 dots per inch (crisp without being huge).
    # bbox_inches="tight" trims excess whitespace from the edges.
    plt.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")

    # Close the figure to release the memory held by its internal state.
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()

    # Step 1 — Probe every package in the manifest.
    results: dict[str, DepInfo] = check_dependencies()
    print_dependency_status(results)

    # Step 2 — Abort if any required package is absent.
    missing: list[str] = missing_required(results)
    if missing:
        show_install_instructions()
        # sys.exit(1) signals to the shell that the process ended with an error.
        sys.exit(1)

    # Step 3 — Explain pip vs Poetry.
    show_manager_comparison()

    # Step 4 — Simulate, load, and analyse.
    # No module objects are extracted from results here: each analysis function
    # does its own local import (safe — step 1 confirmed they are all installed).
    print()
    print("Analyzing Matrix data...")
    print(f"  Generating {N_POINTS} data points with numpy...")
    data: dict[str, object] = simulate_matrix_data()

    print("  Loading into pandas DataFrame...")
    df: object = build_dataframe(data)

    print("  Computing statistics...")
    print_statistics(df)

    # Step 5 — Render and save the figure.
    print()
    print("Generating visualization...")
    generate_visualization(df)

    print(f"Analysis complete! Results saved to: {OUTPUT_FILE}")


# Standard entry-point guard: __name__ equals "__main__" only when this file
# is run directly (python loading.py), not when imported as a module.
if __name__ == "__main__":
    main()
