"""
Module 8: Practice tasks.

Run this file and implement TODO sections.
"""

from __future__ import annotations

import copy
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Final

MIN_PASSWORD_LEN: Final = 8


# ------------------------------
# Task 1: Encapsulation
# ------------------------------
class User:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.__password_hash = None
        self.password = password

    @property
    def password(self) -> str:
        """Hide raw password."""
        return "********"

    @password.setter
    def password(self, raw_password: str) -> None:
        # TODO: validate length >= MIN_PASSWORD_LEN
        # TODO: hash password (use a simple hash for now)
        pass

    def verify_password(self, candidate: str) -> bool:
        # TODO: compare candidate hash with stored hash
        return False


# ------------------------------
# Task 2: JSON serialization
# ------------------------------
@dataclass
class Address:
    city: str
    country: str
    zip_code: str


@dataclass
class UserProfile:
    user_id: int
    email: str
    address: Address
    created_at: datetime

    def to_dict(self) -> dict:
        # TODO: convert to dict, include created_at as ISO string
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        # TODO: reconstruct Address and datetime from dict
        return cls(0, "", Address("", "", ""), datetime.utcnow())


def object_hook(obj: dict):
    # TODO: if obj is a UserProfile dict, return UserProfile instance
    return obj


# ------------------------------
# Task 3: CSV export/import
# ------------------------------

def export_users_csv(users: list[UserProfile], filename: str) -> None:
    # TODO: write CSV with user_id, email, city, country, zip_code, created_at
    pass


def import_users_csv(filename: str) -> list[UserProfile]:
    # TODO: read CSV and reconstruct UserProfile objects
    return []


# ------------------------------
# Task 4: Copying objects
# ------------------------------

def clone_pipeline(config: dict, deep: bool = False) -> dict:
    """Return a shallow or deep copy of config."""
    # TODO: use copy.copy or copy.deepcopy based on the flag
    return {}


# ------------------------------
# Demo runner
# ------------------------------
if __name__ == "__main__":
    print("Practice tasks loaded. Implement TODOs and re-run.")

    # Small demo scaffolding (optional)
    address = Address("Dnipro", "UA", "49000")
    profile = UserProfile(1, "user@example.com", address, datetime.utcnow())

    payload = json.dumps(profile.to_dict())
    print("JSON payload:", payload)

    with open("users_demo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "email", "city", "country", "zip_code", "created_at"])
        writer.writerow([1, profile.email, address.city, address.country, address.zip_code, profile.created_at.isoformat()])

    sample_config = {"steps": ["load", "clean"], "params": {"alpha": 0.1}}
    print("Shallow copy:", clone_pipeline(sample_config, deep=False))
    print("Deep copy:", clone_pipeline(sample_config, deep=True))
