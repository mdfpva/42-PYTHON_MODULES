<div align="center">

```
   ___                _              ___         _
  / __|_ _ _____ __ _(_)_ _  __ _   / __|___  __| |___
 | (_ | '_/ _ \ V  V / | ' \/ _` | | (__/ _ \/ _` / -_)
  \___|_| \___/\_/\_/|_|_||_\__, |  \___\___/\__,_\___|
                            |___/           🌱 42 🌱
```

### 🌱 Python Fundamentals Through Garden Data 🌱

**A 42 School Project — Python Piscine, Module 0**

*Discover Python's fundamental syntax and semantics by analyzing community
garden data. Learn expressions, variables, functions, and control flow while
contributing to sustainable community initiatives.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Functions](#1-functions)
  - [2. Output with print()](#2-output-with-print)
  - [3. Variables and Dynamic Typing](#3-variables-and-dynamic-typing)
  - [4. Input with input()](#4-input-with-input)
  - [5. Type Conversion (Casting)](#5-type-conversion-casting)
  - [6. Expressions and Arithmetic Operators](#6-expressions-and-arithmetic-operators)
  - [7. Strings and f-strings](#7-strings-and-f-strings)
  - [8. Conditionals (if / elif / else)](#8-conditionals-if--elif--else)
  - [9. Comparison Operators](#9-comparison-operators)
  - [10. Loops and range()](#10-loops-and-range)
  - [11. Recursion](#11-recursion)
  - [12. Type Hints (Annotations)](#12-type-hints-annotations)
  - [13. Code Style: flake8 and PEP 8](#13-code-style-flake8-and-pep-8)
  - [14. Static Type Checking with mypy](#14-static-type-checking-with-mypy)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Testing & Linting](#-testing--linting)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🌍 About the Project

**Growing Code** is the introductory Python module of the 42 curriculum. Each
exercise is themed around a **community garden** — tracking harvests, plot
areas, watering schedules and seed inventories — and each one introduces a
fundamental building block of the Python language.

The core rule of this module: **every exercise is a single function, in its
own file** — no main program, no `if __name__ == "__main__":` blocks, no code
outside functions. A provided `main.py` helper imports and tests your
functions automatically.

> Programming, like gardening, is about nurturing growth — both in code and
> in the communities we serve. 🌿

---

## 🧠 Concepts Covered (Theory)

### 1. Functions

A **function** is a named, reusable block of code defined with the `def`
keyword. It only runs when it is *called*.

```python
def ft_hello_garden():      # definition
    print("Hello, Garden Community!")

ft_hello_garden()           # call (done by main.py, never in your file!)
```

- A function may take **parameters** (inputs) and may **return** a value.
- If no `return` statement is executed, the function implicitly returns `None`.
- In this module the functions *handle I/O directly* (they print rather than
  return), which is unusual in real-world code but keeps the focus on syntax.
- Naming convention at 42: exercise functions are prefixed with `ft_`
  ("forty-two").

**Why functions matter:** they are the smallest unit of abstraction —
they let you name a behaviour, reuse it, and test it in isolation.

### 2. Output with `print()`

`print()` writes text to **standard output** (stdout) and appends a newline
by default.

```python
print("Plot area:", 15)      # multiple args, separated by a space
print(f"Plot area: {area}")  # f-string formatting (preferred)
```

- `print()` converts its arguments to `str` automatically.
- Useful keyword arguments: `sep` (separator between args, default `" "`)
  and `end` (what to print at the end, default `"\n"`).

### 3. Variables and Dynamic Typing

A **variable** is a *name bound to an object*. Python is **dynamically
typed**: the type lives with the object, not with the name, and you never
declare types to make code run.

```python
days = 45          # int
name = "Tomato"    # str
ready = False      # bool
```

- Assignment (`=`) binds a name to a value; it is *not* mathematical equality.
- Python is also **strongly typed**: `"5" + 3` raises a `TypeError` — types
  are never silently mixed (unlike C's implicit conversions).
- Core built-in types used in this module: `int`, `str`, `bool`, `None`.

### 4. Input with `input()`

`input()` pauses the program, reads one line from **standard input**, and
returns it — **always as a `str`**, even if the user types digits.

```python
raw = input("Enter length: ")   # raw is "5" (a string!)
```

The optional argument is the *prompt* displayed before reading. Forgetting
that `input()` returns a string is the classic beginner bug — hence the next
concept.

### 5. Type Conversion (Casting)

To do arithmetic on user input you must **convert** the string to a number
using constructor functions:

```python
length = int(input("Enter length: "))   # str -> int
pi_ish = float("3.14")                  # str -> float
text = str(42)                          # int -> str
```

- `int("abc")` raises a `ValueError` — but per the subject, invalid input is
  *undefined behaviour* and does not need to be handled in this module.
- This is **explicit conversion**; Python performs almost no implicit
  conversion between unrelated types (a deliberate design choice: *"explicit
  is better than implicit"* — The Zen of Python).

### 6. Expressions and Arithmetic Operators

An **expression** is any piece of code that evaluates to a value.

| Operator | Meaning            | Example  | Result |
|----------|--------------------|----------|--------|
| `+`      | addition           | `5 + 8`  | `13`   |
| `-`      | subtraction        | `8 - 3`  | `5`    |
| `*`      | multiplication     | `5 * 3`  | `15`   |
| `/`      | true division      | `7 / 2`  | `3.5`  |
| `//`     | floor division     | `7 // 2` | `3`    |
| `%`      | modulo (remainder) | `7 % 2`  | `1`    |
| `**`     | exponentiation     | `2 ** 3` | `8`    |

Note that `/` **always** returns a `float` in Python 3, even between two
`int`s — use `//` when you need integer results.

### 7. Strings and f-strings

Strings (`str`) are **immutable** sequences of Unicode characters.

**f-strings** (formatted string literals, Python 3.6+) embed expressions
directly inside string literals:

```python
total = 16
print(f"Total harvest: {total}")   # -> Total harvest: 16
```

**String methods** return *new* strings (immutability!). The one this module
highlights is `.capitalize()`:

```python
"tomato".capitalize()   # -> "Tomato"  (first char upper, rest lower)
```

Other common ones: `.upper()`, `.lower()`, `.strip()`, `.replace()`,
`.split()`.

### 8. Conditionals (`if` / `elif` / `else`)

Conditionals let the program **branch** — execute different code depending
on a boolean condition.

```python
if age > 60:
    print("Plant is ready to harvest!")
else:
    print("Plant needs more time to grow.")
```

- Python defines blocks by **indentation** (4 spaces, per PEP 8) — there are
  no braces. Indentation is *syntax*, not style.
- `elif` chains multiple exclusive conditions; only the **first** true branch
  runs.
- Any value can be tested for *truthiness*: `0`, `""`, `None`, empty
  collections are falsy; almost everything else is truthy.

### 9. Comparison Operators

Comparisons produce a `bool` (`True` / `False`):

| Operator | Meaning              |
|----------|----------------------|
| `==`     | equal                |
| `!=`     | not equal            |
| `<` `>`  | less / greater       |
| `<=` `>=`| less/greater or equal|

⚠️ **Strictly more than 60** means `age > 60` — a plant aged exactly 60 days
is *not* ready. Reading the subject carefully around `>` vs `>=` is exactly
the kind of detail evaluators check.

Boolean operators `and`, `or`, `not` combine conditions and use
**short-circuit evaluation** (the right operand is only evaluated if needed).

### 10. Loops and `range()`

A **`for` loop** iterates over any iterable. `range(start, stop)` generates
integers from `start` up to **but not including** `stop`:

```python
for day in range(1, days + 1):   # 1, 2, ..., days
    print(f"Day {day}")
print("Harvest time!")
```

- `range(n)` counts from `0` to `n - 1`; `range(1, n + 1)` counts `1..n` —
  the classic *off-by-one* territory.
- `range` is lazy: it produces values on demand instead of building a list
  in memory.
- Python also has `while` loops (repeat while a condition holds), though this
  module's counting exercise is most natural with `for` + `range`.

### 11. Recursion

**Recursion** is a function calling itself. Every correct recursion needs:

1. a **base case** — the condition where it *stops* calling itself;
2. a **recursive step** — a call on a *smaller* subproblem that converges
   toward the base case.

```python
def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count(current: int) -> None:
        if current > days:            # base case
            return
        print(f"Day {current}")
        count(current + 1)            # recursive step

    count(1)
    print("Harvest time!")
```

- Each call gets its own **stack frame**; without a base case you hit
  `RecursionError` (Python's default recursion limit is ~1000 frames).
- The subject accepts three idioms: a **nested helper** (above), **default
  parameter values**, or a **separate helper function**.
- Iteration and recursion are equivalent in expressive power — this exercise
  makes you write *both* to internalize that.

### 12. Type Hints (Annotations)

**Type hints** (PEP 484) annotate the *expected* types of parameters and
return values:

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    ...
```

- `-> None` documents that the function returns nothing meaningful.
- Hints are **not enforced at runtime** — Python stays dynamic. They exist
  for humans, IDEs, and static analysis tools like `mypy`.
- Optional in exercises 0–6, **mandatory in exercise 7** — and mandatory in
  every later Python module of the curriculum, so build the habit now.

### 13. Code Style: flake8 and PEP 8

**PEP 8** is Python's official style guide; **flake8** is the linter that
enforces it (plus detecting some logical errors, via pyflakes).

Key rules you will hit in this module:

- 4-space indentation, no tabs;
- max line length **79 characters**;
- two blank lines before top-level `def`s;
- no unused imports or variables;
- spaces around operators (`a + b`, not `a+b`).

```bash
pip install flake8
flake8 ex0/ ex1/ ex2/ ...     # zero output = zero errors
```

Style is graded at 42: **norm-clean code is part of the deliverable**, just
like norminette in the C projects.

### 14. Static Type Checking with mypy

**mypy** reads your type hints and verifies type consistency *without running
the code*:

```bash
pip install mypy
mypy ex7/ft_seed_inventory.py
# Success: no issues found in 1 source file
```

It catches, at "compile time", bugs like passing a `str` where an `int` is
expected. Together, `flake8` (style) + `mypy` (types) form the quality
baseline used across the whole 42 Python branch.

---

## 📂 Project Structure

```
growing_code/
├── ex0/
│   └── ft_hello_garden.py          # print()
├── ex1/
│   └── ft_garden_name.py           # input() + print()
├── ex2/
│   └── ft_plot_area.py             # int(), arithmetic
├── ex3/
│   └── ft_harvest_total.py         # accumulation
├── ex4/
│   └── ft_plant_age.py             # if / else
├── ex5/
│   └── ft_water_reminder.py        # conditionals
├── ex6/
│   ├── ft_count_harvest_iterative.py   # for + range()
│   └── ft_count_harvest_recursive.py   # recursion
└── ex7/
    └── ft_seed_inventory.py        # type hints, string methods
```

---

## 🌾 Exercises

| Ex  | Function(s) | Authorized | Concepts |
|-----|-------------|------------|----------|
| 0 | `ft_hello_garden` | `print()` | Functions, output |
| 1 | `ft_garden_name` | `input()`, `print()` | Standard input, fixed messages |
| 2 | `ft_plot_area` | `input()`, `int()`, `print()` | Casting, multiplication |
| 3 | `ft_harvest_total` | `input()`, `int()`, `print()` | Accumulating a sum |
| 4 | `ft_plant_age` | `input()`, `int()`, `print()` | `if`/`else`, strict comparison (`> 60`) |
| 5 | `ft_water_reminder` | `input()`, `int()`, `print()` | Conditionals (`> 2` days) |
| 6 | `ft_count_harvest_iterative` / `_recursive` | + `range()`, helper functions | Loops **vs** recursion |
| 7 | `ft_seed_inventory` | `print()`, string methods | Type hints, `.capitalize()`, unit dispatch |

**Exercise 7 output contract:**

```
"packets" -> "<Seed> seeds: <n> packets available"
"grams"   -> "<Seed> seeds: <n> grams total"
"area"    -> "<Seed> seeds: covers <n> square meters"
other     -> "Unknown unit type"        (nothing else on the line)
```

---

## 🚀 Usage

Every file contains **only** the requested function. To test, copy the
provided `main.py` helper next to your exercise files and run:

```bash
python3 main.py
```

The helper imports your functions and lets you test each exercise
interactively. Example session:

```
>>> ft_plot_area()
Enter length: 5
Enter width: 3
Plot area: 15
```

---

## ✅ Testing & Linting

```bash
# Style check (must be clean on every file)
flake8 .

# Type check (required for ex7)
mypy ex7/ft_seed_inventory.py
```

---

## ⚠️ Key Constraints

- Python **3.10+**.
- **flake8-clean** code across all exercises.
- One exercise per file; the file contains **only** the requested function.
- **No** `if __name__ == "__main__":`, no top-level code, no direct calls.
- Function names must match the subject **exactly**.
- Invalid/negative input = undefined behaviour (no validation required).
- Type hints: recommended ex0–ex6, **required** ex7.

---

## 📚 Resources

- [Python official tutorial](https://docs.python.org/3/tutorial/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)

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
