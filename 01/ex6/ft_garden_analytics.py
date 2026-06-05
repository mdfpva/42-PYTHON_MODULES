#!/usr/bin/env python3

class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls: int = 0
            self._age_calls: int = 0
            self._show_calls: int = 0

        def record_grow(self) -> None:
            self._grow_calls += 1

        def record_age(self) -> None:
            self._age_calls += 1

        def record_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, "
                  f"{self._show_calls} show")

    def __init__(self, name: str, height: float, age: int,
                 growth: float) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
        self._growth: float = growth
        self._stats: Plant.Stats = Plant.Stats()

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0, 0.0)

    def grow(self) -> None:
        self._height += self._growth
        self._stats.record_grow()

    def age(self) -> None:
        self._age += 1
        self._stats.record_age()

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
            return
        self._height = height
        print(f"Height updated: {self._height:.0f}cm")

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
            return
        self._age = age
        print(f"Age updated: {self._age} days")

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def show(self) -> None:
        self._stats.record_show()
        print(f"{self._name.capitalize()}: {self._height:.1f}cm, "
              f"{self._age} days old")

    def display_stats(self) -> None:
        self._stats.display()


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, growth: float,
                 color: str) -> None:
        super().__init__(name, height, age, growth)
        self._color: str = color
        self._blooming: bool = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if self._blooming:
            print(f" {self._name.capitalize()} is blooming beautifully!")
        else:
            print(f" {self._name.capitalize()} has not bloomed yet")


class Tree(Plant):
    class TreeStats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls: int = 0

        def record_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, "
                  f"{self._show_calls} show "
                  f"\n {self._shade_calls} shade")

    def __init__(self, name: str, height: float, age: int, growth: float,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age, growth)
        self._trunk_diameter: float = trunk_diameter
        self._stats: Tree.TreeStats = Tree.TreeStats()

    def produce_shade(self) -> None:
        self._stats.record_shade()
        print(f"Tree {self._name.capitalize()} now produces a shade of "
              f"{self._height:.1f}cm long and "
              f"{self._trunk_diameter:.1f}cm wide.")

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {self._trunk_diameter:.1f}cm")


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, growth: float,
                 color: str, seeds: int) -> None:
        super().__init__(name, height, age, growth, color)
        self._seeds: int = seeds

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant._name.capitalize()}]")
    plant.display_stats()


def ft_garden_analytics() -> None:
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_a_year(30)}")
    print(f"Is 400 days more than a year? -> "
          f"{Plant.is_older_than_a_year(400)}")
    print("")
    print("=== Flower")
    rose: Flower = Flower("rose", 15.0, 10, 8.0, "red")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)
    print("")
    print("=== Tree")
    oak: Tree = Tree("oak", 200.0, 365, 0.7, 5.0)
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)
    print("")
    print("=== Seed")
    sunflower: Seed = Seed("sunflower", 80.0, 45, 1.5, "yellow", 0)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    for _ in range(20):
        sunflower.grow()
        sunflower.age()
    sunflower.bloom()
    sunflower._seeds = 42
    sunflower.show()
    display_stats(sunflower)
    print("")
    print("=== Anonymous")
    anon: Plant = Plant.anonymous()
    anon.show()
    display_stats(anon)


def main() -> None:
    ft_garden_analytics()


if __name__ == "__main__":
    main()
