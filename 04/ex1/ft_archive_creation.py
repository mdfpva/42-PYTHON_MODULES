#!/usr/bin/env python3

import sys
import typing


def ft_read_file() -> typing.IO[str] | None:
    f: typing.IO[str] | None = None
    print("=== Cyber Archives Recovery & Preservation ===\n"
          f"Accessing file '{sys.argv[1]}'")
    try:
        f = open(sys.argv[1], "r")
        print(f"---\n\n{f.read()}\n\n---")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    return f


def ft_transform(f: typing.IO[str]) -> str:
    f.seek(0)
    lines = f.read().splitlines()
    transformed = "\n".join(line + "#" if line else line for line in lines)
    return transformed


def ft_save_file(content: str) -> None:
    filename: str = input("Enter new file name (or empty): ")
    if not filename:
        print("Not saving data.")
        return
    f: typing.IO[str] | None = None
    try:
        f = open(filename, "w")
        f.write(content)
        print(f"Saving data to '{filename}'\nData saved in file '{filename}'.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error saving file '{filename}': {e}")
    finally:
        if f is not None and not f.closed:
            f.close()


def ft_archive_creation() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    f: typing.IO[str] | None = ft_read_file()
    if f is None:
        return
    transformed: str = ft_transform(f)
    print(f"Transform data:\n---\n\n{transformed}\n\n---")
    ft_save_file(transformed)


def main() -> None:
    ft_archive_creation()
    return


if __name__ == "__main__":
    main()
