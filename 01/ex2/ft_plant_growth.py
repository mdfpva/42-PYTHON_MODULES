#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth: float) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
        self._growth: float = growth
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


def ft_plant_growth() -> None:
    plants = [
        Plant("Rose", 25.0, 30, 0.8)
    ]
    initial = {plant._name: plant._height for plant in plants}
    print("=== Garden Plant Growth ===")
    for plant in plants:
        plant.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        for plant in plants:
            plant.grow()
            plant.age()
            plant.show()
    for plant in plants:
        print("Growth this week: "
              f"{round(plant._height - initial[plant._name], 1)}cm")
    return


def main() -> None:
    ft_plant_growth()
    return


if __name__ == "__main__":
    main()
