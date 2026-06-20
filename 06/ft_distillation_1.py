#!/usr/bin/env python3

import alchemy


def main() -> None:
    print("=== Distillation 1 ===\n"
          "Using: 'import alchemy' structure to access potions\n"
          f"Testing strength_potion: {alchemy.strength_potion()}\n"
          f"Testing heal alias: {alchemy.heal()}")
    return


if __name__ == "__main__":
    main()
