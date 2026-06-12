#!/usr/bin/env python3

import sys
import typing


def ft_ancient_text() -> None:
    if (len(sys.argv) != 2):
        print("Usage: ft_ancient_text.py <file>")
        return
    f: typing.IO[str] | None = None
    print("===  Cyber Archives Recovery ===\n"
          f"Accessing file '{sys.argv[1]}'")
    try:
        f = open(sys.argv[1], "r")
        print(f"---\n\n{f.read()}\n\n---")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    finally:
        if f is not None and not f.closed:
            f.close()
            print(f"File '{sys.argv[1]}' closed.")
    return


def main() -> None:
    ft_ancient_text()
    return


if __name__ == "__main__":
    main()
