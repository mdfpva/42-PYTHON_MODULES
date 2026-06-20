#!/usr/bin/env python3

import alchemy


def main() -> None:
    print("=== Alembic 4 ===\n"
          "Accessing the alchemy module using 'import alchemy'\n"
          f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached\n"
          "This will raise an exception!\n"
          "Testing hidden create_air: ", end="")
    print(alchemy.create_earth())
    return


if __name__ == "__main__":
    main()
