#!/usr/bin/usr python3

from .creature import Creature


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire", "Ember")
        return

    def attack(self) -> str:
        return f"{self._name} uses {self._attack}!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying", "Flamethrower")
        return

    def attack(self) -> str:
        return f"{self._name} uses {self._attack}!"


class Aquabub(Creature):
    def __init__(self) -> None:
        super().__init__("Aquabub", "Water", "Water Gun")
        return

    def attack(self) -> str:
        return f"{self._name} uses {self._attack}!"


class Torragon(Creature):
    def __init__(self) -> None:
        super().__init__("Torragon", "Water", "Hydro Pump")
        return

    def attack(self) -> str:
        return f"{self._name} uses {self._attack}!"
