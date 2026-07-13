<div align="center">

```
  ___              _      ___       _
 / __|___ ____ __ (_)__  |   \ __ _| |_ __ _
| (__/ _ (_-< '  \| / _| | |) / _` |  _/ _` |
 \___\___/__/_|_|_|_\__| |___/\__,_|\__\__,_|
```

🌌 42 🌌

### Discover Pydantic Models & Validation

**A 42 School Project — Python Piscine, Data Validation Module**

*Master Pydantic data validation through space-themed exercises. Learn to
create robust models, implement custom validation, and handle nested
structures while managing cosmic data streams.*

`Version 3.0` · `Python 3.10+` · `Pydantic 2.x` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. The Validation Problem](#1-the-validation-problem)
  - [2. BaseModel — Declarative Validated Classes](#2-basemodel--declarative-validated-classes)
  - [3. Type Coercion: Lax by Design](#3-type-coercion-lax-by-design)
  - [4. Field() — Constraints Beyond the Type](#4-field--constraints-beyond-the-type)
  - [5. Optional Fields and Defaults](#5-optional-fields-and-defaults)
  - [6. datetime Fields and ISO 8601](#6-datetime-fields-and-iso-8601)
  - [7. Enums as Closed Vocabularies](#7-enums-as-closed-vocabularies)
  - [8. ValidationError — Anatomy of a Failure](#8-validationerror--anatomy-of-a-failure)
  - [9. @model_validator(mode='after')](#9-model_validatormodeafter)
  - [10. Pydantic v1 vs v2 — Why @validator Is Off-Limits](#10-pydantic-v1-vs-v2--why-validator-is-off-limits)
  - [11. Cross-Field Business Rules](#11-cross-field-business-rules)
  - [12. Nested Models — Validation That Recurses](#12-nested-models--validation-that-recurses)
  - [13. Aggregate Rules over Collections](#13-aggregate-rules-over-collections)
  - [14. Serialization: model_dump and Friends](#14-serialization-model_dump-and-friends)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Key Constraints](#%EF%B8%8F-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🚀 About the Project

Welcome to the **Cosmic Data Observatory** — the galaxy's premier data
processing facility. As junior Data Engineer, you validate incoming
streams from space missions, alien contact reports, and station
monitoring systems.

The tool is **Pydantic 2.x**, Python's de-facto standard validation
library (the engine under FastAPI and countless data pipelines). Three
missions of increasing depth:

- **Space Station Data** (ex0) — `BaseModel` + `Field` constraints:
  declarative validation fundamentals.
- **Alien Contact Logs** (ex1) — `@model_validator` for business rules
  that span multiple fields.
- **Space Crew Management** (ex2) — nested models, lists of models, and
  aggregate safety rules over a whole crew.

The through-line: **make invalid data unrepresentable** — if an object
exists, it's already valid.

---

## 🧠 Concepts Covered (Theory)

### 1. The Validation Problem

Python type hints are *documentation checked statically* — at runtime,
nothing stops `crew_size="banana"` from landing in your object. Data
arriving from files, APIs, and users is untrusted by definition, and
hand-written `if not isinstance(...)` walls are verbose, inconsistent,
and easy to forget. **Pydantic** turns the type annotations you already
write into *enforced runtime contracts*: parsing and validation happen at
object construction, and failure is loud, structured, and immediate.
Garbage never gets in — so code past the boundary can trust its data.

### 2. BaseModel — Declarative Validated Classes

Everything starts by inheriting from `BaseModel` and declaring fields as
annotated class attributes:

```python
from datetime import datetime
from pydantic import BaseModel


class SpaceStation(BaseModel):
    station_id: str
    crew_size: int
    last_maintenance: datetime
    is_operational: bool = True
```

Instantiation **is** validation: `SpaceStation(**raw_dict)` checks every
field against its annotation, coercing where sensible (§3) and raising
`ValidationError` otherwise. Compared to a plain class or dataclass, the
`__init__`, the checks, and the helpful errors are all generated for you
— the model is a *schema that executes*.

### 3. Type Coercion: Lax by Design

The subject's first "Think About": *what happens when you pass a string
timestamp to a datetime field?* Answer: **it works**. Pydantic's default
("lax") mode doesn't demand exact types — it attempts *sensible
conversion*:

- `"6"` → `int 6`, `"85.5"` → `float 85.5`, `1` → `bool True`
- `"2024-03-15T10:30:00"` → `datetime(2024, 3, 15, 10, 30)` (§6)

Coercion is principled, not promiscuous: `"banana"` → `int` still fails,
and lossy conversions like `3.7` → `int` are rejected. The philosophy:
data arrives as strings (JSON, CSV, env vars) far more often than as
Python objects, so the boundary layer should absorb that reality. (A
strict mode exists for when exactness matters — knowing both exist is
defense material.)

### 4. Field() — Constraints Beyond the Type

The type says *what kind*; `Field()` says *which values*:

```python
from pydantic import BaseModel, Field


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
```

The core toolkit: `min_length`/`max_length` for strings and lists,
`ge`/`le` (≥/≤) and `gt`/`lt` (>/<) for numbers, `default=` for optional
values, plus `description=` for self-documenting schemas. Violations
produce precise messages — `crew_size=25` yields exactly the subject's
expected line, *"Input should be less than or equal to 20"*. Constraints
live **on the field, in the model, next to the type** — one source of
truth instead of checks scattered through the codebase.

### 5. Optional Fields and Defaults

Two related but distinct ideas, worth keeping straight in the defense:

```python
notes: str | None = Field(default=None, max_length=200)
is_operational: bool = True
```

- **A default** makes the field *omittable* — absent input, the default
  fills in (`is_operational` defaults to `True`).
- **`str | None`** makes `None` an *acceptable value* — the modern 3.10
  spelling of `Optional[str]`.

A field can be either, both (like `notes`), or neither (required).
Constraints still apply when a value *is* provided: a 300-character
`notes` fails even though the field is optional.

### 6. datetime Fields and ISO 8601

Annotating a field as `datetime` buys a full parser: Pydantic accepts
`datetime` objects, **ISO 8601 strings** (`"2024-03-15T10:30:00"`), and
numeric Unix timestamps, converting all of them to real `datetime`
instances. This is coercion (§3) at its most useful — JSON has no date
type, so every API ships dates as strings, and the model absorbs that
mismatch at the boundary instead of leaking string-typed dates through
the program.

### 7. Enums as Closed Vocabularies

`contact_type` isn't "any string" — it's one of exactly four values. The
standard-library `Enum` expresses that, and Pydantic enforces it:

```python
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"
```

Input `"radio"` coerces to `ContactType.RADIO`; input `"smoke_signals"`
fails with the allowed values listed. Inheriting from **both `str` and
`Enum`** makes members behave as strings too (printing, JSON, comparison
with `"radio"`) — the idiomatic pattern for string-valued enums. Typos
become impossible states: the type system now knows the vocabulary.

### 8. ValidationError — Anatomy of a Failure

When validation fails, Pydantic raises **one** `ValidationError`
aggregating **every** problem found — not just the first:

```python
from pydantic import ValidationError

try:
    SpaceStation(**bad_data)
except ValidationError as exc:
    for err in exc.errors():
        print(err["loc"], err["msg"])
```

Each entry carries `loc` (a tuple path to the offending field), `msg`
(human-readable message), and `type` (machine-readable error code). The
demonstration functions in all three exercises are built on this: catch
the exception, surface the message cleanly, never crash. The `loc` path
becomes essential with nesting (§12).

### 9. @model_validator(mode='after')

`Field` handles one field at a time; rules that *relate* fields need the
model-level hook:

```python
from pydantic import model_validator
from typing_extensions import Self   # or typing.Self on 3.11+


class AlienContact(BaseModel):
    ...

    @model_validator(mode="after")
    def check_business_rules(self) -> Self:
        if self.contact_type == ContactType.TELEPATHIC \
                and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        return self
```

Mechanics that matter: with `mode="after"` the validator runs **after**
all field validation, so `self` is a fully-typed, coerced instance —
`witness_count` is already an `int`, `contact_type` already an enum. You
raise `ValueError` for violations (Pydantic wraps it into a
`ValidationError`), and you **must `return self`** — the subject's tip,
because the returned object *is* the validated result; forget it and
construction yields `None`. (`mode="before"` also exists, running on the
raw input dict prior to coercion — useful for preprocessing, not needed
here.)

### 10. Pydantic v1 vs v2 — Why @validator Is Off-Limits

Pydantic 2 was a ground-up rewrite (validation core in Rust — the speed
jump is why the ecosystem migrated fast). The API changed with it, and
the subject pins the module to **v2 syntax**:

| v1 (deprecated) | v2 (this module) |
|---|---|
| `@validator("field")` | `@field_validator("field")` |
| `@root_validator` | `@model_validator(mode=...)` |
| `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
| `class Config:` | `model_config = ConfigDict(...)` |

Old tutorials and AI-generated snippets are full of v1 patterns — they
run with deprecation warnings today and break tomorrow. Recognizing which
dialect a snippet speaks is exactly the "check what the AI gave you"
skill the AI Instructions chapter demands.

### 11. Cross-Field Business Rules

Ex1's four rules are all *relations*, unexpressible as per-field
constraints:

- `contact_id` must start with `"AC"` — a **format** rule (checkable
  per-field, but co-located with the others for cohesion);
- physical contact ⇒ `is_verified` — one field **conditions** another;
- telepathic contact ⇒ `witness_count >= 3` — a **conditional
  threshold**;
- `signal_strength > 7.0` ⇒ `message_received` present — a
  **presence dependency**.

Each check raises a `ValueError` with the exact message the report
should surface. This is the module's conceptual jump: from *type-level*
integrity (ex0) to **domain-level** integrity — the data isn't just
well-formed, it's *plausible* under the Observatory's rules (fraudulent
combinations are rejected at the door).

### 12. Nested Models — Validation That Recurses

Models compose: a field's type can be another model, or a list of them:

```python
class SpaceMission(BaseModel):
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    ...
```

Validation **recurses automatically** — each dict inside the `crew` list
is parsed into a full `CrewMember`, with all its own field constraints
applied. The subject's second "Think About": *what happens when a
CrewMember fails inside a SpaceMission?* The failure **propagates up**
into the mission's single `ValidationError`, and `loc` pinpoints the
culprit through the structure: `("crew", 1, "age")` reads "second crew
member, field `age`". One `try/except` at the top validates an entire
object tree — structural validation for free, path-precise errors
included. Note `Field(min_length=1, max_length=12)` constrains the
**list itself** (crew size), while `CrewMember`'s own fields constrain
each element — two layers, declared once each.

### 13. Aggregate Rules over Collections

Ex2's safety rules quantify over the crew — counting, percentages,
universals — and live in the mission's `@model_validator(mode="after")`,
where `self.crew` is already a `list[CrewMember]` of validated objects:

```python
if not any(m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew):
    raise ValueError("Mission must have at least one Commander or Captain")

if self.duration_days > 365:
    experienced = sum(1 for m in self.crew if m.years_experience >= 5)
    if experienced / len(self.crew) < 0.5:
        raise ValueError("Long missions need 50% experienced crew")
```

`any()` expresses "at least one", `all()` "every" (all crew active), and
a comprehension-driven `sum()` handles the ratio. The layering is the
lesson: field constraints guard **values**, nested models guard
**structure**, aggregate validators guard **the whole** — launch
approval is a property of the crew, not of any single member.

### 14. Serialization: model_dump and Friends

Validation is a two-way door — validated models convert back to plain
data for storage or transmission:

```python
station.model_dump()        # → dict of Python objects
station.model_dump_json()   # → JSON string (datetimes → ISO 8601)
```

The v2 names (§10) matter. This closes the pipeline loop the module's
tools embody: `generated_data/` JSON → model (validate) → transform →
`model_dump_json()` → onward. Parse, don't validate-in-place; serialize,
don't hand-format.

---

## 📂 Project Structure

```
.
├── ex0/
│   └── space_station.py     # SpaceStation model + demo (valid/invalid)
├── ex1/
│   └── alien_contact.py     # ContactType enum, AlienContact + business rules
├── ex2/
│   └── space_crew.py        # Rank enum, CrewMember, SpaceMission (nested)
└── tools/                    # provided by the subject (not graded work)
    ├── data_generator.py     # realistic test data for all exercises
    ├── data_exporter.py      # JSON / CSV / Python export
    └── generated_data/       # ready-made datasets
```

Each exercise's `main()` demonstrates one valid instance, a clean
information display, one deliberately invalid instance, and the resulting
validation message.

---

## 📝 Exercises

| Ex | Model(s) | New Pydantic ground | Signature rule |
|----|----------|--------------------|----------------|
| 0 — Space Station Data | `SpaceStation` | `BaseModel`, `Field` ranges & lengths, defaults, optional `notes`, `datetime` coercion | `crew_size` 1–20 → *"Input should be less than or equal to 20"* |
| 1 — Alien Contact Logs | `ContactType(str, Enum)`, `AlienContact` | enum fields, `@model_validator(mode='after')`, cross-field logic, `return self` | *"Telepathic contact requires at least 3 witnesses"* |
| 2 — Space Crew Management | `Rank`, `CrewMember`, `SpaceMission` | nested models, `list[CrewMember]` with list-level bounds, aggregate validators (`any`/`all`/ratios), `loc` paths through structure | *"Mission must have at least one Commander or Captain"* |

---

## 💻 Usage

```bash
# Environment (mandatory: venv + pip, Pydantic 2.x)
python3 -m venv .venv
source .venv/bin/activate
pip install "pydantic>=2"

# Run the exercises
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py

# Optional: generate fresh test data with the provided tools
python3 tools/data_generator.py

# Style & types (must be clean)
flake8 ex0/ ex1/ ex2/
mypy ex0/ ex1/ ex2/
```

Every demo follows the same rhythm: build a valid model → print it →
attempt an invalid one → show the caught validation message. No
tracebacks, ever — `ValidationError` is always handled.

---

## ⚠️ Key Constraints

- Python **3.10 or later**, **flake8-clean**, fully type-annotated
  (**mypy**).
- **Pydantic 2.x on every exercise**, installed via **pip** inside a
  **virtual environment** (venv/virtualenv/conda) — the venv itself is
  never committed.
- **v2 syntax only**: `@model_validator(mode='after')`, never the
  deprecated v1 `@validator`; remember to `return self`.
- Beyond Pydantic: only standard-library modules (`json`, `csv`,
  `datetime`, …) and the provided `tools/` data; per-exercise Authorized
  is otherwise `None`.
- Exception handling protects the streams — demos display validation
  errors, they don't crash on them.
- Exercises build on each other; complete them **in order**, each in its
  own `exN/` directory, submitting only the requested files.

---

## 📚 Resources

- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic — Fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Pydantic — Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic — v1 → v2 Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [enum — standard library](https://docs.python.org/3/library/enum.html)
- [datetime — standard library](https://docs.python.org/3/library/datetime.html)

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

*Made with 🌌 at 42 Porto*

</div>
