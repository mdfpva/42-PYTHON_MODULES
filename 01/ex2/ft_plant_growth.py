#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, aid: int,
                 growth: float) -> None:
        self.name: str = name
        self.height: float = height
        self.aid: int = aid
        self.growth: float = growth
        return

    def grow(self) -> None:
        self.height += self.growth
        return

    def age(self) -> None:
        self.aid += 1
        return

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, {self.aid} days old")
        return


def ft_plant_growth() -> None:
    plants = [
        Plant("Rose", 25.0, 30, 0.8)
    ]
    initial = {plant.name: plant.height for plant in plants}
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
              f"{round(plant.height - initial[plant.name], 1)}cm")
    return


def main() -> None:
    ft_plant_growth()
    return


if __name__ == "__main__":
    main()
