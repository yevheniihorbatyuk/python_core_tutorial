"""
Module 8.3 (Advanced): Modern Serialization Formats
====================================================

Learning Goals:
- Compare serialization formats (JSON, MessagePack, Protobuf, Parquet)
- Understand trade-offs: speed, size, safety, compatibility
- Implement format-agnostic serialization interface
- Benchmark different formats
- Real-world use cases for each format

⚡ Real-World Applications:
- MessagePack: Microservices, distributed caching
- Protocol Buffers: gRPC services, schema versioning
- Parquet: Data warehouses, analytical storage
- JSON: REST APIs, configuration files
- YAML: DevOps configuration

🏗️ Production Patterns:
- Format selection based on use case
- Cross-language serialization
- Schema evolution
- Performance optimization
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Protocol
from abc import ABC, abstractmethod


# ========================================================================
# SECTION 1: SERIALIZATION INTERFACE (FORMAT-AGNOSTIC)
# ========================================================================

print("=" * 80)
print("SECTION 1: FORMAT-AGNOSTIC SERIALIZATION INTERFACE")
print("=" * 80)


class Serializer(ABC):
    """Abstract base for all serializers."""

    @abstractmethod
    def serialize(self, obj: Any) -> bytes:
        """Convert object to bytes."""
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Convert bytes back to object."""
        pass

    @abstractmethod
    def format_name(self) -> str:
        """Format name for reporting."""
        pass


class JSONSerializer(Serializer):
    """Standard JSON serializer."""

    def serialize(self, obj: Any) -> bytes:
        """Serialize to JSON bytes."""
        json_str = json.dumps(obj, default=str)
        return json_str.encode("utf-8")

    def deserialize(self, data: bytes) -> Any:
        """Deserialize from JSON bytes."""
        json_str = data.decode("utf-8")
        return json.loads(json_str)

    def format_name(self) -> str:
        return "JSON"


# Try to import MessagePack if available
try:
    import msgpack

    class MessagePackSerializer(Serializer):
        """Binary MessagePack serializer (smaller than JSON)."""

        def serialize(self, obj: Any) -> bytes:
            """Serialize to MessagePack bytes."""
            return msgpack.packb(obj, use_bin_type=True)

        def deserialize(self, data: bytes) -> Any:
            """Deserialize from MessagePack bytes."""
            return msgpack.unpackb(data, raw=False)

        def format_name(self) -> str:
            return "MessagePack"

    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False
    print("⚠️  msgpack not installed. Install with: pip install msgpack")


# ========================================================================
# SECTION 2: COMPARISON TABLE
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 2: SERIALIZATION FORMAT COMPARISON")
print("=" * 80)

print("""
FORMAT COMPARISON:

┌─────────────┬──────────────┬──────────┬─────────────┬────────────────┐
│ Format      │ Use Case     │ Speed    │ Size        │ Cross-Language │
├─────────────┼──────────────┼──────────┼─────────────┼────────────────┤
│ JSON        │ APIs, config │ Slow     │ Large (100%)│ ✅ Yes         │
│ MessagePack │ Microservices│ Fast     │ Small (60%) │ ✅ Yes         │
│ Pickle      │ Py cache     │ Very Fast│ Medium (70%)│ ❌ No          │
│ Protobuf    │ gRPC, schema │ Fast     │ Small (40%) │ ✅ Yes         │
│ Parquet     │ Analytics    │ Medium   │ Small (30%) │ ✅ Yes         │
│ YAML        │ Config       │ Slow     │ Large (110%)│ ✅ Yes         │
└─────────────┴──────────────┴──────────┴─────────────┴────────────────┘

DETAILED COMPARISON:

┌──────────────┬────────────────────────────────────────────────────────┐
│ Format       │ Advantages                                             │
├──────────────┼────────────────────────────────────────────────────────┤
│ JSON         │ • Human-readable                                       │
│              │ • Universal support                                    │
│              │ • Web standard                                         │
│              │ • Safe (no code execution)                             │
├──────────────┼────────────────────────────────────────────────────────┤
│ MessagePack  │ • Binary JSON alternative                              │
│              │ • 40-60% smaller than JSON                             │
│              │ • Faster than JSON                                     │
│              │ • Cross-language support                               │
├──────────────┼────────────────────────────────────────────────────────┤
│ Pickle       │ • Python-native                                        │
│              │ • Supports complex objects                             │
│              │ • Very fast                                            │
│              │ • ⚠️ Security risk (code execution)                    │
├──────────────┼────────────────────────────────────────────────────────┤
│ Protobuf     │ • Schema-based (versioning support)                    │
│              │ • Compact binary format                                │
│              │ • Language-agnostic                                    │
│              │ • Requires schema definition                           │
├──────────────┼────────────────────────────────────────────────────────┤
│ Parquet      │ • Columnar (great for analytics)                       │
│              │ • Compression built-in                                 │
│              │ • Efficient for large datasets                         │
│              │ • Standard in data warehouses                          │
├──────────────┼────────────────────────────────────────────────────────┤
│ YAML         │ • Human-friendly syntax                                │
│              │ • Good for configuration                               │
│              │ • Hierarchical support                                 │
│              │ • Complex parsing logic                                │
└──────────────┴────────────────────────────────────────────────────────┘
""")


