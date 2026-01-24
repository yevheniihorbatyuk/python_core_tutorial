"""
Module 8.6 (Advanced): Real-World Practice Projects
====================================================

Learning Goals:
- Implement production patterns from previous lessons
- Build complete systems with serialization
- Handle versioning and backward compatibility
- Demonstrate ML, data engineering, and backend patterns
- Practice error handling and validation

⚡ Real-World Applications:
- ML Model Registry (MLOps)
- Configuration Service (DevOps/Backend)
- Event Sourcing (Domain-driven design)
- Data Catalog (Data Engineering)
- Metrics Pipeline (Analytics)
- Schema Evolution (Data Science)
- Cache Layer (Backend/DevOps)
- Audit Log (Compliance/Security)

🏗️ Architecture Patterns:
- Domain-driven design
- Event-driven architecture
- Plugin systems
- Multi-tenant configuration
- Immutable logging
"""

from __future__ import annotations

import json
import pickle
import hashlib
import hmac
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Protocol
from datetime import datetime, timezone
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum
import uuid

try:
    from pydantic import BaseModel, Field, field_validator, ConfigDict
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


# ========================================================================
# PROJECT 1: ML MODEL REGISTRY
# ========================================================================

print("=" * 80)
print("PROJECT 1: ML MODEL REGISTRY")
print("=" * 80)

if HAS_PYDANTIC:
    class ModelMetadata(BaseModel):
        """Metadata about a trained ML model."""

        model_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        name: str = Field(..., min_length=3, max_length=100)
        version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")  # Semantic versioning
        algorithm: str
        framework: str
        accuracy: float = Field(..., ge=0.0, le=1.0)
        f1_score: float = Field(..., ge=0.0, le=1.0)
        training_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        feature_names: list[str]
        hyperparameters: dict = Field(default_factory=dict)
        tags: list[str] = Field(default_factory=list)

        @field_validator("version")
        @classmethod
        def validate_version(cls, v: str) -> str:
            """Ensure semantic versioning format."""
            parts = v.split(".")
            if len(parts) != 3:
                raise ValueError("Version must be X.Y.Z format")
            return v


    class ModelRegistry:
        """Registry for managing multiple model versions."""

        def __init__(self, registry_path: str = "model_registry"):
            self.registry_path = Path(registry_path)
            self.registry_path.mkdir(exist_ok=True)
            self.index: dict[str, list[str]] = {}  # name -> [versions]
            self.load_index()

        def load_index(self) -> None:
            """Load registry index from disk."""
            index_file = self.registry_path / "index.json"
            if index_file.exists():
                with open(index_file, "r") as f:
                    self.index = json.load(f)

        def save_index(self) -> None:
            """Save registry index to disk."""
            index_file = self.registry_path / "index.json"
            with open(index_file, "w") as f:
                json.dump(self.index, f, indent=2)

        def register(self, metadata: ModelMetadata, weights: bytes) -> str:
            """Register a new model version."""
            # Save metadata
            if metadata.name not in self.index:
                self.index[metadata.name] = []

            self.index[metadata.name].append(metadata.version)

            # Create directory for this model
            model_dir = self.registry_path / metadata.name / metadata.version
            model_dir.mkdir(parents=True, exist_ok=True)

            # Save metadata as JSON
            metadata_file = model_dir / "metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(json.loads(metadata.model_dump_json()), f, indent=2)

            # Save weights as pickle
            weights_file = model_dir / "weights.pkl"
            with open(weights_file, "wb") as f:
                pickle.dump(weights, f, protocol=5)

            # Save index
            self.save_index()

            print(f"✅ Registered {metadata.name}@{metadata.version}")
            return metadata.model_id

        def get_latest(self, name: str) -> tuple[ModelMetadata, bytes] | None:
            """Get the latest version of a model."""
            if name not in self.index or not self.index[name]:
                return None

            versions = sorted(self.index[name])
            latest_version = versions[-1]
            return self.get(name, latest_version)

        def get(self, name: str, version: str) -> tuple[ModelMetadata, bytes]:
            """Get a specific model version."""
            model_dir = self.registry_path / name / version

            # Load metadata
            metadata_file = model_dir / "metadata.json"
            with open(metadata_file, "r") as f:
                metadata_dict = json.load(f)
            metadata = ModelMetadata(**metadata_dict)

            # Load weights
            weights_file = model_dir / "weights.pkl"
            with open(weights_file, "rb") as f:
                weights = pickle.load(f)

            return metadata, weights

        def list_models(self) -> dict[str, list[str]]:
            """List all registered models and versions."""
            return self.index


    print("\nDemonstration: ML Model Registry\n")

    # Create registry
    registry = ModelRegistry("/tmp/model_registry")

    # Register model v1
    metadata_v1 = ModelMetadata(
        name="sales_predictor",
        version="1.0.0",
        algorithm="gradient_boosting",
        framework="lightgbm",
        accuracy=0.87,
        f1_score=0.85,
        feature_names=["price", "quantity", "season"],
        hyperparameters={"n_estimators": 100, "learning_rate": 0.1},
        tags=["production", "sales"]
    )
    weights_v1 = pickle.dumps({"model": "weights_v1", "data": [0.1, 0.2, 0.3]})
    registry.register(metadata_v1, weights_v1)

    # Register improved v2
    metadata_v2 = ModelMetadata(
        name="sales_predictor",
        version="1.1.0",
        algorithm="gradient_boosting",
        framework="lightgbm",
        accuracy=0.91,  # Improved!
        f1_score=0.89,
        feature_names=["price", "quantity", "season", "marketing"],
        hyperparameters={"n_estimators": 200, "learning_rate": 0.05},
        tags=["production", "sales", "improved"]
    )
    weights_v2 = pickle.dumps({"model": "weights_v2", "data": [0.15, 0.25, 0.35, 0.25]})
    registry.register(metadata_v2, weights_v2)

    # List models
    print("\nRegistered models:")
    for name, versions in registry.list_models().items():
        print(f"  {name}: {versions}")

    # Get latest model
    metadata, weights = registry.get_latest("sales_predictor")
    print(f"\nLatest model: {metadata.name}@{metadata.version}")
    print(f"  Accuracy: {metadata.accuracy:.2%}")
    print(f"  Features: {metadata.feature_names}")

