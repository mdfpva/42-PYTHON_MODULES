#!/usr/bin/env python3

"""Higher Realm: functions operating on functions."""
from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    """Return a spell that casts both spells and returns both results."""
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    """Return a spell whose power is multiplied before casting."""
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    """Return a spell that only casts when the condition holds."""
    def guarded(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return guarded


def spell_sequence(spells: list[Callable]) -> Callable:
    """Return a spell that casts every spell in order."""
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def fireball(target: str, power: int) -> str:
    """Deal fire damage to the target."""
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    """Restore hit points to the target."""
    return f"Heal restores {target} for {power} HP"


def shield(target: str, power: int) -> str:
    """Protect the target with a barrier."""
    return f"Shield protects {target} with {power} defense"


def main() -> None:
    """Demonstrate all higher-order spell modifiers."""
    try:
        if not all(map(callable, (fireball, heal, shield))):
            raise TypeError("Grimoire contains non-callable spells")

        print("Testing spell combiner...")
        combined = spell_combiner(fireball, heal)
        first, second = combined("Dragon", 50)
        print(f"Combined spell result: {first}, {second}")

        print("\nTesting power amplifier...")
        mega_fireball = power_amplifier(fireball, 3)
        print(f"Original: {fireball('Goblin', 10)}")
        print(f"Amplified: {mega_fireball('Goblin', 10)}")

        print("\nTesting conditional caster...")
        safe_heal = conditional_caster(
            lambda target, power: power >= 20, heal
        )
        print(f"Power 50: {safe_heal('Knight', 50)}")
        print(f"Power 5: {safe_heal('Knight', 5)}")

        print("\nTesting spell sequence...")
        combo = spell_sequence([shield, fireball, heal])
        for result in combo("Dragon", 30):
            print(f"  {result}")

        print("\nTesting composed modifiers...")
        ultimate = spell_sequence([
            power_amplifier(fireball, 5),
            conditional_caster(lambda t, p: p > 100, heal),
            spell_combiner(shield, heal),
        ])
        for result in ultimate("Lich King", 40):
            print(f"  {result}")
    except TypeError as exc:
        print(f"Spell crafting failed: {exc}")


if __name__ == "__main__":
    main()
