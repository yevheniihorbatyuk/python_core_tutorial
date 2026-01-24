"""
Module 8.1 (Advanced): Modern Encapsulation Patterns
====================================================

Learning Goals:
- Use dataclasses with field validation
- Implement Pydantic models for production
- Create computed properties with descriptors
- Optimize memory with __slots__
- Design abstract base classes
- Handle complex validation scenarios

🔍 Production Patterns:
- Dataclasses for data container optimization
- Pydantic for external API validation
- Descriptors for complex property behavior
- ABC for interface contracts

⚡ Data Science/Engineering Context:
- DataPipeline configuration with validation
- ETL stage validation
- ML model hyperparameter validation
- Feature store schema validation

🏗️ Architecture Focus:
- Type safety through dataclasses and Pydantic
- Runtime validation of config/data
- Memory efficiency with __slots__
- Clean API design with ABCs
"""

from __future__ import annotations

import abc
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Final, Optional

try:
    from pydantic import BaseModel, Field, field_validator, ConfigDict
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    print("⚠️  Pydantic not installed. Install with: pip install pydantic")


# ==========================================================================
# SECTION 1: DATACLASSES WITH FIELD VALIDATION
# ==========================================================================

print("=" * 80)
print("SECTION 1: DATACLASSES WITH FIELD VALIDATION")
print("=" * 80)


@dataclass
class DatabaseConfig:
    """Database configuration with validation in __post_init__."""

    host: str
    port: int
    database: str
    username: str
    password: str
    pool_size: int = 10
    timeout: float = 30.0
    ssl_enabled: bool = True

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.host:
            raise ValueError("Host cannot be empty")
        if not 1 <= self.port <= 65535:
            raise ValueError(f"Port must be 1-65535, got {self.port}")
        if not self.database:
            raise ValueError("Database name cannot be empty")
        if self.pool_size < 1 or self.pool_size > 100:
            raise ValueError(f"Pool size must be 1-100, got {self.pool_size}")
        if self.timeout <= 0:
            raise ValueError(f"Timeout must be positive, got {self.timeout}")

    @property
    def connection_string(self) -> str:
        """Computed property: connection string."""
        protocol = "postgresql+psycopg2" if "postgres" in self.host.lower() else "mysql+pymysql"
        return f"{protocol}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def to_dict(self, include_password: bool = False) -> dict:
        """Convert to dict, optionally excluding password."""
        result = {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "pool_size": self.pool_size,
            "timeout": self.timeout,
            "ssl_enabled": self.ssl_enabled,
        }
        if include_password:
            result["username"] = self.username
            result["password"] = self.password
        return result


print("\nCreating valid database config:")
db_config = DatabaseConfig(
    host="db.example.com",
    port=5432,
    database="production_db",
    username="admin",
    password="secret"
)
print(f"✅ {db_config}")
print(f"Connection string: {db_config.connection_string}")

print("\nAttempting invalid config:")
try:
    bad_config = DatabaseConfig(
        host="db.example.com",
        port=99999,  # Invalid!
        database="test",
        username="user",
        password="pass"
    )
except ValueError as e:
    print(f"❌ {e}")


# ==========================================================================
# SECTION 2: PYDANTIC MODELS FOR PRODUCTION
# ==========================================================================

print("\n" + "=" * 80)
print("SECTION 2: PYDANTIC MODELS FOR PRODUCTION")
print("=" * 80)

if HAS_PYDANTIC:
    class APIConfig(BaseModel):
        """API configuration with Pydantic validation."""

        model_config = ConfigDict(
            str_strip_whitespace=True,
            validate_default=True,
            use_enum_values=True,
        )

        base_url: str = Field(..., description="Base URL for API", examples=["https://api.example.com"])
        api_key: str = Field(..., description="API key", min_length=20)
        timeout: float = Field(default=30.0, gt=0, le=300, description="Timeout in seconds")
        retries: int = Field(default=3, ge=0, le=10, description="Number of retries")
        environment: str = Field(default="development", pattern="^(development|staging|production)$")
        allowed_methods: list[str] = Field(default_factory=lambda: ["GET", "POST"])

        @field_validator("base_url")
        @classmethod
        def validate_base_url(cls, v: str) -> str:
            """Validate that base_url is a valid URL."""
            if not v.startswith(("http://", "https://")):
                raise ValueError("base_url must start with http:// or https://")
            return v

        @field_validator("allowed_methods")
        @classmethod
        def validate_methods(cls, v: list[str]) -> list[str]:
            """Validate HTTP methods."""
            valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
            for method in v:
                if method not in valid_methods:
                    raise ValueError(f"Invalid HTTP method: {method}")
            return v

        def to_safe_dict(self) -> dict:
            """Convert to dict without sensitive data."""
            data = self.model_dump()
            if "api_key" in data:
                data["api_key"] = data["api_key"][:5] + "***"
            return data

    print("\nCreating Pydantic API config:")
    api_config = APIConfig(
        base_url="https://api.example.com",
        api_key="sk-1234567890abcdefghij",
        environment="production"
    )
    print(f"✅ {api_config}")
    print(f"Safe dict: {api_config.to_safe_dict()}")

    print("\nValidation errors:")
    try:
        bad_api = APIConfig(
            base_url="not-a-url",  # Invalid!
            api_key="short",  # Too short!
            allowed_methods=["INVALID"]  # Invalid method!
        )
    except Exception as e:
        print(f"❌ Validation failed: {e}")

