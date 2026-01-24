"""
Module 8.3: JSON and CSV Serialization Basics
==============================================

Learning Goals:
- Serialize objects to JSON (text format, human-readable)
- Serialize objects to CSV (tabular format for spreadsheets)
- Implement custom object serialization with object_hook
- Handle nested data structures
- Understand JSON limitations

🔍 Where you'll use this:
- API responses and requests (JSON)
- Configuration files (JSON, YAML)
- Data exports to Excel/Sheets (CSV)
- Web application data interchange
- Database imports/exports

⚡ Data Science/Engineering Context:
- JSON: API communication (ML APIs, cloud services)
- CSV: Data warehouse exports, analysis in spreadsheets
- Both: Data validation pipelines, ETL configurations
- Analytics: Generating reports in CSV for stakeholders

💡 Key Difference from Pickle:
- JSON/CSV are TEXT formats (human-readable, safe)
- JSON can be parsed by any programming language
- CSV is standard for tabular data (Excel, Pandas, databases)
- Pickle is BINARY format (Python-only, faster, safer objects)
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


# ==========================================================================
# SECTION 1: SIMPLE OBJECTS TO JSON
# ==========================================================================

print("=" * 70)
print("SECTION 1: SIMPLE OBJECTS TO JSON")
print("=" * 70)


@dataclass
class Address:
    """Address dataclass with serialization methods."""
    city: str
    country: str
    zip_code: str

    def to_dict(self) -> dict:
        """Convert to dictionary (needed for JSON serialization)."""
        return {
            "city": self.city,
            "country": self.country,
            "zip_code": self.zip_code,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Address:
        """Reconstruct Address from dictionary."""
        return cls(
            city=data["city"],
            country=data["country"],
            zip_code=data["zip_code"]
        )


# Create and serialize
address = Address(city="Kyiv", country="Ukraine", zip_code="01001")
address_dict = address.to_dict()

print(f"\nOriginal object: {address}")
print(f"As dictionary: {address_dict}")

# Convert to JSON string
json_string = json.dumps(address_dict, indent=2)
print(f"\nJSON representation:\n{json_string}")

# Parse back from JSON
parsed_dict = json.loads(json_string)
restored_address = Address.from_dict(parsed_dict)
print(f"Restored object: {restored_address}")
print(f"Objects equal: {address == restored_address}")


# ==========================================================================
# SECTION 2: COMPLEX OBJECTS WITH NESTED DATA
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 2: COMPLEX OBJECTS WITH NESTED DATA")
print("=" * 70)


class User:
    """User class with address (composition)."""

    def __init__(
        self,
        user_id: int,
        email: str,
        address: Address,
        created_at: datetime | None = None
    ):
        self.user_id = user_id
        self.email = email
        self.address = address
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Serialize to dict, handling nested Address."""
        return {
            "__type__": "User",  # Marker for custom deserialization
            "user_id": self.user_id,
            "email": self.email,
            "address": self.address.to_dict(),  # Nested object
            "created_at": self.created_at.isoformat(),  # DateTime as ISO string
        }

    @classmethod
    def from_dict(cls, data: dict) -> User:
        """Reconstruct User from dict, handling nested Address."""
        address = Address.from_dict(data["address"])
        created_at = datetime.fromisoformat(data["created_at"])
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            address=address,
            created_at=created_at
        )

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, email={self.email!r}, city={self.address.city!r})"


# Create users
users = [
    User(1, "alice@example.com", Address("Lviv", "Ukraine", "79000")),
    User(2, "bob@example.com", Address("Warsaw", "Poland", "00-001")),
    User(3, "charlie@example.com", Address("Berlin", "Germany", "10115")),
]

print("\nOriginal users:")
for user in users:
    print(f"  - {user}")

# Convert to JSON with pretty printing
json_data = json.dumps([u.to_dict() for u in users], indent=2)
print(f"\nJSON representation:\n{json_data}")


# ==========================================================================
# SECTION 3: CUSTOM DESERIALIZATION WITH object_hook
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 3: AUTOMATIC DESERIALIZATION WITH object_hook")
print("=" * 70)


def user_object_hook(obj: dict) -> Any:
    """
    Custom hook called during JSON deserialization.

    This allows automatic conversion of dicts to User objects.
    """
    if obj.get("__type__") == "User":
        print(f"  ℹ️  Deserializing User: {obj['email']}")
        return User.from_dict(obj)
    return obj


print("\nDeserializing JSON with custom hook:")
restored_users = json.loads(json_data, object_hook=user_object_hook)

print("\nRestored users:")
for user in restored_users:
    print(f"  - {user} (type: {type(user).__name__})")

print("\n✅ Notice: object_hook automatically converted dicts to User objects!")


