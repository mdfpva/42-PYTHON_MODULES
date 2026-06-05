#!/usr/bin/env python3

def ft_helper(day, duh) -> None:
    if (day > duh):
        print("Harvest time!")
        return
    print(f"Day {day}")
    ft_helper(day + 1, duh)
    return


def ft_count_harvest_recursive() -> None:
    duh: int = int(input("Days until harvest: "))
    ft_helper(1, duh)
    return
