#!/usr/bin/env python3
"""Ex0 - Space Station Data validation with Pydantic BaseModel."""

import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Represents a space station monitored by the Observatory."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    """Display station information in the standard format."""
    status = "Operational" if station.is_operational else "Offline"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def find_data_dir() -> Path | None:
    """Locate the generated_data directory if it exists."""
    for candidate in (Path("generated_data"), Path("../generated_data")):
        if candidate.is_dir():
            return candidate
    return None


def load_json_data(filepath: Path) -> list[dict[str, object]]:
    """Load a list of records from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise ValueError(f"{filepath} does not contain a list")
    return raw


def validate_dataset(filepath: Path) -> None:
    """Validate every record in a JSON dataset against the model."""
    try:
        records = load_json_data(filepath)
    except (OSError, ValueError) as error:
        # Protect the data stream: report and keep going
        print(f"Could not load {filepath.name}: {error}")
        return

    valid_count = 0
    for index, record in enumerate(records):
        print(f"Record {index}:")
        try:
            station = SpaceStation.model_validate(record)
            valid_count += 1
            display_station(station)
        except ValidationError as error:
            msg = error.errors()[0]["msg"]
            print(f"INVALID - {msg}")
        print()

    print(f"{filepath.name}: {valid_count}/{len(records)} records valid")


def main() -> None:
    """Demonstrate SpaceStation validation with valid and invalid data."""
    print("Space Station Data Validation")
    print("=" * 40)

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2026, 7, 1, 12, 0),
        is_operational=True,
    )

    print("Valid station created:")
    display_station(station)

    print("=" * 40)
    try:
        SpaceStation(
            station_id="DS9",
            name="Deep Space Nine",
            crew_size=42,
            power_level=50.0,
            oxygen_level=75.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])

    # Bonus: validate the datasets produced by the data tools
    data_dir = find_data_dir()
    if data_dir is not None:
        print("=" * 40)
        print("Validating generated datasets:")
        validate_dataset(data_dir / "space_stations.json")
        validate_dataset(data_dir / "invalid_stations.json")


if __name__ == "__main__":
    main()
