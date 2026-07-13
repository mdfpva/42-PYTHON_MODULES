<div align="center">

```
 _____ _          __  __      _       _
|_   _| |_  ___  |  \/  |__ _| |_ _ _(_)_ __
  | | | ' \/ -_) | |\/| / _` |  _| '_| \ \ /
  |_| |_||_\___| |_|  |_\__,_|\__|_| |_/_\_\
```

💊 42 💊

### Welcome to the Real World of Data Engineering

**A 42 School Project — Python Piscine, Environment & Tooling Module**

*You've taken the red pill. Now it's time to learn how to architect data
systems in the real world. Master virtual environments, package management,
and environment configuration to build your first data pipeline.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. The Problem: One Global Python for Everything](#1-the-problem-one-global-python-for-everything)
  - [2. Virtual Environments — the Construct](#2-virtual-environments--the-construct)
  - [3. What Activation Actually Does](#3-what-activation-actually-does)
  - [4. Detecting a venv from Inside Python](#4-detecting-a-venv-from-inside-python)
  - [5. site-packages: Global vs Isolated](#5-site-packages-global-vs-isolated)
  - [6. pip and requirements.txt](#6-pip-and-requirementstxt)
  - [7. Poetry and pyproject.toml](#7-poetry-and-pyprojecttoml)
  - [8. pip vs Poetry — the Real Differences](#8-pip-vs-poetry--the-real-differences)
  - [9. Graceful Degradation: Optional Imports](#9-graceful-degradation-optional-imports)
  - [10. Introspecting Installed Versions](#10-introspecting-installed-versions)
  - [11. Environment Variables — the Mainframe's Config](#11-environment-variables--the-mainframes-config)
  - [12. .env Files and python-dotenv](#12-env-files-and-python-dotenv)
  - [13. Precedence: Real Environment Beats the File](#13-precedence-real-environment-beats-the-file)
  - [14. Secrets Hygiene: .env.example and .gitignore](#14-secrets-hygiene-envexample-and-gitignore)
  - [15. Dev vs Production Configuration](#15-dev-vs-production-configuration)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Field Notes: Poetry on the 42 Cluster](#-field-notes-poetry-on-the-42-cluster)
- [Key Constraints](#%EF%B8%8F-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🚀 About the Project

*"There is no spoon. But there are virtual environments, and they're very
real."*

This module leaves language features behind and tackles the **operational
layer** every data engineer lives in: isolated environments, dependency
management, and configuration. Three missions:

- **Entering the Matrix** (ex0) — a program that knows whether it's inside
  a virtual environment, and teaches you to build one.
- **Loading Programs** (ex1) — a pandas/numpy/matplotlib analysis tool that
  survives missing dependencies and ships with *both* pip and Poetry
  manifests.
- **Accessing the Mainframe** (ex2) — configuration through environment
  variables and `.env` files, with secrets that never touch Git.

The subject's closing line is the point: it's not making the code work —
it's understanding the **why** behind these tools.

---

## 🧠 Concepts Covered (Theory)

### 1. The Problem: One Global Python for Everything

Install every project's packages into the system Python and you get
**dependency hell**: project A needs `pandas 1.x`, project B needs
`pandas 2.x`, and the last `pip install` wins — silently breaking the
other project. Worse, on shared machines you may not even have permission
to install globally, and polluting the system interpreter can break OS
tools that depend on it. Isolation is not a luxury; it's the baseline.

### 2. Virtual Environments — the Construct

A **virtual environment** is a lightweight, self-contained directory with
its own `python` executable (a copy or symlink of a base interpreter),
its own `site-packages` (where its packages live), and its own scripts
directory (`bin/` on Unix). Created with the standard library:

```bash
python3 -m venv matrix_env
```

Packages installed inside affect **only** this environment. Delete the
folder, the environment is gone — nothing global was ever touched. One
environment per project is the norm; that's why the subject forbids
committing it: it's disposable, rebuildable from the manifest (see §6–7),
and full of machine-specific paths.

### 3. What Activation Actually Does

`source matrix_env/bin/activate` is less magical than it looks. It's a
shell script that:

1. **Prepends** `matrix_env/bin` to your `PATH` — so `python` and `pip`
   now resolve to the venv's copies first;
2. Sets the `VIRTUAL_ENV` environment variable to the env's path;
3. Tweaks your prompt (`(matrix_env) $>`), and defines `deactivate` to
   undo it all.

That's it — activation is PATH manipulation. Which means you can skip it
entirely by calling the interpreter by its full path
(`matrix_env/bin/python script.py`); the venv's Python *always* uses its
own `site-packages`, activated or not. Understanding this demystifies
`poetry run` too (§7).

### 4. Detecting a venv from Inside Python

The `sys` module carries the answer. A venv's interpreter has **two**
prefixes: `sys.prefix` points to the venv, while `sys.base_prefix` points
to the base installation it was created from. Outside a venv, they're
equal:

```python
import sys