else:
    print("\n⚠️  Pydantic not installed. Install with: pip install pydantic")
    print("Skipping Pydantic examples.")


# ==========================================================================
# SECTION 3: DESCRIPTORS FOR ADVANCED PROPERTIES
# ==========================================================================

print("\n" + "=" * 80)
print("SECTION 3: DESCRIPTORS FOR ADVANCED PROPERTIES")
print("=" * 80)


class BoundedInt:
    """Descriptor for integers with min/max bounds."""

    def __init__(self, name: str, min_val: int, max_val: int):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.private_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any = None) -> int:
        """Get the value."""
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj: Any, value: int) -> None:
        """Set with validation."""
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be int, got {type(value)}")
        if not self.min_val <= value <= self.max_val:
            raise ValueError(f"{self.name} must be {self.min_val}-{self.max_val}, got {value}")
        setattr(obj, self.private_name, value)


class BoundedFloat:
    """Descriptor for floats with min/max bounds."""

    def __init__(self, name: str, min_val: float, max_val: float):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.private_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any = None) -> float:
        """Get the value."""
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj: Any, value: float) -> None:
        """Set with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be float, got {type(value)}")
        float_value = float(value)
        if not self.min_val <= float_value <= self.max_val:
            raise ValueError(f"{self.name} must be {self.min_val}-{self.max_val}, got {float_value}")
        setattr(obj, self.private_name, float_value)


class ModelHyperparameters:
    """ML model hyperparameters using descriptors."""

    learning_rate = BoundedFloat("learning_rate", 0.0, 1.0)
    batch_size = BoundedInt("batch_size", 1, 1024)
    epochs = BoundedInt("epochs", 1, 10000)

    def __init__(self, learning_rate: float, batch_size: int, epochs: int):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epochs = epochs

    def __repr__(self) -> str:
        return f"Hyperparameters(lr={self.learning_rate}, bs={self.batch_size}, ep={self.epochs})"


print("\nUsing descriptors for validation:")
try:
    params = ModelHyperparameters(learning_rate=0.001, batch_size=32, epochs=100)
    print(f"✅ {params}")
except ValueError as e:
    print(f"❌ {e}")

print("\nAttempting invalid value:")
try:
    params.batch_size = 2000  # Too large!
except ValueError as e:
    print(f"❌ {e}")


# ==========================================================================
# SECTION 4: MEMORY OPTIMIZATION WITH __slots__
# ==========================================================================

print("\n" + "=" * 80)
print("SECTION 4: MEMORY OPTIMIZATION WITH __slots__")
print("=" * 80)

import sys


class Point:
    """Point without __slots__ (uses __dict__)."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class PointSlots:
    """Point with __slots__ (optimized memory)."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


print("\nMemory comparison:")
p1 = Point(1.0, 2.0, 3.0)
p2 = PointSlots(1.0, 2.0, 3.0)

print(f"Point (with __dict__): {sys.getsizeof(p1)} bytes")
print(f"PointSlots (__slots__): {sys.getsizeof(p2)} bytes")

# For thousands of objects
points = [Point(i, i+1, i+2) for i in range(1000)]
slots_points = [PointSlots(i, i+1, i+2) for i in range(1000)]

total_regular = sum(sys.getsizeof(p) for p in points)
total_slots = sum(sys.getsizeof(p) for p in slots_points)

print(f"\n1000 Points: {total_regular} bytes")
print(f"1000 PointSlots: {total_slots} bytes")
print(f"Savings: {total_regular - total_slots} bytes ({(1 - total_slots/total_regular)*100:.1f}%)")

print("\n💡 __slots__ benefits:")
print("  - Reduces memory by ~40% for thousands of objects")
print("  - Faster attribute access")
print("  - Prevents adding arbitrary attributes (safer)")


# ==========================================================================
# SECTION 5: ABSTRACT BASE CLASSES FOR INTERFACES
# ==========================================================================

print("\n" + "=" * 80)
print("SECTION 5: ABSTRACT BASE CLASSES FOR INTERFACES")
print("=" * 80)


class Serializer(abc.ABC):
    """Abstract base class for serialization strategies."""

    @abc.abstractmethod
    def serialize(self, obj: Any) -> bytes:
        """Serialize object to bytes."""
        pass

    @abc.abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Deserialize bytes to object."""
        pass

    @abc.abstractmethod
    def format_name(self) -> str:
        """Return format name."""
        pass


