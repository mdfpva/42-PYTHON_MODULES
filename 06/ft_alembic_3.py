#!/usr/bin/env python3

from alchemy.elements import create_air


def main() -> None:
    print("=== Alembic 3 ===\n"
          "Accessing alchemy/elements.py using"
          " 'from ... import ...' structure\n"
          f"Testing create_air: {create_air()}")
    return


if __name__ == "__main__":
    main()
