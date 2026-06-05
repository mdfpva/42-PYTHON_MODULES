#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)
        return


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)
        return


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)
        return


def check_plant(plant: str) -> None:
    raise PlantError(f"The {plant} plant is wilting!")
    return


def check_water(liters: int) -> None:
    if (liters < 10):
        raise WaterError("Not enough water in the tank!")
    return


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===\n")
    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print("")
    print("Testing WaterError...")
    try:
        check_water(1)
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print("")
    errors = [
        lambda: check_plant("tomato"),
        lambda: check_water(2)
    ]
    print("Testing catching all garden errors...")
    for error in errors:
        try:
            error()
        except GardenError as e:
            print(f"Caught GardenError: {e}")
    print("\nAll custom error types work correctly!")
    return


def main() -> None:
    test_custom_errors()
    return


if __name__ == "__main__":
    main()
