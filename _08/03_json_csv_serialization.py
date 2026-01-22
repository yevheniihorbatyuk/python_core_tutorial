"""
Module 8.3: JSON and CSV serialization with custom object hooks.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Address:
    city: str
    country: str
    zip_code: str

    def to_dict(self) -> dict:
        return {
            "city": self.city,
            "country": self.country,
            "zip_code": self.zip_code,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        return cls(data["city"], data["country"], data["zip_code"])


class User:
    def __init__(self, user_id: int, email: str, address: Address, created_at: datetime | None = None) -> None:
        self.user_id = user_id
        self.email = email
        self.address = address
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "__type__": "User",
            "user_id": self.user_id,
            "email": self.email,
            "address": self.address.to_dict(),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        address = Address.from_dict(data["address"])
        created_at = datetime.fromisoformat(data["created_at"])
        return cls(user_id=data["user_id"], email=data["email"], address=address, created_at=created_at)

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, email={self.email!r}, city={self.address.city!r})"


def user_object_hook(obj: dict):
    if obj.get("__type__") == "User":
        return User.from_dict(obj)
    return obj


def to_json(users: list[User]) -> str:
    return json.dumps([u.to_dict() for u in users], indent=2)


def from_json(payload: str) -> list[User]:
    return json.loads(payload, object_hook=user_object_hook)


def users_to_csv(users: list[User], filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "email", "city", "country", "zip_code", "created_at"])
        writer.writeheader()
        for u in users:
            writer.writerow(
                {
                    "user_id": u.user_id,
                    "email": u.email,
                    "city": u.address.city,
                    "country": u.address.country,
                    "zip_code": u.address.zip_code,
                    "created_at": u.created_at.isoformat(),
                }
            )


def users_from_csv(filename: str) -> list[User]:
    users: list[User] = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            address = Address(row["city"], row["country"], row["zip_code"])
            created_at = datetime.fromisoformat(row["created_at"])
            users.append(User(int(row["user_id"]), row["email"], address, created_at))
    return users


if __name__ == "__main__":
    users = [
        User(1, "alice@example.com", Address("Lviv", "UA", "79000")),
        User(2, "bob@example.com", Address("Warsaw", "PL", "00-001")),
    ]

    print("JSON serialization:")
    payload = to_json(users)
    print(payload)

    print("\nJSON deserialization into real objects (object_hook):")
    restored = from_json(payload)
    for u in restored:
        print(u, type(u))

    print("\nCSV serialization:")
    users_to_csv(users, "users.csv")
    restored_csv = users_from_csv("users.csv")
    for u in restored_csv:
        print(u)
