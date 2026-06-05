#!/usr/bin/env python3

import sys


def create_inventory() -> dict:
    inventory: dict = {}
    print("=== Inventory System Analysis ===")
    for arg in sys.argv[1:]:
        parts = arg.split(":")
        if (len(parts) != 2):
            print(f"Error - invalid parameter '{arg}'")
            continue
        name, quantity = parts[0], parts[1]
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            inventory[name] = int(quantity)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
    return inventory


def ft_inventory_system() -> None:
    inventory: dict = create_inventory()
    print(f"Got inventory: {inventory}")
    items: list = list(inventory.keys())
    print(f"Item list: {items}")
    total: int = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")
    for name in inventory:
        print(f"Item {name} represents {round(inventory[name] / total * 100, 1)}%")
    most: str = items[0]
    least: str = items[0]
    for name in items:
        if (inventory[name] > inventory[most]):
            most = name
        if (inventory[name] < inventory[least]):
            least = name
    return


def main() -> None:
    ft_inventory_system()
    return


if __name__ == "__main__":
    main()
