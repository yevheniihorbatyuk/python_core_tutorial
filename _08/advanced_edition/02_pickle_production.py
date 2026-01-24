"""
Module 8.2 (Advanced): Pickle in Production
============================================

Learning Goals:
- Understand pickle security risks and mitigations
- Implement restricted unpicklers for safety
- Optimize pickle performance (protocol, buffering)
- Handle versioning and backward compatibility
- Real-world ML model serialization patterns
- Distributed computing with pickle

🔒 SECURITY WARNING: Pickle can execute arbitrary code!
   Only unpickle data you created or trust completely.

⚡ Real-World Applications:
- scikit-learn model persistence (joblib wrapper)
- PyTorch state_dict saving
- TensorFlow checkpoint saving
- Ray distributed computing
- Dask task serialization
- Celery task pickling

🏗️ Production Patterns:
- Version management
- Backward compatibility
- Error handling
- Monitoring and metrics
"""

from __future__ import annotations

import pickle
import io
import sys
from dataclasses import dataclass
from typing import Any, Type

# ========================================================================
# SECTION 1: PICKLE SECURITY RISKS
# ========================================================================

print("=" * 80)
print("SECTION 1: PICKLE SECURITY RISKS")
print("=" * 80)

print("""
⚠️  CRITICAL SECURITY ISSUE:

Pickle can execute ARBITRARY PYTHON CODE during unpickling!

Why? pickle stores references to Python functions and classes.
When deserializing, it imports and calls them. An attacker can
exploit this to execute malicious code.

Example of what an attacker could do:
1. Create a pickle that imports os.system
2. Call os.system("rm -rf /")  <- DELETE ALL FILES!
3. Send you the pickle file
4. You run: pickle.loads(attacker_pickle)
5. Your computer is compromised!
""")

print("\nDemonstration of the risk:")
print("If we unpickled this malicious code, it could execute anything.")
print("⚠️  NEVER unpickle untrusted data!")


# ========================================================================
# SECTION 2: SAFE UNPICKLING WITH RESTRICTED IMPORTS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 2: SAFE UNPICKLING - RESTRICTED UNPICKLER")
print("=" * 80)


class RestrictedUnpickler(pickle.Unpickler):
    """
    Safer unpickler that restricts which classes can be imported.

    Only allows specific safe classes.
    """

    # Whitelist of safe classes
    SAFE_MODULES = {
        ("__main__", "User"),
        ("__main__", "Address"),
        ("__main__", "Config"),
        ("builtins", "dict"),
        ("builtins", "list"),
        ("builtins", "tuple"),
        ("builtins", "set"),
        ("datetime", "datetime"),
    }

    def find_class(self, module: str, name: str):
        """Override to restrict which classes can be unpickled."""
        if (module, name) not in self.SAFE_MODULES:
            raise pickle.UnpicklingError(
                f"Unpickling of {module}.{name} is not allowed! "
                f"Only these classes are safe: {self.SAFE_MODULES}"
            )
        return super().find_class(module, name)


@dataclass
class User:
    """Safe class for demonstration."""
    user_id: int
    email: str


@dataclass
class Address:
    """Safe class for demonstration."""
    city: str
    country: str


print("\nUsing RestrictedUnpickler:")

# Create safe data
user = User(user_id=1, email="alice@example.com")
safe_pickle = pickle.dumps(user)

print("Unpickling safe data:")
data = RestrictedUnpickler(io.BytesIO(safe_pickle)).load()
print(f"  ✅ Success: {data}")


# ========================================================================
# SECTION 3: PICKLE PERFORMANCE OPTIMIZATION
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 3: PICKLE PERFORMANCE OPTIMIZATION")
print("=" * 80)

import time

# Create large dataset
large_data = {
    "users": [User(i, f"user{i}@example.com") for i in range(1000)],
    "metadata": {"version": 1, "timestamp": "2026-01-22"},
}

print("\nBenchmarking pickle protocols:")
print("(serializing 1000 User objects + metadata)\n")

for protocol in range(6):
    try:
        start = time.time()
        for _ in range(100):  # 100 iterations
            serialized = pickle.dumps(large_data, protocol=protocol)
        elapsed = time.time() - start

        single = pickle.dumps(large_data, protocol=protocol)
        size = len(single)

        print(f"Protocol {protocol}:")
        print(f"  Size: {size:8d} bytes")
        print(f"  Time (100x): {elapsed:.4f}s")
        print(f"  Speed: {size * 100 / elapsed / 1024:.0f} KB/s")
        print()
    except Exception as e:
        print(f"Protocol {protocol}: Not available ({e})\n")

