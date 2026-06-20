#!/usr/bin/env python3

from alchemy.potions import healing_potion, strength_potion


def main() -> None:
    print("=== Distillation 0 ===\n"
          "Direct access to alchemy/potions.py\n"
          f"Testing strength_potion: {healing_potion()}\n"
          f"Testing heal alias: {strength_potion()}")
    return


if __name__ == "__main__":
    main()