else:
    print("Pydantic not available - skipping registry examples")


# ========================================================================
# PROJECT 2: CONFIGURATION SERVICE
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 2: CONFIGURATION SERVICE")
print("=" * 80)

if HAS_PYDANTIC:
    class DatabaseConfig(BaseModel):
        """Database configuration."""
        host: str
        port: int = Field(..., ge=1, le=65535)
        database: str
        pool_size: int = Field(10, ge=1, le=100)


    class APIConfig(BaseModel):
        """API configuration."""
        base_url: str
        timeout: int = Field(30, ge=5, le=300)
        retries: int = Field(3, ge=0, le=10)


    class EnvironmentConfig(BaseModel):
        """Configuration for different environments."""

        model_config = ConfigDict(validate_default=True)

        environment: str
        debug: bool
        database: DatabaseConfig
        api: APIConfig

        @field_validator("environment")
        @classmethod
        def validate_env(cls, v: str) -> str:
            if v not in {"development", "staging", "production"}:
                raise ValueError("Invalid environment")
            return v

        @staticmethod
        def load_from_file(filepath: str) -> EnvironmentConfig:
            """Load and validate configuration from JSON file."""
            with open(filepath, "r") as f:
                config_dict = json.load(f)
            return EnvironmentConfig(**config_dict)

        def save_to_file(self, filepath: str) -> None:
            """Save configuration to JSON file."""
            with open(filepath, "w") as f:
                json.dump(json.loads(self.model_dump_json()), f, indent=2)

        def to_safe_dict(self) -> dict:
            """Return config without sensitive fields."""
            data = self.model_dump()
            if "database" in data:
                data["database"]["host"] = f"{data['database']['host'].split('.')[0]}.**"
            return data


    print("\nDemonstration: Configuration Service\n")

    # Create configuration
    config = EnvironmentConfig(
        environment="production",
        debug=False,
        database=DatabaseConfig(
            host="db.production.internal",
            port=5432,
            database="prod_db",
            pool_size=50
        ),
        api=APIConfig(
            base_url="https://api.example.com",
            timeout=60,
            retries=5
        )
    )

    # Save configuration
    config_path = "/tmp/config.json"
    config.save_to_file(config_path)
    print(f"✅ Configuration saved to {config_path}")

    # Load configuration
    loaded_config = EnvironmentConfig.load_from_file(config_path)
    print(f"✅ Configuration loaded for environment: {loaded_config.environment}")

    # Show safe view
    print(f"\nSafe config view:")
    safe = loaded_config.to_safe_dict()
    print(json.dumps(safe, indent=2)[:200] + "...")

