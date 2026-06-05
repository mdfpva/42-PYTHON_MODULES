#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, aid: int,
                 growth: float) -> None:
        self.name: str = name
        self.height: float = height
        self.aid: int = aid
        self.growth: float = growth
        print(f"Created: {self.name}: {round(self.height, 1)}cm, "
              f"{self.aid} days old")
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


def ft_plant_factory() -> None:
    print("=== Plant Factory Output ===")
    plants = [
        Plant("Rose", 25.0, 30, 0.8),
        Plant("Oak", 200.0, 365, 0.7),
        Plant("Cactus", 5.0, 90, 0.6),
        Plant("Sunflower", 80.0, 45, 0.5),
        Plant("Fern", 15.0, 120, 0.4)
    ]
    for plant in plants:
        plant.age()
    return


def main() -> None:
    ft_plant_factory()
    return


if __name__ == "__main__":
    main()
