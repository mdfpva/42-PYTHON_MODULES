"""Ex2 - Space Crew Management with nested Pydantic models."""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Crew ranks recognized by the Observatory."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Represents an individual crew member."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """Represents a space mission with crew validation rules."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_rules(self) -> "SpaceMission":
        """Validate mission safety and operational requirements."""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        leaders = (Rank.COMMANDER, Rank.CAPTAIN)
        if not any(member.rank in leaders for member in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


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
        try:
            SpaceMission.model_validate(record)
            valid_count += 1
        except ValidationError as error:
            msg = error.errors()[0]["msg"]
            print(f"  Record {index}: {msg.removeprefix('Value error, ')}")

    print(f"{filepath.name}: {valid_count}/{len(records)} records valid")


def main() -> None:
    """Demonstrate SpaceMission validation with valid/invalid crews."""
    print("Space Mission Crew Validation")
    print("=" * 41)

    crew = [
        CrewMember(
            member_id="CM001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission Command",
            years_experience=20,
        ),
        CrewMember(
            member_id="CM002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=8,
        ),
        CrewMember(
            member_id="CM003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=4,
        ),
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 11, 1, 8, 0),
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )

    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value})"
            f" - {member.specialization}"
        )

    print("=" * 41)
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime(2024, 12, 1, 8, 0),
            duration_days=30,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Wilson",
                    rank=Rank.CADET,
                    age=22,
                    specialization="Geology",
                    years_experience=1,
                ),
            ],
            budget_millions=150.0,
        )
    except ValidationError as error:
        print("Expected validation error:")
        msg = error.errors()[0]["msg"]
        print(msg.removeprefix("Value error, "))

    # Bonus: validate the datasets produced by the data tools
    data_dir = find_data_dir()
    if data_dir is not None:
        print("=" * 41)
        print("Validating generated datasets:")
        validate_dataset(data_dir / "space_missions.json")


if __name__ == "__main__":
    main()
