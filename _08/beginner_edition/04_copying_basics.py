"""
Module 8.4: Object Copying - Shallow vs Deep Copy
==================================================

Learning Goals:
- Understand shallow copy vs deep copy
- Learn how references work in Python
- Implement copy with __copy__ and __deepcopy__
- Avoid mutable default argument pitfall
- Understand copy performance implications

🔍 Where you'll use this:
- Data pipeline stages (avoid modifying original data)
- ML preprocessing (preserve original features)
- Configuration management (copy before modification)
- Test setup (isolate test data)

⚡ Data Science/Engineering Context:
- DataFrame operations (copy vs view performance)
- Feature engineering (creating new columns without modifying original)
- Model experiments (copy hyperparameters for grid search)
- Data caching (when to copy vs share references)

🔒 SECURITY NOTE:
- Shallow copy exposes mutable fields (dangerous if shared)
- Deep copy is safer but slower (duplicates all data)
- Choose based on your needs and data size
"""

from __future__ import annotations

import copy
from typing import Any


# ==========================================================================
# SECTION 1: UNDERSTANDING REFERENCES AND MUTABLE OBJECTS
# ==========================================================================

print("=" * 70)
print("SECTION 1: REFERENCES AND MUTABILITY")
print("=" * 70)

# Lists are mutable and share references
original_list = [1, 2, 3]
reference = original_list  # Just creates reference, doesn't copy

print(f"\nOriginal list: {original_list}")
print(f"Reference: {reference}")
print(f"Same object? {original_list is reference}")  # True - same memory!

# Modify through reference
reference.append(4)
print(f"\nAfter reference.append(4):")
print(f"Original: {original_list}")  # Also modified!
print(f"Reference: {reference}")

print("\n⚠️  Problem: Modifying the reference changes the original!")


# ==========================================================================
# SECTION 2: SHALLOW COPY
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 2: SHALLOW COPY")
print("=" * 70)

print("\nShallow copy: Copies the container, but NOT the contents")

list_a = [1, 2, 3]
list_b = copy.copy(list_a)

print(f"\nOriginal: {list_a}")
print(f"Shallow copy: {list_b}")
print(f"Same object? {list_a is list_b}")  # False - different objects

list_b.append(4)
print(f"\nAfter list_b.append(4):")
print(f"Original: {list_a}")  # Not modified
print(f"Copy: {list_b}")  # Only copy is modified

print("✅ For simple values, shallow copy works fine!")

# But with nested mutable objects, shallow copy is dangerous
print("\n⚠️  SHALLOW COPY PITFALL - with nested objects:")

original_nested = [[1, 2], [3, 4]]
shallow_copy_nested = copy.copy(original_nested)

print(f"\nOriginal: {original_nested}")
print(f"Shallow copy: {shallow_copy_nested}")
print(f"Are they the same list object? {original_nested is shallow_copy_nested}")  # False
print(f"But inner lists are shared? {original_nested[0] is shallow_copy_nested[0]}")  # True!

# Modify inner list
shallow_copy_nested[0].append(99)
print(f"\nAfter shallow_copy[0].append(99):")
print(f"Original: {original_nested}")  # Modified through shared reference!
print(f"Shallow copy: {shallow_copy_nested}")

print("❌ Problem: Inner lists are shared!")


# ==========================================================================
# SECTION 3: DEEP COPY
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 3: DEEP COPY")
print("=" * 70)

print("\nDeep copy: Recursively copies everything (safe but slower)")

original_nested = [[1, 2], [3, 4]]
deep_copy_nested = copy.deepcopy(original_nested)

print(f"\nOriginal: {original_nested}")
print(f"Deep copy: {deep_copy_nested}")
print(f"Are they the same list object? {original_nested is deep_copy_nested}")  # False
print(f"Are inner lists shared? {original_nested[0] is deep_copy_nested[0]}")  # False

# Modify deep copy
deep_copy_nested[0].append(99)
print(f"\nAfter deep_copy[0].append(99):")
print(f"Original: {original_nested}")  # NOT modified!
print(f"Deep copy: {deep_copy_nested}")

print("✅ Deep copy is completely independent!")


