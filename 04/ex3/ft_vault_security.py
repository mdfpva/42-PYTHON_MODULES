#!/usr/bin/env python3

def secure_archive(
    filename: str,
    action: str = "read",
    content: str = ""
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as f:
                return (True, f.read())
        else:
            with open(filename, "w") as f:
                f.write(content)
                return (True, "Content successfully written to file")
    except (FileNotFoundError, PermissionError) as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", result[1]))


if __name__ == "__main__":
    main()
