#!/usr/bin/env python3

"""Ancient Library: functools treasures."""
import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    """Reduce spell powers with the given operator-based operation."""
    if not spells:
        return 0
    operations: dict[str, Callable[[int, int], int]] = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': lambda a, b: max(a, b),
        'min': lambda a, b: min(a, b),
    }
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    return functools.reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    """Create element-specialized enchanters via functools.partial."""
    return {
        'fire': functools.partial(base_enchantment, 50, 'fire'),
        'ice': functools.partial(base_enchantment, 50, 'ice'),
        'lightning': functools.partial(base_enchantment, 50, 'lightning'),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Return the nth Fibonacci number with lru_cache memoization."""
    if n < 0:
        raise ValueError("Fibonacci is undefined for negative numbers")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """Create a singledispatch-based spell casting system."""
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast


def enchant(power: int, element: str, target: str) -> str:
    """Base enchantment following the (power, element, target) contract."""
    return f"{element.title()} enchantment ({power} power) on {target}"


def main() -> None:
    """Demonstrate the functools artifacts."""
    try:
        print("Testing spell reducer...")
        spells = [10, 20, 30, 40]
        print(f"Sum: {spell_reducer(spells, 'add')}")
        print(f"Product: {spell_reducer(spells, 'multiply')}")
        print(f"Max: {spell_reducer(spells, 'max')}")
        print(f"Min: {spell_reducer(spells, 'min')}")
        print(f"Empty: {spell_reducer([], 'add')}")
        try:
            spell_reducer(spells, 'divide')
        except ValueError as exc:
            print(f"Error handled: {exc}")

        print("\nTesting partial enchanter...")
        enchanters = partial_enchanter(enchant)
        for enchanter in enchanters.values():
            print(enchanter("Sword"))

        print("\nTesting memoized fibonacci...")
        print(f"Fib(0): {memoized_fibonacci(0)}")
        print(f"Fib(1): {memoized_fibonacci(1)}")
        print(f"Fib(10): {memoized_fibonacci(10)}")
        print(f"Fib(15): {memoized_fibonacci(15)}")
        print(f"Cache info: {memoized_fibonacci.cache_info()}")

        print("\nTesting spell dispatcher...")
        cast = spell_dispatcher()
        print(cast(42))
        print(cast("fireball"))
        print(cast(["heal", "shield", "haste"]))
        print(cast(3.14))
    except (ValueError, TypeError) as exc:
        print(f"Artifact malfunction: {exc}")


if __name__ == "__main__":
    main()