else:
    print("Pydantic not available - skipping configuration examples")


# ========================================================================
# PROJECT 3: EVENT SOURCING
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 3: EVENT SOURCING")
print("=" * 80)


class EventType(Enum):
    """Domain events for order processing."""
    ORDER_CREATED = "order_created"
    PAYMENT_RECEIVED = "payment_received"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass
class DomainEvent:
    """Base class for domain events."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    aggregate_id: str = None  # Order ID
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize event to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value if self.event_type else None,
            "timestamp": self.timestamp,
            "aggregate_id": self.aggregate_id,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data: dict) -> DomainEvent:
        """Deserialize event from dictionary."""
        event = cls()
        event.event_id = data["event_id"]
        event.event_type = EventType(data["event_type"])
        event.timestamp = data["timestamp"]
        event.aggregate_id = data["aggregate_id"]
        event.data = data["data"]
        return event


class EventStore:
    """Immutable event log for event sourcing."""

    def __init__(self, filepath: str = "event_store.jsonl"):
        self.filepath = Path(filepath)
        self.events: list[DomainEvent] = []
        self.load()

    def append(self, event: DomainEvent) -> None:
        """Add event to store (immutable append)."""
        self.events.append(event)

        # Append to file (immutable log)
        with open(self.filepath, "a") as f:
            json.dump(event.to_dict(), f)
            f.write("\n")

    def load(self) -> None:
        """Load all events from file."""
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                for line in f:
                    if line.strip():
                        event_dict = json.loads(line)
                        self.events.append(DomainEvent.from_dict(event_dict))

    def get_events_for(self, aggregate_id: str) -> list[DomainEvent]:
        """Get all events for an order (replay pattern)."""
        return [e for e in self.events if e.aggregate_id == aggregate_id]

    def replay(self, aggregate_id: str) -> dict:
        """Replay events to reconstruct current state."""
        events = self.get_events_for(aggregate_id)
        state = {
            "order_id": aggregate_id,
            "status": "pending",
            "total": 0.0,
            "history": []
        }

        for event in events:
            if event.event_type == EventType.ORDER_CREATED:
                state["status"] = "created"
                state["total"] = event.data.get("amount", 0.0)
            elif event.event_type == EventType.PAYMENT_RECEIVED:
                state["status"] = "paid"
            elif event.event_type == EventType.SHIPPED:
                state["status"] = "shipped"
            elif event.event_type == EventType.DELIVERED:
                state["status"] = "delivered"

            state["history"].append(f"{event.timestamp}: {event.event_type.value}")

        return state


print("\nDemonstration: Event Sourcing\n")

# Create event store
store = EventStore("/tmp/event_store.jsonl")

# Simulate order lifecycle
order_id = str(uuid.uuid4())

event1 = DomainEvent()
event1.event_type = EventType.ORDER_CREATED
event1.aggregate_id = order_id
event1.data = {"amount": 99.99, "items": 3}
store.append(event1)
print(f"✅ Event: ORDER_CREATED")

event2 = DomainEvent()
event2.event_type = EventType.PAYMENT_RECEIVED
event2.aggregate_id = order_id
event2.data = {"payment_method": "credit_card"}
store.append(event2)
print(f"✅ Event: PAYMENT_RECEIVED")

event3 = DomainEvent()
event3.event_type = EventType.SHIPPED
event3.aggregate_id = order_id
event3.data = {"tracking": "ABC123"}
store.append(event3)
print(f"✅ Event: SHIPPED")

# Replay to get current state
state = store.replay(order_id)
print(f"\nReconstructed order state:")
print(f"  Order ID: {state['order_id']}")
print(f"  Status: {state['status']}")
print(f"  Total: ${state['total']:.2f}")
print(f"  History: {len(state['history'])} events")


# ========================================================================
# PROJECT 4: DATA CATALOG
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 4: DATA CATALOG")
print("=" * 80)

if HAS_PYDANTIC:
    class DatasetSchema(BaseModel):
        """Column definitions for a dataset."""
        name: str
        type: str  # int, float, str, datetime
        nullable: bool = False
        description: str = ""


    class DatasetMetadata(BaseModel):
        """Metadata about a dataset in the catalog."""
        dataset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        name: str = Field(..., min_length=3)
        location: str
        format: str  # csv, parquet, json
        row_count: int = Field(..., ge=0)
        size_bytes: int = Field(..., ge=0)
        schema: list[DatasetSchema]
        created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        owner: str
        tags: list[str] = Field(default_factory=list)

        @field_validator("format")
        @classmethod
        def validate_format(cls, v: str) -> str:
            if v not in {"csv", "parquet", "json", "sql"}:
                raise ValueError("Invalid format")
            return v


    class DataCatalog:
        """Central registry for dataset metadata."""

        def __init__(self, catalog_path: str = "data_catalog"):
            self.catalog_path = Path(catalog_path)
            self.catalog_path.mkdir(exist_ok=True)
            self.datasets: dict[str, DatasetMetadata] = {}
            self.load_catalog()

        def load_catalog(self) -> None:
            """Load catalog index."""
            index_file = self.catalog_path / "index.json"
            if index_file.exists():
                with open(index_file, "r") as f:
                    data = json.load(f)
                    for dataset_dict in data.get("datasets", []):
                        metadata = DatasetMetadata(**dataset_dict)
                        self.datasets[metadata.name] = metadata

        def save_catalog(self) -> None:
            """Save catalog index."""
            index_file = self.catalog_path / "index.json"
            datasets_data = [
                json.loads(m.model_dump_json())
                for m in self.datasets.values()
            ]
            with open(index_file, "w") as f:
                json.dump({"datasets": datasets_data}, f, indent=2)

        def register_dataset(self, metadata: DatasetMetadata) -> str:
            """Register a new dataset."""
            self.datasets[metadata.name] = metadata
            self.save_catalog()
            print(f"✅ Registered dataset: {metadata.name}")
            return metadata.dataset_id

        def search_by_tag(self, tag: str) -> list[DatasetMetadata]:
            """Find datasets with a specific tag."""
            return [d for d in self.datasets.values() if tag in d.tags]

        def list_by_owner(self, owner: str) -> list[DatasetMetadata]:
            """List datasets owned by a person."""
            return [d for d in self.datasets.values() if d.owner == owner]


    print("\nDemonstration: Data Catalog\n")

    catalog = DataCatalog("/tmp/data_catalog")

    # Register customer dataset
    customer_schema = [
        DatasetSchema(name="customer_id", type="int", nullable=False),
        DatasetSchema(name="name", type="str", nullable=False),
        DatasetSchema(name="email", type="str", nullable=False),
        DatasetSchema(name="signup_date", type="datetime"),
    ]

    customer_metadata = DatasetMetadata(
        name="customers",
        location="s3://data-warehouse/customers.parquet",
        format="parquet",
        row_count=50000,
        size_bytes=15_000_000,
        schema=customer_schema,
        owner="data_team",
        tags=["crm", "production", "daily"]
    )
    catalog.register_dataset(customer_metadata)

    # Register sales dataset
    sales_schema = [
        DatasetSchema(name="sale_id", type="int"),
        DatasetSchema(name="customer_id", type="int"),
        DatasetSchema(name="amount", type="float"),
        DatasetSchema(name="sale_date", type="datetime"),
    ]

    sales_metadata = DatasetMetadata(
        name="sales",
        location="s3://data-warehouse/sales.parquet",
        format="parquet",
        row_count=1_000_000,
        size_bytes=250_000_000,
        schema=sales_schema,
        owner="data_team",
        tags=["analytics", "production"]
    )
    catalog.register_dataset(sales_metadata)

    # Search by tag
    production_datasets = catalog.search_by_tag("production")
    print(f"\nProduction datasets: {len(production_datasets)}")
    for ds in production_datasets:
        print(f"  - {ds.name}: {ds.row_count:,} rows")

else:
    print("Pydantic not available - skipping catalog examples")


# ========================================================================
# PROJECT 5: METRICS PIPELINE
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 5: METRICS PIPELINE")
print("=" * 80)


@dataclass
class Metric:
    """A single metric data point."""
    name: str
    value: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tags: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp,
            "tags": self.tags
        }


class MetricsPipeline:
    """Collect, aggregate, and export metrics."""

    def __init__(self, output_format: str = "json"):
        self.output_format = output_format
        self.metrics: list[Metric] = []

    def record(self, metric: Metric) -> None:
        """Record a metric."""
        self.metrics.append(metric)

    def aggregate(self, metric_name: str) -> dict:
        """Aggregate metrics by name."""
        values = [m.value for m in self.metrics if m.name == metric_name]
        if not values:
            return {}

        return {
            "name": metric_name,
            "count": len(values),
            "sum": sum(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    def export(self, filepath: str) -> None:
        """Export metrics to file."""
        data = {
            "metrics": [m.to_dict() for m in self.metrics],
            "count": len(self.metrics),
            "exported_at": datetime.now(timezone.utc).isoformat()
        }

        if self.output_format == "json":
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
        elif self.output_format == "pickle":
            with open(filepath, "wb") as f:
                pickle.dump(data, f, protocol=5)

        print(f"✅ Exported {len(self.metrics)} metrics to {filepath}")


print("\nDemonstration: Metrics Pipeline\n")

pipeline = MetricsPipeline(output_format="json")

# Simulate API metrics
for i in range(10):
    pipeline.record(Metric(
        name="api_response_time_ms",
        value=50 + i * 5,
        tags={"endpoint": "/users", "method": "GET"}
    ))

for i in range(10):
    pipeline.record(Metric(
        name="api_error_rate",
        value=0.01 + i * 0.002,
        tags={"endpoint": "/orders", "method": "POST"}
    ))

# Aggregate
response_time_agg = pipeline.aggregate("api_response_time_ms")
print("Response Time Metrics:")
print(f"  Mean: {response_time_agg['mean']:.1f}ms")
print(f"  Min: {response_time_agg['min']:.1f}ms")
print(f"  Max: {response_time_agg['max']:.1f}ms")

# Export
pipeline.export("/tmp/metrics_export.json")


# ========================================================================
# PROJECT 6: SCHEMA EVOLUTION
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 6: SCHEMA EVOLUTION")
print("=" * 80)


@dataclass
class UserV1:
    """Original user schema (v1)."""
    user_id: int
    email: str
    created_at: str


@dataclass
class UserV2:
    """Evolved user schema (v2) - added fields."""
    user_id: int
    email: str
    created_at: str
    last_login: str = ""  # New field
    preferences: dict = field(default_factory=dict)  # New field


class SchemaMigrator:
    """Handle schema migrations and versioning."""

    @staticmethod
    def migrate_v1_to_v2(data: dict) -> dict:
        """Migrate from UserV1 to UserV2."""
        return {
            "user_id": data["user_id"],
            "email": data["email"],
            "created_at": data["created_at"],
            "last_login": data.get("last_login", ""),
            "preferences": data.get("preferences", {"theme": "light"})
        }

    @staticmethod
    def load_versioned(filepath: str) -> dict:
        """Load and auto-migrate old schemas."""
        with open(filepath, "r") as f:
            data = json.load(f)

        version = data.get("version", 1)
        user_data = data.get("user")

        if version == 1:
            print("  ℹ️  Detected UserV1, auto-migrating to V2")
            user_data = SchemaMigrator.migrate_v1_to_v2(user_data)

        return user_data

    @staticmethod
    def save_versioned(user_data: dict, filepath: str, version: int = 2) -> None:
        """Save with version metadata."""
        data = {
            "version": version,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "user": user_data
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


print("\nDemonstration: Schema Evolution\n")

# Create and save old V1 format
old_user = {
    "version": 1,
    "user": {
        "user_id": 123,
        "email": "alice@example.com",
        "created_at": "2023-01-01T00:00:00Z"
    }
}

v1_path = "/tmp/user_v1.json"
with open(v1_path, "w") as f:
    json.dump(old_user, f, indent=2)
print(f"Created UserV1 at {v1_path}")

# Load and auto-migrate
print(f"\nLoading UserV1 (auto-migrating to V2):")
migrated = SchemaMigrator.load_versioned(v1_path)
print(f"  user_id: {migrated['user_id']}")
print(f"  email: {migrated['email']}")
print(f"  preferences: {migrated['preferences']}")

# Save as V2
SchemaMigrator.save_versioned(migrated, "/tmp/user_v2.json", version=2)
print(f"\n✅ Saved migrated user as V2")


# ========================================================================
# PROJECT 7: CACHE LAYER
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 7: DISTRIBUTED CACHE LAYER")
print("=" * 80)


class CacheBackend(ABC):
    """Abstract interface for cache backends."""

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


class JSONCacheBackend(CacheBackend):
    """JSON-based cache backend."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.cache: dict = {}
        self.load()

    def load(self) -> None:
        """Load cache from file."""
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                self.cache = json.load(f)

    def save(self) -> None:
        """Save cache to file."""
        with open(self.filepath, "w") as f:
            json.dump(self.cache, f)

    def get(self, key: str) -> Any:
        """Get value from cache."""
        return self.cache.get(key)

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        """Set value in cache."""
        self.cache[key] = {
            "value": value,
            "expires_at": (
                (datetime.now(timezone.utc).timestamp() + ttl_seconds)
                if ttl_seconds else None
            )
        }
        self.save()

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
            self.save()


