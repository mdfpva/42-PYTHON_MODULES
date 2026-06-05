#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int, growth: float):
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

    def set_height(self, height: float) -> None:
        if (height < 0):
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
            return
        self._height = height
        print(f"Height updated: {self._height:.0f}cm")
        return

    def set_age(self, age: int) -> None:
        if (age < 0):
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
            return
        self._age = age
        print(f"Age updated: {self._age} days")
        return

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def show(self) -> None:
        print(f"{self._name.capitalize()}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
        return


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, growth: float,
                 color: str) -> None:
        super().__init__(name, height, age, growth)
        self._color: str = color
        self._blooming: bool = False
        print("=== Flower")
        self.show()
        return

    def bloom(self) -> None:
        print(f"[asking the {self._name} to bloom]")
        self._blooming = True
        return

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if (self._blooming):
            print(f" {self._name.capitalize()} is blooming beautifully!")
        else:
            print(f" {self._name.capitalize()} has not bloomed yet")
        return


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int, growth: float,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age, growth)
        self._trunk_diameter: float = trunk_diameter
        print("=== Tree")
        self.show()
        return

    def produce_shade(self) -> None:
        print(f"[asking the {self._name} to produce shade]")
        print(f"Tree {self._name.capitalize()} now produces a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide.")
        return

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {round(self._trunk_diameter, 1)}cm")
        return


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, growth: float,
                 harvest_season: str, nutritional_value: int) -> None:
        super().__init__(name, height, age, growth)
        self._harvest_season: str = harvest_season
        self._nutritional_value: int = nutritional_value
        print("=== Vegetable")
        self.show()
        return

    def grow_and_age(self, days: int) -> None:
        for day in range(0, days):
            super().age()
            super().grow()
            self._nutritional_value += 1
        print(f"[make tomato grow and age for {days} days]")
        return

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value}")
        return


def ft_plant_types() -> None:
    print("=== Garden Plant Types ===")
    rose: Flower = Flower("rose", 15.0, 10, 0.8, "red")
    rose.bloom()
    rose.show()
    print("")
    oak: Tree = Tree("oak", 200.0, 365, 5.0, 5.0)
    oak.produce_shade()
    print("")
    tomato: Vegetable = Vegetable("tomato", 5.0, 10, 2.1, "April", 0)
    tomato.grow_and_age(20)
    tomato.show()
    return


def main() -> None:
    ft_plant_types()
    return


if __name__ == "__main__":
    main()
