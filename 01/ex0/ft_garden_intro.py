#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age
        return


def ft_garden_intro() -> None:
    plant: Plant = Plant("Rose", 25, 30)
    print("=== Welcome to My Garden ===")
    print(f"Plant: {plant.name}")
    print(f"Height: {plant.height}cm")
    print(f"Age: {plant.age} days")
    print("\n=== End of Program ===")
    return


def main() -> None:
    ft_garden_intro()
    return


if __name__ == "__main__":
    main()