# ========================================================================
# SECTION 3: BENCHMARKING SERIALIZATION FORMATS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 3: PERFORMANCE BENCHMARKING")
print("=" * 80)


@dataclass
class Person:
    """Sample data structure for benchmarking."""
    name: str
    age: int
    email: str
    phone: str
    address: str


def benchmark_serializer(serializer: Serializer, data: dict, iterations: int = 1000) -> dict:
    """Benchmark a serializer."""
    # Single serialization for size
    serialized = serializer.serialize(data)
    size = len(serialized)

    # Time multiple serializations
    start = time.time()
    for _ in range(iterations):
        serializer.serialize(data)
    serialize_time = time.time() - start

    # Time multiple deserializations
    start = time.time()
    for _ in range(iterations):
        serializer.deserialize(serialized)
    deserialize_time = time.time() - start

    return {
        "format": serializer.format_name(),
        "size": size,
        "serialize_time": serialize_time,
        "deserialize_time": deserialize_time,
        "total_time": serialize_time + deserialize_time,
    }


# Create test data: 1000 person objects
test_data = {
    "people": [
        {
            "name": f"Person{i}",
            "age": 20 + (i % 60),
            "email": f"person{i}@example.com",
            "phone": f"+1-555-{i:04d}",
            "address": f"{i} Main St, City, Country"
        }
        for i in range(1000)
    ]
}

print(f"\nBenchmarking with 1000 person records:\n")

serializers = [JSONSerializer()]
if HAS_MSGPACK:
    serializers.append(MessagePackSerializer())

results = []
for serializer in serializers:
    result = benchmark_serializer(serializer, test_data)
    results.append(result)

# Display results
print(f"{'Format':<15} {'Size':<10} {'Serialize':<12} {'Deserialize':<12} {'Speedup':<10}")
print("-" * 60)

json_size = results[0]["size"]
for result in results:
    size = result["size"]
    speedup = json_size / size
    print(
        f"{result['format']:<15} "
        f"{size:<10} "
        f"{result['serialize_time']:<12.4f}s "
        f"{result['deserialize_time']:<12.4f}s "
        f"{speedup:<10.1f}x"
    )

print("\n💡 Observations:")
if HAS_MSGPACK:
    print(f"  • MessagePack is {results[0]['size']/results[1]['size']:.1f}x smaller than JSON")
    print(f"  • MessagePack is {results[0]['total_time']/results[1]['total_time']:.1f}x faster than JSON")
print("  • Use MessagePack for bandwidth/speed optimization")
print("  • Use JSON for readability and debugging")


# ========================================================================
# SECTION 4: PROTOCOL BUFFERS OVERVIEW
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 4: PROTOCOL BUFFERS (SCHEMA-BASED)")
print("=" * 80)

print("""
PROTOCOL BUFFERS (.proto):

Protobuf uses schema definition files (.proto) that look like this:

    syntax = "proto3";

    message Person {
      int32 user_id = 1;
      string name = 2;
      string email = 3;
      repeated string addresses = 4;
    }

KEY ADVANTAGES:
✓ Schema versioning (forward/backward compatible)
✓ Compact binary format
✓ Code generation for multiple languages
✓ Strongly typed
✓ Perfect for gRPC microservices
✓ Efficient large-scale systems

EXAMPLE USE CASE:
    Microservices communicate using Protobuf:
    • Service A sends gRPC request (Protobuf)
    • Service B receives, processes, responds (Protobuf)
    • Different languages can communicate (Java, Python, Go, etc.)

COMPARISON TO JSON:
    JSON: {"person": {"id": 1, "name": "Alice", "email": "alice@ex.com"}}
    Size: ~70 bytes (human-readable)

    Protobuf: [binary] (optimized, ~35 bytes)
    Size: ~35 bytes (compact, but needs schema to decode)

Note: Protobuf requires code generation. For this educational module,
we show the concept but don't implement full .proto compilation.
""")


