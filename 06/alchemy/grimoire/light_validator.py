#!/usr/bin/env python3

__all__ = ["validate_ingredients"]


def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients
    allowed = light_spell_allowed_ingredients()
    valid = any(i in ingredients.lower() for i in allowed)
    status = "VALID" if valid else "INVALID"
    return f"{ingredients} - {status}"
