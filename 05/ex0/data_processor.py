#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessorError(Exception):
    def __init__(self, message: str = "Unknown Processor Error") -> None:
        super().__init__(message)
        return


class NumericProcessorError(DataProcessorError):
    def __init__(self, message: str = "Unknown NumericProcessor Error") -> None:
        super().__init__(message)
        return


class TextProcessorError(DataProcessorError):
    def __init__(self, message: str = "Unknown TextProcessor Error") -> None:
        super().__init__(message)
        return


class LogProcessorError(DataProcessorError):
    def __init__(self, message: str = "Unknown LogProcessor Error") -> None:
        super().__init__(message)
        return


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._counter: int = 0
        return

    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

    def output(self) -> tuple[int, str]:
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        return isinstance(data, (int, float))

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise NumericProcessorError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._counter, str(item)))
            self._counter += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TextProcessorError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._counter, item))
            self._counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(isinstance(i, str) and isinstance(j, str)
                    for i, j in item.items()
                ) for item in data
            )
        return isinstance(data, dict) and all(
            isinstance(i, str) 
            and isinstance(j, str)
            for i, j in data.items()
        )

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise LogProcessorError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append((self._counter, f"{item['log_level']}: {item['log_message']}"))
            self._counter += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    np = NumericProcessor()
    print(f"Trying to validate input '42': {np.validate(42)}")
    print(f"Trying to validate input 'Hello': {np.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        np.ingest("foo")  # type: ignore
    except DataProcessorError as e:
        print(f"Got exception: {e}")
    data_n = [1, 2, 3, 4, 5]
    print(f"Processing data: {data_n}")
    np.ingest(data_n)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = np.output()
        print(f"Numeric value {rank}: {value}")

    print()

    print("Testing Text Processor...")
    tp = TextProcessor()
    print(f"Trying to validate input '42': {tp.validate(42)}")
    data_t = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {data_t}")
    tp.ingest(data_t)
    print("Extracting 1 value...")
    rank, value = tp.output()
    print(f"Text value {rank}: {value}")

    print()

    print("Testing Log Processor...")
    lp = LogProcessor()
    print(f"Trying to validate input 'Hello': {lp.validate('Hello')}")
    data_l = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {data_l}")
    lp.ingest(data_l)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = lp.output()
        print(f"Log entry {rank}: {value}")
    return


if __name__ == "__main__":
    main()
