# Module 06 — The Codex: Mastering Python's Import Mysteries

*by mide-fre*

---

## Description

An exploration of Python's import system through the metaphor of an alchemist's laboratory. This module covers the full spectrum of import mechanics — from basic module access to nested packages, absolute vs relative imports, and circular dependency resolution.

The project is divided into four parts, each building on the previous:

- **Part I — The Alembic**: Basic import structures (`import`, `from ... import`) applied to local modules and packages.
- **Part II — Distillation**: Nested imports across package boundaries, function aliasing via `__init__.py`.
- **Part III — The Great Transmutation**: Subpackage architecture, combining absolute and relative imports within the same module.
- **Part IV — Avoid the Explosion**: Identifying and resolving circular dependencies using lazy imports.

---

## Structure

```
06/
├── elements.py                          # Root module — fire & water
├── ft_alembic_{0..5}.py                 # Part I test scripts
├── ft_distillation_{0,1}.py             # Part II test scripts
├── ft_transmutation_{0,1,2}.py          # Part III test scripts
├── ft_kaboom_{0,1}.py                   # Part IV test scripts
└── alchemy/
    ├── __init__.py                      # Exposes: create_air, strength_potion, heal, lead_to_gold
    ├── elements.py                      # Earth & air
    ├── potions.py                       # Healing & strength potions
    ├── transmutation/
    │   ├── __init__.py
    │   └── recipes.py                   # lead_to_gold — mixes absolute & relative imports
    └── grimoire/
        ├── __init__.py
        ├── light_spellbook.py           # Safe — uses lazy import to break circular dep
        ├── light_validator.py           # Validates light spell ingredients
        ├── dark_spellbook.py            # Dangerous — circular dep at module level
        └── dark_validator.py            # Imports from dark_spellbook → explosion
```

---

## Instructions

**Requirements**: Python 3.10+, flake8, mypy

**Run any script from the project root:**

```bash
cd 06/
python3 ft_alembic_0.py
python3 ft_distillation_0.py
python3 ft_transmutation_0.py
python3 ft_kaboom_0.py   # works
python3 ft_kaboom_1.py   # intentionally explodes
```

> All scripts must be run from `06/` — relative and absolute imports depend on this working directory.

**Lint & type check:**

```bash
flake8 .
mypy .
```

> `ft_alembic_4.py` raises a mypy error on purpose (`alchemy.create_earth` is not exposed), as required by the subject.

---

## Key Concepts

### Absolute vs Relative imports

```python
# Absolute — full path from sys.path root
from elements import create_fire
from alchemy.potions import strength_potion

# Relative — relative to current file location
from .elements import create_air       # same package
from ..potions import strength_potion  # one level up
```

Use **absolute** for modules outside your package (root modules, installed libraries).
Use **relative** for modules within the same package — they survive package renames.

### Controlling the public interface via `__init__.py`

```python
# alchemy/__init__.py
from .elements import create_air
from .potions import strength_potion, healing_potion as heal
from .transmutation import lead_to_gold

__all__ = ["create_air", "strength_potion", "heal", "lead_to_gold"]
```

Only what is in `__all__` is exposed through `import alchemy`. Functions not listed (e.g. `create_earth`) raise `AttributeError` when accessed.

### Circular dependency — and how to break it

Dark magic creates a circular import at module level:

```
dark_spellbook  →  imports dark_validator
dark_validator  →  imports dark_spellbook   ← loop → ImportError
```

Light magic breaks the cycle with a **lazy import** (import inside the function body):

```python
# light_validator.py
def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients  # only runs on call
    ...
```

By the time `validate_ingredients()` is called, `light_spellbook` is already fully loaded in `sys.modules` — no conflict.

Other valid approaches: **separate constants module**, **dependency inversion**, **restructuring**.

---

## Resources

- [Python docs — The import system](https://docs.python.org/3/reference/import.html)
- [PEP 328 — Relative imports](https://peps.python.org/pep-0328/)
- [PEP 366 — `__package__`](https://peps.python.org/pep-0366/)
- [Real Python — Circular imports](https://realpython.com/python-import/#handle-cyclical-imports)

*AI tool (Claude by Anthropic) was used to review solutions and explain concepts during development.*
