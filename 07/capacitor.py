#!/usr/bin/env python3

from typing import cast

from ex0 import CreatureFactory
from ex1 import (
    HealCapability,
    HealingCreatureFactory,
    TransformCapability,
    TransformCreatureFactory,
)


def test_healing(factory: CreatureFactory) -> None:
    print("Testing Creature with healing capability")
    print("base:")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(cast(HealCapability, base).heal())
    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    print(cast(HealCapability, evolved).heal())


def test_transform(factory: CreatureFactory) -> None:
    print("Testing Creature with transform capability")
    print("base:")
    base = factory.create_base()
    base_t = cast(TransformCapability, base)
    print(base.describe())
    print(base.attack())
    print(base_t.transform())
    print(base.attack())
    print(base_t.revert())
    print("evolved:")
    evolved = factory.create_evolved()
    evolved_t = cast(TransformCapability, evolved)
    print(evolved.describe())
    print(evolved.attack())
    print(evolved_t.transform())
    print(evolved.attack())
    print(evolved_t.revert())


def main() -> None:
    test_healing(HealingCreatureFactory())
    test_transform(TransformCreatureFactory())


if __name__ == "__main__":
    main()
