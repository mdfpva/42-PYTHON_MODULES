#!/usr/bin/env python3

import random


def ft_data_alchemist() -> None:
    print("=== Game Data Alchemist ===")
    players = [
        "Alice",
        "bob",
        "Charlie",
        "dylan",
        "Emma",
        "Gregory",
        "john",
        "kevin",
        "Liam"
    ]
    print(f"Initial list of players: {players}")
    all_capitalized: list = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {all_capitalized}")
    only_capitalized: list = [name for name in players if name[0].isupper()]
    print(f"New list of capitalized names only: {only_capitalized}")
    scores: dict = {name: random.randint(1, 1000) for name in all_capitalized}
    print(f"Score dict: {scores}")
    average: float = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average}")
    high_scores: dict = {
        name: score for name, score in scores.items() if score > average
    }
    print(f"High scores: {high_scores}")
    return


def main() -> None:
    ft_data_alchemist()
    return


if __name__ == "__main__":
    main()
