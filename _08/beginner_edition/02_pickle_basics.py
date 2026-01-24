"""
Module 8.2: Pickle Serialization Basics
========================================

Learning Goals:
- Understand object serialization (converting objects to bytes)
- Learn pickle protocol and limitations
- Implement __getstate__ and __setstate__ for custom serialization
- Handle pickle files safely
- Understand pickle security risks

🔍 Where you'll use this:
- Caching computation results in ML pipelines
- Saving training models
- Distributed computing (passing objects between processes)
- Application state persistence

⚡ Data Science/Engineering Context:
- Scikit-learn uses pickle for model persistence
- Cached computations in data pipelines
- Distributed processing (Spark, Dask, Ray)
- Database session caching

🔒 SECURITY WARNING: Never unpickle data from untrusted sources!
   Pickle can execute arbitrary code during deserialization.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from datetime import datetime, timezone


# ==========================================================================
# SECTION 1: BASIC PICKLE - SIMPLE OBJECTS
# ==========================================================================

print("=" * 70)
print("SECTION 1: BASIC PICKLE - SIMPLE OBJECTS")
print("=" * 70)


@dataclass
class Address:
    """Simple dataclass for address information."""
    city: str
    country: str
    zip_code: str


# Create objects
address = Address(city="Kyiv", country="Ukraine", zip_code="01001")
print(f"\nOriginal address: {address}")

# Serialize to bytes
serialized = pickle.dumps(address)
print(f"Serialized (pickle bytes): {serialized[:50]}...")
print(f"Serialized size: {len(serialized)} bytes")

# Deserialize back to object
restored = pickle.loads(serialized)
print(f"Restored address: {restored}")
print(f"Type matches: {type(restored) == type(address)}")
print(f"Values match: {restored == address}")


# ==========================================================================
# SECTION 2: PICKLING LISTS OF OBJECTS
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 2: PICKLING LISTS OF OBJECTS")
print("=" * 70)


addresses = [
    Address(city="Kyiv", country="Ukraine", zip_code="01001"),
    Address(city="Lviv", country="Ukraine", zip_code="79000"),
    Address(city="Warsaw", country="Poland", zip_code="00-001"),
]

print("\nOriginal list:")
for i, addr in enumerate(addresses):
    print(f"  {i+1}. {addr}")

# Serialize the whole list
serialized_list = pickle.dumps(addresses)
print(f"\nSerialized size: {len(serialized_list)} bytes")

# Deserialize
restored_list = pickle.loads(serialized_list)
print("\nRestored list:")
for i, addr in enumerate(restored_list):
    print(f"  {i+1}. {addr}")


# ==========================================================================
# SECTION 3: PICKLE TO FILE
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 3: PICKLE TO FILE (PERSISTENCE)")
print("=" * 70)

# Save to file
filename = "addresses.pkl"
with open(filename, "wb") as f:
    pickle.dump(addresses, f)
    print(f"✅ Saved {len(addresses)} addresses to {filename}")

# Load from file
with open(filename, "rb") as f:
    loaded_addresses = pickle.load(f)
    print(f"✅ Loaded {len(loaded_addresses)} addresses from {filename}")

print("\nLoaded data:")
for addr in loaded_addresses:
    print(f"  - {addr.city}, {addr.country}")


# ==========================================================================
# SECTION 4: CUSTOM SERIALIZATION WITH __getstate__ and __setstate__
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 4: CUSTOM SERIALIZATION (__getstate__ and __setstate__)")
print("=" * 70)


class User:
    """User class with custom serialization behavior."""

    def __init__(self, user_id: int, email: str, address: Address):
        self.user_id = user_id
        self.email = email
        self.address = address
        self.created_at = datetime.now(timezone.utc)
        self.__password_hash = "hashed-password-demo"  # Demo only

    def __getstate__(self) -> dict:
        """
        Called when pickling. Return the state to serialize.

        Use this to exclude sensitive fields or transform data.
        """
        state = self.__dict__.copy()
        # Remove sensitive password field before saving
        state.pop("_User__password_hash", None)
        print(f"  ℹ️  __getstate__: Removing password hash before serialization")
        return state

    def __setstate__(self, state: dict) -> None:
        """
        Called when unpickling. Restore from the saved state.

        Use this to migrate old formats or re-initialize missing fields.
        """
        print(f"  ℹ️  __setstate__: Restoring user {state.get('email')}")
        # Add new fields that might not exist in old pickles
        state.setdefault("__password_hash", None)
        self.__dict__.update(state)

    def __repr__(self) -> str:
        return f"User(id={self.user_id}, email={self.email!r}, city={self.address.city!r})"


# Create and serialize a user
user = User(
    user_id=1001,
    email="alice@example.com",
    address=Address(city="Lviv", country="Ukraine", zip_code="79000")
)
print(f"\nOriginal: {user}")

# Serialize
print("\nSerializing...")
user_bytes = pickle.dumps(user)
print(f"Serialized size: {len(user_bytes)} bytes")

# Deserialize
print("\nDeserializing...")
restored_user = pickle.loads(user_bytes)
print(f"Restored: {restored_user}")
print(f"Password hash preserved? {hasattr(restored_user, '_User__password_hash')}")
print("Note: Password hash was removed by __getstate__ for security")


# ==========================================================================
# SECTION 5: PICKLE PROTOCOLS
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 5: PICKLE PROTOCOLS")
print("=" * 70)

print("\nPickle protocols (different formats for different use cases):\n")

protocols_info = {
    0: "ASCII (human-readable, large, old Python versions)",
    1: "Old binary (Python 1.x era)",
    2: "Binary (Python 2.3+)",
    3: "Binary (Python 3.0+, supports bytes)",
    4: "Binary (Python 3.4+, larger objects, faster)",
    5: "Binary (Python 3.8+, out-of-band data, zero-copy)",
}

data_to_pickle = {"addresses": addresses, "user": user}

print("Comparing sizes across protocols:")
for protocol in range(6):
    try:
        serialized = pickle.dumps(data_to_pickle, protocol=protocol)
        print(f"  Protocol {protocol}: {len(serialized):6d} bytes  - {protocols_info.get(protocol, 'unknown')}")
    except Exception as e:
        print(f"  Protocol {protocol}: Not available ({e})")

print("\n💡 Recommendation:")
print("  - Use protocol=5 for new code (smaller, faster, better compatibility)")
print("  - Use protocol=4 if you need Python 3.4-3.7 compatibility")
print("  - Avoid protocol 0-2 unless you have legacy system requirements")


# ==========================================================================
# SECTION 6: ERROR HANDLING
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 6: ERROR HANDLING")
print("=" * 70)

# Handle corrupted pickle
print("\nAttempting to unpickle corrupted data:")
corrupted_data = b"not a real pickle"
try:
    pickle.loads(corrupted_data)
except (pickle.UnpicklingError, ValueError) as e:
    print(f"❌ {type(e).__name__}: {e}")

# Handle missing class
print("\nAttempting to unpickle object with missing class:")
# This would fail if the class definition changed or module was deleted
# For now, we just document it
print("(Skipped - would require deleting class definition first)")


# ==========================================================================
# SECTION 7: PICKLE WITH CONTEXT MANAGERS (BEST PRACTICE)
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 7: USING CONTEXT MANAGERS (BEST PRACTICE)")
print("=" * 70)

def save_objects(objects: list, filename: str, protocol: int = 5) -> None:
    """Save objects to pickle file using context manager."""
    with open(filename, "wb") as f:
        pickle.dump(objects, f, protocol=protocol)
    print(f"✅ Saved {len(objects)} objects to {filename}")


def load_objects(filename: str) -> list:
    """Load objects from pickle file using context manager."""
    with open(filename, "rb") as f:
        objects = pickle.load(f)
    print(f"✅ Loaded {len(objects)} objects from {filename}")
    return objects


# Demonstrate
filename = "demo_objects.pkl"
demo_data = [address, user, addresses]

save_objects(demo_data, filename)
loaded_data = load_objects(filename)

print(f"\nLoaded {len(loaded_data)} items:")
for item in loaded_data:
    print(f"  - {type(item).__name__}: {item}")


# ==========================================================================
# SECTION 8: PERFORMANCE CONSIDERATION
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 8: PICKLE PERFORMANCE")
print("=" * 70)

import sys

# Pickle creates references to objects, reducing size
shared_address = Address(city="Kyiv", country="Ukraine", zip_code="01001")
users_with_shared_address = [
    User(i, f"user{i}@example.com", shared_address)
    for i in range(3)
]

print("\n3 users sharing same address object:")
print(f"  Memory (in-memory): {sys.getsizeof(users_with_shared_address)} bytes")

serialized = pickle.dumps(users_with_shared_address, protocol=5)
print(f"  Pickled: {len(serialized)} bytes")

print("\nPickle preserves object references:")
print("  Shared objects won't be duplicated in the pickle")
print("  After unpickling, if you modify shared address, it affects all users")


# ==========================================================================
# SUMMARY
# ==========================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

summary = """
✅ KEY PICKLE CONCEPTS:

