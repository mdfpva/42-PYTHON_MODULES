#!/usr/bin/env python3

import sys
import typing


def ft_read_file() -> str | None:
    print("=== Cyber Archives Recovery & Preservation ===\n"
          f"Accessing file '{sys.argv[1]}'")
    f: typing.IO[str] | None = None
    content: str | None = None
    try:
        f = open(sys.argv[1], "r")
        content = f.read()
        print(f"---\n\n{content}\n\n---")
    except (FileNotFoundError, PermissionError) as e:
        sys.stderr.write(f"[STDERR] Error opening file '{sys.argv[1]}': {e}\n")
    finally:
        if f is not None and not f.closed:
            f.close()
            print(f"File '{sys.argv[1]}' closed.")
    return content


def ft_transform(content: str) -> str:
    lines = content.splitlines()
    lines_with_hash = [line + "#" if line != "" else "" for line in lines]
    return "\n".join(lines_with_hash)


def ft_save_file(content: str) -> None:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    filename: str = sys.stdin.readline().strip()
    if not filename:
        print("Not saving data.")
        return
    f: typing.IO[str] | None = None
    try:
        f = open(filename, "w")
        print(f"Saving data to '{filename}'")
        f.write(content)
        print(f"Data saved in file '{filename}'.")
    except (FileNotFoundError, PermissionError) as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        print("Data not saved.")
    finally:
        if f is not None and not f.closed:
            f.close()


def ft_stream_management() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_stream_management.py <file>")
        return
    content: str | None = ft_read_file()
    if content is None:
        return
    transformed: str = ft_transform(content)
    print(f"Transform data:\n---\n\n{transformed}\n\n---")
    ft_save_file(transformed)


def main() -> None:
    ft_stream_management()
    return


if __name__ == "__main__":
    main()