print("💡 Recommendation:")
print("  - Protocol 5 (Python 3.8+): Best balance of speed and size")
print("  - Protocol 4 (Python 3.4+): Good compatibility")
print("  - Protocol 0-2: Avoid (slow and large)")


# ========================================================================
# SECTION 4: VERSIONING AND BACKWARD COMPATIBILITY
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 4: VERSIONING FOR COMPATIBILITY")
print("=" * 80)


@dataclass
class ModelV1:
    """Original model version."""
    name: str
    weights: list[float]


@dataclass
class ModelV2:
    """Updated model version with new field."""
    name: str
    weights: list[float]
    metadata: dict = None  # New field
    version: int = 2


def load_model(data: bytes) -> ModelV2:
    """
    Load model from pickle, handling version migrations.

    This function handles loading both V1 and V2 models,
    automatically upgrading V1 to V2.
    """
    # Try to load
    try:
        obj = pickle.loads(data)

        # Check if it's V1 (no metadata field)
        if isinstance(obj, ModelV1):
            print("Loaded V1 model, upgrading to V2...")
            # Migrate V1 -> V2
            return ModelV2(
                name=obj.name,
                weights=obj.weights,
                metadata={"upgraded_from": "v1"},
                version=2
            )

        # Already V2
        return obj

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise


print("\nDemonstrating version migration:")

# Create V1 model and save
v1_model = ModelV1(name="legacy_model", weights=[0.1, 0.2, 0.3])
v1_pickle = pickle.dumps(v1_model)
print(f"Created V1 model pickle: {len(v1_pickle)} bytes")

# Load and upgrade
v2_model = load_model(v1_pickle)
print(f"Loaded as V2: {v2_model}")

# Create V2 model for comparison
v2_model_native = ModelV2(name="new_model", weights=[0.4, 0.5, 0.6])
v2_pickle = pickle.dumps(v2_model_native)

v2_loaded = load_model(v2_pickle)
print(f"Direct V2 load: {v2_loaded}")


# ========================================================================
# SECTION 5: ML MODEL SERIALIZATION PATTERNS
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 5: ML MODEL SERIALIZATION PATTERNS")
print("=" * 80)


@dataclass
class MLModel:
    """Simple ML model for demonstration."""
    model_name: str
    algorithm: str
    weights: list[float]
    feature_names: list[str]
    training_date: str
    accuracy: float

    def predict(self, features: list[float]) -> float:
        """Make a prediction (simplified)."""
        # In real ML: return model.predict(features)
        return sum(w * f for w, f in zip(self.weights, features))

    def save(self, filepath: str) -> None:
        """Save model to file."""
        with open(filepath, "wb") as f:
            pickle.dump(self, f, protocol=5)
        print(f"✅ Saved model to {filepath}")

    @classmethod
    def load(cls, filepath: str) -> MLModel:
        """Load model from file."""
        with open(filepath, "rb") as f:
            model = pickle.load(f)
        print(f"✅ Loaded model from {filepath}")
        return model


print("\nML Model Serialization Workflow:")

# Create a trained model
model = MLModel(
    model_name="sales_predictor_v2.1",
    algorithm="gradient_boosting",
    weights=[0.15, 0.25, 0.30, 0.20, 0.10],
    feature_names=["price", "quantity", "season", "marketing", "trend"],
    training_date="2026-01-22",
    accuracy=0.92
)

print(f"\n1. Created model: {model.model_name}")
print(f"   Accuracy: {model.accuracy:.2%}")

# Make a prediction with original model
test_features = [100.0, 5.0, 0.8, 500.0, 1.2]
prediction = model.predict(test_features)
print(f"\n2. Made prediction: {prediction:.2f}")

# Save
model.save("ml_model_production.pkl")

# Load
loaded_model = MLModel.load("ml_model_production.pkl")

# Make prediction with loaded model
loaded_prediction = loaded_model.predict(test_features)
print(f"\n3. Loaded model made same prediction: {loaded_prediction:.2f}")
print(f"   Predictions match: {abs(prediction - loaded_prediction) < 0.001}")


# ========================================================================
# SECTION 6: DISTRIBUTED COMPUTING WITH PICKLE
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 6: DISTRIBUTED COMPUTING WITH PICKLE")
print("=" * 80)

print("""
In Distributed Computing Frameworks:
- Ray: Uses pickle to serialize tasks across workers
- Dask: Pickles data and functions for parallel execution
- Spark: Uses pickle for Python UDF serialization
- Celery: Pickles task arguments for workers

Challenge: Worker processes must be able to deserialize
the pickled objects. This requires:
1. Same Python version
2. Same packages installed
3. Same code available to workers

Example: Processing data with Ray
""")