1. WHAT IS PICKLE?
   - Serializes Python objects to bytes (binary format)
   - Protocol 5 is recommended for modern Python
   - Works with any Python object (lists, dicts, custom classes)

2. WHEN TO USE PICKLE:
   ✓ Saving ML models (scikit-learn)
   ✓ Caching computation results
   ✓ IPC (inter-process communication)
   ✓ Distributed computing frameworks
   ✗ DO NOT use for data persistence across Python versions
   ✗ DO NOT use for data interchange with other languages (use JSON/Parquet)

3. CUSTOM SERIALIZATION:
   - __getstate__(): Control what gets serialized (e.g., exclude passwords)
   - __setstate__(): Control how data is restored (e.g., migrate old formats)

4. SECURITY CONSIDERATIONS:
   ⚠️  NEVER unpickle data from untrusted sources!
   ⚠️  Pickle can execute arbitrary Python code during deserialization
   ✓ Only unpickle data you created or trust completely
   ✓ Use restricted unpicklers for safer deserialization

5. PICKLE ALTERNATIVES:
   - JSON: Text format, human-readable, cross-language
   - MessagePack: Binary format, smaller than pickle, cross-language
   - Parquet: For large datasets, columnar format
   - Protocol Buffers: Schema-based, strongly typed

💡 BEST PRACTICES:
   - Use context managers (with statement)
   - Specify protocol=5 explicitly
   - Test unpickling with actual pickled data
   - Document pickle file format and version
   - Consider protocol compatibility if needed
"""

print(summary)
