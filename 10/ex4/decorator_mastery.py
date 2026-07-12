#!/usr/bin/env python3

"""Master's Tower: decorator mastery and class methods."""
import functools
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """Decorate a spell to measure and report its execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    """Create a decorator that validates the spell's power argument."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get('power', args[-1] if args else 0)
            if not isinstance(power, int) or power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    """Create a decorator that retries a failing spell."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    """Guild managing mage registration and spell casting."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Check that a name has >= 3 chars, letters and spaces only."""
        stripped = name.replace(" ", "")
        return len(name) >= 3 and stripped.isalpha() and bool(stripped)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """Cast a spell when the power validator allows it."""
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    """Demonstrate decorators and static methods."""
    try:
        print("Testing spell timer...")

        @spell_timer
        def fireball() -> str:
            time.sleep(0.1)
            return "Fireball cast!"

        print(f"Result: {fireball()}")
        print(f"Metadata preserved: {fireball.__name__}")

        print("\nTesting power validator...")

        @power_validator(min_power=30)
        def lightning_bolt(power: int) -> str:
            return f"Lightning bolt strikes with {power} power"

        print(lightning_bolt(50))
        print(lightning_bolt(5))

        print("\nTesting retrying spell...")

        @retry_spell(max_attempts=3)
        def unstable_spell() -> str:
            raise RuntimeError("Mana surge")

        print(unstable_spell())

        attempts = iter([True, True, False])

        @retry_spell(max_attempts=3)
        def waaagh_spell() -> str:
            if next(attempts):
                raise RuntimeError("Not enough rage")
            return "Waaaaaaagh spelled !"

        print(waaagh_spell())

        print("\nTesting MageGuild...")
        print(MageGuild.validate_mage_name("Gandalf the Grey"))
        print(MageGuild.validate_mage_name("R2"))
        guild = MageGuild()
        print(guild.cast_spell("Lightning", 15))
        print(guild.cast_spell("Lightning", 5))
    except (TypeError, ValueError) as exc:
        print(f"Tower trial failed: {exc}")


if __name__ == "__main__":
    main()
