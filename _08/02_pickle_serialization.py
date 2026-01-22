"""
Module 8.2: Pickle serialization with __getstate__ and __setstate__.
WARNING: Never load pickle from untrusted sources.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Address:
    city: str
    country: str
    zip_code: str


class User:
    def __init__(self, user_id: int, email: str, address: Address) -> None:
        self.user_id = user_id
        self.email = email
        self.address = address
        self.created_at = datetime.utcnow()
        self.__password_hash = "secret-hash"  # Demo placeholder

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        # Save id and remove sensitive fields before serialization.
        state["user_id"] = self.user_id
        state.pop("_User__password_hash", None)
        return state

    def __setstate__(self, state: dict) -> None:
        user_id = state.get("user_id")
        email = state.get("email", "")
        state["email"] = f"{email}#id={user_id}"
        self.__dict__.update(state)

    def __repr__(self) -> str:
        return f"User(email={self.email!r}, user_id={self.user_id}, city={self.address.city!r})"


if __name__ == "__main__":
    address = Address(city="Kyiv", country="UA", zip_code="01001")
    user = User(user_id=1001, email="student@example.com", address=address)

    print("Original:", user)

    # Serialize to bytes
    blob = pickle.dumps(user)
    print("Pickle size (bytes):", len(blob))

    # Serialize to file
    with open("user.pkl", "wb") as f:
        f.write(blob)

    # Deserialize
    restored = pickle.loads(blob)
    print("Restored:", restored)
    print("Restored email mutated by __setstate__:", restored.email)

    print("\nNote: Pickle is unsafe for untrusted data.")
