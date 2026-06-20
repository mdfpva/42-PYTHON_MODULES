#!/usr/bin/env python3

from alchemy import create_air


def main() -> None:
    print("=== Alembic 3 ===\n"
          "Accessing alchemy module using"
          " 'from alchemy import ...'\n"
          f"Testing create_air: {create_air()}")
    return


if __name__ == "__main__":
    main()
