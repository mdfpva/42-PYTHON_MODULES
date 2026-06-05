#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    temp: int = int(temp_str)
    if (temp < 0):
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    elif (temp > 40):
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")
    return temp


def test_temperature() -> None:
    inputs = [
        "25",
        "abc",
        "100",
        "-50"
    ]
    print("=== Garden Temperature ===\n")
    for temp in inputs:
        print(f"Input data is '{temp}'")
        try:
            print(f"Temperature is now {input_temperature(temp)}°C\n")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}\n")
    print("All tests completed - program didn't crash!")
    return


def main() -> None:
    test_temperature()
    return


if __name__ == "__main__":
    main()
