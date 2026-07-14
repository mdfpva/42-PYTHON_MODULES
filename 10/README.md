<div align="center">

```
 ___             __  __
| __|  _ _ _  __|  \/  |__ _ __ _ ___
| _| || | ' \/ _| |\/| / _` / _` / -_)
|_| \_,_|_||_\__|_|  |_\__,_\__, \___|
                            |___/
```

🧙 42 🧙

### ⚡ Ancient Arts of Functional Programming ⚡

**A 42 School Project — Python Piscine, Functional Programming Module**

*In the year 2142, the Lambda Codex lies scattered across five mystical
realms. Master lambda expressions, higher-order functions, closures,
functools artifacts, and decorators to reunite its fragments.*

`Version 3.2` · `Python 3.10+` · `flake8 compliant` · `fully type-hinted`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Functional Programming: The Paradigm](#1-functional-programming-the-paradigm)
  - [2. Functions as First-Class Citizens](#2-functions-as-first-class-citizens)
  - [3. Lambda Expressions](#3-lambda-expressions)
  - [4. Key Functions: sorted, min, max](#4-key-functions-sorted-min-max)
  - [5. map and filter: Lazy Iterators](#5-map-and-filter-lazy-iterators)
  - [6. Higher-Order Functions](#6-higher-order-functions)
  - [7. Callable and callable()](#7-callable-and-callable)
  - [8. Lexical Scoping and the LEGB Rule](#8-lexical-scoping-and-the-legb-rule)
  - [9. Closures](#9-closures)
  - [10. nonlocal vs global](#10-nonlocal-vs-global)
  - [11. functools.reduce and the operator Module](#11-functoolsreduce-and-the-operator-module)
  - [12. Partial Application with functools.partial](#12-partial-application-with-functoolspartial)
  - [13. Memoization with functools.lru_cache](#13-memoization-with-functoolslru_cache)
  - [14. Type Dispatch with functools.singledispatch](#14-type-dispatch-with-functoolssingledispatch)
  - [15. Decorators and functools.wraps](#15-decorators-and-functoolswraps)
  - [16. Decorator Factories, Methods and staticmethod](#16-decorator-factories-methods-and-staticmethod)
- [Project Structure](#-project-structure)
- [The Five Realms (Exercises)](#-the-five-realms-exercises)
- [Usage](#-usage)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [AI Usage Disclosure](#-ai-usage-disclosure)

---

## 🔮 About the Project

In the year 2142, the digital realm is in chaos. The **Lambda Codex** — a
legendary artifact holding the secrets of **higher-order functions**,
**decorators**, and **lexical scoping** — has been scattered across five
mystical realms, and only a Function Mage can reunite its fragments.

Behind the lore, this module is the Python Piscine's deep dive into
**functional programming**: treating functions as data, composing behavior
instead of duplicating it, capturing state in closures instead of globals,
and wrapping cross-cutting concerns (timing, validation, retries) around any
function with decorators. It builds directly on the fundamentals, OOP, and
exception-handling modules that precede it — the goal here is not new syntax
for its own sake, but a new way of *thinking* about code: **functions are
first-class citizens**, and once you internalize that, entire categories of
duplication disappear.

Each exercise ships as a single self-testing file: running
`python3 <file>.py` demonstrates the required behavior (from a
`if __name__ == "__main__":` block), while the functions themselves remain
pure and importable for peer review.

---

## 🧠 Concepts Covered (Theory)

### 1. Functional Programming: The Paradigm

Functional programming (FP) models computation as the **evaluation of
functions** rather than a sequence of state mutations. Its pillars:

- **Pure functions** — same inputs always produce the same output, with no
  side effects (no prints, no mutation of shared state, no I/O).
- **Immutability** — data is transformed into *new* values rather than
  edited in place.
- **Composition** — small functions are combined into bigger ones, like
  chaining spells.

Python is **multi-paradigm**: it is not a pure functional language (it has
mutable state everywhere), but it borrows FP's best tools — first-class
functions, `map`/`filter`, closures, `functools`. This is exactly why the
subject forbids **global variables**: hidden shared state is the antithesis
of functional purity, making code untestable and unpredictable. Every
exercise in this module replaces state you would normally put in a global or
an attribute with either *pure transformation* (ex0/ex1) or *encapsulated
closure state* (ex2).

### 2. Functions as First-Class Citizens

In Python, a function is an **object** like any other. It can be:

```python
def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"

restore = heal              # assigned to a variable (same object!)
grimoire = {"heal": heal}   # stored in a data structure
def use(spell): ...         # passed as an argument
def make_spell(): ...       # returned from another function
```

🛡️ **Defense question (from the subject):** *"What makes functions
first-class citizens in Python?"* — Precisely this: they can be assigned,
passed, returned, and stored, because `def` just binds a *name* to a
*function object*. Note that `restore is heal` returns `True`: assignment
creates an alias, not a copy. Everything in this module — higher-order
functions, closures, decorators — is a consequence of this single fact.

### 3. Lambda Expressions

A lambda is an **anonymous function** limited to a single expression:

```python
lambda a: a["power"]          # takes a dict, returns its power
lambda x, y: x + y            # multiple parameters are fine
```

- The expression's value is implicitly returned — no `return` keyword.
- No statements allowed (`if`/`for`/`while` blocks, assignments) — only
  expressions (conditional expressions `x if c else y` are OK).
- No type annotations — which is why the subject only requires hints on
  `def` signatures.

**When lambda vs `def`?** Lambdas shine as short, throwaway functions passed
*inline* — sort keys, `map`/`filter` transforms. Use `def` when the function
needs a name for reuse, a docstring, multiple statements, or a readable
traceback.

🛡️ **Defense nugget:** flake8 raises **E731** (*"do not assign a lambda
expression, use a def"*) if you write `f = lambda x: x + 1`. That is not a
contradiction with ex0's "lambdas only" rule — the point of ex0 is to use
lambdas **inline** inside `sorted`/`map`/`filter`, never to give them names.

### 4. Key Functions: sorted, min, max

`sorted()`, `min()`, and `max()` accept a `key=` function that is applied to
each element to produce the comparison value:

```python
sorted(artifacts, key=lambda a: a["power"], reverse=True)   # descending
strongest = max(mages, key=lambda m: m["power"])
```

🛡️ **Defense nugget:** with `key=`, `min`/`max` return the **element**, not
the key value — `strongest` above is the whole mage dict, so the power level
is `strongest["power"]`. For an average, combine authorized builtins:

```python
avg = round(sum(map(lambda m: m["power"], mages)) / len(mages), 2)
```

Also worth knowing: `sorted()` returns a **new list** (the original is
untouched — functional style), and Python's sort is **stable** (equal keys
keep their relative order).

### 5. map and filter: Lazy Iterators

```python
result = map(lambda s: f"* {s} *", ["fireball", "heal"])
print(result)        # <map object at 0x...>  — nothing computed yet!
print(list(result))  # ['* fireball *', '* heal *']
print(list(result))  # []  — the iterator is exhausted
```

- `map(func, iterable)` applies `func` to every element.
- `filter(pred, iterable)` keeps elements where `pred(elem)` is truthy.
- In Python 3 both return **lazy iterators**: values are produced on demand,
  in a single pass. To return a `list[...]` as the signatures require, wrap
  them in `list()`.

🛡️ **Defense nugget:** laziness is a feature — `map` over a million items
costs nothing until consumed, and can be chained without intermediate lists.
The classic evaluator trap is printing a `map` object and consuming an
iterator twice. (List comprehensions are often considered more pythonic, but
this realm explicitly trains the `map`/`filter` idiom.)

### 6. Higher-Order Functions

A **higher-order function (HOF)** takes one or more functions as arguments
and/or returns a function. `map`, `filter`, and `sorted` are built-in HOFs;
ex1 has you build your own. The universal shape:

```python
def loud(spell: Callable[[str, int], str]) -> Callable[[str, int], str]:
    def wrapper(target: str, power: int) -> str:
        return spell(target, power).upper() + "!!!"
    return wrapper
```

The outer function *configures*; the inner function *executes later*. Because
every spell shares the same contract `(target: str, power: int) -> str`,
spells become interchangeable building blocks: you can combine two into one,
pre-transform their arguments (amplify power), gate them behind a condition,
or run a whole list in sequence — all **without touching the original
functions**.

🛡️ **Defense question (from the subject):** *"How do HOFs enable code reuse
and composition?"* — Instead of writing `loud_heal`, `loud_fireball`,
`loud_shield`… you write `loud` **once** and apply it to any spell. Behavior
becomes a value you pass around.

### 7. Callable and callable()

Two related but different tools:

```python
from collections.abc import Callable   # ✅ the recommended import

def spell_sequence(spells: list[Callable[[str, int], str]]) -> Callable: ...
```

- **`Callable`** is a *type hint*: `Callable[[ArgType1, ArgType2], ReturnType]`
  describes the contract of a function-shaped parameter.
- **`callable(obj)`** is a *built-in function*: returns `True` if `obj` can
  be called with `()` — functions, lambdas, classes, and any instance
  defining `__call__`. Useful for validating inputs before invoking them.

🛡️ **Defense question (from the subject):** *"From which package is it
recommended to use Callable?"* — **`collections.abc`**. Since Python 3.9
(PEP 585), the standard ABCs support subscripting directly, and
`typing.Callable` is a deprecated alias kept for backwards compatibility.

### 8. Lexical Scoping and the LEGB Rule

Python resolves names by **where the code is written** (lexical/static
scoping), not by where it is called. Lookup follows **LEGB**:

1. **L**ocal — the current function.
2. **E**nclosing — any outer function(s), innermost first.
3. **G**lobal — the module.
4. **B**uilt-in — `len`, `print`, `max`, …

```python
def outer():
    secret = 42            # Enclosing scope for inner()
    def inner():
        return secret      # found at step E
    return inner
```

The **E** level is what makes this whole module possible: an inner function
can *see* its birth environment. Lexical scoping means you can predict what a
function sees just by reading the source — no runtime surprises.

### 9. Closures

A **closure** is a function that *captures* variables from its enclosing
scope and keeps them alive after the outer function has returned:

```python
def make_counter() -> Callable[[], int]:
    count = 0
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

a = make_counter()
b = make_counter()
a(), a(), b()        # (1, 2, 1) — independent state!
```

Each call to `make_counter()` creates a **fresh `count` cell**, so `a` and
`b` never interfere — exactly the independence ex2 demands. The captured
variables live in `a.__closure__` as *cell objects*:

```python
a.__closure__[0].cell_contents   # 2
```

🛡️ **Defense question (from the subject):** *"How do closures 'remember'
their creation environment?"* — At definition time, Python stores references
to the needed enclosing variables in the function's `__closure__` cells; the
frame may die, the cells survive. This gives you **private, encapsulated
state without globals and without classes** — a counter, an accumulator, or
a whole vault (`store`/`recall` sharing one hidden dict) in a few lines.

### 10. nonlocal vs global

By default, **assigning** to a name inside a function creates a *new local
variable* — even if an enclosing one exists. To rebind an outer name you must
declare it:

- `nonlocal name` → rebinds the variable in the nearest **enclosing
  function** scope (closures).
- `global name` → rebinds the variable at **module level**.

🛡️ **Defense question (from the subject):** *"Why is `global` forbidden but
`nonlocal` allowed?"* — `global` creates **shared mutable state visible to
the entire module**: any function can read or corrupt it, tests can't run in
isolation, and purity is gone. `nonlocal` keeps the state **sealed inside
one closure**: only the functions born in that scope can touch it — it
behaves like a private instance attribute, minus the class.

🛡️ **Defense nugget:** `nonlocal` is only needed to **rebind** (`count += 1`
rebinds an `int`). *Mutating* a captured mutable object needs no declaration:
a `memory_vault` closure can `memories[key] = value` on its hidden dict
freely, because the name `memories` itself is never reassigned.

### 11. functools.reduce and the operator Module

`reduce(func, iterable[, initializer])` **folds** a sequence into a single
value by repeatedly applying a two-argument function left-to-right:

```python
from functools import reduce
import operator

reduce(operator.add, [10, 20, 30, 40])    # ((10+20)+30)+40 → 100
reduce(operator.mul, [10, 20, 30, 40])    # 240000
reduce(operator.add, [], 0)               # 0 — initializer handles empty
reduce(operator.add, [])                  # 💥 TypeError!
```

The **`operator`** module provides named, C-implemented versions of the
operators (`add`, `mul`, `truediv`, `itemgetter`, …) — clearer and faster
than the equivalent throwaway lambdas. A tidy way to support several
operations is a dispatch dict, `{"add": operator.add, "multiply":
operator.mul, "max": max, "min": min}` — yes, the builtins `max`/`min` work
perfectly as binary reducers. An unknown operation should be handled
explicitly (e.g. raise/catch a `ValueError`) rather than crashing with a
cryptic `KeyError`.

🛡️ **Defense nuggets:** `reduce` was a builtin in Python 2 and was moved to
`functools` in Python 3 — Guido considered explicit loops more readable, so
its use is a deliberate choice. And the empty-iterable `TypeError` is exactly
why ex3 requires returning `0` for empty input: pass an initializer or guard
first.

### 12. Partial Application with functools.partial

`partial(func, *args, **kwargs)` returns a new callable with some arguments
**pre-filled** (frozen):

```python
from functools import partial

def enchant(power: int, element: str, target: str) -> str:
    return f"{element} {target} ({power})"

flaming = partial(enchant, 50, "Flaming")
flaming("Sword")                 # 'Flaming Sword (50)'
```

Unlike a wrapping lambda, a `partial` object is introspectable (`.func`,
`.args`, `.keywords`) and freezes **values**, not variables — which defuses
the classic **late-binding trap**:

```python
# ❌ all three lambdas capture the VARIABLE e — which ends as "Shocking"
fns = [lambda t: enchant(50, e, t) for e in ("Flaming", "Frozen", "Shocking")]
fns[0]("Sword")                  # 'Shocking Sword (50)' 😱

# ✅ partial freezes the VALUE of e at creation time
fns = [partial(enchant, 50, e) for e in ("Flaming", "Frozen", "Shocking")]
fns[0]("Sword")                  # 'Flaming Sword (50)'
```

🛡️ **Defense nugget:** the lambda version can be fixed with a default
argument (`lambda t, e=e: …`), because defaults are evaluated at definition
time — but `partial` states the intent directly. Expect an evaluator to ask
about this exact trap.

### 13. Memoization with functools.lru_cache

**Memoization** caches a function's results keyed by its arguments, so
repeated calls with the same inputs are answered instantly:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)
```

Naive recursive Fibonacci recomputes the same subproblems exponentially —
roughly **O(2ⁿ)** calls. With `lru_cache`, each `fibonacci(k)` is computed
**once**: **O(n)** time, O(n) cache. The subject's own hint,
`memoized_fibonacci.cache_info()`, returns
`CacheInfo(hits=…, misses=…, maxsize=…, currsize=…)` — the proof that the
cache is working (hits > 0 on repeated calls).

🛡️ **Defense nuggets:** *LRU* = Least Recently Used — with a bounded
`maxsize`, the oldest-used entries are evicted first; `maxsize=None` means
unbounded (Python 3.9+ adds `@functools.cache` as a shortcut for exactly
that). Arguments must be **hashable** (they are dict keys internally), and
caching is only *correct* for **pure functions** — a cached impure function
would replay stale side effects. FP concepts reinforcing each other.

### 14. Type Dispatch with functools.singledispatch

`@singledispatch` turns a function into a **generic function** that selects
an implementation based on the **type of its first argument**:

```python
from functools import singledispatch
from typing import Any

@singledispatch
def cast(spell: Any) -> str:
    return "Unknown spell type"          # fallback for unregistered types

@cast.register
def _(spell: int) -> str:
    return f"Damage spell: {spell} damage"

@cast.register
def _(spell: list) -> str:
    return f"Multi-cast: {len(spell)} spells"

cast(42)          # 'Damage spell: 42 damage'
cast(3.14)        # 'Unknown spell type'
```

Since Python 3.7, `.register` reads the **type annotation** of the
implementation's first parameter (you can also write
`@cast.register(str)` explicitly). It's the functional answer to a chain of
`isinstance` checks — open for extension (register new types anywhere)
without modifying the base function.

🛡️ **Defense nugget:** "single" means dispatch happens on the **first
argument only** — Python has no built-in multiple dispatch. Bonus trivia:
`bool` is a subclass of `int`, so `cast(True)` hits the `int` handler unless
you register `bool` separately.

### 15. Decorators and functools.wraps

A **decorator** is a higher-order function that receives a function and
returns a (usually enhanced) replacement. The `@` syntax is pure sugar:

```python
@spell_timer
def fireball(): ...
# …is exactly equivalent to:
fireball = spell_timer(fireball)
```

The canonical wrapper pattern:

```python
import functools
import time

def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)                      # ← preserve identity!
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)          # the real call
        print(f"Spell completed in {time.perf_counter() - start:.3f} seconds")
        return result                           # never swallow the result
    return wrapper
```

- `*args, **kwargs` makes the wrapper **signature-transparent**: it forwards
  any call unchanged, so one decorator fits every function.
- Without `@functools.wraps`, the decorated function's `__name__` becomes
  `'wrapper'` and its docstring vanishes — breaking introspection, debugging,
  and `help()`. `wraps` copies `__name__`, `__qualname__`, `__doc__`,
  `__module__`, `__dict__` and sets `__wrapped__` (the undisguised original).

🛡️ **Defense question (from the subject):** *"How do decorators enable
separation of concerns?"* — Timing, validation, retrying, and logging are
**cross-cutting concerns**: they apply to many functions but belong to none.
A decorator isolates each concern in one reusable place, keeping the spell's
body purely about its own logic. (`time.perf_counter()` beats `time.time()`
for durations: it is monotonic and high-resolution.)

### 16. Decorator Factories, Methods and staticmethod

A decorator can't take parameters directly — so a **decorator factory** adds
one more layer. Three nested levels, each with one job:

```python
def power_validator(min_power: int):            # 1. factory: takes the config
    def decorator(func: Callable) -> Callable:  # 2. decorator: takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):           # 3. wrapper: takes the call
            ...                                 #    validate, then func(...)
        return wrapper
    return decorator

@power_validator(min_power=10)                  # note the CALL: returns level 2
def cast_lightning(target: str, power: int) -> str: ...
```

`min_power` is simply **closed over** by the two inner levels — decorator
factories are closures wearing a hat. `retry_spell(max_attempts)` follows
the same shape, with the wrapper looping over attempts in a `try`/`except`
and only reporting failure after the last one.

**Decorating methods:** the same wrapper works on instance methods because
`self` just arrives as `args[0]`. That's also the catch — the argument you
validate (`power`) is no longer at a fixed position, so a robust wrapper
locates it defensively (check `kwargs` first, fall back to the last
positional) instead of hardcoding an index. This is exactly why the subject
applies `power_validator` to both a standalone function *and*
`MageGuild.cast_spell`.

**`@staticmethod`** — itself a built-in decorator! — declares a method that
receives **no `self` and no `cls`**: it can't touch instance or class state.
It's a plain function namespaced inside the class because it *belongs there
conceptually* (`MageGuild.validate_mage_name("Gandalf")` works on the class
or on an instance).

🛡️ **Defense question (from the subject):** *"@staticmethod vs regular
instance methods?"* — An instance method receives `self` and can read/mutate
the object's state; a static method receives nothing implicit and is pure
utility. If a method never uses `self`, making it static documents that fact
and lets you call it without an instance. Name validation depends only on
the name → static; casting a spell conceptually belongs to a guild member →
instance.

---

## 🗂️ Project Structure

```
funcmage/
├── data_generator.py           # provided helper — sample mages, artifacts & spells
├── ex0/
│   └── lambda_spells.py        # artifact_sorter, power_filter, spell_transformer, mage_stats
├── ex1/
│   └── higher_magic.py         # spell_combiner, power_amplifier, conditional_caster, spell_sequence
├── ex2/
│   └── scope_mysteries.py      # mage_counter, spell_accumulator, enchantment_factory, memory_vault
├── ex3/
│   └── functools_artifacts.py  # spell_reducer, partial_enchanter, memoized_fibonacci, spell_dispatcher
├── ex4/
│   └── decorator_mastery.py    # spell_timer, power_validator, retry_spell, MageGuild
└── README.md
```

---

## 🗺️ The Five Realms (Exercises)

| Ex | Realm | File to submit | Authorized | You will master |
|:--:|-------|----------------|------------|-----------------|
| 0 | 🏛️ Lambda Sanctum | `ex0/lambda_spells.py` | `map`, `filter`, `sorted`, `min`, `max`, `round`, `sum`, `len` | Anonymous functions & `key=`-based transforms — sorting artifacts, filtering mages, mapping spell names, computing stats |
| 1 | ☁️ Higher Realm | `ex1/higher_magic.py` | `callable()`, `Callable` | Higher-order functions — combining, amplifying, gating, and sequencing spells that share one contract |
| 2 | 🕳️ Memory Depths | `ex2/scope_mysteries.py` | `nonlocal` | Closures & lexical scoping — independent counters, accumulators, enchantment factories, and a private memory vault |
| 3 | 📚 Ancient Library | `ex3/functools_artifacts.py` | `functools`, `operator` | `reduce` folds, `partial` application, `lru_cache` memoization, `singledispatch` type dispatch |
| 4 | 🗼 Master's Tower | `ex4/decorator_mastery.py` | `functools.wraps`, `staticmethod` | Decorators, parameterized decorator factories, retry logic, and `@staticmethod` vs instance methods |

---

## ⚙️ Usage

```bash
# Clone and enter the module
git clone <repository-url>
cd funcmage

# Each realm is a self-testing script
python3 ex0/lambda_spells.py
python3 ex1/higher_magic.py
python3 ex2/scope_mysteries.py
python3 ex3/functools_artifacts.py
python3 ex4/decorator_mastery.py

# Generate realistic test data (mages, artifacts, spells) — provided helper
python3 data_generator.py

# Lint everything before pushing
flake8 ex0/ ex1/ ex2/ ex3/ ex4/
```

Example run (ex2):

```
$> python3 scope_mysteries.py
Testing mage counter...
counter_a call 1: 1
counter_a call 2: 2
counter_b call 1: 1
...
```

---

## 📏 Key Constraints

- **Python 3.10+**, **flake8-compliant**, **type hints on every function
  signature and return type**.
- `Callable` must be imported from **`collections.abc`** (not `typing`).
- One exercise = one file, with the **exact filename** the subject specifies.
- Exception handling must protect the data streams from corruption.
- **Forbidden:** external libraries (no `pip install`), file I/O,
  `eval()` / `exec()`, global variables, and over-engineered algorithms —
  the focus is the functional patterns themselves.
- `functools` and `operator` are only authorized where explicitly listed
  (ex3; `functools.wraps` in ex4).
- Ex0 additionally forbids `def` for simple one-shot transformations —
  lambdas, used inline.
- Output messages may be personalized as long as the core structure and
  essential information are preserved.

---

## 📚 Resources

- [functools — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html)
- [operator — Standard operators as functions](https://docs.python.org/3/library/operator.html)
- [collections.abc — Abstract Base Classes (Callable)](https://docs.python.org/3/library/collections.abc.html)
- [Python Tutorial — Lambda Expressions](https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions)
- [Python FAQ — Why do lambdas defined in a loop all return the same result?](https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result)
- [Real Python — Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/) · [flake8](https://flake8.pycqa.org/)
- *Fluent Python* — Luciano Ramalho (chapters on first-class functions,
  closures, and decorators)

---

## 🤖 AI Usage Disclosure

In line with the AI guidelines included in this subject, AI assistance
(Anthropic's Claude) was used for:

- structuring and formatting this README;
- discussing and clarifying the theory behind the concepts covered.

All submitted solutions are my own work, fully understood and defensible
during peer evaluation.

---

<div align="center">

*Made with 🧙 at 42 Porto*

</div>
