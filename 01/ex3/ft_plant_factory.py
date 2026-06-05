#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth: float) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
        self._growth: float = growth
        print(f"Created: {self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
        return

    def grow(self) -> None:
        self._height += self._growth
        return

    def age(self) -> None:
        self._age += 1
        return

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
        return


def ft_plant_factory() -> None:
    print("=== Plant Factory Output ===")
    plants = [
        Plant("Rose", 25.0, 30, 0.8),
        Plant("Oak", 200.0, 365, 0.7),
        Plant("Cactus", 5.0, 90, 0.6),
        Plant("Sunflower", 80.0, 45, 0.5),
        Plant("Fern", 15.0, 120, 0.4)
    ]
    _ = plants
    return


def main() -> None:
    ft_plant_factory()
    return


if __name__ == "__main__":
    main()
