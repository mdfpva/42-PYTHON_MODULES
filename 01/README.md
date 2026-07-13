<div align="center">

```
  ___         _       ___     _ _   _          _   _
 / __|___  __| |___  / __|  _| | |_(_)_ ____ _| |_(_)___ _ _
| (__/ _ \/ _` / -_)| (_| || | |  _| \ V / _` |  _| / _ \ ' \
 \___\___/\__,_\___| \___\_,_|_|\__|_|\_/\__,_|\__|_\___/_||_|
                                            🌱 42 🌱
```

### 🌿 Object-Oriented Garden Systems 🌿

**A 42 School Project — Python Piscine, OOP Module**

*Build a comprehensive digital garden ecosystem while discovering advanced
Python concepts. Create tools to manage community gardens efficiently
through data-driven approaches.*

`Version 3.2` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Program Structure and `__name__ == "__main__"`](#1-program-structure-and-__name__--__main__)
  - [2. The Shebang Line](#2-the-shebang-line)
  - [3. Classes and Objects](#3-classes-and-objects)
  - [4. Attributes and Instantiation](#4-attributes-and-instantiation)
  - [5. Methods and `self`](#5-methods-and-self)
  - [6. The Constructor: `__init__()`](#6-the-constructor-__init__)
  - [7. Encapsulation](#7-encapsulation)
  - [8. Getters, Setters and Validation](#8-getters-setters-and-validation)
  - [9. Inheritance](#9-inheritance)
  - [10. `super()` and Method Overriding](#10-super-and-method-overriding)
  - [11. Static Methods](#11-static-methods)
  - [12. Class Methods](#12-class-methods)
  - [13. Decorators (Intro)](#13-decorators-intro)
  - [14. Nested Classes (Composition)](#14-nested-classes-composition)
  - [15. Polymorphism and Duck Typing](#15-polymorphism-and-duck-typing)
  - [16. Naming Conventions](#16-naming-conventions)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Testing & Linting](#-testing--linting)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🌍 About the Project

**Code Cultivation** is the Object-Oriented Programming module of the 42
Python branch. Building on the fundamentals from *Growing Code*, it walks
through the full OOP toolbox — classes, encapsulation, inheritance,
`super()`, static/class methods, nested classes — by incrementally growing a
single `Plant` class into a complete **digital garden ecosystem**.

Unlike the previous module, programs here are *real programs*: each file has
an entry point guarded by `if __name__ == "__main__":`, and each exercise
**reuses and improves** the classes from the previous one.

> "You can't plant flowers and then pull them up every day to see how the
> roots are doing." — the same applies to code. 🌱

---

## 🧠 Concepts Covered (Theory)

### 1. Program Structure and `__name__ == "__main__"`

Every Python module has a built-in variable `__name__`. Its value depends on
*how the file is being used*:

- Run directly (`python3 ft_garden_intro.py`) → `__name__ == "__main__"`
- Imported (`import ft_garden_intro`) → `__name__ == "ft_garden_intro"`

```python
def main() -> None:
    print("=== Welcome to My Garden ===")


if __name__ == "__main__":
    main()
```

This guard makes a file **dual-purpose**: it behaves as a program when
executed, and as an importable library when imported — the import will *not*
trigger the main code. This is the foundation of the Python import system
(covered in a later module) and a habit evaluators *will* ask you to justify.

### 2. The Shebang Line

The first line `#!/usr/bin/env python3` is the **shebang**. On Unix systems,
when a file is executed directly (`./ft_garden_intro.py`), the kernel reads
this line to know *which interpreter* should run the script.

```bash
chmod +x ft_garden_intro.py   # make it executable
./ft_garden_intro.py          # runs via the shebang, no "python3" needed
```

- `#!/usr/bin/env python3` is preferred over a hardcoded path
  (`#!/usr/bin/python3`) because `env` looks up `python3` in the user's
  `$PATH` — portable across systems and virtualenvs.
- To Python itself it's just a comment (`#`), so it never breaks anything.
- ⚠️ The evaluation will ask you to **add the shebang live** — know it.

### 3. Classes and Objects

A **class** is a *blueprint*: it defines the shape of a category of things
(what data they hold, what they can do). An **object** (or *instance*) is a
concrete thing built from that blueprint.

```python
class Plant:            # the blueprint (one)
    ...

rose = Plant()          # an instance (as many as you want)
cactus = Plant()
```

Instead of juggling parallel variables (`rose_name`, `rose_height`,
`rose_age`, `cactus_name`, ...), OOP bundles **state** (attributes) and
**behaviour** (methods) into one coherent unit. That's the whole point:
*organizing code the way a gardener organizes a garden — everything has its
proper place*.

### 4. Attributes and Instantiation

**Attributes** are variables attached to an object. **Instantiation** is the
act of creating the object by *calling the class*:

```python
rose = Plant()          # instantiation
rose.name = "Rose"      # setting attributes
rose.height = 25
rose.age = 30
```

Each instance carries its **own** copy of the attributes — modifying
`rose.height` never touches `cactus.height`. (Attributes set directly on
instances like this are *instance attributes*; class attributes, shared by
all instances, exist too but behave differently.)

### 5. Methods and `self`

A **method** is a function defined *inside* a class. Its first parameter is
always **`self`** — the reference to the specific instance the method is
acting on:

```python
class Plant:
    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")

rose.show()     # Python translates this to: Plant.show(rose)
```

- `self` is not a keyword, it's a convention — but *never* rename it.
- Through `self`, a method reads and mutates the state of *its own* object:
  `grow()` and `age()` are exactly this — operations that modify state.

### 6. The Constructor: `__init__()`

`__init__()` is the **initializer** (commonly called constructor): a special
*dunder* ("double underscore") method that Python calls automatically right
after creating a new instance. It lets you **instantiate and initialize at
the same time**:

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

oak = Plant("Oak", 200.0, 365)   # ready to use immediately
```

- Arguments passed to `Plant(...)` are forwarded to `__init__`.
- The object is **fully valid from birth** — no window of time where it
  exists half-initialized. This is the "Plant Factory" idea of ex3.
- `__init__` returns `None`; the instance itself is returned by the class
  call machinery (`__new__`, which you rarely touch).

### 7. Encapsulation

**Encapsulation** = bundling data with the methods that operate on it, and
**restricting direct access** to the internal state so it can't be corrupted
from outside.

Python has *no enforced* `private` keyword. Instead it uses conventions:

| Prefix | Name | Meaning |
|--------|------|---------|
| `name` | public | free to access |
| `_name` | **protected** (convention) | "internal — don't touch from outside" |
| `__name` | name **mangling** | Python renames it to `_ClassName__name` |

```python
class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name        # protected by convention
        self._height = height
        self._age = age
```

This module explicitly requires the **protected convention (single
underscore), not mangling**. It's a *social contract*: nothing stops access
to `plant._height`, but the underscore tells every reader "go through the
public interface instead". *"We're all consenting adults here"* — the
Pythonic philosophy of trust + convention over enforcement.

### 8. Getters, Setters and Validation

With attributes protected, the class exposes **controlled access points**:

- **Getters** (`get_height()`) — safe *read* access;
- **Setters** (`set_height()`) — *write* access that **validates** first.

```python
def set_height(self, height: float) -> None:
    if height < 0:
        print(f"{self._name}: Error, height can't be negative")
        return                      # data left unchanged
    self._height = height

def get_height(self) -> float:
    return self._height
```

The validation logic lives **inside the class** — the single place where the
rules of "what is a valid Plant" are enforced. Invalid input never corrupts
state: it's rejected with an error message, and the object keeps its previous
(or default) values. This is *data integrity by design*.

> 📝 Idiomatic Python would later replace get/set pairs with the `@property`
> decorator — but explicit getters/setters are the pedagogical step to
> understand what properties automate.

### 9. Inheritance

**Inheritance** lets a class (*child* / subclass) reuse and extend another
(*parent* / superclass). The child **is a** specialized version of the
parent:

```python
class Flower(Plant):                 # Flower IS-A Plant
    def __init__(self, name: str, height: float, age: int,
                 color: str) -> None:
        super().__init__(name, height, age)   # parent handles common part
        self.color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True
```

- `Flower`, `Tree` and `Vegetable` all inherit `name`/`height`/`age`
  handling, `grow()`, `age()` and `show()` **without rewriting them** — the
  DRY principle (*Don't Repeat Yourself*) applied to class design.
- Each child adds its own attributes (`color`, `trunk_diameter`,
  `harvest_season`...) and behaviours (`bloom()`, `produce_shade()`...).
- Inheritance chains can go deeper: `Seed → Flower → Plant` (ex6).

### 10. `super()` and Method Overriding

**Overriding** = redefining a parent method in the child with the same name.
The child's version wins when called on a child instance.

**`super()`** returns a proxy to the parent class, letting the override
*reuse* the parent logic instead of duplicating it:

```python
class Flower(Plant):
    def show(self) -> None:
        super().show()               # print the standard Plant part
        print(f" Color: {self.color}")   # then the Flower extras
```

This *extend, don't replace* pattern is everywhere in real code — the child
adds a layer on top of behaviour it trusts the parent to do right. The same
applies to `__init__`: `super().__init__(...)` ensures the parent's
initialization (including validation from ex4!) always runs.

### 11. Static Methods

A **static method** belongs to the class *namespace* but receives **no
`self` and no `cls`** — it's a plain function that lives inside the class
because it's thematically related:

```python
class Plant:
    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

Plant.is_older_than_a_year(400)   # True — no instance needed
```

Use it when the logic concerns the *concept* (any age, any plant) rather
than one particular object's state. Both the decorator syntax
(`@staticmethod`) and the function-call syntax
(`method = staticmethod(method)`) are accepted by the subject — the
decorator is what everyone uses in practice.

### 12. Class Methods

A **class method** receives the **class itself** as first argument (`cls`
by convention) instead of an instance:

```python
class Plant:
    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)
```

Its killer use case is the **alternative constructor** (factory method):
creating instances in a different way than `__init__` — here, an
"anonymous" plant when you don't yet have the data. Because it uses `cls`
rather than a hardcoded `Plant`, it plays nicely with inheritance:
`Flower.anonymous()` would build a `Flower`.

**`self` vs `cls` vs nothing:**

| Kind | 1st param | Sees instance state? | Sees class? |
|-----------------|-----------|----------------------|-------------|
| instance method | `self` | ✅ | ✅ |
| class method | `cls` | ❌ | ✅ |
| static method | — | ❌ | ❌ |

### 13. Decorators (Intro)

`@staticmethod` and `@classmethod` are your first contact with
**decorators**: syntax that *wraps or transforms* the function defined just
below it.

```python
@classmethod                 # equivalent to: anonymous = classmethod(anonymous)
def anonymous(cls) -> "Plant":
    ...
```

A decorator is just a callable that takes a function and returns a modified
one — the `@` line is syntactic sugar for reassignment. Custom decorators
are explored in later modules; for now, recognize the pattern and what these
two built-ins do.

### 14. Nested Classes (Composition)

A **nested class** is a class defined *inside* another class. In ex6 each
`Plant` owns an internal statistics tracker:

```python
class Plant:
    class _Stats:                      # nested, protected
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

    def __init__(self, ...) -> None:
        ...
        self._stats = Plant._Stats()   # each plant HAS-A stats object
```

- Nesting signals: "`_Stats` only makes sense in the context of `Plant`" —
  it scopes a helper type and keeps the global namespace clean.
- This is **composition** ("has-a") working *alongside* inheritance
  ("is-a"): a `Tree` **is a** `Plant`, and a `Plant` **has a** `_Stats`.
  Knowing when to use which is a core design skill.
- Subclasses can extend the nested component too — `Tree` tracks an extra
  counter for `produce_shade()` calls.

### 15. Polymorphism and Duck Typing

**Polymorphism** = the same call producing type-appropriate behaviour.
`plant.show()` prints different things for a `Flower`, a `Tree`, a `Seed` —
the *caller doesn't need to know* the concrete type.

The final ex6 requirement — *one free function that displays statistics for
any kind of plant* — is polymorphism in action:

```python
def display_stats(plant: Plant) -> None:
    plant.show_stats()     # works for Plant, Flower, Tree, Seed, ...
```

Python takes this further with **duck typing**: *"if it walks like a duck
and quacks like a duck, it's a duck"* — any object exposing the expected
method works, related by inheritance or not. Combined with overriding, this
is what makes OOP systems **extensible**: add a new plant type tomorrow and
`display_stats()` keeps working, untouched.

### 16. Naming Conventions

PEP 8 naming, enforced in this module:

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | **PascalCase** | `Plant`, `GardenSecurity` |
| Functions / methods | **snake_case** | `produce_shade()` |
| Variables / attributes | **snake_case** | `trunk_diameter` |
| Protected members | `_snake_case` | `_height`, `_stats` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_HEIGHT` |

Plus the module-wide requirements: **type hints on every function and
method** (checked with `mypy`), flake8-clean style, and programs that always
run without errors.

---

## 📂 Project Structure

```
code_cultivation/
├── ex0/
│   └── ft_garden_intro.py      # __main__ guard, variables, shebang
├── ex1/
│   └── ft_garden_data.py       # first Plant class, show() method
├── ex2/
│   └── ft_plant_growth.py      # grow()/age() methods, state mutation
├── ex3/
│   └── ft_plant_factory.py     # __init__ constructor
├── ex4/
│   └── ft_garden_security.py   # encapsulation, getters/setters, validation
├── ex5/
│   └── ft_plant_types.py       # inheritance: Flower, Tree, Vegetable
└── ex6/
    └── ft_garden_analytics.py  # static/class methods, nested class, Seed
```

---

## 🌾 Exercises

| Ex  | File | Authorized | Concepts |
|-----|------|------------|----------|
| 0 | `ft_garden_intro.py` | `print()` | Program entry point, `__main__`, shebang |
| 1 | `ft_garden_data.py` | `print()` | `Plant` class, attributes, `show()` method |
| 2 | `ft_plant_growth.py` | + `range()`, `round()` | `grow()`/`age()`, mutating state, week simulation |
| 3 | `ft_plant_factory.py` | `print()`, `range()`, `round()` | `__init__`, ≥5 plants created ready-to-use |
| 4 | `ft_garden_security.py` | `print()`, `range()`, `round()` | Encapsulation (`_attr`), get/set, validation, error messages |
| 5 | `ft_plant_types.py` | + `super()` | Inheritance, overriding `show()`, `bloom()`, `produce_shade()` |
| 6 | `ft_garden_analytics.py` | + `staticmethod()`, `classmethod()` | Static/class methods, `Seed(Flower)`, nested `_Stats`, polymorphic display |

**Progression logic:** each exercise *evolves the same `Plant` class* —
ex1 creates it, ex2 gives it behaviour, ex3 a constructor, ex4 armour,
ex5 children, ex6 an analytics nervous system. By the end you have one
cohesive ecosystem, not seven isolated snippets.

---

## 🚀 Usage

Every exercise is a standalone program:

```bash
python3 ex5/ft_plant_types.py
```

```
=== Garden Plant Types ===
=== Flower
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[asking the rose to bloom]
...
```

Or, with the shebang + execute permission:

```bash
chmod +x ex0/ft_garden_intro.py
./ex0/ft_garden_intro.py
```

Test blocks live inside `if __name__ == "__main__":` — importing any file
from another module triggers **no** side effects.

---

## ✅ Testing & Linting

```bash
# Style (all files must be clean)
flake8 .

# Type checking (type hints are mandatory on every function/method)
mypy ex0/ ex1/ ex2/ ex3/ ex4/ ex5/ ex6/
```

---

## ⚠️ Key Constraints

- Python **3.10+**, flake8-clean, **type hints everywhere** (mypy-checked).
- One exercise per directory; programs must **always run without errors**.
- Naming: classes **PascalCase**, functions/variables **snake_case**.
- `if __name__ == "__main__":` blocks are allowed (and expected) from ex0 on.
- Encapsulation in ex4+ uses the **protected convention** (`_attr`), *not*
  name mangling (`__attr`).
- ex4: invalid values (negative height/age) are rejected **from inside the
  class** with an error message; data stays unchanged or defaults are used.
- No validation needed for the *new* attributes of ex5's subclasses.
- Be ready to explain: why `__main__` matters, what the shebang does (live
  edit during evaluation!), `self` vs `cls`, is-a vs has-a.

---

## 📚 Resources

- [Python Classes — official tutorial](https://docs.python.org/3/tutorial/classes.html)
- [PEP 8 — Style Guide (naming conventions)](https://peps.python.org/pep-0008/)
- [`super()` explained](https://docs.python.org/3/library/functions.html#super)
- [Built-in `staticmethod` / `classmethod`](https://docs.python.org/3/library/functions.html#staticmethod)
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