# ========================================================================
# SECTION 5: PARQUET FOR ANALYTICS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 5: PARQUET (ANALYTICS FORMAT)")
print("=" * 80)

print("""
PARQUET FORMAT:

Parquet is a columnar storage format optimized for analytics.

KEY CHARACTERISTICS:
✓ Columnar storage (analyze single column efficiently)
✓ Compression built-in (Snappy, GZIP, etc.)
✓ Schema versioning
✓ Splittable (parallel processing)
✓ Standard in big data (Spark, Hadoop, etc.)

WHY COLUMNAR IS BETTER FOR ANALYTICS:

Traditional row storage (CSV):
    [id1, name1, age1, city1]
    [id2, name2, age2, city2]
    [id3, name3, age3, city3]

    Query: "Average age of all users"
    → Must read ALL columns, ALL rows
    → Slow for large datasets

Columnar storage (Parquet):
    [id1, id2, id3, ...]         # ID column
    [name1, name2, name3, ...]   # Name column
    [age1, age2, age3, ...]      # Age column
    [city1, city2, city3, ...]   # City column

    Query: "Average age of all users"
    → Read ONLY age column
    → Much faster!

PYTHON EXAMPLE (with pandas):
    import pandas as pd

    # Write
    df.to_parquet('data.parquet')

    # Read
    df = pd.read_parquet('data.parquet')

    # Efficient column-specific read
    df = pd.read_parquet('data.parquet', columns=['age'])

USE CASES:
• Data warehouse storage (Snowflake, BigQuery)
• Apache Spark processing
• Data lake storage (S3, GCS)
• Large analytical queries
""")


# ========================================================================
# SECTION 6: YAML FOR CONFIGURATION
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 6: YAML FOR CONFIGURATION")
print("=" * 80)

print("""
YAML: Human-Friendly Configuration Format

EXAMPLE YAML FILE (app-config.yaml):

    app:
      name: MyApp
      version: 1.0.0
      debug: false

    database:
      host: localhost
      port: 5432
      credentials:
        username: admin
        password: secret  # ⚠️ Should use secrets manager!

    features:
      enable_cache: true
      enable_logging: true
      log_level: INFO

KEY ADVANTAGES:
✓ Human-readable (indentation-based)
✓ Supports hierarchical data
✓ Comments support
✓ Lists and dictionaries
✓ Common in Kubernetes, Docker Compose

PYTHON EXAMPLE:
    import yaml

    # Load YAML
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    # Access nested values
    db_host = config['database']['host']

COMPARISON:
    YAML (readable):
        server:
          host: localhost
          port: 8000

    JSON (strict):
        {"server": {"host": "localhost", "port": 8000}}

    YAML allows comments and is more flexible
""")


# ========================================================================
# SECTION 7: SELECTING THE RIGHT FORMAT
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 7: DECISION GUIDE - WHICH FORMAT TO USE")
print("=" * 80)

decision_guide = """
DECISION FLOWCHART:

Q1: Is it cross-language communication?
    ├─ YES → Go to Q2
    └─ NO  → Consider Pickle (Python-only)

Q2: Do you need schema versioning?
    ├─ YES → Protocol Buffers or Parquet
    └─ NO  → Go to Q3

Q3: Is human readability important?
    ├─ YES → JSON or YAML
    └─ NO  → Go to Q4

Q4: Is size/speed critical?
    ├─ YES → MessagePack or Protobuf
    └─ NO  → JSON (universal standard)

Q5: Is it analytical data (millions of rows)?
    ├─ YES → Parquet
    └─ NO  → Use result from above

PRACTICAL RECOMMENDATIONS:

┌──────────────────┬───────────────────────────┬──────────────┐
│ Use Case         │ Recommended Format        │ Reason       │
├──────────────────┼───────────────────────────┼──────────────┤
│ REST API         │ JSON                      │ Web standard │
│ Microservices    │ Protobuf (gRPC)           │ Schema+speed │
│ Configuration    │ YAML or JSON              │ Readability  │
│ Caching          │ Pickle or MessagePack     │ Speed        │
│ Internal Python  │ Pickle                    │ Simplicity   │
│ Data warehouse   │ Parquet                   │ Efficiency   │
│ Cross-language   │ JSON or MessagePack       │ Compatibility│
│ Mobile app data  │ MessagePack or Protobuf   │ Size/speed   │
│ ML model output  │ JSON or pickle            │ Integration  │
└──────────────────┴───────────────────────────┴──────────────┘

PRODUCTION PATTERNS:

1. API LAYER:          JSON (always)
2. INTERNAL COMMS:     MessagePack (speed) or JSON (compatibility)
3. PERSISTENT STORE:   Parquet (analytics) or JSON (simplicity)
4. CONFIGURATION:      YAML or JSON (human-readable)
5. ML MODELS:          Pickle (scikit-learn) or joblib
6. MICROSERVICES:      Protobuf/gRPC (typed) or JSON (simple)
"""

