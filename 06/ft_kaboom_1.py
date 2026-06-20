#!/usr/bin/env python3

print("=== Kaboom 1 ===")
print("Access to alchemy/grimoire/dark_spellbook.py directly")
print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")

from alchemy.grimoire.dark_spellbook import dark_spell_record


def main() -> None:
    print(f"Testing record dark spell: {dark_spell_record('Evil Fantasy', 'bats and frogs')}")
    return


if __name__ == "__main__":
    main()
