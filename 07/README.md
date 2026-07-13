<div align="center">

```
 ___       _        ___         _
|   \ __ _| |_ __ _|   \ ___ __| |__
| |) / _` |  _/ _` | |) / -_) _| / /
|___/\__,_|\__\__,_|___/\___\__|_\_\
```

🃏 42 🃏

### Abstract Card Architecture

**A 42 School Project — Python Piscine, Design Patterns Module**

*Master Python's design patterns with abstract classes and interfaces by
building a modular card system. Gotta catch 'em all; but sometimes, the real
treasure is the skills we made along the way.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Design Patterns — Why They Exist](#1-design-patterns--why-they-exist)
  - [2. The Factory Idea](#2-the-factory-idea)
  - [3. The Abstract Factory Pattern](#3-the-abstract-factory-pattern)
  - [4. Programming Against the Abstraction](#4-programming-against-the-abstraction)
  - [5. Hiding Concretes: the Package as an API Boundary](#5-hiding-concretes-the-package-as-an-api-boundary)
  - [6. Multiple Inheritance](#6-multiple-inheritance)
  - [7. Capabilities as Mixins](#7-capabilities-as-mixins)
  - [8. The MRO — Method Resolution Order](#8-the-mro--method-resolution-order)
  - [9. Stateful Behavior: the Transform Capability](#9-stateful-behavior-the-transform-capability)
  - [10. The Strategy Pattern](#10-the-strategy-pattern)
  - [11. Capability Detection with isinstance()](#11-capability-detection-with-isinstance)
  - [12. Custom Exceptions](#12-custom-exceptions)
  - [13. Composition over Inheritance: the Opponent Tuple](#13-composition-over-inheritance-the-opponent-tuple)
  - [14. Round-Robin Pairing](#14-round-robin-pairing)
  - [15. The Patterns Working Together](#15-the-patterns-working-together)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Key Constraints](#%EF%B8%8F-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🚀 About the Project

You are designing a creature-based card game inspired by monster-collecting
classics. Cards aren't static objects — they belong to **families**, they
**evolve**, they carry **capabilities** used strategically. The challenge:
a system flexible enough for thousands of card types while staying clean and
maintainable.

Building on the abstract classes and polymorphism of the previous module,
this one climbs to **senior-architect patterns**:

- **Abstract Factory** (ex0) — families of creatures created through a
  uniform factory interface, with concretes fully hidden behind the package.
- **Capabilities / Mixins** (ex1) — orthogonal behaviors (`heal`,
  `transform`) added through multiple inheritance, deliberately *outside*
  the `Creature` hierarchy.
- **Strategy** (ex2) — battle behavior extracted into interchangeable
  strategy objects, so one `battle` function runs a whole tournament without
  knowing any capability exists.

---

## 🧠 Concepts Covered (Theory)

### 1. Design Patterns — Why They Exist

A **design pattern** is a named, reusable solution to a recurring design
problem — vocabulary as much as technique. Saying "this is an Abstract
Factory" transmits an entire structure (roles, relationships, trade-offs)
in three words. The patterns here are classics from the Gang of Four
catalog, and they share one root idea, the module's real lesson:

> **Encapsulate what varies, and depend on abstractions, not concretions.**

Creature families vary → factory. Capabilities vary → mixin. Battle
behavior varies → strategy.

### 2. The Factory Idea

Calling `Flameling()` directly couples the caller to a concrete class
forever. A **factory** moves object creation behind a method, so the caller
asks *"give me a base creature"* without naming which one:

```python
creature = factory.create_base()   # which class? the factory decides
```

Creation becomes a swappable decision. That indirection is what lets
`battle.py` test *any* family with one function.

### 3. The Abstract Factory Pattern

**Abstract Factory** goes one step further: a factory interface for creating
**families of related objects** — here, a base creature and its evolution
that must belong together:

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...

    @abstractmethod
    def create_evolved(self) -> Creature: ...


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()
```

Two parallel hierarchies emerge — products (`Creature` → Flameling, Pyrodon,
Aquabub, Torragon) and factories (`CreatureFactory` → FlameFactory,
AquaFactory) — with **family consistency** as the pattern's guarantee: a
`FlameFactory` can never accidentally hand you a Torragon. Note the return
type is the *abstract* `Creature`, not the concrete class: the signature
itself hides the product.

### 4. Programming Against the Abstraction

The `battle.py` test scenario encodes the pattern's payoff — a **single**
function that receives *any* factory:

```python
def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    ...
```

This function will work, unchanged, for every family invented in ex1 and
any future one — the Open/Closed Principle in action: **open for extension
(new factories), closed for modification (test code never changes)**.

### 5. Hiding Concretes: the Package as an API Boundary

The subject's sharpest constraint: *the package cannot expose concrete
Creatures — only factories.* This weaponizes the previous module's
`__init__.py` lesson as an architectural tool:

```python
# ex0/__init__.py
from .factories import FlameFactory, AquaFactory

__all__ = ["FlameFactory", "AquaFactory"]
```

`battle.py` **cannot** write `Flameling()` — the name isn't exported. The
only path to a creature is through a factory. This is enforced
encapsulation: the module boundary makes the wrong design physically
unavailable, not merely discouraged. (Concrete classes typically live in an
internal module the `__init__.py` simply doesn't re-export.)

### 6. Multiple Inheritance

Python allows a class to inherit from **several bases**:

```python
class Sproutling(Creature, HealCapability):
    ...
```

`Sproutling` *is a* Creature **and** *has the* heal contract — it must
implement the abstract methods of **both** parents (`attack` from Creature,
`heal` from HealCapability) before it can be instantiated. `isinstance`
answers `True` for both bases. Multiple inheritance is powerful and
dangerous in equal measure; the discipline that keeps it safe is the mixin
style below plus understanding the MRO (§8).

### 7. Capabilities as Mixins

The subject's key design sentence: capabilities *"will not inherit from the
Creature base class"* — because one day they might apply to non-Creatures
(items? trainers?). A **mixin** is exactly that: a small class encoding one
orthogonal behavior, designed to be *mixed into* hierarchies it knows
nothing about:

```python
class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str: ...


class TransformCapability(ABC):
    @abstractmethod
    def transform(self) -> str: ...

    @abstractmethod
    def revert(self) -> str: ...
```

Keeping capabilities out of the `Creature` tree avoids the classic trap of
cramming optional features into a base class (forcing every creature to
carry `heal` it doesn't use) or exploding the hierarchy into
`HealingCreature`, `TransformingCreature`,
`HealingTransformingCreature`... With mixins, features **compose**
combinatorially instead of multiplying subclasses. This is
interface-segregation thinking: many small contracts beat one fat one.

### 8. The MRO — Method Resolution Order

With multiple bases, which parent's method wins? Python computes a
deterministic **Method Resolution Order** using the C3 linearization:

```python
Sproutling.__mro__
# (Sproutling, Creature, HealCapability, ABC, object)
```

Rules of thumb that matter for the defense: a class always precedes its
parents, and parents appear in the order listed in the class statement —
so `class Sproutling(Creature, HealCapability)` searches `Creature` before
`HealCapability`. `super()` doesn't mean "my parent"; it means **"the next
class in the MRO"**, which is what makes cooperative `__init__` chains work
across multiple bases. If two bases define the same method name, the MRO
(not luck) decides — and `SomeClass.__mro__` is your debugging tool.

### 9. Stateful Behavior: the Transform Capability

`TransformCapability` is more than a method bundle — it demands a
**persistent state attribute** that *changes what `attack` does*:

```python
class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        super().__init__("Shiftling", "Normal")
        self._transformed = False

    def transform(self) -> str:
        self._transformed = True
        return "Shiftling shifts into a sharper form!"

    def attack(self) -> str:
        if self._transformed:
            return "Shiftling performs a boosted strike!"
        return "Shiftling attacks normally."
```

The same method call produces different output depending on internal state —
`attack` / `transform` / `attack` / `revert` demonstrates it. This is a
miniature **State** idea living inside a mixin: behavior varies with an
encapsulated flag, and only the object itself mutates it.

### 10. The Strategy Pattern

Ex2's problem: a tournament must run creatures whose rituals differ
(healers attack-then-heal; transformers transform-attack-revert). Naive
battle code becomes a chain of `if isinstance(...)` that grows with every
capability. The **Strategy pattern** extracts each ritual into an
interchangeable object with a common interface:

```python
class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...

    @abstractmethod
    def act(self, creature: Creature) -> str: ...


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> str:
        ...  # transform + attack + revert
```

The tournament calls `strategy.act(creature)` and nothing else — battle
code that is **capability-blind**, which is precisely the subject's teaser
("we need battle code that is aware of each capability. Or maybe not?").
Adding a fourth ritual tomorrow = one new class, zero changes to `battle`.
Strategy differs from plain polymorphism in *where* behavior lives: not in
the creature (inheritance) but in a separate object **paired with** it at
runtime — behavior becomes a parameter.

### 11. Capability Detection with isinstance()

`is_valid` bridges strategies and mixins: because capabilities are classes,
`isinstance(creature, TransformCapability)` is a clean runtime test for
"does this creature speak transform?". `NormalStrategy.is_valid` returns
`True` for any `Creature`; the specialized strategies gate on their mixin.
This is the mixin architecture paying off a second time — the capability
class doubles as a **queryable marker**. (The duck-typing alternative,
`hasattr(creature, "transform")`, works but checks a name rather than a
declared contract; with ABCs available, the explicit contract is the
stronger check.)

### 12. Custom Exceptions

An invalid creature–strategy pairing whose `act` is forced must raise "a
dedicated exception with a clear message" — meaning a **domain-specific
exception class**, not a recycled `ValueError`:

```python
class InvalidStrategyError(Exception):
    """Raised when a strategy is applied to an unsuitable Creature."""
```

Benefits: callers can catch *exactly* this failure
(`except InvalidStrategyError`), the class name documents the failure mode,
and the message carries the specifics (`"Invalid Creature 'Flameling' for
this aggressive strategy"`). The tournament demonstrates graceful handling:
catch, print `Battle error, aborting tournament: ...`, and stop — no
traceback, no crash, per the general instructions.

### 13. Composition over Inheritance: the Opponent Tuple

An opponent is a `tuple[CreatureFactory, BattleStrategy]` — a creature
source **paired with** a behavior. Nothing inherits from anything here:
the pairing is pure **composition**, assembled at runtime, and any factory
can be matched with any strategy (validity checked later by `is_valid`).
Compare the alternative — subclassing `AggressiveFlameCreature` for every
combination — and the flexibility gap is the whole argument for
*composition over inheritance*.

### 14. Round-Robin Pairing

"Each opponent fights once all other opponents" is a **round-robin**: all
unordered pairs, no repeats, no self-fights. The idiomatic index pattern:

```python
for i in range(len(opponents)):
    for j in range(i + 1, len(opponents)):
        fight(opponents[i], opponents[j])
```

`j = i + 1` is what guarantees each pair appears exactly once — n opponents
produce n·(n−1)/2 battles (3 opponents → 3 battles, matching the example).
A classic evaluator question: *why not `j in range(len(...))` with
`i != j`?* Because that yields each pair twice, in both orders.

### 15. The Patterns Working Together

The final `tournament.py` composes all three exercises into one pipeline:

```
Abstract Factory  →  creates creatures without naming classes
Mixins            →  give creatures orthogonal capabilities
Strategy          →  runs each creature's ritual, capability-blind
```

The `battle` function touches only three abstractions — `CreatureFactory`,
`Creature`, `BattleStrategy` — and never a single concrete class. That's
the Dependency Inversion Principle end-to-end, and the reason this codebase
could absorb a thousand new card types without editing the tournament.

---

## 📂 Project Structure

```
.
├── ex0/                     # Abstract Factory package
│   ├── __init__.py          # exposes ONLY FlameFactory, AquaFactory
│   └── ...                  # Creature ABC, concretes, CreatureFactory ABC
├── ex1/                     # Capabilities package (builds on ex0)
│   ├── __init__.py          # exposes ONLY Healing/TransformCreatureFactory
│   └── ...                  # HealCapability, TransformCapability, concretes
├── ex2/                     # Strategy package
│   ├── __init__.py
│   └── ...                  # BattleStrategy + Normal/Aggressive/Defensive
├── battle.py                # ex0 test — factories & a fight
├── capacitor.py             # ex1 test — heal & transform rituals
└── tournament.py            # ex2 test — round-robin tournament
```

Test scripts live at the **repo root**; each `exN/` is a proper package with
a **mandatory `__init__.py`**.

---

## 📝 Exercises

| Ex | Pattern | Deliverables | Core idea |
|----|---------|--------------|-----------|
| 0 — Creature Factory | Abstract Factory | `Creature` ABC (abstract `attack`, concrete `describe`), 4 concretes, `CreatureFactory` ABC (`create_base`, `create_evolved`), `FlameFactory`, `AquaFactory`; `battle.py` | Families of related products behind one interface; package exposes factories only; one test function serves every factory |
| 1 — Capabilities | Mixins / multiple inheritance | `HealCapability`, `TransformCapability` (independent of `Creature`), Sproutling/Bloomelle + Shiftling/Morphagon, two new factories; `capacitor.py` | Orthogonal behaviors composed in, not inherited down; transform state persists and alters `attack` |
| 2 — Abstract Strategy | Strategy | `BattleStrategy` ABC (`is_valid`, `act`), Normal/Aggressive/Defensive strategies, dedicated exception; `tournament.py` with a **single** `battle` function | Behavior as a runtime-pluggable object; capability-blind tournament; graceful handling of invalid pairings |

---

## 💻 Usage

```bash
# Exercise 0 — abstract factory
python3 battle.py

# Exercise 1 — capabilities
python3 capacitor.py

# Exercise 2 — strategy tournament
python3 tournament.py

# Style & types (must be clean)
flake8 .
mypy .
```

Flavor of the tournament error path (handled, no crash):

```
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

---

## ⚠️ Key Constraints

- Python **3.10 or later**, **flake8-clean**, fully type-annotated (**mypy**).
- Authorized imports: **`abc` and `typing`** (plus builtins and standard
  types); external libraries forbidden; no `eval()` / `exec()`.
- `__init__.py` is **mandatory** in every exercise folder; test scripts sit
  at the repo root.
- ex0/ex1 packages must **not** expose concrete Creatures — factories only.
- Capability ABCs must **not** inherit from `Creature`.
- ex1 **builds on ex0**; ex2 uses factories from both.
- Exceptions are handled gracefully — the tournament aborts with a message,
  never a traceback.
- Prerequisites: inheritance, abstract classes, polymorphism, and imports
  (previous modules).

---

## 📚 Resources

- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [Python docs — Multiple inheritance](https://docs.python.org/3/tutorial/classes.html#multiple-inheritance)
- [The Python MRO (C3 linearization)](https://docs.python.org/3/howto/mro.html)
- [Refactoring Guru — Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)
- [Refactoring Guru — Strategy](https://refactoring.guru/design-patterns/strategy)
- [Python docs — super()](https://docs.python.org/3/library/functions.html#super)
- *Design Patterns: Elements of Reusable Object-Oriented Software* — Gamma, Helm, Johnson, Vlissides (the "Gang of Four")

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

*Made with 🃏 at 42 Porto*

</div>
