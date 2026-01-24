"""
Module 8.1: Object-Oriented Programming - Encapsulation and Safe Password Handling
======================================================================================

Learning Goals:
- Understand classes and objects
- Learn about private attributes and name mangling
- Implement property decorators (getters/setters)
- Hash passwords securely
- Use Enums for constants

🔍 Where you'll use this:
- User management systems (web apps, mobile apps)
- Authentication and authorization
- Any system with sensitive data (passwords, API keys, secrets)

⚡ Data Science/Engineering Context:
- ML pipelines need user authentication
- Data access control requires secure user models
- Experiment tracking systems need user identity
"""

from __future__ import annotations

import hashlib
import hmac
import os
from enum import Enum
from typing import Final

MIN_PASSWORD_LEN: Final = 8
MAX_PASSWORD_LEN: Final = 128


# ==========================================================================
# SECTION 1: ENUM FOR CONSTANTS (safer than strings)
# ==========================================================================

print("=" * 70)
print("SECTION 1: USING ENUM FOR CONSTANTS")
print("=" * 70)


class Role(Enum):
    """User roles - immutable constants that can't be accidentally modified."""
    ADMIN = "admin"
    ANALYST = "analyst"
    STUDENT = "student"


# Example: accessing enum values
print("\nAvailable roles:")
for role in Role:
    print(f"  - {role.name}: {role.value}")


# ==========================================================================
# SECTION 2: PASSWORD HASHING FUNCTION (utility)
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 2: PASSWORD HASHING WITH PBKDF2")
print("=" * 70)


def _hash_password(password: str, salt: bytes) -> bytes:
    """
    Hash a password using PBKDF2-SHA256 with a salt.

    Args:
        password: Plain text password
        salt: Random bytes used for hashing

    Returns:
        Hashed password as bytes

    Note:
        In production, use bcrypt, Argon2, or scrypt instead of PBKDF2.
        PBKDF2 is acceptable but slower alternatives are more secure.
    """
    # PBKDF2 with 120,000 iterations (OWASP recommended minimum)
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        120_000
    )


# Demonstrate hashing
sample_password = "MySecurePass123"
sample_salt = os.urandom(16)
sample_hash = _hash_password(sample_password, sample_salt)

print(f"\nPassword: {sample_password}")
print(f"Salt (first 8 bytes): {sample_salt[:8].hex()}")
print(f"Hash (first 8 bytes): {sample_hash[:8].hex()}")
print("Note: Same password with same salt always produces same hash")


# ==========================================================================
# SECTION 3: USER CLASS WITH ENCAPSULATION
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 3: USER CLASS WITH PRIVATE ATTRIBUTES AND PROPERTIES")
print("=" * 70)


class User:
    """
    User class demonstrating encapsulation best practices.

    Private attributes:
    - __salt: Random salt for password hashing
    - __password_hash: Hashed password (never the plain text)

    Properties:
    - password (getter/setter): Write-only password interface
    - email (public): User's email address
    """

    def __init__(
        self,
        email: str,
        password: str,
        user_id: int,
        role: Role = Role.STUDENT
    ) -> None:
        """
        Initialize a user.

        Args:
            email: User's email
            password: Plain text password (will be hashed immediately)
            user_id: Unique identifier
            role: User role (from Role enum)

        Raises:
            ValueError: If password is invalid
        """
        self.email = email
        self.user_id = user_id
        self.role = role

        # Private attributes (convention: double underscore)
        self.__salt = os.urandom(16)
        self.__password_hash: bytes | None = None

        # Use the property setter to hash the password
        self.password = password

    @property
    def password(self) -> str:
        """
        Getter: Always returns masked password for security.

        This prevents accidental password leaks when printing or logging.
        """
        return "********"

    @password.setter
    def password(self, raw_password: str) -> None:
        """
        Setter: Validates and hashes the password.

        Args:
            raw_password: Plain text password

        Raises:
            ValueError: If password doesn't meet security requirements
        """
        if not raw_password:
            raise ValueError("❌ Password cannot be empty")
        if len(raw_password) < MIN_PASSWORD_LEN:
            raise ValueError(f"❌ Password must be at least {MIN_PASSWORD_LEN} characters")
        if len(raw_password) > MAX_PASSWORD_LEN:
            raise ValueError(f"❌ Password must not exceed {MAX_PASSWORD_LEN} characters")

        # Hash and store
        self.__password_hash = _hash_password(raw_password, self.__salt)
        print(f"✅ Password set for {self.email}")

    def verify_password(self, candidate: str) -> bool:
        """
        Check if a candidate password matches the stored hash.

        Uses constant-time comparison to prevent timing attacks.

        Args:
            candidate: Password to verify

        Returns:
            True if password matches, False otherwise
        """
        if self.__password_hash is None:
            return False

        candidate_hash = _hash_password(candidate, self.__salt)
        # hmac.compare_digest prevents timing attacks
        return hmac.compare_digest(candidate_hash, self.__password_hash)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"User(email={self.email!r}, user_id={self.user_id}, role={self.role.value!r})"


# Demonstrate User class
print("\nCreating user...")
user = User(
    email="alice.student@example.com",
    password="SecurePass123",
    user_id=1001,
    role=Role.STUDENT
)

print(f"\nUser object: {user}")
print(f"Email: {user.email}")
print(f"Password (via getter): {user.password}  ← Always masked!")
print(f"Role: {user.role.value}")

