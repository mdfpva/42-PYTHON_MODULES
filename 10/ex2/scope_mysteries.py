#!/usr/bin/env python3

"""Memory Depths: lexical scoping and closures."""
from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    """Return a counter closure with independent persistent state."""
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable:
    """Return a closure that accumulates power from a base value."""
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    """Return a closure that enchants items with a fixed type."""
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchant


def memory_vault() -> dict[str, Callable]:
    """Return store/recall closures sharing a private memory dict."""
    memories: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        memories[key] = value

    def recall(key: str) -> Any:
        return memories.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main() -> None:
    """Demonstrate closures and lexical scoping."""
    try:
        print("Testing mage counter...")
        counter_a = mage_counter()
        counter_b = mage_counter()
        print(f"counter_a call 1: {counter_a()}")
        print(f"counter_a call 2: {counter_a()}")
        print(f"counter_b call 1: {counter_b()}")

        print("\nTesting spell accumulator...")
        accumulator = spell_accumulator(100)
        print(f"Base 100, add 20: {accumulator(20)}")
        print(f"Base 100, add 30: {accumulator(30)}")

        print("\nTesting enchantment factory...")
        flaming = enchantment_factory("Flaming")
        frozen = enchantment_factory("Frozen")
        print(flaming("Sword"))
        print(frozen("Shield"))

        print("\nTesting memory vault...")
        vault = memory_vault()
        vault['store']('secret', 42)
        print("Store 'secret' = 42")
        print(f"Recall 'secret': {vault['recall']('secret')}")
        print(f"Recall 'unknown': {vault['recall']('unknown')}")
    except (KeyError, TypeError) as exc:
        print(f"Memory corruption detected: {exc}")


if __name__ == "__main__":
    main()