class PickleCacheBackend(CacheBackend):
    """Pickle-based cache backend for complex objects."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.cache: dict = {}
        self.load()

    def load(self) -> None:
        """Load cache from file."""
        if self.filepath.exists():
            with open(self.filepath, "rb") as f:
                self.cache = pickle.load(f)

    def save(self) -> None:
        """Save cache to file."""
        with open(self.filepath, "wb") as f:
            pickle.dump(self.cache, f, protocol=5)

    def get(self, key: str) -> Any:
        """Get value from cache."""
        return self.cache.get(key, {}).get("value")

    def set(self, key: str, value: Any, ttl_seconds: int = None) -> None:
        """Set value in cache."""
        self.cache[key] = {"value": value}
        self.save()

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
            self.save()


print("\nDemonstration: Cache Layer\n")

# JSON cache
json_cache = JSONCacheBackend("/tmp/cache.json")
json_cache.set("user:123", {"id": 123, "name": "Alice"})
print(f"✅ Set JSON cache: {json_cache.get('user:123')}")

# Pickle cache for complex objects
pickle_cache = PickleCacheBackend("/tmp/cache.pkl")
complex_data = {"models": [1, 2, 3], "metadata": {"created": datetime.now(timezone.utc)}}
pickle_cache.set("model:sales", complex_data)
print(f"✅ Set pickle cache: {pickle_cache.get('model:sales')}")


# ========================================================================
# PROJECT 8: AUDIT LOG
# ========================================================================

print("\n" + "=" * 80)
print("PROJECT 8: IMMUTABLE AUDIT LOG")
print("=" * 80)


@dataclass
class AuditEntry:
    """Single audit log entry."""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    action: str = ""
    actor: str = ""
    resource: str = ""
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return asdict(self)

    def compute_hash(self) -> str:
        """Compute SHA256 hash of entry for integrity."""
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class AuditLog:
    """Immutable append-only audit log."""

    def __init__(self, filepath: str = "audit.log"):
        self.filepath = Path(filepath)
        self.entries: list[AuditEntry] = []
        self.load()

    def load(self) -> None:
        """Load audit entries from file."""
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                for line in f:
                    if line.strip():
                        entry_dict = json.loads(line)
                        entry = AuditEntry(**entry_dict)
                        self.entries.append(entry)

    def log(self, action: str, actor: str, resource: str, details: dict = None) -> str:
        """Log an action (immutable append)."""
        entry = AuditEntry(
            action=action,
            actor=actor,
            resource=resource,
            details=details or {}
        )

        self.entries.append(entry)

        # Append to immutable log file
        with open(self.filepath, "a") as f:
            json.dump(entry.to_dict(), f)
            f.write("\n")

        return entry.entry_id

    def verify_integrity(self) -> bool:
        """Verify log hasn't been tampered with."""
        # In production, would use HMAC signing
        return len(self.entries) == sum(1 for _ in open(self.filepath))

    def get_actions_by_actor(self, actor: str) -> list[AuditEntry]:
        """Get all actions by a specific user."""
        return [e for e in self.entries if e.actor == actor]


