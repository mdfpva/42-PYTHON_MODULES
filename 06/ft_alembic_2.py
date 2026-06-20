#!/usr/bin/env python3

import alchemy


def main() -> None:
    print("=== Alembic 2 ===\n"
          "Accessing alchemy/elements.py using 'import ...' structure\n"
          f"Testing create_earth: {alchemy.elements.create_earth()}")
    return


if __name__ == "__main__":
    main()