# ==========================================================================
# SECTION 4: COPYING CUSTOM OBJECTS
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 4: COPYING CUSTOM OBJECTS")
print("=" * 70)


class Config:
    """Configuration object that needs copying."""

    def __init__(self, name: str, params: dict[str, Any]):
        self.name = name
        self.params = params  # Mutable dict

    def __repr__(self) -> str:
        return f"Config(name={self.name!r}, params={self.params})"


# Original config
config1 = Config("experiment_1", {"learning_rate": 0.01, "epochs": 100})
print(f"\nOriginal: {config1}")

# Shallow copy (default)
config2 = copy.copy(config1)
print(f"Shallow copy: {config2}")

# Modify params in shallow copy
config2.params["learning_rate"] = 0.05
print(f"\nAfter modifying shallow_copy.params:")
print(f"Original: {config1}")  # ⚠️  Original modified!
print(f"Shallow copy: {config2}")

# Deep copy (safe)
config1_original = Config("experiment_2", {"learning_rate": 0.01, "epochs": 100})
config3 = copy.deepcopy(config1_original)
print(f"\n\nOriginal: {config1_original}")
print(f"Deep copy: {config3}")

config3.params["learning_rate"] = 0.05
print(f"\nAfter modifying deep_copy.params:")
print(f"Original: {config1_original}")  # ✅ Not modified!
print(f"Deep copy: {config3}")


# ==========================================================================
# SECTION 5: CUSTOM COPY BEHAVIOR
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 5: CUSTOM __copy__ AND __deepcopy__ METHODS")
print("=" * 70)


class SmartConfig:
    """Config with custom copy behavior."""

    def __init__(self, name: str, params: dict, locked: bool = False):
        self.name = name
        self.params = params
        self.locked = locked

    def __copy__(self) -> SmartConfig:
        """Custom shallow copy behavior."""
        print(f"  ℹ️  __copy__ called for {self.name}")
        # Shallow copy: just copy the params dict reference
        return SmartConfig(self.name, self.params, self.locked)

    def __deepcopy__(self, memo: dict) -> SmartConfig:
        """Custom deep copy behavior."""
        print(f"  ℹ️  __deepcopy__ called for {self.name}")
        # Deep copy: copy params dict recursively
        return SmartConfig(
            self.name,
            copy.deepcopy(self.params, memo),
            self.locked
        )

    def __repr__(self) -> str:
        return f"SmartConfig(name={self.name!r}, params={self.params}, locked={self.locked})"


print("\nCreating SmartConfig:")
smart1 = SmartConfig("model_v1", {"alpha": 0.1, "beta": 0.2})
print(f"Original: {smart1}")

print("\nShallow copy:")
smart2 = copy.copy(smart1)
print(f"Copy: {smart2}")

print("\nDeep copy:")
smart3 = copy.deepcopy(smart1)
print(f"Copy: {smart3}")


# ==========================================================================
# SECTION 6: THE MUTABLE DEFAULT ARGUMENT PITFALL
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 6: MUTABLE DEFAULT ARGUMENT PITFALL")
print("=" * 70)

print("\n⚠️  COMMON MISTAKE:")


def bad_function(item: str, items_list: list = []):
    """
    ❌ NEVER use mutable objects as default arguments!
    The default list is created ONCE when function is defined,
    not each time the function is called.
    """
    items_list.append(item)
    return items_list


print("\nCalling bad_function three times:")
result1 = bad_function("first")
print(f"Call 1: {result1}")

result2 = bad_function("second")
print(f"Call 2: {result2}")  # ⚠️  Contains both first AND second!

result3 = bad_function("third")
print(f"Call 3: {result3}")  # ⚠️  Contains all three!

print("\n❌ Problem: The default list is shared across all calls!")

print("\n✅ CORRECT APPROACH:")


def good_function(item: str, items_list: list | None = None):
    """Use None as default, create new list inside."""
    if items_list is None:
        items_list = []
    items_list.append(item)
    return items_list


print("\nCalling good_function three times:")
result1 = good_function("first")
print(f"Call 1: {result1}")

