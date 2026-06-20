#!/usr/bin/env python3

from elements import create_fire, create_water
from .elements import create_earth, create_air


__all__ = ["healing_potion", "strength_potion"]


def healing_potion() -> str:
    return (f"Healing potion brewed with '{create_earth()}'"
            f" and '{create_air()}'")


def strength_potion() -> str:
    return (f"Strength potion brewed with '{create_fire()}'"
            f" and '{create_water()}'")
