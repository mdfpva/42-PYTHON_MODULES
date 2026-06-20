#!/usr/bin/env python3

from elements import create_water


def main() -> None:
    print("=== Alembic 1 ===\n"
          "Using: 'from ... import ...' structure to access elements.py\n"
          f"Testing create_water: {create_water()}")
    return


if __name__ == "__main__":
    main()
