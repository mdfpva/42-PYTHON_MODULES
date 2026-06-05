#!/usr/bin/env python3

def ft_count_harvest_iterative() -> None:
    duh: int = int(input("Days until harvest: "))
    for i in range(1, duh + 1):
        print(f"Day {i}")
    print("Harvest time!")
    return
