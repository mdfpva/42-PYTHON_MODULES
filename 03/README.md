<div align="center">

```
 ___       _           ___              _
|   \ __ _| |_ __ _   / _ \ _  _ ___ __| |_
| |) / _` |  _/ _` | | (_) | || / -_|_-<  _|
|___/\__,_|\__\__,_|  \__\_\\_,_\___/__/\__|
                              🎮 42 🎮
```

### ⚔️ Mastering Python Collections ⚔️

**A 42 School Project — Python Piscine, Collections Module**

*Journey through the digital realm as a data engineer! Master Python's
powerful data structures while building and processing game data.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Your Data Structure Is Your Algorithm](#1-your-data-structure-is-your-algorithm)
  - [2. Imports and the `sys` Module](#2-imports-and-the-sys-module)
  - [3. Command-Line Arguments: `sys.argv`](#3-command-line-arguments-sysargv)
  - [4. Lists](#4-lists)
  - [5. Indexing and Slicing](#5-indexing-and-slicing)
  - [6. Tuples](#6-tuples)
  - [7. Tuple Unpacking](#7-tuple-unpacking)
  - [8. Sets](#8-sets)
  - [9. Set Algebra: union, intersection, difference](#9-set-algebra-union-intersection-difference)
  - [10. Dictionaries](#10-dictionaries)
  - [11. Iterating Collections](#11-iterating-collections)
  - [12. Generators and `yield`](#12-generators-and-yield)
  - [13. Typing Generators](#13-typing-generators)
  - [14. Comprehensions](#14-comprehensions)
  - [15. The `random` and `math` Modules](#15-the-random-and-math-modules)
  - [16. Choosing the Right Collection](#16-choosing-the-right-collection)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Testing & Linting](#-testing--linting)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🌍 About the Project

**Data Quest** is the collections module of the 42 Python branch. Framed as
a *game analytics platform* — player scores, 3D coordinates, achievements,
RPG inventories, live event streams — each exercise "unlocks" one of
Python's core data structures: **lists**, **tuples**, **sets**,
**dictionaries**, then the power-ups on top of them: **generators** and
**comprehensions**.

The module's thesis comes straight from its foreword, recounting Twitter's
early scaling wars: nothing was logically wrong with the code, but the wrong
container turned linear time into a production headache. **At scale, your
data structure is your algorithm.**

---

## 🧠 Concepts Covered (Theory)

### 1. Your Data Structure Is Your Algorithm

Every container makes some operations cheap and others expensive:

| Operation | `list` | `set` / `dict` |
|-----------|--------|----------------|
| `x in c` (membership) | O(n) — scans every element | **O(1)** — hash lookup |
| append / add | O(1) | O(1) |
| access by index | O(1) | — (no order/index) |
| keep insertion order | ✅ | dict ✅ (3.7+), set ❌ |
| duplicates | allowed | impossible |

A membership check that costs microseconds on 100 elements becomes a
bottleneck when it runs millions of times per second on millions of
elements. Sets and dicts achieve O(1) via **hashing**: the element's hash
tells Python *where to look* instead of scanning. Choosing the container
**is** choosing the algorithm.

### 2. Imports and the `sys` Module

An **import** loads another module and binds its name in your namespace:

```python
import sys          # now sys.argv, sys.exit, ... are reachable
import math         # math.sqrt(...)
import random       # random.choice(...), random.randint(...)
```

- `import x` runs the module once (cached afterwards) and gives you the
  `x.` prefix — explicit about where each name comes from.
- The import system (packages, relative imports, `from ... import`) gets
  its own module later; here you only need the basic form, always at the
  top of the file (flake8 enforces this).

### 3. Command-Line Arguments: `sys.argv`

`sys.argv` is a **list of strings** holding the command line, exactly like
`argv` in C:

```bash
python3 ft_command_quest.py hello world 42
```

```python
sys.argv        # ['ft_command_quest.py', 'hello', 'world', '42']
sys.argv[0]     # program name — always present
sys.argv[1:]    # the actual arguments (slicing skips the name)
len(sys.argv)   # total count, program name included
```

Key facts: `argv[0]` is the script name, so "no arguments" means
`len(sys.argv) == 1`; every element is a `str` (even `"42"` — convert
explicitly); the shell handles quoting, so `"Data Quest"` arrives as *one*
element. Skipping the program name has several idioms (`argv[1:]` slice,
starting the loop at index 1, `enumerate(argv[1:], start=1)`) — the subject
warns you'll discuss alternatives at evaluation.

### 4. Lists

The **list** is Python's ordered, mutable, growable sequence:

```python
scores: list[int] = []
scores.append(1500)        # grow in place
scores[0] = 2000           # replace by index
scores.remove(2000)        # delete by value
len(scores), sum(scores), max(scores), min(scores)
```

- **Ordered**: elements keep their position; index access is O(1).
- **Mutable**: the same object changes in place — which also means two
  names can point to the same list (aliasing!).
- **Heterogeneous-capable** but typically homogeneous
  (`list[int]`, `list[tuple[str, str]]`...).
- Built-ins that pair with lists everywhere in this module: `len()`,
  `sum()`, `max()`, `min()` — the whole of ex1's stats
  (range = `max - min`) falls out of them.

### 5. Indexing and Slicing

Sequences (lists, tuples, strings) share the same access syntax:

```python
argv[0]       # first element
argv[-1]      # last element (negative = from the end)
argv[1:]      # slice: from index 1 to the end (NEW list)
argv[1:4]     # indices 1, 2, 3 — stop is exclusive
```

Slices **copy**: `argv[1:]` is a new list, leaving the original untouched —
the cleanest way to "drop the program name" without mutating `sys.argv`.

### 6. Tuples

The **tuple** is the immutable sequence — *"data written in stone"*:

```python
pos: tuple[float, float, float] = (1.0, 2.5, 3.0)
pos[0]          # 1.0 — indexing works like a list
pos[0] = 9.9    # TypeError! tuples cannot change
```

Why immutability is a *feature*, not a limitation:

- **Integrity** — a 3D position handed to other code cannot be corrupted;
- **Hashability** — because they can't change, tuples can be `set` members
  and `dict` keys (lists can't!);
- **Fixed shape** — a tuple's *positions have meaning*: `(x, y, z)`,
  `(name, action)`. A list is *many of the same thing*; a tuple is *one
  thing with several fields*.

### 7. Tuple Unpacking

Assign a whole tuple into named variables in one statement:

```python
x, y, z = pos                    # unpacking
name, action = event             # ('bob', 'run') -> name='bob', ...
for name, action in events:      # unpack directly in the loop head
    print(f"Player {name} did action {action}")
```

The number of names must match the tuple length. This is the idiomatic way
to display "each coordinate separately" (ex2) and to consume `(name,
action)` events (ex5) — no `event[0]` / `event[1]` noise.

### 8. Sets

The **set** is an unordered collection of **unique**, hashable elements:

```python
achievements = {"First Steps", "Boss Slayer"}
achievements.add("Boss Slayer")     # already there -> no effect
"Untouchable" in achievements       # O(1) membership
```

- **No duplicates, ever** — adding an existing element is a silent no-op.
  This is the tool for "unique achievements".
- **No order, no indexing** — `s[0]` doesn't exist; printing order can vary.
- Built from an iterable with `set(iterable)`, or with `{...}` literals.
- ⚠️ The empty set prints as `set()` — because `{}` is already taken by the
  empty *dict*. That's the answer to the subject's lightbulb question.

### 9. Set Algebra: union, intersection, difference

Sets implement mathematical set theory — the ex3 toolkit:

| Operation | Method | Operator | Meaning (players A, B) |
|-----------|--------|----------|------------------------|
| Union | `a.union(b)` | `a \| b` | achievements *anyone* has |
| Intersection | `a.intersection(b)` | `a & b` | shared by *all* |
| Difference | `a.difference(b)` | `a - b` | in `a` but not in `b` |

They chain across many sets — `a.union(b, c, d)` — which maps 1:1 onto the
exercise: **all distinct** = union of everyone; **common** = intersection
of everyone; **only Alice has** = Alice − (union of everyone else);
**Alice is missing** = (union of everyone) − Alice. Each returns a **new
set**; the operands are untouched.

### 10. Dictionaries

The **dict** maps unique, hashable **keys** to arbitrary **values** — the
RPG inventory made literal:

```python
inventory: dict[str, int] = {}
inventory["sword"] = 1              # insert / overwrite
inventory["sword"]                  # O(1) lookup by key
"sword" in inventory                # O(1) key membership -> spot redundant items
inventory.keys()                    # view of keys  -> list(inventory.keys())
inventory.values()                  # view of values -> sum(inventory.values())
inventory.update({"magic_item": 1}) # merge another mapping in
```

- One value per key: re-inserting a key **overwrites** — which is exactly
  why ex4 must *check first* (`in`) and report `Redundant item 'sword'`
  instead of silently replacing.
- Since Python 3.7, dicts **preserve insertion order** — the display order
  in the expected output is simply first-come order from the command line
  (and it's why "first from the command line wins in a tie" is observable).
- `keys()` / `values()` return live *views*; wrap in `list()` when a real
  list is needed.

### 11. Iterating Collections

`for` works on every collection, each with its idiom:

```python
for score in scores: ...                      # list -> elements
for name, action in events: ...               # list of tuples -> unpack
for item in inventory: ...                    # dict -> KEYS by default
for item, qty in inventory.items(): ...       # dict -> key/value pairs
for i, arg in enumerate(sys.argv[1:], 1): ... # index + element together
```

Percentages per item (ex4) are one pass: total = `sum(values())`, then each
item's share is `round(qty * 100 / total, 1)`.

### 12. Generators and `yield`

A **generator function** contains `yield`. Calling it runs *no code* — it
returns a **generator object** that produces values **on demand**:

```python
def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:                                  # endless is fine!
        yield (random.choice(players), random.choice(actions))

events = gen_event()      # nothing ran yet
next(events)              # runs UNTIL the first yield -> ('bob', 'run')
next(events)              # resumes AFTER the yield -> next event
```

The mental model: `yield` **pauses** the function, hands a value out, and
remembers all local state; `next()` **resumes** it. Consequences:

- **Laziness** — values exist one at a time; 1000 events or 10 million cost
  the same memory. That's how games process endless event streams.
- **Infinite generators are legal** — `while True: yield ...` never "runs
  forever" because it only advances when asked.
- A generator is an **iterator**: `for event in consume_event(lst):` calls
  `next()` for you and stops cleanly when the function returns
  (`StopIteration` is handled by the loop).
- ex5's `consume_event` shows a generator that *mutates* its source: pick a
  random element, remove it, `yield` it, until the list is empty — a
  draining stream, used directly in `for .. in ..`.

### 13. Typing Generators

The precise type from the `typing` module:

```python
from typing import Generator     # subject authorizes "import typing" style too

def gen_event() -> Generator[tuple[str, str], None, None]: ...
```

`Generator[YieldType, SendType, ReturnType]` — you only yield, so send and
return are `None`. (Modern shorthand: `Iterator[tuple[str, str]]`; the
subject explicitly authorizes `typing.Generator`, so use that.)

### 14. Comprehensions

**Comprehensions** condense the build-a-collection-in-a-loop pattern into a
single declarative expression — the "final boss" transformation syntax:

```python
# list comprehension: transform every element
capitalized = [name.capitalize() for name in players]

# list comprehension with filter: keep only some
already_caps = [name for name in players if name == name.capitalize()]

# dict comprehension: build key -> value
scores = {name: random.randint(0, 1000) for name in capitalized}

# dict comprehension with filter: high scores only
high = {n: s for n, s in scores.items() if s > average}
```

Anatomy: `[EXPRESSION for ITEM in ITERABLE if CONDITION]` — the `if` is
optional. Set comprehensions exist too (`{x for x in ...}`). Rules of
taste enforced by the subject: **one comprehension = one line** (unless it
exceeds line length), and comprehensions are for *building collections* —
side-effect loops should stay as regular `for` loops.

### 15. The `random` and `math` Modules

Utility modules the exercises lean on:

```python
math.sqrt(x)                    # ex2: Euclidean distance
random.choice(seq)              # ex3/5: pick one element
random.sample(population, k)    # ex3: k DISTINCT picks -> perfect for a set
random.randint(a, b)            # ex3/6: random int, both ends included
```

The 3D distance is the Pythagorean theorem extended to three axes:
`math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)` — distance to the center
is the same formula against `(0, 0, 0)`.

### 16. Choosing the Right Collection

The module's takeaway, as a decision table:

| You need... | Use |
|-------------|-----|
| Ordered sequence, will grow/change | `list` |
| Fixed group of fields, must not change, dict-key/set-member | `tuple` |
| Uniqueness, fast membership, set algebra | `set` |
| Lookup by key, associations, counting | `dict` |
| A stream too big (or endless) for memory | **generator** |
| Transform/filter an existing collection | **comprehension** |

---

## 📂 Project Structure

```
data_quest/
├── ex0/
│   └── ft_command_quest.py        # sys.argv: your first (ready-made) list
├── ex1/
│   └── ft_score_analytics.py      # lists + stats, invalid input filtering
├── ex2/
│   └── ft_coordinate_system.py    # tuples, unpacking, 3D distance
├── ex3/
│   └── ft_achievement_tracker.py  # sets, union/intersection/difference
├── ex4/
│   └── ft_inventory_system.py     # dicts, keys/values/update, percentages
├── ex5/
│   └── ft_data_stream.py          # generators, yield, next(), streams
└── ex6/
    └── ft_data_alchemist.py       # list & dict comprehensions
```

---

## 🌾 Exercises

| Ex  | File | Authorized (beyond keywords) | Data structure unlocked |
|-----|------|------------------------------|-------------------------|
| 0 | `ft_command_quest.py` | `import sys`, `sys.argv`, `len()`, `print()` | **list** (read-only): `sys.argv` |
| 1 | `ft_score_analytics.py` | + `sum()`, `max()`, `min()` | **list** (built by you) + stats, error filtering |
| 2 | `ft_coordinate_system.py` | `import math`, `math.sqrt()`, `input()`, `round()`, `print()` | **tuple**: 3D coords, retry-until-valid input |
| 3 | `ft_achievement_tracker.py` | `len()`, `print()`, `import random`, `random.*`, `set()`, `set.union()`, `set.intersection()`, `set.difference()` | **set** + set algebra across ≥4 players |
| 4 | `ft_inventory_system.py` | `import sys`, `sys.argv`, `len()`, `print()`, `sum()`, `list()`, `round()`, `dict.keys()`, `dict.values()`, `dict.update()` | **dict**: parse `name:qty`, stats, tie → first from CLI |
| 5 | `ft_data_stream.py` | `next()`, `range()`, `len()`, `print()`, `import typing`, `typing.Generator`, `import random`, `random.*` | **generator**: endless `gen_event()`, draining `consume_event()` |
| 6 | `ft_data_alchemist.py` | `import random`, `random.*`, `print()`, `len()`, `sum()`, `round()` | **comprehensions**: 2 list + 2 dict |

**Progression logic:** ex0 hands you a list that already exists
(`sys.argv`), ex1 has you build your own, ex2 freezes data into tuples,
ex3 removes duplicates and adds algebra, ex4 adds key→value association,
ex5 makes data *flow* instead of *sit*, and ex6 condenses everything into
comprehension one-liners.

---

## 🚀 Usage

```bash
# ex1 — scores as CLI arguments; invalid ones discarded with a message
python3 ex1/ft_score_analytics.py 1500 2300 1800 2100 1950

# ex4 — inventory as name:quantity pairs
python3 ex4/ft_inventory_system.py sword:1 potion:5 shield:2 armor:3
```

```
=== Player Score Analytics ===
Scores processed: [1500, 2300, 1800, 2100, 1950]
Total players: 5
Total score: 9650
Average score: 1930.0
High score: 2300
Low score: 1500
Score range: 800
```

ex2 and ex5 are interactive / self-running:

```bash
python3 ex2/ft_coordinate_system.py    # prompts for 'x,y,z' until valid
python3 ex5/ft_data_stream.py          # streams 1000 events, then drains 10
```

---

## ✅ Testing & Linting

```bash
flake8 .
mypy ex0/ ex1/ ex2/ ex3/ ex4/ ex5/ ex6/
```

---

## ⚠️ Key Constraints

- Python **3.10+**, flake8-clean, **type hints everywhere** (mypy-checked).
- Exceptions handled gracefully — programs must not crash on bad input.
- **No file I/O** — data lives in memory or arrives via the command line.
- `str`, `int`, `float` and *all their methods* are always allowed; each
  data structure (and its methods) unlocks when an exercise introduces it.
- ex1: mixed valid/invalid input → discard invalid with a message, proceed
  with the rest; only if *nothing* valid remains, show the usage line.
- ex2: `get_player_pos()` retries until valid; distinguish bad syntax
  ("Invalid syntax") from a bad float (report the original `ValueError`).
- ex3: tune total/per-player achievement counts so all requested sets are
  likely non-empty; know why the empty set prints as `set()`.
- ex4: quantities stored as `int`; redundant keys and malformed pairs are
  reported and discarded; ties resolved by command-line order.
- ex5: `gen_event()` is *endless*; `consume_event()` must be consumed
  directly by `for .. in ..`.
- ex6: each comprehension on a **single line**; two list + two dict
  comprehensions, filtering the second of each.
- Be ready to discuss: alternate ways to skip `argv[0]`, why tuples can be
  dict keys, why membership in a set beats a list, how `next()` drives a
  generator.

---

## 📚 Resources

- [Data Structures — official tutorial](https://docs.python.org/3/tutorial/datastructures.html)
- [`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv)
- [Set types — reference](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Mapping types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Generators — Python wiki](https://wiki.python.org/moin/Generators)
- [`random` module](https://docs.python.org/3/library/random.html)
- [TimeComplexity — cost of operations per container](https://wiki.python.org/moin/TimeComplexity)

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

*Made with 🎮 at 42 Porto*

</div>
