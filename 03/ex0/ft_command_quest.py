#!/usr/bin/env python3

import sys


def ft_command_quest() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    if (len(sys.argv) == 1):
        print("No arguments provided!")
    else:
        print(f"Arguments recived: {len(sys.argv) - 1}")
        for i in range(1, len(sys.argv)):
            print(f"Argument {i}: {sys.argv[i]}")
    print(f"Total arguments: {len(sys.argv)}")
    return


def main() -> None:
    ft_command_quest()
    return


if __name__ == "__main__":
    main()