print(decision_guide)


# ========================================================================
# SECTION 8: REAL-WORLD EXAMPLE - MULTI-FORMAT STORAGE
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 8: REAL-WORLD EXAMPLE - MULTI-FORMAT APPROACH")
print("=" * 80)

print("""
PRODUCTION ARCHITECTURE:

A data pipeline might use multiple formats:

    User Input (JSON API)
           ↓
    ┌──────────────────┐
    │ Web Service      │ ← JSON (HTTP)
    └──────────────────┘
           ↓
    ┌──────────────────┐
    │ Internal RPC     │ ← MessagePack/Protobuf (speed)
    └──────────────────┘
           ↓
    ┌──────────────────┐
    │ Data Pipeline    │ ← Parquet (storage)
    └──────────────────┘
           ↓
    ┌──────────────────┐
    │ Analytics DB     │ ← Parquet (columnar)
    └──────────────────┘
           ↓
    Dashboard (JSON API)

EXAMPLE WORKFLOW:
1. User submits form → JSON
2. Backend receives → deserialize JSON to Python object
3. Passes to data service → serialize to MessagePack (fast)
4. Data service stores → writes to Parquet (compressed)
5. Analytics reads → reads Parquet (efficient columns)
6. Dashboard requests → returns JSON (human-readable)

BENEFITS:
✓ Each layer optimized for its constraints
✓ JSON ensures external compatibility
✓ Parquet provides storage efficiency
✓ MessagePack speeds internal communication
✓ Standard patterns across industry
""")


# ========================================================================
# SUMMARY
# ========================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ MODERN SERIALIZATION FORMATS:

1. JSON:
   ✓ Universal standard for APIs
   ✓ Human-readable debugging
   ✓ Built-in Python support
   ✗ Larger file size
   ✗ Slower than binary formats

2. MessagePack:
   ✓ 40-60% smaller than JSON
   ✓ 2-3x faster than JSON
   ✓ Cross-language support
   ✓ Good for microservices
   ✗ Binary (harder to debug)
   ✗ Requires extra library

3. Protocol Buffers:
   ✓ Schema versioning (evolved safely)
   ✓ Very compact (30-40% of JSON)
   ✓ Multiple language support
   ✓ Perfect for gRPC
   ✗ Requires code generation
   ✗ Steeper learning curve

4. Parquet:
   ✓ Columnar (efficient analytics)
   ✓ Compression built-in
   ✓ Standard in data warehouses
   ✓ Splittable (parallel processing)
   ✗ Complex format
   ✗ Not suitable for small objects

5. YAML:
   ✓ Very human-readable
   ✓ Good for configuration
   ✓ Supports hierarchies
   ✗ Larger files than JSON
   ✗ Complex parsing

🏗️ ARCHITECTURE PRINCIPLES:
   1. Use JSON for external APIs (universal standard)
   2. Use MessagePack/Protobuf for internal communication
   3. Use Parquet for analytical data storage
   4. Use YAML for configuration files
   5. Use Pickle only for Python-only internal caching

💡 PERFORMANCE TRADE-OFFS:
   Speed:        Pickle > MessagePack > Protobuf > JSON > YAML
   Size:         Parquet < Protobuf < MessagePack < JSON < YAML
   Readability:  YAML > JSON > Pickle > Protobuf > Parquet
   Safety:       JSON = YAML > Protobuf > MessagePack > Pickle
   Compatibility: JSON = YAML = Protobuf > MessagePack > Pickle

🔒 SECURITY CONSIDERATIONS:
   ✓ JSON: Safe (no code execution)
   ✓ Protobuf: Safe (schema-based)
   ✓ MessagePack: Safe (binary data only)
   ⚠️ Pickle: DANGEROUS (can execute code)
   ✓ Parquet: Safe (columnar data only)

🚀 WHEN TO OPTIMIZE:
   → Start with JSON (simplicity)
   → Profile actual performance
   → Switch to MessagePack if bandwidth is bottleneck
   → Use Parquet for large analytical datasets
   → Use Protobuf for complex microservice schemas
"""

print(summary)
