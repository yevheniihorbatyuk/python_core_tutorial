"""
Module 8.5: Practice Tasks - Beginner Level
============================================

Complete all TODOs below. Test your understanding by running this file
after implementing each task.

Estimated time: 3-4 hours
Difficulty: ⭐⭐ (Intermediate)
"""

from __future__ import annotations

import copy
import csv
import json
import pickle
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final

MIN_PASSWORD_LEN: Final = 8

# ==============================================================================
# TASK 1: PASSWORD VALIDATION AND HASHING
# ==============================================================================

print("=" * 70)
print("TASK 1: PASSWORD VALIDATION AND HASHING")
print("=" * 70)


class User:
    """User class with password management."""

    def __init__(self, email: str, password: str) -> None:
        """
        TODO: Implement __init__ to:
        1. Store email
        2. Validate and hash password using password.setter
        """
        self.email = email
        self.__password_hash = None
        self.password = password

    @property
    def password(self) -> str:
        """Hide raw password via getter."""
        return "********"

    @password.setter
    def password(self, raw_password: str) -> None:
        """
        TODO: Implement password setter to:
        1. Validate length >= MIN_PASSWORD_LEN
        2. Hash password using hashlib.pbkdf2_hmac (see example below)
        3. Store hash in self.__password_hash
        4. Print success message with email

        Example hash function:
            import hashlib, os
            salt = os.urandom(16)
            hash = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
        """
        import hashlib
        import os

        # Validation
        if not raw_password:
            raise ValueError("Password cannot be empty")
        if len(raw_password) < MIN_PASSWORD_LEN:
            raise ValueError(f"Password must be at least {MIN_PASSWORD_LEN} characters")

        # Hashing
        self.__salt = os.urandom(16)
        self.__password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            raw_password.encode("utf-8"),
            self.__salt,
            100_000
        )
        print(f"✅ Password set for {self.email}")

    def verify_password(self, candidate: str) -> bool:
        """
        TODO: Implement password verification to:
        1. Hash the candidate password using same salt
        2. Compare with stored hash using hmac.compare_digest
        3. Return True if match, False otherwise
        """
        import hashlib
        import hmac

        if self.__password_hash is None or not hasattr(self, "_User__salt"):
            return False

        candidate_hash = hashlib.pbkdf2_hmac(
            "sha256",
            candidate.encode("utf-8"),
            self.__salt,
            100_000
        )
        return hmac.compare_digest(candidate_hash, self.__password_hash)


# Test Task 1
print("\nTest Task 1:")
try:
    user1 = User("alice@example.com", "SecurePass123")
    print(f"User created: {user1.email}")
    print(f"Password verification (correct): {user1.verify_password('SecurePass123')}")
    print(f"Password verification (wrong): {user1.verify_password('WrongPass')}")
    print("✅ Task 1 working!\n")
except Exception as e:
    print(f"❌ Task 1 error: {e}\n")


# ==============================================================================
# TASK 2: JSON SERIALIZATION OF COMPLEX OBJECTS
# ==============================================================================

print("=" * 70)
print("TASK 2: JSON SERIALIZATION")
print("=" * 70)


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
        """
        TODO: Convert UserProfile to dict for JSON serialization
        Include:
        - All fields
        - created_at as ISO format string (.isoformat())
        - address as dict (recursively call address dict conversion)
        - Add "__type__": "UserProfile" marker for deserialization
        """
        return {
            "__type__": "UserProfile",
            "user_id": self.user_id,
            "email": self.email,
            "address": {
                "city": self.address.city,
                "country": self.address.country,
                "zip_code": self.address.zip_code,
            },
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> UserProfile:
        """
        TODO: Reconstruct UserProfile from dict
        Include:
        - Creating Address from nested address dict
        - Parsing created_at from ISO string (datetime.fromisoformat())
        """
        address = Address(
            city=data["address"]["city"],
            country=data["address"]["country"],
            zip_code=data["address"]["zip_code"],
        )
        created_at = datetime.fromisoformat(data["created_at"])
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            address=address,
            created_at=created_at,
        )


def object_hook(obj: dict):
    """
    TODO: Implement object_hook for automatic UserProfile deserialization
    Check if obj.get("__type__") == "UserProfile"
    If yes, return UserProfile.from_dict(obj)
    Otherwise, return obj unchanged
    """
    if obj.get("__type__") == "UserProfile":
        return UserProfile.from_dict(obj)
    return obj


# Test Task 2
print("\nTest Task 2:")
try:
    addr = Address("Kyiv", "Ukraine", "01001")
    profile = UserProfile(1, "user@example.com", addr, datetime.now(timezone.utc))

    # Serialize
    json_str = json.dumps(profile.to_dict(), indent=2)
    print("Serialized to JSON:")
    print(json_str[:100] + "...")

    # Deserialize
    restored = json.loads(json_str, object_hook=object_hook)
    print(f"Deserialized: {type(restored).__name__} - {restored.email}")
    print("✅ Task 2 working!\n")
except Exception as e:
    print(f"❌ Task 2 error: {e}\n")


# ==============================================================================
# TASK 3: CSV EXPORT AND IMPORT
# ==============================================================================

print("=" * 70)
print("TASK 3: CSV EXPORT AND IMPORT")
print("=" * 70)