class JSONSerializer(Serializer):
    """JSON serialization implementation."""

    import json

    def serialize(self, obj: dict) -> bytes:
        """Serialize dict to JSON bytes."""
        return json.dumps(obj).encode("utf-8")

    def deserialize(self, data: bytes) -> dict:
        """Deserialize JSON bytes to dict."""
        return json.loads(data.decode("utf-8"))

    def format_name(self) -> str:
        return "JSON"


class PickleSerializer(Serializer):
    """Pickle serialization implementation."""

    import pickle

    def serialize(self, obj: Any) -> bytes:
        """Serialize object to pickle bytes."""
        return self.pickle.dumps(obj, protocol=5)

    def deserialize(self, data: bytes) -> Any:
        """Deserialize pickle bytes to object."""
        return self.pickle.loads(data)

    def format_name(self) -> str:
        return "Pickle"


print("\nUsing abstract base class pattern:")

data = {"name": "Alice", "age": 30}

for serializer_class in [JSONSerializer, PickleSerializer]:
    serializer = serializer_class()
    print(f"\n{serializer.format_name()} Serializer:")
    serialized = serializer.serialize(data)
    print(f"  Serialized: {len(serialized)} bytes")
    deserialized = serializer.deserialize(serialized)
    print(f"  Deserialized: {deserialized}")


# ==========================================================================
# SECTION 6: DATACLASS FACTORIES
# ==========================================================================

print("\n" + "=" * 80)
print("SECTION 6: DATACLASS FACTORIES")
print("=" * 80)


@dataclass
class DataPipelineConfig:
    """Configuration for ETL pipeline."""

    name: str
    input_path: str
    output_path: str
    batch_size: int = 1000
    parallel_jobs: int = 4
    retry_count: int = 3
    timeout_seconds: float = 300.0
    _created_at: str = field(default_factory=lambda: __import__('datetime').datetime.now(
        __import__('datetime').timezone.utc
    ).isoformat())

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.batch_size < 1:
            raise ValueError("batch_size must be positive")
        if self.parallel_jobs < 1:
            raise ValueError("parallel_jobs must be positive")

    @classmethod
    def for_development(cls) -> DataPipelineConfig:
        """Factory: development configuration."""
        return cls(
            name="dev-pipeline",
            input_path="/tmp/input",
            output_path="/tmp/output",
            batch_size=10,
            parallel_jobs=1,
            retry_count=1
        )

    @classmethod
    def for_production(cls) -> DataPipelineConfig:
        """Factory: production configuration."""
        return cls(
            name="prod-pipeline",
            input_path="/data/input",
            output_path="/data/output",
            batch_size=10000,
            parallel_jobs=8,
            retry_count=5
        )

    @classmethod
    def from_dict(cls, data: dict) -> DataPipelineConfig:
        """Factory: from dictionary."""
        return cls(**{k: v for k, v in data.items() if k != "_created_at"})


print("\nUsing dataclass factories:")

print("\nDevelopment config:")
dev_config = DataPipelineConfig.for_development()
print(f"  {dev_config}")

print("\nProduction config:")
prod_config = DataPipelineConfig.for_production()
print(f"  {prod_config}")

print("\nFrom dictionary:")
config_dict = {"name": "custom", "input_path": "/input", "output_path": "/output", "batch_size": 5000}
custom_config = DataPipelineConfig.from_dict(config_dict)
print(f"  {custom_config}")


# ==========================================================================
# SUMMARY
# ==========================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ ADVANCED ENCAPSULATION PATTERNS:

1. DATACLASSES WITH VALIDATION:
   - Use __post_init__ for complex validation
   - Computed properties with @property
   - Type safety with annotations
   - Factory methods for common configs

2. PYDANTIC FOR PRODUCTION:
   - Runtime validation of external data
   - Automatic JSON serialization
   - Field constraints (min, max, pattern)
   - Custom validators
   - Configuration validation for APIs

3. DESCRIPTORS:
   - Control attribute access
   - Complex property behavior
   - Type checking and validation
   - Better than just @property for advanced cases

4. MEMORY OPTIMIZATION:
   - __slots__ reduces memory by ~40%
   - Important for data-heavy applications
   - Prevents arbitrary attribute assignment

5. ABSTRACT BASE CLASSES:
   - Define interfaces
   - Ensure implementations
   - Document contracts
   - Polymorphic behavior

6. FACTORY METHODS:
   - Encapsulate object creation
   - Common configurations (dev, prod)
   - Deserialization from dictionaries

💡 PRODUCTION PATTERNS:
   ✓ Use Pydantic for API validation
   ✓ Use dataclasses for internal data
   ✓ Use __slots__ for memory-heavy objects
   ✓ Use ABCs for plugin systems
   ✓ Use factories for configuration

🏗️ ARCHITECTURE BENEFITS:
   - Type safety across the system
   - Clear API contracts
   - Memory efficient
   - Testable and modular
   - Production-ready validation
"""

print(summary)
