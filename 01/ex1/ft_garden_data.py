#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name: str = name
        self.height: int = height
        self.age: int = age
        return

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")
        return


def ft_garden_data() -> None:
    plants = [
        Plant("Rose", 25, 30),
        Plant("Sunflower", 80, 45),
        Plant("Cactus", 15, 120)
    ]
    print("=== Garden Plant Registry ===")
    for plant in plants:
        plant.show()
    return


def main() -> None:
    ft_garden_data()
    return


if __name__ == "__main__":
    main()
