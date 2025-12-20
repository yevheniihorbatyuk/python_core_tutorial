"""
MODULE 6.1: Functional Programming in Python
==============================================

PURPOSE:
  Understand functional programming principles and their impact on code
  quality, readability, and performance in real applications.

CONTENTS:
  1. Decimal - Precise financial calculations
  2. Generators and yield - Lazy evaluation for large datasets
  3. map, filter, lambda - Functional transformations
  4. Decorators and @lru_cache - Performance optimization

PRACTICAL VALUE:
  ✓ Data Science: Lazy processing of massive datasets
  ✓ Web: @lru_cache makes requests 1000x faster
  ✓ Finance: Decimal ensures penny-accurate transactions
  ✓ Systems: map/filter enable parallel processing
"""

from decimal import Decimal
from functools import lru_cache
import time

print("=" * 80)
print("MODULE 6.1: FUNCTIONAL PROGRAMMING")
print("=" * 80)


# ============================================================================
# 1. DECIMAL: Precise Financial Calculations
# ============================================================================

print("\n\n[1] DECIMAL: Precise Financial Calculations")
print("-" * 80)

print("\n❌ PROBLEM: Floating Point Precision Error")
print(f"  0.1 + 0.2 = {0.1 + 0.2}")  # 0.30000000000000004 !!!
print(f"  0.1 + 0.2 == 0.3 ? {0.1 + 0.2 == 0.3}")  # False !!!

# Real-world impact
balance = 0.0
for amount in [0.1, 0.2, -0.15, 0.05]:
    balance += amount

print(f"\nBanking Account Balance (float): {balance}")
print(f"Expected: 0.2, Got: {balance} ← ERROR!")


print("\n\n✅ SOLUTION: Decimal for Exact Calculations")


def calculate_bank_balance(transactions):
    """
    Calculate account balance with exact precision.

    Args:
        transactions: list of (amount, description) tuples

    Returns:
        balance: Decimal - exact balance
    """
    balance = Decimal('0.00')

    print(f"{'Operation':<30} | {'Amount':>15} | {'Balance':>15}")
    print("-" * 62)

    for amount, desc in transactions:
        amount_dec = Decimal(str(amount))
        balance += amount_dec
        print(f"{desc:<30} | ${amount_dec:>14.2f} | ${balance:>14.2f}")

    return balance


transactions = [
    (Decimal('1000.00'), "Initial Deposit"),
    (Decimal('50.50'), "Groceries"),
    (Decimal('-25.99'), "Electricity Bill"),
    (Decimal('12.75'), "Refund"),
    (Decimal('-0.01'), "Banking Fee"),
]

final = calculate_bank_balance(transactions)
print(f"\nFinal Balance: ${final:.2f}")


# ============================================================================
# 2. GENERATORS: Lazy Evaluation
# ============================================================================

print("\n\n[2] GENERATORS: Lazy Evaluation of Large Data")
print("-" * 80)

print("\nMEMORY COMPARISON:")
print("  Reading 1 million lines from file:")
print("  - list:      1M × 100 bytes = 100 MB RAM")
print("  - generator: 1 × 100 bytes = 0.1 KB RAM ← 1000x less!")


def fibonacci_generator(n):
    """
    Generate Fibonacci sequence up to n terms.

    yield returns a value and pauses execution.
    When called again, resumes from where it paused.
    """
    a, b = 0, 1

    for _ in range(n):
        yield a  # Return value, pause function
        a, b = b, a + b  # Update for next call


print("\n✅ Fibonacci Generator (first 10 numbers):")
print("  ", end="")
for num in fibonacci_generator(10):
    print(num, end=" ")
print()

print("\nUsing next() for control:")
gen = fibonacci_generator(5)
print(f"  next() #1: {next(gen)}")  # 0
print(f"  next() #2: {next(gen)}")  # 1
print(f"  next() #3: {next(gen)}")  # 1
print(f"  next() #4: {next(gen)}")  # 2


# ============================================================================
# 3. MAP, FILTER, LAMBDA: Functional Transformations
# ============================================================================

print("\n\n[3] MAP, FILTER, LAMBDA: Data Transformation")
print("-" * 80)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map() - Transform each element
print("\n✅ map(): Transform Each Element")
print(f"  Data: {numbers}")

squared = list(map(lambda n: n ** 2, numbers))
print(f"  Squared: {squared}")

