"""Ex1 - Alien Contact Logs with model_validator business rules."""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Types of alien contact recognized by the Observatory."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Represents an alien contact report with business rules."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        """Validate cross-field business rules after field validation."""
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
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
            AlienContact.model_validate(record)
            valid_count += 1
        except ValidationError as error:
            msg = error.errors()[0]["msg"]
            print(f"  Record {index}: {msg.removeprefix('Value error, ')}")

    print(f"{filepath.name}: {valid_count}/{len(records)} records valid")


def main() -> None:
    """Demonstrate AlienContact validation with valid/invalid reports."""
    print("Alien Contact Log Validation")
    print("=" * 38)

    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 6, 15, 3, 42),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )

    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")

    print("=" * 38)
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2024, 6, 16, 22, 10),
            location="Serra da Estrela, Portugal",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=4.2,
            duration_minutes=15,
            witness_count=1,
        )
    except ValidationError as error:
        print("Expected validation error:")
        msg = error.errors()[0]["msg"]
        print(msg.removeprefix("Value error, "))

    # Bonus: validate the datasets produced by the data tools
    data_dir = find_data_dir()
    if data_dir is not None:
        print("=" * 38)
        print("Validating generated datasets:")
        validate_dataset(data_dir / "alien_contacts.json")
        validate_dataset(data_dir / "invalid_contacts.json")


if __name__ == "__main__":
    main()
