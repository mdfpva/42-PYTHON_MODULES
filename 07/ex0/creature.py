#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str, attack: str) -> None:
        self._name: str = name
        self._type: str = creature_type
        self._attack: str = attack
        return

    @abstractmethod
    def attack(self) -> str: ...

    def describe(self) -> str:
        return f"{self._name} is a {self._type} type Creature"
