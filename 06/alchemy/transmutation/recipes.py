#!/usr/bin/env python3

from elements import create_fire
from alchemy import create_air
from alchemy.potions import strength_potion


__all__ = ["lead_to_gold"]


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: brew "
            f"'{create_air()}' and '{strength_potion()}'"
            f" mixed with '{create_fire()}'")
