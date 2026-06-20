#!/usr/bin/env python3

from .dark_validator import validate_ingredients

__all__ = ["dark_spell_allowed_ingredients", "dark_spell_record"]


def dark_spell_allowed_ingredients() -> list:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result = validate_ingredients(ingredients)
    if "INVALID" in result:
        return f"Dark spell rejected: {spell_name} ({result})"
    return f"Dark spell recorded: {spell_name} ({result})"