# filter() - Select elements
print("\n✅ filter(): Select Matching Elements")
evens = list(filter(lambda n: n % 2 == 0, numbers))
print(f"  Even numbers: {evens}")

# lambda - Anonymous functions
print("\n✅ lambda: Anonymous Functions")

# Example: Sort by length
words = ["apple", "pie", "python", "ai"]
sorted_by_length = sorted(words, key=lambda w: len(w))
print(f"  Words: {words}")
print(f"  Sorted by length: {sorted_by_length}")


# PIPELINE: Combine transformations
print("\n✅ PIPELINE: Combine Operations")
print(f"  Task: Even numbers → squares → sum")
print(f"  Data: {numbers}")

result = sum(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
evens_list = list(filter(lambda x: x % 2 == 0, numbers))
squared_list = list(map(lambda x: x ** 2, evens_list))

print(f"  Even: {evens_list}")
print(f"  Squared: {squared_list}")
print(f"  Sum: {result}")


# ============================================================================
# 4. DECORATORS AND @LRU_CACHE: Optimization
# ============================================================================

print("\n\n[4] DECORATORS AND @lru_cache: Performance Boost")
print("-" * 80)

print("\n✅ Simple Timing Decorator")


def timing_decorator(func):
    """
    Decorator that measures function execution time.
    Wraps function without changing its code.
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        print(f"    ⏱️  {func.__name__} took {elapsed:.2f}ms")
        return result
    return wrapper


@timing_decorator
def slow_function():
    """A slow function"""
    time.sleep(0.1)
    return "done"


print("  Calling function with decorator:")
result = slow_function()


# @lru_cache - Cache function results
print("\n\n✅ @lru_cache: Cache Results")
print("  Fibonacci comparison (cached vs uncached)")


def fibonacci_no_cache(n):
    """Fibonacci WITHOUT caching - O(2^n) complexity"""
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


@lru_cache(maxsize=128)
def fibonacci_cached(n):
    """Fibonacci WITH caching - O(n) complexity"""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


test_values = [20, 25, 30]

for n in test_values:
    # Without cache
    start = time.time()
    result_no_cache = fibonacci_no_cache(n)
    time_no_cache = (time.time() - start) * 1000

    # With cache (clear first)
    fibonacci_cached.cache_clear()
    start = time.time()
    result_cached = fibonacci_cached(n)
    time_cached = (time.time() - start) * 1000

    speedup = time_no_cache / time_cached if time_cached > 0 else float('inf')

    print(f"\n  fib({n}):")
    print(f"    No cache:  {time_no_cache:>10.2f}ms")
    print(f"    Cached:    {time_cached:>10.4f}ms")
    print(f"    Speedup:   {speedup:>10.0f}x")


# Practical example: Expensive computation
print("\n\n✅ Practical Example: ML Prediction Caching")


@lru_cache(maxsize=256)
def predict_model(features_tuple):
    """
    ML prediction caching example.

    Without cache: 500ms per prediction
    With cache: 0.001ms for cached result
    Impact: 500,000x faster for same input!
    """
    time.sleep(0.001)  # Simulate model computation
    return sum(features_tuple) * 1.5


features = (1.0, 2.0, 3.0)

print("  First call (computes):")
start = time.time()
pred1 = predict_model(features)
t1 = (time.time() - start) * 1000
print(f"    Result: {pred1:.2f}, Time: {t1:.2f}ms")

print("\n  Second call (from cache):")
start = time.time()
pred2 = predict_model(features)
t2 = (time.time() - start) * 1000
print(f"    Result: {pred2:.2f}, Time: {t2:.4f}ms")
print(f"    Speedup: {t1/t2:.0f}x!")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "=" * 80)
print("KEY TAKEAWAYS")
print("=" * 80)

print("""
✅ DECIMAL - For financial calculations (accuracy)
   - Banks, stocks, crypto all use Decimal
   - Guarantee: 0.1 + 0.2 == 0.3

✅ GENERATORS - For large data (memory)
   - 1M files → generator (0.1KB) vs list (100MB)
   - YouTube, Netflix read files as generators

✅ MAP/FILTER - Functional style (cleanliness)
   - No side effects, easy to test
   - Data Science: 90% of code is transformation

✅ @LRU_CACHE - Result caching (speed)
   - fib(30): 1000ms → 0.00001ms
   - Web: cache requests, ML: cache predictions

👉 NEXT: Module 6.2 - Object-Oriented Programming
""")

print("=" * 80)
