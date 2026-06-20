#!/usr/bin/env python3

import alchemy.transmutation as transmutation


def main() -> None:
    print("=== Transmutation 1 ===\n"
          "Import transmutation module directly\n"
          "Testing lead to gold:"
          f"{transmutation.lead_to_gold()}")
    return


if __name__ == "__main__":
    main()
