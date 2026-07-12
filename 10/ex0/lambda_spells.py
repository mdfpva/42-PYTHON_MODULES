#!/usr/bin/env python3

"""Lambda Sanctum: mastering anonymous functions."""


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort artifacts by power level in descending order."""
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """Filter mages with power >= min_power."""
    return list(filter(lambda m: m['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Add '* ' prefix and ' *' suffix to each spell name."""
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Compute max, min and average power levels of mages."""
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    return {
        'max_power': max(mages, key=lambda m: m['power'])['power'],
        'min_power': min(mages, key=lambda m: m['power'])['power'],
        'avg_power': round(
            sum(map(lambda m: m['power'], mages)) / len(mages), 2
        ),
    }


def main() -> None:
    """Run demonstration tests for the Lambda Sanctum."""
    try:
        artifacts = [
            {'name': 'Crystal Orb', 'power': 85, 'type': 'divination'},
            {'name': 'Fire Staff', 'power': 92, 'type': 'attack'},
            {'name': 'Ice Shield', 'power': 71, 'type': 'defense'},
        ]
        print("Testing artifact sorter...")
        first, second = artifact_sorter(artifacts)[:2]
        print(f"{first['name']} ({first['power']} power) comes before "
              f"{second['name']} ({second['power']} power)")

        mages = [
            {'name': 'Aria', 'power': 88, 'element': 'fire'},
            {'name': 'Bolt', 'power': 45, 'element': 'lightning'},
            {'name': 'Cora', 'power': 67, 'element': 'water'},
        ]
        print("\nTesting power filter...")
        strong = power_filter(mages, 60)
        print("Mages with power >= 60:",
              ", ".join(map(lambda m: m['name'], strong)))

        print("\nTesting spell transformer...")
        print(" ".join(spell_transformer(['fireball', 'heal', 'shield'])))

        print("\nTesting mage stats...")
        stats = mage_stats(mages)
        print(f"Max power: {stats['max_power']}")
        print(f"Min power: {stats['min_power']}")
        print(f"Avg power: {stats['avg_power']}")
    except (KeyError, TypeError) as exc:
        print(f"Data stream corrupted: {exc}")


if __name__ == "__main__":
    main()