def expensive_computation(user_id: int, data: dict) -> dict:
    """
    A task that might run on a distributed worker.
    In production, this would be:
    - CPU-intensive
    - Memory-intensive
    - Parallelizable
    """
    # Simulate computation
    result = sum(data.get("values", []))
    return {"user_id": user_id, "result": result, "processed": True}


# Simulate what would be pickled for a worker
task_data = {"user_id": 1, "data": {"values": [1, 2, 3, 4, 5]}}

print(f"\nTask to be distributed:")
print(f"  Function: expensive_computation")
print(f"  Data: {task_data}")

# Pickle the task
task_pickle = pickle.dumps((expensive_computation, task_data), protocol=5)
print(f"  Pickled size: {len(task_pickle)} bytes")

# Unpickle and execute on "worker"
func, data = pickle.loads(task_pickle)
result = func(**data)
print(f"  Result from worker: {result}")

print("""
✅ In production:
   - Framework handles serialization automatically
   - Use cloudpickle for more complex objects
   - Ensure workers have same environment
""")


# ========================================================================
# SECTION 7: ERROR HANDLING AND RESILIENCE
# ========================================================================

print("\n" + "=" * 80)
print("SECTION 7: ERROR HANDLING AND RESILIENCE")
print("=" * 80)


def safe_load_pickle(filepath: str, default: Any = None) -> Any:
    """
    Safely load a pickle file with error handling.

    Returns default value if loading fails, allowing
    graceful degradation in production.
    """
    try:
        with open(filepath, "rb") as f:
            data = pickle.load(f)
        print(f"✅ Loaded pickle from {filepath}")
        return data
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return default
    except (pickle.UnpicklingError, EOFError) as e:
        print(f"❌ Corrupted pickle: {e}")
        return default
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return default


print("\nDemonstrating error handling:")

# Try loading non-existent file
data = safe_load_pickle("nonexistent.pkl", default={"fallback": True})
print(f"Result: {data}\n")

# Try loading corrupted file
with open("corrupted.pkl", "wb") as f:
    f.write(b"not a valid pickle!")

data = safe_load_pickle("corrupted.pkl", default={"fallback": True})
print(f"Result: {data}")


# ========================================================================
# SUMMARY
# ========================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ PICKLE IN PRODUCTION:

1. SECURITY:
   ⚠️  NEVER unpickle untrusted data (code execution risk)
   ✓ Use RestrictedUnpickler to limit what can be imported
   ✓ Validate data source before unpickling
   ✓ Use signed/encrypted transport for pickles

2. PERFORMANCE:
   ✓ Use protocol=5 (Python 3.8+)
   ✓ Benchmark different protocols
   ✓ Consider alternative formats (MessagePack) for cross-language

3. VERSIONING:
   ✓ Include version metadata with pickles
   ✓ Implement migration functions for old versions
   ✓ Test backward compatibility

4. ML MODEL PATTERNS:
   ✓ Save model + hyperparameters + metadata
   ✓ Include training date and accuracy metrics
   ✓ Version your models (model_v1.pkl, model_v2.pkl)
   ✓ Use joblib for scikit-learn (better than raw pickle)

5. DISTRIBUTED COMPUTING:
   ✓ Framework handles serialization (Ray, Dask, Spark)
   ✓ Use cloudpickle for complex objects
   ✓ Ensure worker environments match

6. ERROR HANDLING:
   ✓ Wrap unpickling in try/except
   ✓ Provide sensible defaults
   ✓ Log errors for monitoring
   ✓ Implement graceful degradation

🏗️ PRODUCTION ARCHITECTURE:
   - Save pickle to durable storage (S3, GCS, local)
   - Include metadata (version, date, checksum)
   - Validate on load (size, magic bytes, version)
   - Use async I/O for large files
   - Monitor serialization performance

💡 WHEN TO USE PICKLE:
   ✓ Model persistence (with joblib wrapper)
   ✓ Internal caching (same application)
   ✓ Distributed task passing (same framework)
   ✗ Cross-language APIs (use JSON/Protobuf)
   ✗ Long-term storage (version management issues)
   ✗ Untrusted data sources (security risk)

🔒 SECURITY BEST PRACTICES:
   1. Only unpickle your own data
   2. Use RestrictedUnpickler if accepting external pickles
   3. Sign pickles cryptographically
   4. Validate before unpickling
   5. Never trust pickles from internet
   6. Monitor and audit pickle operations
"""

print(summary)