# ==========================================================================
# SECTION 4: JSON LIMITATIONS
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 4: JSON LIMITATIONS (WHAT YOU CAN'T SERIALIZE)")
print("=" * 70)

print("\nJSON supports only these types:")
print("  - Strings (\"text\")")
print("  - Numbers (42, 3.14)")
print("  - Booleans (true, false)")
print("  - null (None in Python)")
print("  - Arrays/Lists ([1, 2, 3])")
print("  - Objects/Dicts ({\"key\": \"value\"})")

print("\nJSON does NOT support:")
print("  - datetime (must convert to string first)")
print("  - bytes (must encode to base64)")
print("  - sets (must convert to list)")
print("  - custom classes (must convert to dict)")

# Example: why datetime fails
print("\nExample: Attempting to serialize datetime directly:")
try:
    json.dumps({"created_at": datetime.now(timezone.utc)})
except TypeError as e:
    print(f"  ❌ TypeError: {e}")

print("\nSolution: Convert to ISO format string first:")
created_at_str = datetime.now(timezone.utc).isoformat()
print(f"  ✅ {json.dumps({'created_at': created_at_str})}")


# ==========================================================================
# SECTION 5: CSV SERIALIZATION
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 5: CSV SERIALIZATION (FOR SPREADSHEETS)")
print("=" * 70)


def users_to_csv(users: list[User], filename: str) -> None:
    """Export users to CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        # Define columns
        fieldnames = ["user_id", "email", "city", "country", "zip_code", "created_at"]

        # Create CSV writer
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write data rows (flattening nested Address)
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


# Export to CSV
csv_filename = "users_export.csv"
users_to_csv(users, csv_filename)

# Show the CSV content
print(f"\nCSV file content:")
with open(csv_filename, "r") as f:
    content = f.read()
    print(content)


# ==========================================================================
# SECTION 6: CSV DESERIALIZATION
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 6: CSV DESERIALIZATION")
print("=" * 70)


def users_from_csv(filename: str) -> list[User]:
    """Import users from CSV file."""
    users = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # Each row is a dict
        for row in reader:
            print(f"  Reading: {row['email']}")
            # Reconstruct Address from flattened columns
            address = Address(
                city=row["city"],
                country=row["country"],
                zip_code=row["zip_code"]
            )
            # Reconstruct User
            user = User(
                user_id=int(row["user_id"]),
                email=row["email"],
                address=address,
                created_at=datetime.fromisoformat(row["created_at"])
            )
            users.append(user)

    print(f"✅ Imported {len(users)} users from {filename}")
    return users


# Import from CSV
imported_users = users_from_csv(csv_filename)

print("\nImported users:")
for user in imported_users:
    print(f"  - {user}")


# ==========================================================================
# SECTION 7: PRETTY PRINTING JSON
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 7: PRETTY PRINTING JSON")
print("=" * 70)

user_data = users[0].to_dict()

print("\nCompact JSON (one line):")
print(json.dumps(user_data))

print("\nPretty JSON (indent=2):")
print(json.dumps(user_data, indent=2))

print("\nPretty JSON (indent=4, sorted keys):")
print(json.dumps(user_data, indent=4, sort_keys=True))


# ==========================================================================
# SECTION 8: HANDLING MISSING OR EXTRA FIELDS
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 8: ROBUST DESERIALIZATION")
print("=" * 70)

# What if JSON is missing fields or has extra fields?
incomplete_json = '''
{
    "__type__": "User",
    "user_id": 999,
    "email": "newuser@example.com",
    "address": {"city": "Paris", "country": "France"},
    "extra_field": "ignored"
}
'''

print("\nAttempting to deserialize incomplete data:")
try:
    incomplete_dict = json.loads(incomplete_json)
    # This will fail because zip_code is missing
    restored = User.from_dict(incomplete_dict)
except KeyError as e:
    print(f"  ❌ KeyError: Missing required field {e}")

print("\nSolution: Use dict.get() with defaults:")


def address_from_dict_safe(data: dict) -> Address:
    """Safer version with defaults for missing fields."""
    return Address(
        city=data.get("city", "Unknown"),
        country=data.get("country", "Unknown"),
        zip_code=data.get("zip_code", "00000")
    )


def user_from_dict_safe(data: dict) -> User:
    """Safer User deserialization with defaults."""
    address = address_from_dict_safe(data.get("address", {}))
    return User(
        user_id=data.get("user_id", 0),
        email=data.get("email", "unknown@example.com"),
        address=address,
        created_at=None  # Will use current time
    )


incomplete_dict = json.loads(incomplete_json)
safe_user = user_from_dict_safe(incomplete_dict)
print(f"  ✅ Restored safely: {safe_user}")


# ==========================================================================
# SUMMARY
# ==========================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

summary = """
✅ KEY CONCEPTS:

1. JSON SERIALIZATION:
   ✓ Text format, human-readable, cross-language
   ✓ Implement to_dict() and from_dict() for custom classes
   ✓ Handle nested objects by serializing recursively
   ✓ Convert non-JSON types (datetime, bytes) to strings

2. CSV SERIALIZATION:
   ✓ Use csv.DictWriter for structured output
   ✓ Use csv.DictReader for structured input
   ✓ Flatten nested objects (Address → city, country, zip_code)
   ✓ Best for tabular data (rows × columns)

3. CUSTOM DESERIALIZATION:
   ✓ Use object_hook in json.loads() for automatic conversion
   ✓ Use __type__ markers to distinguish different classes
   ✓ Handle missing fields with dict.get(key, default)

4. WHEN TO USE:
   ✓ JSON: APIs, web applications, configuration files
   ✓ CSV: Spreadsheets, data analysis, database imports
   ✗ JSON: Binary data, custom Python objects (use pickle)
   ✗ CSV: Nested/hierarchical data (use JSON)

5. GOTCHAS:
   ⚠️  datetime → must convert to string (isoformat())
   ⚠️  bytes → must encode to base64 or hex
   ⚠️  sets → must convert to list
   ⚠️  Circular references → will cause infinite recursion

💡 BEST PRACTICES:
   - Always implement both to_dict() AND from_dict()
   - Use object_hook for automatic deserialization
   - Handle missing fields with defaults
   - Test with incomplete/malformed data
   - Use sorted_keys=True for deterministic JSON output
"""

print(summary)
