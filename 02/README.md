<div align="center">

```
  ___             _            ___                  _ _
 / __|__ _ _ _ __| |___ _ _   / __|_  _ __ _ _ _ __| (_)__ _ _ _
| (_ / _` | '_/ _` / -_) ' \ | (_ | || / _` | '_/ _` | / _` | ' \
 \___\__,_|_| \__,_\___|_||_| \___|\_,_\__,_|_| \__,_|_\__,_|_||_|
                                                 🌱 42 🌱
```

### 🛡️ Data Engineering for Smart Agriculture 🛡️

**A 42 School Project — Python Piscine, Exception Handling Module**

*Build resilient data pipelines for your smart garden! Learn to handle
sensor failures, process agricultural data streams, and create robust
monitoring systems that keep your digital greenhouse thriving.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. What Is an Exception?](#1-what-is-an-exception)
  - [2. `try` / `except`: Catching Errors](#2-try--except-catching-errors)
  - [3. The Exception Object (`as e`)](#3-the-exception-object-as-e)
  - [4. Raising Exceptions (`raise`)](#4-raising-exceptions-raise)
  - [5. Built-in Exception Types](#5-built-in-exception-types)
  - [6. The Exception Hierarchy](#6-the-exception-hierarchy)
  - [7. Catching Multiple Exception Types](#7-catching-multiple-exception-types)
  - [8. Custom Exceptions](#8-custom-exceptions)
  - [9. Exception Hierarchies of Your Own](#9-exception-hierarchies-of-your-own)
  - [10. The `finally` Block](#10-the-finally-block)
  - [11. Resource Cleanup and the Try/Finally Pattern](#11-resource-cleanup-and-the-tryfinally-pattern)
  - [12. EAFP vs LBYL](#12-eafp-vs-lbyl)
  - [13. Defensive Programming: "Never Crash"](#13-defensive-programming-never-crash)
  - [14. Type Hints with Exceptions](#14-type-hints-with-exceptions)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Testing & Linting](#-testing--linting)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🌍 About the Project

**Garden Guardian** is the exception handling module of the 42 Python
branch. Framed as *agricultural data engineering* — sensors that transmit
garbage, watering systems that must always shut down, temperature readings
outside plant-survivable ranges — it covers the full Python error-handling
toolkit: `try`/`except`/`finally`, `raise`, built-in exception types, and
custom exception hierarchies.

The golden rule of the module, straight from the subject: **your programs
must never crash.** Robust systems aren't built to avoid failures — they're
designed to *gracefully handle the unexpected*.

---

## 🧠 Concepts Covered (Theory)

### 1. What Is an Exception?

An **exception** is an object that signals *"something exceptional happened
and normal execution cannot continue here."* When Python hits an error —
`int("abc")`, `1 / 0`, opening a missing file — it **raises** an exception:
normal flow stops immediately and the exception *propagates* up the call
stack, function by function, until either:

1. some `try/except` block **catches** it, or
2. it reaches the top → Python prints a **traceback** and the program
   **crashes**.

Exceptions therefore separate the *happy path* from *error handling*: the
code that detects a problem (deep inside a pipeline) doesn't have to be the
code that decides what to do about it (up at the caller).

### 2. `try` / `except`: Catching Errors

```python
try:
    temp = int(temp_str)          # code that MIGHT fail
except ValueError:
    print("Caught input_temperature error: bad reading")
# execution continues here — the program did NOT crash
```

- The `try` block runs normally **until** an exception occurs; the rest of
  the block is skipped.
- Python then looks for the first `except` clause matching the exception
  type; that handler runs, and execution continues *after* the whole
  `try/except` statement.
- If nothing in the `try` fails, all `except` clauses are skipped.
- Catch the **most specific** type you can. A bare `except Exception:`
  works (ex0 explicitly allows it) but hides bugs — knowing *which* error
  you expect is part of understanding your code.

### 3. The Exception Object (`as e`)

The exception carries information — most importantly its **message**:

```python
try:
    temp = int("abc")
except ValueError as e:
    print(f"Caught input_temperature error: {e}")
    # -> invalid literal for int() with base 10: 'abc'
```

`as e` binds the exception *instance* to a name. Converting it to `str`
yields the human-readable message. This is exactly what the module's
expected outputs show — the original error text, forwarded by *your*
handler. You report the failure; you don't invent it.

### 4. Raising Exceptions (`raise`)

You are not limited to catching — you can **signal errors yourself**:

```python
def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)                     # may raise ValueError itself
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    return temp
```

- `raise SomeError("message")` creates the exception and throws it.
- This turns *domain rules* ("plants live between 0 and 40 °C") into the
  **same failure channel** as built-in errors — the caller handles both
  with one mechanism. That's the ex1 insight: a value can be a perfectly
  valid `int` and still be *invalid data* for your domain.
- A function that raises **stops immediately** — nothing after the `raise`
  executes, and it never returns a value.

### 5. Built-in Exception Types

Python ships with dozens of precise error types. The ones this module
exercises (ex2 makes you trigger each on purpose):

| Exception | Raised when... | Trigger example |
|-----------|----------------|-----------------|
| `ValueError` | right type, wrong value | `int("abc")` |
| `ZeroDivisionError` | dividing by zero | `1 / 0` |
| `FileNotFoundError` | opening a missing file | `open("/non/existent/file")` |
| `TypeError` | incompatible types mixed | `"str" + 1` |
| `KeyError` | missing dict key | `d["nope"]` |
| `IndexError` | sequence index out of range | `lst[99]` |
| `AttributeError` | missing attribute/method | `None.foo` |

Different types exist so handlers can **react differently** to different
problems — retry on a network error, reject on bad data, create on a
missing file. One generic "error" type would make that impossible.

### 6. The Exception Hierarchy

Exceptions are **classes**, organized in an inheritance tree:

```
BaseException
 └── Exception
      ├── ValueError
      ├── TypeError
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── OSError
      │    └── FileNotFoundError
      ├── LookupError
      │    ├── KeyError
      │    └── IndexError
      └── ...
```

The rule that makes everything click: **`except X` catches `X` and every
subclass of `X`.** That's why `except Exception:` catches (almost)
everything, and why `except OSError:` also catches `FileNotFoundError`.
(`BaseException` also covers `KeyboardInterrupt` and `SystemExit` — which is
why you catch `Exception`, not `BaseException`.)

### 7. Catching Multiple Exception Types

Two tools, two meanings:

```python
# (a) Different reactions -> separate except clauses
try:
    garden_operations(n)
except ValueError as e:
    print(f"Caught ValueError: {e}")
except ZeroDivisionError as e:
    print(f"Caught ZeroDivisionError: {e}")

# (b) Same reaction -> one clause, a TUPLE of types
try:
    garden_operations(n)
except (ValueError, TypeError) as e:
    print(f"Caught bad data: {e}")
```

The first matching clause wins, so **order matters**: put subclasses before
their parents, or the parent clause swallows everything. The subject's hint
"you can't use `type()`" points here — you distinguish errors by *which
clause catches them* (or via the hierarchy), not by inspecting types
manually.

### 8. Custom Exceptions

When built-ins aren't specific enough, define your own — an exception is
just a class inheriting from `Exception`:

```python
class GardenError(Exception):
    """Base error for garden problems."""

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)
```

- Inheriting from `Exception` is what makes the class *raisable* and
  *catchable*.
- A **default message** in `__init__` (forwarded via
  `super().__init__(message)`) means `raise GardenError()` still produces
  something meaningful.
- Custom names turn tracebacks and handlers into documentation:
  `except WaterError:` says exactly what situation is being handled.

### 9. Exception Hierarchies of Your Own

This is where the OOP module pays off — **inheritance organizes errors**:

```python
class GardenError(Exception): ...          # base

class PlantError(GardenError): ...         # specialization
class WaterError(GardenError): ...         # specialization
```

Because `except X` catches subclasses:

- `except PlantError:` → only plant problems;
- `except GardenError:` → *any* garden problem (`PlantError` **and**
  `WaterError`), while unrelated errors (`ValueError`...) still propagate.

This mirrors how real libraries design their APIs (e.g. `requests` has one
base `RequestException`): callers choose their **granularity** — handle one
precise failure, or the whole family with a single clause.

### 10. The `finally` Block

`finally` attaches a block that runs **no matter what**:

```python
try:
    water_plant("Tomato")
    water_plant("lettuce")     # raises PlantError
except PlantError as e:
    print(f"Caught PlantError: {e}")
    return                     # even returning...
finally:
    print("Closing watering system")   # ...this STILL runs
```

`finally` executes on success, on a caught exception, on an *uncaught*
exception (just before it propagates), and even when the `try` or `except`
block hits a `return` — the ex4 case, worth internalizing: **the `finally`
runs between the `return` statement and the actual function exit.**

There is also an optional `else:` clause (runs only if *no* exception
occurred), completing the full form `try/except/else/finally`.

### 11. Resource Cleanup and the Try/Finally Pattern

The canonical use of `finally` is **releasing resources** — files, locks,
network connections, or a garden watering system:

```python
def test_watering_system() -> None:
    print("Opening watering system")       # acquire
    try:
        for plant in ("Tomato", "lettuce", "Carrots"):
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")   # ALWAYS release
```

A resource left open after a crash is a leak: the file stays locked, the
valve stays open, the greenhouse floods. `try/finally` guarantees the
release is coupled to the acquisition. (Python's idiomatic evolution of
this pattern is the `with` statement / context managers — coming in a later
module; `finally` is the mechanism they're built on.)

### 12. EAFP vs LBYL

Two philosophies for dealing with things that can fail:

- **LBYL** — *Look Before You Leap*: check preconditions first
  (`if temp_str.isdigit(): ...`).
- **EAFP** — *Easier to Ask Forgiveness than Permission*: just try it and
  handle the exception (`try: int(temp_str) except ValueError: ...`).

Python culture strongly favors **EAFP**: it avoids duplicated logic, has no
race window between "check" and "use", and the error path is explicit. This
whole module is EAFP training — you *attempt* the conversion, the division,
the file open, and you *handle* the failure.

### 13. Defensive Programming: "Never Crash"

The module's contract — *your programs must never crash* — is a design
stance, not just a grading rule:

- every entry point (`main`, each `test_*()` function) runs to completion
  and prints its final line, whatever inputs did;
- errors are **contained** where they can be handled, and **reported**
  clearly (which error, which input, what it means);
- error paths are *demonstrated*, not just possible — each exercise shows
  the failure happening and the program surviving it.

One deliberate subtlety (ex2): the code that triggers the `TypeError` is a
*known* type error — **mypy will flag it, and the subject says to keep it
on purpose**. Static analysis catches what it can at "compile time";
exception handling covers what only happens at runtime. You need both, and
you need to know which tool owns which failure.

### 14. Type Hints with Exceptions

Exceptions are **invisible to the type system** — a signature says what a
function *returns*, not what it may *raise*:

```python
def input_temperature(temp_str: str) -> int:   # may raise ValueError — not shown
    ...

def test_temperature() -> None:                # handles everything, returns nothing
    ...
```

- A function that returns a value *or raises* is typed by its success path
  (`-> int`); the raise simply means "no value came back this time".
- Documenting *what* a function raises belongs in its docstring, not the
  signature.
- The subject's note "it's up to you to properly adjust the type hints" is
  about exactly this discipline — and it applies to all upcoming projects.

---

## 📂 Project Structure

```
garden_guardian/
├── ex0/
│   └── ft_first_exception.py   # first try/except, program survives bad data
├── ex1/
│   └── ft_raise_exception.py   # raise: domain validation (0–40°C)
├── ex2/
│   └── ft_different_errors.py  # 4 built-in error types, multi-catch
├── ex3/
│   └── ft_custom_errors.py     # GardenError / PlantError / WaterError
└── ex4/
    └── ft_finally_block.py     # try/except/finally, guaranteed cleanup
```

---

## 🌾 Exercises

| Ex  | File | Authorized | Concepts |
|-----|------|------------|----------|
| 0 | `ft_first_exception.py` | `int()`, `print()` | `try`/`except`, exception message via `as e`, program keeps running |
| 1 | `ft_raise_exception.py` | `int()`, `print()` | `raise`, domain validation (0–40 °C inclusive), extreme-value tests |
| 2 | `ft_different_errors.py` | `print()`, `open()`, `int()` | `ValueError`, `ZeroDivisionError`, `FileNotFoundError`, `TypeError`; separate & combined catches |
| 3 | `ft_custom_errors.py` | `print()` | Custom exception classes, inheritance, default messages, catching the base class |
| 4 | `ft_finally_block.py` | `print()`, `str.capitalize()` | `finally`, cleanup on success/failure/`return`, reuse of `PlantError` |

**Progression logic:** ex0 *catches*, ex1 *raises*, ex2 *distinguishes*,
ex3 *designs* its own error types, ex4 *guarantees cleanup*. Together they
form the complete lifecycle of an exception: born (`raise`), classified
(type hierarchy), handled (`except`), and survived (`finally`).

---

## 🚀 Usage

Every exercise is a standalone program with its tests called from the
`__main__` block:

```bash
python3 ex1/ft_raise_exception.py
```

```
=== Garden Temperature Checker ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)
...
All tests completed - program didn't crash!
```

---

## ✅ Testing & Linting

```bash
# Style
flake8 .

# Types — note: ex2 keeps ONE intentional type error ("str" + int)
# so the TypeError can actually be raised at runtime; mypy flagging
# it is expected and documented by the subject.
mypy ex0/ ex1/ ex3/ ex4/
mypy ex2/    # expected: 1 error on the deliberate TypeError line
```

---

## ⚠️ Key Constraints

- Python **3.10+**, flake8-clean, **type hints on every function** (mypy).
- Each exercise in its own file; **programs must never crash**.
- Show **both** normal operation and error scenarios in every demo.
- ex1: valid range is 0–40 °C, **limits included** — `0` and `40` pass.
- ex2: `garden_operations(n)` raises a different error for n = 0..3; other
  values simply return. The `TypeError` line is intentionally left in
  despite mypy (see above). No need to `close()` a file that never opened.
- ex3: `PlantError` and `WaterError` inherit from `GardenError`; each class
  has a default message; demo must show `except GardenError` catching both.
- ex4: on invalid plant, stop and return to `main` — the `finally` must
  still print "Closing watering system".
- Be ready to explain: how one `try` catches multiple types (no `type()`),
  why hierarchies help, why `finally` runs even on `return`.

---

## 📚 Resources

- [Errors and Exceptions — official tutorial](https://docs.python.org/3/tutorial/errors.html)
- [Built-in exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
- [`raise` statement reference](https://docs.python.org/3/reference/simple_stmts.html#raise)
- [EAFP — Python glossary](https://docs.python.org/3/glossary.html#term-EAFP)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

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

*Made with 🌱 at 42 Porto*

</div>
