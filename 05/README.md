<div align="center">

```
  ___         _       _  _
 / __|___  __| |___  | \| |_____ ___  _ ___
| (__/ _ \/ _` / -_) | .` / -_) \ / || (_-<
 \___\___/\__,_\___| |_|\_\___/_\_\\_,_/__/
```

🌐 42 🌐

### Polymorphic Data Streams in the Digital Matrix

**A 42 School Project — Python Piscine, OOP Module**

*Master abstract classes, method overriding, and subtype polymorphism while
building advanced data processing pipelines that adapt and evolve in real time.*

`Version 3.1` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Abstract Classes and ABC](#1-abstract-classes-and-abc)
  - [2. Abstract Methods and @abstractmethod](#2-abstract-methods-and-abstractmethod)
  - [3. Inheritance Hierarchies](#3-inheritance-hierarchies)
  - [4. Method Overriding](#4-method-overriding)
  - [5. Subtype Polymorphism](#5-subtype-polymorphism)
  - [6. The Liskov Substitution Principle (LSP)](#6-the-liskov-substitution-principle-lsp)
  - [7. Signature Specialization and Any](#7-signature-specialization-and-any)
  - [8. isinstance() and Runtime Type Checks](#8-isinstance-and-runtime-type-checks)
  - [9. Exception Handling as a Data Guard](#9-exception-handling-as-a-data-guard)
  - [10. FIFO Semantics — Queues Inside Objects](#10-fifo-semantics--queues-inside-objects)
  - [11. Duck Typing](#11-duck-typing)
  - [12. Protocol — Structural Typing](#12-protocol--structural-typing)
  - [13. Nominal vs Structural Typing](#13-nominal-vs-structural-typing)
  - [14. Composition: Registering Processors](#14-composition-registering-processors)
  - [15. Building CSV and JSON by Hand](#15-building-csv-and-json-by-hand)
  - [16. Type Annotations and mypy](#16-type-annotations-and-mypy)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Key Constraints](#%EF%B8%8F-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🚀 About the Project

The year is 2087. In the digital metropolis of Neo-Tokyo, the **Code Nexus**
is a cybernetic cathedral where billions of data streams converge, transform,
and evolve. Each stream carries its own digital signature — and yet a single
system must understand them all.

This module teaches how to make **one workflow handle many data types**
through the core pillars of object-oriented design:

- **Abstract base classes** (`abc.ABC`) that define contracts, not implementations.
- **Method overriding**, where each subclass provides its own behavior.
- **Subtype polymorphism**, letting code call `validate()`/`ingest()` on a
  `DataProcessor` without knowing (or caring) which concrete processor it is.
- **Duck typing formalized with `Protocol`**, plugging export backends into
  the pipeline without any inheritance relationship at all.

Three exercises build on each other: isolated processors (ex0), a polymorphic
stream router (ex1), and a full input→process→export pipeline (ex2).

---

## 🧠 Concepts Covered (Theory)

### 1. Abstract Classes and ABC

An **abstract class** is a class that is not meant to be instantiated
directly — it exists to define a *common interface* that subclasses must
implement. In Python this is done with the `abc` module:

```python
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...
```

Inheriting from `ABC` gives the class the `ABCMeta` metaclass, which enforces
one rule: **you cannot instantiate a class that still has unimplemented
abstract methods**.

```python
proc = DataProcessor()   # TypeError: Can't instantiate abstract class
```

This turns "please implement these methods" from a comment into a guarantee
checked at object-creation time.

### 2. Abstract Methods and @abstractmethod

`@abstractmethod` marks a method as part of the contract. Subclasses **must
override it** or they remain abstract themselves. An abstract class can mix:

- **Abstract methods** (`validate`, `ingest`) — no useful implementation,
  each subclass decides.
- **Concrete methods** (`output`) — implemented once in the base class and
  inherited as-is. This is *code reuse through inheritance*: the FIFO
  extraction logic is identical for every processor, so it lives in one place.

That mix is exactly what the subject asks for: two abstract methods, one
standard method.

### 3. Inheritance Hierarchies

Inheritance models an **"is-a" relationship**:

```
            DataProcessor (abstract)
           /       |        \
NumericProcessor TextProcessor LogProcessor
```

Every `NumericProcessor` *is a* `DataProcessor`. Consequences:

- Shared attributes/methods are written **once** in the parent.
- Any function typed to accept a `DataProcessor` accepts all three children.
- `super().__init__()` lets children reuse parent initialization (e.g. the
  internal storage list and the processing rank counter).

### 4. Method Overriding

**Overriding** means a subclass redefines a method inherited from its parent.
The subclass version *replaces* the parent version for instances of that
subclass. Python resolves which method runs at **runtime**, based on the
actual type of the object — this is called **dynamic dispatch**:

```python
proc: DataProcessor = TextProcessor()
proc.validate("hello")   # runs TextProcessor.validate, not the base one
```

The static type of the variable (`DataProcessor`) does not matter; the
**dynamic type** of the object (`TextProcessor`) decides.

### 5. Subtype Polymorphism

**Polymorphism** ("many forms") is the ability to use objects of different
classes through the same interface. The `DataStream` in ex1 is the textbook
example:

```python
for proc in self._processors:        # list[DataProcessor]
    if proc.validate(element):       # each proc answers differently
        proc.ingest(element)         # each proc processes differently
```

`DataStream` never mentions `NumericProcessor` or `LogProcessor`. It only
knows the abstract contract. Benefits:

- **Extensibility** — add a fourth processor tomorrow; `DataStream` code
  does not change (Open/Closed Principle).
- **Decoupling** — the router depends on an abstraction, not on concrete
  classes (Dependency Inversion).
- **Uniformity** — one loop handles all types.

### 6. The Liskov Substitution Principle (LSP)

LSP states: *anywhere a base-class object is expected, a subclass object must
work without breaking the program.* The subject encodes this subtly:

- `validate(self, data: Any) -> bool` **keeps the same signature** in every
  subclass. Why? Because the caller (`DataStream`) throws arbitrary data at
  it — narrowing the parameter type in a child would break substitutability
  (a parameter type may widen in a subclass, never narrow — this is
  **contravariance** of parameters).
- `ingest` *does* narrow its parameter in subclasses. That is technically an
  LSP violation, which is why the subject makes you provoke it deliberately:
  calling `ingest` with invalid data raises an exception, and mypy flags the
  call — **on purpose**. It's a lesson in what the type checker protects you
  from.

### 7. Signature Specialization and Any

`Any` is the escape hatch of Python's type system: it is compatible with
everything, in both directions. The base class uses it because it genuinely
cannot know what will arrive:

```python
# Base
def ingest(self, data: Any) -> None: ...

# NumericProcessor — specialized signature
def ingest(self, data: int | float | list[int | float]) -> None: ...
```

Python 3.10 lets you write unions natively with `|` instead of
`typing.Union`, and use `list[...]`/`dict[...]` instead of `typing.List`.
The specialized signature **documents** what the processor accepts and lets
mypy catch bad direct calls — while the `Any` in the base keeps the
polymorphic path open.

### 8. isinstance() and Runtime Type Checks

Static types vanish at runtime, so `validate` must check types dynamically:

```python
def validate(self, data: Any) -> bool:
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return True
    if isinstance(data, list):
        return all(isinstance(x, (int, float)) for x in data)
    return False
```

Classic trap worth knowing for the defense: **`bool` is a subclass of
`int`** in Python, so `isinstance(True, int)` is `True`. Whether you accept
or exclude booleans is a design decision — just be able to justify it.
Similarly, an **empty list** passes `all(...)` vacuously; decide and defend.

### 9. Exception Handling as a Data Guard

The subject requires that `ingest` **raises an exception** when fed invalid
data without prior validation. The idiom:

```python
def ingest(self, data: int | float | list[int | float]) -> None:
    if not self.validate(data):
        raise ValueError("Improper numeric data")
    ...
```

And on the caller side:

```python
try:
    numeric.ingest("foo")  # type: ignore intentionally NOT used
except ValueError as exc:
    print(f"Got exception: {exc}")
```

This is the **EAFP vs LBYL** discussion: *Look Before You Leap* (call
`validate` first) vs *Easier to Ask Forgiveness than Permission* (just call
`ingest` and catch). The architecture supports both, and exceptions are the
safety net protecting the stream from corruption.

### 10. FIFO Semantics — Queues Inside Objects

Each processor stores items and `output()` extracts **the oldest first**
along with its **processing rank** — a First-In, First-Out queue:

```python
def output(self) -> tuple[int, str]:
    item = self._storage.pop(0)      # oldest element
    rank = self._next_rank
    ...
    return (rank, item)
```

Design points to master:

- **Encapsulation**: storage and rank counter are internal state
  (conventionally prefixed `_`), touched only through methods.
- The rank is *per processor* and survives extraction — statistics in ex1
  report "total processed" (rank counter) and "remaining" (len of storage)
  as two independent numbers.
- With only lists authorized, `pop(0)` is the tool (O(n), fine here; in real
  code you'd reach for `collections.deque`).

### 11. Duck Typing

*"If it walks like a duck and quacks like a duck, it's a duck."* Duck typing
means an object's **suitability is determined by the methods it has**, not by
its class or ancestry. Ex2's export plugins don't inherit from anything:

```python
class CSVExportPlugin:                 # no base class!
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
```

Any object with a matching `process_output` method works. That is the
opposite philosophy from ex0/ex1's inheritance — and the module makes you use
**both**, because real systems mix them.

### 12. Protocol — Structural Typing

Raw duck typing is invisible to mypy. `typing.Protocol` fixes that by
formalizing the duck:

```python
from typing import Protocol


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
```

Now `output_pipeline(self, nb: int, plugin: ExportPlugin)` type-checks: mypy
verifies that whatever you pass **has a compatible `process_output`
method** — no inheritance required. A `Protocol` is a *contract checked by
shape*. (You never instantiate the Protocol itself; it only exists for
typing.)

### 13. Nominal vs Structural Typing

The module's deep lesson, worth articulating in the defense:

| | Nominal (ABC) | Structural (Protocol) |
|---|---|---|
| Compatibility by | declared inheritance | matching method shapes |
| Enforced | at instantiation (runtime) | by mypy (static) |
| Coupling | plugin must import the base | zero coupling |
| Best for | closed family you control | open plugin ecosystems |

`DataProcessor` is **nominal**: subclasses explicitly opt in via inheritance.
`ExportPlugin` is **structural**: any third-party class with the right method
just works. Choosing between them is an architecture decision, not a syntax
one.

### 14. Composition: Registering Processors

`DataStream` doesn't inherit from `DataProcessor` — it **has** processors
(a *"has-a"* relationship, i.e. **composition**):

```python
def register_processor(self, proc: DataProcessor) -> None:
    self._processors.append(proc)
```

Routing then becomes first-match dispatch: for each stream element, ask each
registered processor `validate(element)`; the first that says `True` ingests
it; if none does, print a `DataStream error`. Registration order therefore
*matters* — a fact evaluators like to poke at.

### 15. Building CSV and JSON by Hand

No `csv`/`json` imports allowed — you build the strings manually, which
forces you to know the formats:

- **CSV**: values joined by commas — `",".join(value for _, value in data)`.
  Real CSV needs quoting/escaping rules; the exercise data avoids them, but
  know they exist.
- **JSON**: keys and string values wrapped in **double quotes** (single
  quotes are invalid JSON — a favourite trap):

```python
pairs = ", ".join(f'"item_{rank}": "{value}"' for rank, value in data)
print("{" + pairs + "}")
```

The rank returned by `output()` becomes the JSON key (`item_3`, `item_4`,
...), which is why `output` returns a `tuple[int, str]` and not just a
string.

### 16. Type Annotations and mypy

The whole module runs under comprehensive annotations checked with mypy:

- Modern 3.10+ syntax: `int | float`, `list[tuple[int, str]]`,
  `dict[str, str]` — no `Optional`, `Union`, `List` from `typing` needed.
- The **one intentional mypy warning**: passing an invalid literal to a
  specialized `ingest` in ex0's test. Leave it — the subject wants you to see
  mypy catching the LSP-violating call that only an exception catches at
  runtime.
- `flake8` enforces PEP 8 (79-char lines, two blank lines between top-level
  defs, etc.). Clean output from both tools is part of the deliverable.

---

## 📂 Project Structure

```
.
├── ex0/
│   └── data_processor.py    # DataProcessor ABC + 3 specialized processors
├── ex1/
│   └── data_stream.py       # DataStream: polymorphic routing + statistics
└── ex2/
    └── data_pipeline.py     # ExportPlugin Protocol + CSV/JSON plugins
```

---

## 📝 Exercises

| Ex | File | Goal | Core concepts |
|----|------|------|---------------|
| 0 | `data_processor.py` | Abstract `DataProcessor` with `validate`/`ingest` (abstract) and `output` (concrete); `NumericProcessor`, `TextProcessor`, `LogProcessor` | ABC, `@abstractmethod`, overriding, signature specialization, exceptions, FIFO `output` |
| 1 | `data_stream.py` | `DataStream` routes a mixed `list[Any]` to registered processors; prints errors for unroutable elements and per-processor statistics | Subtype polymorphism, dynamic dispatch, composition, `register_processor` / `process_stream` / `print_processors_stats` |
| 2 | `data_pipeline.py` | `ExportPlugin(Protocol)` contract; `output_pipeline(nb, plugin)` consumes `nb` items from every processor and exports them; hand-built CSV & JSON plugins | Duck typing, `Protocol`, structural typing, manual serialization |

**Processor domains (ex0):**

| Processor | Accepts | Stored as |
|-----------|---------|-----------|
| `NumericProcessor` | `int`, `float`, lists of both (mixed OK) | each item converted to `str` |
| `TextProcessor` | `str`, `list[str]` | each item as-is |
| `LogProcessor` | `dict[str, str]`, `list[dict[str, str]]` | `"LEVEL: message"` strings |

---

## 💻 Usage

```bash
# Run each exercise
python3 ex0/data_processor.py
python3 ex1/data_stream.py
python3 ex2/data_pipeline.py

# Style check (must be clean)
flake8 ex0/ ex1/ ex2/

# Type check (one intentional warning in ex0's test section)
mypy ex0/data_processor.py
mypy ex1/data_stream.py
mypy ex2/data_pipeline.py
```

Expected flavor of output (ex1):

```
== DataStream statistics ==
Numeric Processor: total 8 items processed, remaining 5 on processor
Text Processor: total 3 items processed, remaining 1 on processor
Log Processor: total 2 items processed, remaining 1 on processor
```

---

## ⚠️ Key Constraints

- Python **3.10 or later** — native `|` unions and builtin generics.
- **flake8-clean** code; comprehensive type annotations checked with **mypy**.
- Authorized imports: **`abc` and `typing` only** (plus builtins and standard
  types/collections with their methods).
- Exception handling must protect the streams: invalid `ingest` **raises**.
- `output()` returns `tuple[int, str]` and is **not** overridden.
- CSV/JSON strings are built **manually** — no `csv` or `json` imports.
- Ex0's test deliberately triggers **one mypy warning** (invalid ingestion).

---

## 📚 Resources

- [abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [typing.Protocol — Structural subtyping](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 544 — Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
- [PEP 604 — `X | Y` union syntax](https://peps.python.org/pep-0604/)
- [Python docs — Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
- [mypy — Protocols and structural subtyping](https://mypy.readthedocs.io/en/stable/protocols.html)
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

*Made with 🌐 at 42 Porto*

</div>