def in_venv() -> bool:
    return sys.prefix != sys.base_prefix
```

This is the documented, canonical check — and the heart of
`construct.py`. Complementary sources: `os.environ.get("VIRTUAL_ENV")`
(set by activation — but absent if the venv's python was invoked by path,
which is why the `sys` check is more reliable), `sys.executable` (the
running interpreter's path, which visibly lives inside the env), and
`site.getsitepackages()` for the package directories (§5).

### 5. site-packages: Global vs Isolated

`site-packages` is where `pip install` actually puts packages. The
`site` module reveals the active locations:

```python
import site

site.getsitepackages()
# global : ['/usr/lib/python3.11/site-packages']
# venv   : ['/path/to/matrix_env/lib/python3.11/site-packages']
```

Displaying both realities side by side is exactly ex0's fourth
requirement — the visible proof that the construct is a separate world:
same import statement, different search path, different packages.

### 6. pip and requirements.txt

**pip** is Python's package installer; **requirements.txt** is the
conventional manifest listing what to install:

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
```

One command rebuilds the environment: `pip install -r requirements.txt`.
Version specifiers matter: `==2.1.0` pins exactly, `>=2.0` sets a floor,
`~=2.1` allows patch updates only. The file is simple and universal —
but it's *just a list*: pip installs what you wrote, resolves transitive
dependencies at install time, and records nothing about what it decided.
Reproducibility depends on how strictly you pinned (a fully-pinned
snapshot is what `pip freeze` produces).

### 7. Poetry and pyproject.toml

**Poetry** manages the whole project lifecycle around
**pyproject.toml** — the standardized (PEP 518/621) project file:

```toml
[project]
name = "loading"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "pandas>=2.0",
    "numpy>=1.24",
    "matplotlib>=3.7",
]
```

`poetry install` does three things pip doesn't do by itself: **resolves**
the full dependency graph up front (detecting conflicts before installing
anything), **locks** the exact resolved versions into `poetry.lock` (so
every machine installs byte-identical dependency sets), and **manages the
venv for you** (creating one per project; `poetry run python loading.py`
executes inside it without manual activation — see §3 for why that
works). The lock file is the reproducibility guarantee requirements.txt
only approximates.

### 8. pip vs Poetry — the Real Differences

The comparison ex1 must surface in its own output:

| | pip + requirements.txt | Poetry + pyproject.toml |
|---|---|---|
| Manifest | flat list of specs | structured project metadata |
| Resolution | per-install, best effort | full-graph resolver, upfront conflicts |
| Lock file | none (DIY via `pip freeze`) | `poetry.lock`, automatic |
| Venv handling | manual (`python -m venv`) | automatic, per project |
| Scope | installer | installer + env + build + publish |

Neither is "better" universally: pip is everywhere and zero-ceremony;
Poetry buys determinism and project management at the cost of a heavier
tool. Shipping **both** files, as the subject requires, is also real-world
practice — many projects maintain the two for different consumers.

### 9. Graceful Degradation: Optional Imports

ex1 must run **without** its dependencies and fail helpfully instead of
crashing. The idiom is import-time exception handling:

```python
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
```

The program then checks its flags, reports `[OK] / [MISSING]` per
package, prints installation instructions for both pip and Poetry, and
exits cleanly when requirements aren't met. This is why the subject
*exceptionally* tolerates flake8/mypy import errors here — static tools
can't know the import is guarded (the "mechanics to avoid those errors"
it teases include `importlib.import_module()` for fully dynamic imports,
which the linters can't flag).

### 10. Introspecting Installed Versions

