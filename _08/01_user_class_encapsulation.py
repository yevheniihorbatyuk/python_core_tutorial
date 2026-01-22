"""
Module 8.1: Encapsulation and safe password handling.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from enum import Enum
from typing import Final

MIN_PASSWORD_LEN: Final = 8
MAX_PASSWORD_LEN: Final = 128


class Role(Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    STUDENT = "student"


def _hash_password(password: str, salt: bytes) -> bytes:
    """Hash password with PBKDF2 (demo only, use stronger policy in prod)."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)


class User:
    def __init__(self, email: str, password: str, user_id: int, role: Role = Role.STUDENT) -> None:
        self.email = email
        self.user_id = user_id
        self.role = role
        self.__salt = os.urandom(16)
        self.__password_hash: bytes | None = None
        self.__password: str | None = None  # Demo only: never store raw passwords in real systems.
        self.password = password

    @property
    def password(self) -> str:
        """Hide the raw password via getter."""
        return "********"

    @password.setter
    def password(self, raw_password: str) -> None:
        if not raw_password:
            raise ValueError("Password cannot be empty")
        if len(raw_password) < MIN_PASSWORD_LEN:
            raise ValueError("Password is too short")
        if len(raw_password) > MAX_PASSWORD_LEN:
            raise ValueError("Password is too long")

        self.__password = raw_password
        self.__password_hash = _hash_password(raw_password, self.__salt)

    def verify_password(self, candidate: str) -> bool:
        if self.__password_hash is None:
            return False
        candidate_hash = _hash_password(candidate, self.__salt)
        return hmac.compare_digest(candidate_hash, self.__password_hash)

    def __repr__(self) -> str:
        return f"User(email={self.email!r}, user_id={self.user_id}, role={self.role.value!r})"


if __name__ == "__main__":
    user = User(email="ds.engineer@example.com", password="StrongPass123", user_id=42)

    print("Public view:")
    print(user)
    print("Password getter:", user.password)
    print("Verify correct:", user.verify_password("StrongPass123"))
    print("Verify wrong:", user.verify_password("wrong-pass"))

    print("\nName mangling is not security:")
    print("Access via _User__password:", user._User__password)

    print("\nEnum constants example:")
    print([role.value for role in Role])
