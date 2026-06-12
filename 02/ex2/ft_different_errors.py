#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    if (operation_number == 0):
        int("abc")
    elif (operation_number == 1):
        1 / 0
    elif (operation_number == 2):
        open("/non/existent/file")
    elif (operation_number == 3):
        "escola" + 42  # type: ignore
    return


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for operation in range(5):
        print(f"Testing operation {operation}...")
        try:
            garden_operations(operation)
            print("Operation completed successfully")
        except (ValueError, ZeroDivisionError, FileNotFoundError,
                TypeError) as e:
            print(f"Caught {type(e).__name__}: {e}")
    print("\nAll error types tested successfully!")
    return


def main() -> None:
    test_error_types()
    return


if __name__ == "__main__":
    main()