The version-comparison function has two clean sources. Most packages
expose `__version__` (`pd.__version__` → `"2.1.0"`); the robust,
package-agnostic route is the standard library's metadata reader:

```python
from importlib.metadata import version, PackageNotFoundError

try:
    print(version("pandas"))
except PackageNotFoundError:
    print("pandas not installed")
```

`importlib.metadata` reads the same installation records pip writes —
which is exactly how `pip list` knows what's installed.

### 11. Environment Variables — the Mainframe's Config

**Environment variables** are key–value pairs the OS hands to every
process it spawns — configuration that lives *outside* the code. Python
reads them through `os.environ` (a dict-like view) and the safer
`os.getenv`:

```python
import os

mode = os.getenv("MATRIX_MODE", "development")   # default if unset
api_key = os.getenv("API_KEY")                    # None if unset → handle it!
```

Why config belongs here and not in code: secrets stay out of source
control, and the **same code** runs in dev and production with different
behavior — the deploy environment injects the difference. This is the
"config" factor of the twelve-factor app methodology.

### 12. .env Files and python-dotenv

Exporting ten variables by hand every session doesn't scale. A **`.env`
file** keeps development values in one place:

```
MATRIX_MODE=development
DATABASE_URL=sqlite:///local.db
API_KEY=dev-key-not-a-real-secret
LOG_LEVEL=DEBUG
ZION_ENDPOINT=http://localhost:8080
```

**python-dotenv** loads it into the process environment at startup:

```python
from dotenv import load_dotenv

load_dotenv()          # reads .env, populates os.environ
```

After `load_dotenv()`, the rest of the program uses plain `os.getenv` —
the file is invisible to the config-consuming code. The subject is
explicit: use the library, don't hand-roll a parser; the lesson is the
*workflow*, not string splitting.

### 13. Precedence: Real Environment Beats the File

By default, `load_dotenv()` **does not overwrite** variables that already
exist in the environment. That default is the feature:

```bash
MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
# .env says development — the command line wins
```

The `.env` file supplies *development defaults*; real environment
variables are *deployment overrides*. That layering is what makes the
same `oracle.py` behave differently per environment with zero code
changes — and it's the third usage example the subject demands. (An
`override=True` flag exists to invert this; knowing why the default is
the sane one is defense material.)

### 14. Secrets Hygiene: .env.example and .gitignore

The `.env` file contains secrets, so it **must never be committed**. The
professional pattern is a pair of files:

- **`.env`** — real values, listed in `.gitignore`, exists only on each
  machine;
- **`.env.example`** — same *keys*, placeholder values, committed — the
  template a teammate copies (`cp .env.example .env`) and fills in.

Why so strict? Git **remembers forever**: a secret committed once lives
in the history even after deletion, and public repos are scraped for keys
within minutes. Rotating a leaked credential is the only fix — prevention
via `.gitignore` is infinitely cheaper. Be ready to say exactly this in
review; the subject warns you'll be asked why.

### 15. Dev vs Production Configuration

`MATRIX_MODE` drives visible behavioral differences — the subject leaves
the *what* open but demands the difference be observable in output.
Classic axes: log verbosity (`DEBUG` chatter vs `ERROR`-only), data
backends (local SQLite vs production database URL), endpoints (localhost
vs real service), and error detail (full tracebacks in dev, terse
messages in prod). One codebase, many behaviors, all selected by
environment — the payoff of everything above, and the module's definition
of a pipeline that "connects to external systems safely": validated
config, helpful errors when it's missing, secrets nowhere in the code.

---

## 📂 Project Structure

```
.
├── ex0/
│   └── construct.py         # venv detection & guidance
├── ex1/
│   ├── loading.py           # pandas/numpy/matplotlib analysis + dep checks
│   ├── requirements.txt     # pip manifest
│   └── pyproject.toml       # Poetry manifest
└── ex2/
    ├── oracle.py            # dotenv-based configuration system
    ├── .env.example         # committed template (placeholder values)
    └── .gitignore           # hides .env (and friends) from Git
```

Not in the repo, by design: any `matrix_env/` (venvs are rebuilt on
demand), any real `.env`, and generated artifacts like
`matrix_analysis.png`.

---

## 📝 Exercises

