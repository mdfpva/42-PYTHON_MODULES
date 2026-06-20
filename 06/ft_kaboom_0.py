#!/usr/bin/env python3

from alchemy.grimoire import light_spell_record


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    print(f"Testing record light spell: {light_spell_record('Fantasy', 'Earth, wind and fire')}")
    return


if __name__ == "__main__":
    main()
