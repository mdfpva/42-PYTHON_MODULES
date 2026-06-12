#!/usr/bin/env python3

import typing
import random

PLAYERS: list = [
    "alice",
    "bob",
    "charlie",
    "dylan"
]
ACTIONS: list = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "use",
    "release"
]


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    while (True):
        yield (random.choice(PLAYERS), random.choice(ACTIONS))


def consume_event(event_list: list) -> typing.Generator[tuple[str, str],
                                                        None, None]:
    while (len(event_list) > 0):
        event: tuple[str, str] = random.choice(event_list)
        event_list.remove(event)
        yield event
    return


def ft_data_stream() -> None:
    print("=== Game Data Stream Processor ===")
    stream: typing.Generator[tuple[str, str], None, None] = gen_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")
    event_list: list = [next(stream) for i in range(10)]
    print(f"Built list of 10 events: {event_list}")
    for event in consume_event(event_list):
        print(f"Got event from list: {event}\n"
              f"Remains in list: {event_list}")
    return


def main() -> None:
    ft_data_stream()
    return


if __name__ == "__main__":
    main()
