#!/usr/bin/env python3

import random


ALL_ACHIEVEMENTS = [
    "First Steps", "Boss Slayer", "Speed Runner", "Untouchable",
    "World Savior", "Master Explorer", "Collector Supreme", "Strategist",
    "Survivor", "Treasure Hunter", "Crafting Genius", "Sharp Mind",
    "Unstoppable", "Hidden Path Finder", "Dragon Slayer", "Legend"
]


def gen_player_achievements() -> set:
    return set(random.sample(ALL_ACHIEVEMENTS, random.randint(5, 10)))


def ft_achievement_tracker() -> None:
    all_achievements: set = set(ALL_ACHIEVEMENTS)
    players = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements()
    }
    print("=== Achievement Tracker System ===\n")
    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")
    print("")
    all_distinct: set = set()
    for achievements in players.values():
        all_distinct = set.union(all_distinct, achievements)
    print(f"All distinct achievements: {all_distinct}")
    print("")
    common: set = all_achievements.copy()
    for achievements in players.values():
        common = set.intersection(common, achievements)
    print(f"Common achievements: {common}")
    print("")
    for name, achievements in players.items():
        others: set = set()
        for o_name, o_achievements in players.items():
            if (name != o_name):
                others = set.union(others, o_achievements)
        print(f"Only {name} has: {set.difference(achievements, others)}")
    print("")
    for name, achievements in players.items():
        print(f"{name} is missing: "
              f"{set.difference(all_achievements, achievements)}")
    return


def main() -> None:
    ft_achievement_tracker()
    return


if __name__ == "__main__":
    main()