print("\nVerifying passwords:")
print(f"Correct password 'SecurePass123': {user.verify_password('SecurePass123')}")
print(f"Wrong password 'WrongPass': {user.verify_password('WrongPass')}")
print(f"Empty password '': {user.verify_password('')}")


# ==========================================================================
# SECTION 4: IMPROVING USER CLASS - EMAIL VALIDATION
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 4: ADDING EMAIL VALIDATION")
print("=" * 70)


class UserWithEmailValidation(User):
    """Extended User class with email validation."""

    def __init__(
        self,
        email: str,
        password: str,
        user_id: int,
        role: Role = Role.STUDENT
    ) -> None:
        if not self._validate_email(email):
            raise ValueError(f"❌ Invalid email: {email}")
        super().__init__(email, password, user_id, role)

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Simple email validation (production code needs more checks)."""
        return "@" in email and "." in email.split("@")[1]


try:
    valid_user = UserWithEmailValidation(
        email="bob.analyst@company.com",
        password="AnotherPass456",
        user_id=1002,
        role=Role.ANALYST
    )
    print(f"✅ Created: {valid_user}")
except ValueError as e:
    print(f"Error: {e}")

try:
    invalid_user = UserWithEmailValidation(
        email="invalid-email",
        password="SomePass123",
        user_id=1003
    )
except ValueError as e:
    print(f"❌ {e}")


# ==========================================================================
# SECTION 5: NAME MANGLING - NOT REAL SECURITY
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 5: UNDERSTANDING NAME MANGLING (NOT SECURITY)")
print("=" * 70)

print("\n⚠️  Python name mangling (__attribute) is NOT a security feature!")
print("It's just a convention to avoid accidental name conflicts in inheritance.\n")

user2 = User(email="charlie@example.com", password="YetAnother789", user_id=1004)

# Name mangling makes attributes inaccessible by default name
print("Direct access to __password_hash (fails):")
try:
    print(f"  user2.__password_hash = {user2.__password_hash}")
except AttributeError as e:
    print(f"  ❌ AttributeError: {e}")

# But we can still access it using the mangled name
print("\nAccess via name mangling (works!):")
mangled_hash = user2._User__password_hash
print(f"  user2._User__password_hash = {mangled_hash[:8].hex()}...")
print("  ⚠️  Lesson: Name mangling only prevents ACCIDENTAL access, not deliberate!")

print("\n💡 For real security:")
print("  - Use OS-level security (files with restricted permissions)")
print("  - Use encryption for sensitive data at rest")
print("  - Use TLS/HTTPS for data in transit")
print("  - Never rely on Python conventions for security")


# ==========================================================================
# SECTION 6: PRACTICAL EXAMPLE - BANK ACCOUNT
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 6: PRACTICAL EXAMPLE - BANK ACCOUNT WITH ENCAPSULATION")
print("=" * 70)


class BankAccount:
    """Demonstrates why encapsulation matters with mutable state."""

    def __init__(self, account_number: str, owner: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        self.__balance = initial_balance  # Private to prevent unauthorized changes

    @property
    def balance(self) -> float:
        """Read-only balance access."""
        return self.__balance

    def deposit(self, amount: float) -> bool:
        """Deposit money with validation."""
        if amount <= 0:
            print(f"❌ Cannot deposit {amount}: amount must be positive")
            return False
        self.__balance += amount
        print(f"✅ Deposited {amount}. New balance: {self.__balance}")
        return True

    def withdraw(self, amount: float) -> bool:
        """Withdraw money with validation."""
        if amount <= 0:
            print(f"❌ Cannot withdraw {amount}: amount must be positive")
            return False
        if amount > self.__balance:
            print(f"❌ Cannot withdraw {amount}: insufficient funds (balance: {self.__balance})")
            return False
        self.__balance -= amount
        print(f"✅ Withdrew {amount}. New balance: {self.__balance}")
        return True

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, account={self.account_number}, balance={self.balance})"


# Demonstrate bank account
account = BankAccount("UA2834756203", owner="Diana Student", initial_balance=1000.0)
print(f"\n{account}")
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)  # Fails - insufficient funds
print(f"\nFinal: {account}")


# ==========================================================================
# SUMMARY
# ==========================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

summary_text = """
✅ KEY CONCEPTS:

1. ENCAPSULATION: Hide internal details, expose only necessary interface
   - Public attributes: freely accessible (email, user_id)
   - Private attributes: use __ prefix, harder to access accidentally
   - Properties: control get/set behavior with @property

2. PASSWORD SECURITY:
   - Hash passwords, never store plain text
   - Use salt to prevent rainbow table attacks
   - Use PBKDF2 (or better: bcrypt, Argon2)
   - Verify with hmac.compare_digest (prevents timing attacks)

3. ENUMS: Better than magic strings for constants
   - Type-safe and enumerable
   - IDE autocomplete support
   - Self-documenting code

4. NAME MANGLING (__attr) is NOT security:
   - Just prevents accidental access
   - Deliberate access still possible: _ClassName__attr
   - Use real security measures for sensitive data

5. VALIDATION: Check inputs in property setters
   - Prevent invalid state
   - Clear error messages
   - Fail fast

💡 USE CASES IN YOUR CAREER:
   - User authentication systems (web apps, APIs)
   - Access control (role-based permissions)
   - Data protection (PII, financial data, health records)
   - Configuration management (API keys, secrets)
"""

print(summary_text)