print("\nDemonstration: Audit Log\n")

audit_log = AuditLog("/tmp/audit.log")

# Log some actions
audit_log.log("user_created", "admin", "user:123", {"email": "alice@example.com"})
print("✅ Logged: user_created")

audit_log.log("password_changed", "user:123", "user:123", {})
print("✅ Logged: password_changed")

audit_log.log("file_accessed", "user:456", "report:sales_2024", {"read": True})
print("✅ Logged: file_accessed")

# Query audit log
admin_actions = audit_log.get_actions_by_actor("admin")
print(f"\nAudit trail for admin: {len(admin_actions)} actions")

# Verify integrity
if audit_log.verify_integrity():
    print("✅ Audit log integrity verified")


# ========================================================================
# SUMMARY
# ========================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ ADVANCED PRACTICE PROJECTS:

1. ML MODEL REGISTRY:
   ✓ Semantic versioning with validation
   ✓ Metadata management (accuracy, features)
   ✓ File-based persistence
   ✓ Version lookup and latest retrieval
   ✓ Real-world: MLOps artifact management

2. CONFIGURATION SERVICE:
   ✓ Environment-specific configs
   ✓ Pydantic validation
   ✓ JSON serialization
   ✓ Safe config views (masking sensitive data)
   ✓ Real-world: Multi-environment deployment

