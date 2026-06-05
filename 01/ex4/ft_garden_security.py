#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth: float) -> None:
        self._name: str = name
        self._height: float = height
        self._age: int = age
        self._growth: float = growth
        print(f"Plant created: {self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
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
        print(f"Current state: {self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
        return


def ft_garden_security() -> None:
    print("=== Garden Security System ===")
    rose: Plant = Plant("Rose", 15.0, 10, 0.8)
    print("")
    rose.set_height(25.0)
    rose.set_age(30)
    print("")
    rose.set_height(-25.0)
    rose.set_age(-30)
    print("")
    rose.show()
    return


def main() -> None:
    ft_garden_security()
    return


if __name__ == "__main__":
    main()