result2 = good_function("second")
print(f"Call 2: {result2}")  # Only second

result3 = good_function("third")
print(f"Call 3: {result3}")  # Only third

print("✅ Each call gets its own list!")


# ==========================================================================
# SECTION 7: COPY PERFORMANCE
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 7: COPY PERFORMANCE CONSIDERATIONS")
print("=" * 70)

import sys

large_data = list(range(1000))

print(f"\nMemory size of original list: {sys.getsizeof(large_data)} bytes")

shallow = copy.copy(large_data)
deep = copy.deepcopy(large_data)

print(f"Shallow copy size: {sys.getsizeof(shallow)} bytes")
print(f"Deep copy size: {sys.getsizeof(deep)} bytes")

print("\nPerformance implications:")
print("  - Shallow copy: Fast (O(1) for simple objects)")
print("  - Deep copy: Slow (O(n) where n = total items to copy)")
print("  - For large datasets, deep copy can be expensive!")

print("\nChoose based on:")
print("  ✓ Use shallow copy if you won't modify mutable fields")
print("  ✓ Use deep copy if you'll modify nested structures")
print("  ✓ Consider alternatives (views, slices) for performance")


# ==========================================================================
# SECTION 8: PRACTICAL EXAMPLE - DATA PIPELINE
# ==========================================================================

print("\n" + "=" * 70)
print("SECTION 8: PRACTICAL EXAMPLE - DATA PIPELINE")
print("=" * 70)


class DataPipeline:
    """Data processing pipeline that copies data between stages."""

    def __init__(self, data: list[dict]):
        self.data = copy.deepcopy(data)  # Ensure isolation
        self.stages = []

    def add_stage(self, name: str, transform):
        """Add processing stage."""
        self.stages.append((name, transform))
        return self

    def execute(self):
        """Execute pipeline, showing data at each stage."""
        current_data = copy.deepcopy(self.data)  # Start with copy

        print(f"\nInput data: {current_data}")

        for stage_name, transform in self.stages:
            current_data = [transform(item) for item in current_data]
            print(f"After {stage_name}: {current_data}")

        return current_data


# Example pipeline
original_numbers = [{"val": 1}, {"val": 2}, {"val": 3}]

pipeline = DataPipeline(original_numbers)
result = (
    pipeline
    .add_stage("increment", lambda x: {"val": x["val"] + 1})
    .add_stage("double", lambda x: {"val": x["val"] * 2})
    .execute()
)

print(f"\nOriginal data unchanged: {original_numbers}")
print(f"Final result: {result}")
print("✅ Pipeline stages work on copies, original data preserved!")


# ==========================================================================
# SUMMARY
# ==========================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

summary = """
✅ KEY CONCEPTS:

1. REFERENCES VS COPIES:
   - Reference: points to same object (dangerous!)
   - Shallow copy: copies container, shares contents
   - Deep copy: copies everything recursively (safe but slow)

2. WHEN TO USE:
   ✓ Reference: when you WANT shared state (rare)
   ✓ Shallow copy: simple data (numbers, strings), no modification
   ✓ Deep copy: complex data structures, will be modified

3. CUSTOM COPY BEHAVIOR:
   - Implement __copy__() for custom shallow copy
   - Implement __deepcopy__(memo) for custom deep copy
   - memo dict tracks already-copied objects (prevents infinite recursion)

4. COMMON PITFALLS:
   ❌ Mutable default arguments (use None, create inside)
   ❌ Shallow copy of nested structures (modifies original)
   ❌ Forgetting to copy before modification
   ❌ Deep copying everything (performance issues)

5. ALTERNATIVES TO COPY:
   - Slicing: data[:]  (creates shallow copy of list)
   - comprehensions: [x for x in data]  (creates new list)
   - list(): new_list = list(old_list)  (shallow copy)
   - pandas.DataFrame.copy(): similar behavior for DataFrames

💡 BEST PRACTICES:
   - Default to deep copy if unsure
   - Profile copy performance in data pipelines
   - Document when/why you're copying
   - Use copy only when necessary (avoid premature copying)
   - Consider structural sharing for large data (persistent data structures)
"""

print(summary)