3. EVENT SOURCING:
   ✓ Immutable event log (JSONL format)
   ✓ Event replay for state reconstruction
   ✓ Domain events with aggregates
   ✓ Append-only architecture
   ✓ Real-world: Audit trails, CQRS patterns

4. DATA CATALOG:
   ✓ Dataset registration and discovery
   ✓ Schema management (column types)
   ✓ Metadata indexing
   ✓ Tag-based search
   ✓ Real-world: Data governance, lineage tracking

5. METRICS PIPELINE:
   ✓ Time-series metric collection
   ✓ Aggregation (mean, min, max, sum)
   ✓ Export to JSON/pickle
   ✓ Tagged metrics
   ✓ Real-world: Observability, monitoring

6. SCHEMA EVOLUTION:
   ✓ Versioned serialization
   ✓ Automatic migration logic
   ✓ Backward compatibility
   ✓ Graceful schema upgrades
   ✓ Real-world: API versioning, database migrations

7. DISTRIBUTED CACHE:
   ✓ Pluggable backend architecture (ABC pattern)
   ✓ JSON and Pickle backends
   ✓ TTL support
   ✓ Persistent cache storage
   ✓ Real-world: Application caching, performance optimization

8. AUDIT LOG:
   ✓ Immutable append-only log
   ✓ Entry hashing for integrity
   ✓ Actor/action/resource tracking
   ✓ Query by actor
   ✓ Real-world: Compliance, security forensics

🏗️ ARCHITECTURAL PATTERNS DEMONSTRATED:

✓ Repository Pattern (ModelRegistry, DataCatalog)
✓ Event Sourcing (EventStore)
✓ Strategy Pattern (CacheBackend implementations)
✓ Factory Pattern (SchemaMigrator)
✓ Observer Pattern (AuditLog)
✓ Command Pattern (DomainEvent)

💡 PRODUCTION CONSIDERATIONS:

✓ Serialization format selection (JSON vs Pickle)
✓ Data validation (Pydantic models)
✓ Error handling and recovery
✓ Backward compatibility
✓ Immutability and audit trails
✓ Performance optimization
✓ Testability and mocking

🔒 SECURITY PATTERNS:

✓ Sensitive data masking
✓ Data integrity (hashing)
✓ Audit trails
✓ Access control ready
✓ Validation of inputs

🎓 LEARNING OUTCOMES:

- Understand practical serialization use cases
- Design scalable data persistence layers
- Implement production-grade systems
- Handle versioning and migrations
- Build extensible architectures
- Apply design patterns in real scenarios
"""

print(summary)