def export_users_csv(users: list[UserProfile], filename: str) -> None:
    """
    TODO: Export users to CSV file
    1. Open file with csv.DictWriter
    2. Write header row with fieldnames:
       ['user_id', 'email', 'city', 'country', 'zip_code', 'created_at']
    3. For each user, flatten nested address and write row
    4. Convert datetime to ISO string format
    5. Close file and print success message
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["user_id", "email", "city", "country", "zip_code", "created_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for user in users:
            writer.writerow({
                "user_id": user.user_id,
                "email": user.email,
                "city": user.address.city,
                "country": user.address.country,
                "zip_code": user.address.zip_code,
                "created_at": user.created_at.isoformat(),
            })

    print(f"✅ Exported {len(users)} users to {filename}")


def import_users_csv(filename: str) -> list[UserProfile]:
    """
    TODO: Import users from CSV file
    1. Open file with csv.DictReader
    2. For each row:
       - Create Address from city, country, zip_code fields
       - Parse created_at from ISO string
       - Create UserProfile with all fields
       - Append to users list
    3. Return list of UserProfile objects
    """
    users: list[UserProfile] = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            address = Address(row["city"], row["country"], row["zip_code"])
            created_at = datetime.fromisoformat(row["created_at"])
            user = UserProfile(int(row["user_id"]), row["email"], address, created_at)
            users.append(user)

    print(f"✅ Imported {len(users)} users from {filename}")
    return users


# Test Task 3
print("\nTest Task 3:")
try:
    test_users = [
        UserProfile(1, "alice@example.com", Address("Lviv", "Ukraine", "79000"), datetime.now(timezone.utc)),
        UserProfile(2, "bob@example.com", Address("Warsaw", "Poland", "00-001"), datetime.now(timezone.utc)),
    ]

    csv_file = "test_users.csv"
    export_users_csv(test_users, csv_file)
    imported = import_users_csv(csv_file)

    print(f"Imported {len(imported)} users")
    print(f"First user: {imported[0].email} from {imported[0].address.city}")
    print("✅ Task 3 working!\n")
except Exception as e:
    print(f"❌ Task 3 error: {e}\n")


# ==============================================================================
# TASK 4: SHALLOW VS DEEP COPY
# ==============================================================================

print("=" * 70)
print("TASK 4: SHALLOW VS DEEP COPY")
print("=" * 70)


def clone_config(config: dict, deep: bool = False) -> dict:
    """
    TODO: Implement config cloning
    1. If deep is True, use copy.deepcopy()
    2. If deep is False, use copy.copy()
    3. Return the copied config
    """
    if deep:
        return copy.deepcopy(config)
    else:
        return copy.copy(config)


# Test Task 4
print("\nTest Task 4:")
try:
    original_config = {
        "name": "experiment_1",
        "params": {"alpha": 0.1, "beta": 0.2},
        "nested": {"list": [1, 2, 3]}
    }

    shallow = clone_config(original_config, deep=False)
    deep = clone_config(original_config, deep=True)

    # Modify shallow copy
    shallow["params"]["alpha"] = 0.5
    print(f"After modifying shallow copy:")
    print(f"  Original params: {original_config['params']}")  # Will show 0.5!
    print(f"  Shallow params: {shallow['params']}")

    # Modify deep copy
    deep["params"]["beta"] = 0.9
    print(f"\nAfter modifying deep copy:")
    print(f"  Original params: {original_config['params']}")  # Still has original
    print(f"  Deep params: {deep['params']}")

    print("✅ Task 4 working!\n")
except Exception as e:
    print(f"❌ Task 4 error: {e}\n")


# ==============================================================================
# BONUS TASK 5: PICKLE SERIALIZATION
# ==============================================================================

print("=" * 70)
print("BONUS TASK 5: PICKLE SERIALIZATION")
print("=" * 70)


def save_to_pickle(obj: object, filename: str) -> None:
    """Save object to pickle file."""
    with open(filename, "wb") as f:
        pickle.dump(obj, f, protocol=5)
    print(f"✅ Saved to {filename}")


def load_from_pickle(filename: str) -> object:
    """Load object from pickle file."""
    with open(filename, "rb") as f:
        obj = pickle.load(f)
    print(f"✅ Loaded from {filename}")
    return obj


# Test Bonus Task 5
print("\nTest Bonus Task 5:")
try:
    sample_user = UserProfile(
        1,
        "test@example.com",
        Address("Kyiv", "Ukraine", "01001"),
        datetime.now(timezone.utc)
    )

    pickle_file = "user_sample.pkl"
    save_to_pickle(sample_user, pickle_file)
    restored_user = load_from_pickle(pickle_file)

    print(f"Original: {sample_user.email}")
    print(f"Restored: {restored_user.email}")
    print("✅ Bonus Task 5 working!\n")
except Exception as e:
    print(f"❌ Bonus Task 5 error: {e}\n")


# ==============================================================================
# SUMMARY
# ==============================================================================

print("=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
✅ Completed Tasks:

1. ✅ Password validation and hashing with PBKDF2
2. ✅ JSON serialization with custom to_dict/from_dict
3. ✅ CSV export/import with flattening
4. ✅ Shallow vs deep copy comparison
5. ✅ Pickle serialization (bonus)

💡 Next Steps:
- Try modifying the classes to add more fields
- Combine multiple serialization formats
- Test error handling with invalid data
- Move to advanced_edition for production patterns
""")
