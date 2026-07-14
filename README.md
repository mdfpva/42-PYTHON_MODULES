<div align="center">

```
 _ _ ___   ___      _   _
| | |_  ) | _ \_  _| |_| |_  ___ _ _
|_  _/ /  |  _/ || |  _| ' \/ _ \ ' \
  |_/___| |_|  \_, |\__|_||_\___/_||_|
               |__/
```

🐍 42 🐍

### The Python Branch of the 42 Curriculum — Eleven Modules, One Language

**From first `print()` to decorators, design patterns, and Pydantic —
a complete, peer-reviewed journey through modern Python at 42 Porto.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Style](https://img.shields.io/badge/style-flake8%20%2F%20PEP%208-blueviolet)
![Types](https://img.shields.io/badge/types-mypy%20%2B%20full%20hints-2A6DB2)
![Validation](https://img.shields.io/badge/data-Pydantic%202.x-E92063)
![School](https://img.shields.io/badge/school-42%20Porto-black)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [The Modules](#-the-modules)
- [Skills Demonstrated](#-skills-demonstrated)
- [About 42](#-about-42)
- [Repository Layout](#-repository-layout)
- [Getting Started](#-getting-started)
- [Quality Standards](#-quality-standards)
- [AI Usage Disclosure](#-ai-usage-disclosure)
- [Author](#-author)

---

## 🔭 Overview

This repository contains my complete work for the **Python branch of the 42
curriculum**: eleven self-contained modules that progress from the language's
fundamentals to advanced software design — object-oriented and functional
paradigms, exception-safe data pipelines, Python's import system, design
patterns, professional tooling with Poetry, and data validation with
Pydantic 2.x.

Every module was **defended in front of peers** in 42's evaluation system,
which means each concept here isn't just implemented — it's explained,
questioned, and justified line by line. To support that, **each module folder
ships its own in-depth README**: a numbered theory section covering every
concept the module teaches (typically 14–16 topics), written to
evaluation-level depth, plus the exercise breakdown, constraints, and usage.

If you're reviewing this as a recruiter or fellow developer: start with the
[module table](#-the-modules) below, then open any module's README — that's
where the depth lives.

---

## 🗺️ The Modules

Each module is a themed set of progressive exercises. Click a module to open
its folder and full README.

| # | Module | Focus | Key concepts |
|:-:|--------|-------|--------------|
| 00 | [🌱 Growing Code](./00) | **Python Fundamentals** | Variables & dynamic typing, functions, control flow, loops & recursion, f-strings, type hints, PEP 8 |
| 01 | [🌿 Code Cultivation](./01) | **Object-Oriented Programming** | Classes & instances, attributes and methods, inheritance, encapsulation, properties, dunder methods |
| 02 | [🛡️ Garden Guardian](./02) | **Exception Handling** | `try`/`except`/`else`/`finally`, raising, custom exception hierarchies, building resilient data pipelines |
| 03 | [🎮 DataQuest](./03) | **Collections** | Lists, dicts, sets & tuples, comprehensions, iteration patterns, choosing the right structure for the job |
| 04 | [🗄️ Data Archivist](./04) | **File I/O** | `open()` & context managers, text vs binary modes, JSON/CSV handling, safe data persistence |
| 05 | [🌐 Code Nexus](./05) | **Polymorphism & Abstraction** | Abstract base classes, method overriding, subtype polymorphism, duck typing, polymorphic data streams |
| 06 | [🧪 The Codex](./06) | **Imports & Packages** | Modules vs packages, `__init__.py` and public interfaces, absolute vs relative imports, circular-import resolution, `sys.modules` |
| 07 | [🃏 DataDeck](./07) | **Design Patterns** | Interfaces via ABCs, composition, extensible architecture — a modular card system built on abstract contracts |
| 08 | [💊 The Matrix](./08) | **Environment & Tooling** | Virtual environments, **Poetry**, dependency management, project packaging, reproducible setups (incl. real 42-cluster field notes) |
| 09 | [🪐 Cosmic Data](./09) | **Data Validation** | **Pydantic 2.x** models, fields & validators, typed parsing, precise error reporting |
| 10 | [🧙 FuncMage](./10) | **Functional Programming** | Lambdas, higher-order functions, closures & lexical scoping, `functools` (`reduce`, `partial`, `lru_cache`, `singledispatch`), decorators |

**The arc:** fundamentals → object-oriented design → robustness → data
handling → architecture (imports, patterns) → professional tooling →
validation → functional programming. By module 10, the same language looks
completely different than it did in module 00.

---

## 💼 Skills Demonstrated

- **Idiomatic modern Python** — Python 3.10+, full type-hint coverage on
  every signature, comfort across both object-oriented and functional
  paradigms.
- **Software design** — abstraction with ABCs and interfaces, composition,
  design patterns, clean import architecture and package interfaces,
  separation of concerns via decorators.
- **Robustness & data integrity** — deliberate exception design, defensive
  pipelines that protect data streams, schema-level validation with
  Pydantic 2.x.
- **Data handling** — collections and comprehensions, file formats
  (JSON/CSV), stream processing, stateful computation without global state
  (closures).
- **Engineering practice** — flake8/PEP 8 compliance and mypy static
  checking across the codebase, dependency management with Poetry, Git-based
  submission, and self-testing scripts (`python3 <exercise>.py` demonstrates
  each requirement).
- **Communication** — every module documented to teaching depth; every
  project defended and explained in peer evaluations.

---

## 🎓 About 42

[42](https://www.42porto.com/) is a tuition-free, project-based programming
school with **no teachers and no classes**. Learning happens through
hands-on projects and **peer-to-peer evaluation**: every submission is
defended in front of other students, who probe the code and the reasoning
behind it. You don't pass by making it work — you pass by *understanding
why* it works.

This repository is my work from the Python branch at **42 Porto**, completed
on the school's Linux clusters under its constraints (strict subjects,
authorized-function lists, and peer review of every module).

---

## 🗂️ Repository Layout

```
42-PYTHON_MODULES/
├── 00/   Growing Code       — Python fundamentals
├── 01/   Code Cultivation   — OOP foundations
├── 02/   Garden Guardian    — Exception handling
├── 03/   DataQuest          — Collections
├── 04/   Data Archivist     — File I/O
├── 05/   Code Nexus         — Polymorphism & abstraction
├── 06/   The Codex          — Imports & packages
├── 07/   DataDeck           — Design patterns
├── 08/   The Matrix         — Environment & tooling (Poetry)
├── 09/   Cosmic Data        — Pydantic data validation
├── 10/   FuncMage           — Functional programming
└── README.md                — you are here
```

Inside each module:

```
XX/
├── README.md          # full theory (14–16 concepts) + exercise guide
├── ex0/ … exN/        # progressive exercises, one concept at a time
└── ...                # module-specific helpers or testers
```

---

## ⚙️ Getting Started

```bash
git clone https://github.com/mdfpva/42-PYTHON_MODULES.git
cd 42-PYTHON_MODULES

# Pick a module and read its README first
cd 10 && cat README.md

# Every exercise is a self-testing script
python3 ex0/lambda_spells.py

# Lint any module the way the subjects require
flake8 .
```

No external dependencies are required to run the exercises — the subjects
forbid third-party libraries except where the module *is about* them
(Pydantic in `09/`, Poetry in `08/`).

---

## 📏 Quality Standards

Every module in this repository follows the same bar, enforced by the 42
subjects and checked at evaluation:

- **Python 3.10+** and **flake8 (PEP 8)** compliance throughout.
- **Type hints on every function signature and return type**; mypy-checked
  where the subject requires it.
- **No global variables** — state lives in objects or closures, never in
  module scope.
- **Exception handling as a design tool**, not an afterthought: data streams
  are protected from corruption at every boundary.
- **Exact naming and structure** as specified by each subject — evaluated
  down to the filename.
- **Self-demonstrating code**: running any exercise file shows the required
  behavior from an `if __name__ == "__main__":` block, while the functions
  stay importable and pure for review.

---

## 🤖 AI Usage Disclosure

In line with 42's AI guidelines, AI assistance (Anthropic's Claude) was used
across these modules for **documentation** (structuring the module READMEs)
and for **discussing and clarifying theory**. All submitted solutions are my
own work, fully understood and defended in peer evaluations.

---

## 👤 Author

**Miguel** — student at [42 Porto](https://www.42porto.com/)

- 🐙 GitHub: [@mdfpva](https://github.com/mdfpva)
- 🎓 42 intra: `mide-fre`
<!-- - 💼 LinkedIn: add your profile URL here -->

*If you're hiring for Python roles or just want to talk shop about any
module in here — my inbox is open.*

---

<div align="center">

*Made with 🐍 at 42 Porto*

</div>