| Ex | Program | Mission | Core concepts |
|----|---------|---------|---------------|
| 0 — Entering the Matrix | `construct.py` | Detect venv vs global, show interpreter/env details, print creation & activation instructions, contrast package locations | `sys.prefix` vs `sys.base_prefix`, `VIRTUAL_ENV`, `sys.executable`, `site.getsitepackages()` |
| 1 — Loading Programs | `loading.py` (+ both manifests) | numpy-generated "Matrix data" analyzed with pandas, visualized with matplotlib; survives missing deps; compares pip vs Poetry in its output | guarded imports, `importlib.metadata`, requirements.txt vs pyproject.toml + lock, version introspection |
| 2 — Accessing the Mainframe | `oracle.py` (+ `.env.example`, `.gitignore`) | Load config from env vars and `.env`, dev/prod behavioral switch, graceful handling of missing keys | `os.getenv` with defaults, `load_dotenv`, override precedence, secrets hygiene |

---

## 💻 Usage

```bash
# ── Exercise 0 ──────────────────────────────────────────
python3 ex0/construct.py                 # outside: warns + instructions
python3 -m venv matrix_env
source matrix_env/bin/activate
python3 ex0/construct.py                 # inside: env details
deactivate

# ── Exercise 1 ──────────────────────────────────────────
cd ex1/
python3 loading.py                       # no deps: report + install help

pip install -r requirements.txt         # pip path
python3 loading.py                       # → matrix_analysis.png

poetry install                           # Poetry path
poetry run python loading.py

# ── Exercise 2 ──────────────────────────────────────────
cd ex2/
python3 oracle.py                        # missing-config warnings
cp .env.example .env                     # then edit values
python3 oracle.py                        # loads from .env
MATRIX_MODE=production API_KEY=secret123 python3 oracle.py   # env wins

# ── Style & types ───────────────────────────────────────
flake8 .    # ex1 import errors exceptionally tolerated
mypy .
```

---

## 🔧 Field Notes: Poetry on the 42 Cluster

Hard-won adjustments for running this module on the school machines
(no root, disk quota, Python 3.10):

- **`package-mode = false`** under `[tool.poetry]` — this project is an
  application, not an installable package; without this, Poetry demands
  full packaging metadata (or a matching package directory) before
  installing anything.
- **`poetry config virtualenvs.in-project true`** — keeps the venv in a
  local `.venv/` instead of a hidden cache dir; easier to inspect, wipe,
  and keep inside quota.
- Pin **`requires-python = ">=3.10"`** to match the cluster interpreter —
  resolver errors about Python versions almost always trace back to this
  line.
- After editing `pyproject.toml` by hand, run **`poetry lock`** then
  `poetry install` — the lock file must be regenerated to match the
  manifest.

---

## ⚠️ Key Constraints

- Python **3.10 or later**, **flake8-clean**, fully type-annotated
  (**mypy**) — with the single sanctioned exception: import errors in ex1.
- Authorized per exercise: ex0 → `sys`, `os`, `site`; ex1 → `pandas`,
  `numpy`, `matplotlib`, `requests` (optional), `sys`, `importlib`;
  ex2 → `os`, `sys`, `python-dotenv`, file operations.
- ex1's dataset must be **generated by numpy** — no hardcoded lists, no
  `range()`.
- **Never commit**: virtual environments (rebuildable on demand) or real
  `.env` files (secrets). `.env.example` is the committed template.
- Programs must be tested in multiple environments — with/without venv,
  with/without dependencies — and behave sensibly in all of them.
- Exception handling protects every path: missing packages, missing
  config keys, missing files.

---

## 📚 Resources

- [venv — standard library](https://docs.python.org/3/library/venv.html)
- [Python docs — how venvs work (sys.prefix)](https://docs.python.org/3/library/venv.html#how-venvs-work)
- [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
- [Poetry documentation](https://python-poetry.org/docs/)
- [PEP 621 — project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [The Twelve-Factor App — Config](https://12factor.net/config)

---

## 👤 Author

**mide-fre** — student at [42 Porto](https://www.42porto.com/)
GitHub: [@mdfpva](https://github.com/mdfpva)

### 🤖 AI Usage Disclosure

AI tools were used in accordance with the 42 AI guidelines: as a support for
understanding concepts, reviewing code, and producing documentation. All
submitted solutions are my own work, fully understood and defensible during
peer evaluation.

---

<div align="center">

*Made with 💊 at 42 Porto*

</div>
