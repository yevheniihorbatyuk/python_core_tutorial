"""
BEGINNER EDITION: Lesson 4 - @lru_cache for Performance Optimization
====================================================================

PROBLEM:
--------
Some functions are called repeatedly with same arguments.
Recalculating same results wastes CPU time.
- Fibonacci(30) with recursion = 1 billion operations = 1+ second
- ML recommendations calculated per user = hours of computing

SOLUTION:
---------
Cache results using @lru_cache decorator.
When called again with same arguments, return cached result instantly.

WHY IT MATTERS:
---------------
- Netflix saves 10,000+ seconds daily with caching
- Google caches search results (same queries repeat)
- Financial models cache calculations
- ML systems cache predictions

This lesson shows:
1. Why caching matters (performance impact)
2. How @lru_cache works (decorator concept)
3. Fibonacci example (10,000x+ speedup)
4. Practical recommendation engine
5. Cache statistics and when to use caching
"""

from functools import lru_cache
from decimal import Decimal
from time import time
from typing import Dict, List, Set, Tuple
import random
from config import CACHE_CONFIG, LOGGING_CONFIG


# ============================================================================
# PART 1: THE PROBLEM - EXPENSIVE RECURSION
# ============================================================================

def fibonacci_no_cache(n: int) -> int:
    """
    Calculate Fibonacci number WITHOUT caching.

    This recalculates the same values many times:
    fib(5) = fib(4) + fib(3)
           = (fib(3) + fib(2)) + (fib(2) + fib(1))
           = ((fib(2) + fib(1)) + (fib(1) + fib(0))) + ((fib(1) + fib(0)) + fib(1))

    fib(2) calculated 3 times! fib(1) calculated 5 times!
    This gets exponentially worse.
    """
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


def count_calls_fibonacci(n: int) -> Tuple[int, int]:
    """
    Count how many function calls to calculate fib(n).

    Shows how exponential the problem is.
    """
    call_count = [0]  # Mutable counter

    def fib_counting(n):
        call_count[0] += 1
        if n <= 1:
            return n
        return fib_counting(n - 1) + fib_counting(n - 2)

    result = fib_counting(n)
    return result, call_count[0]


def demonstrate_fibonacci_problem():
    """
    Show how expensive Fibonacci is without caching.
    """
    print("\n" + "=" * 70)
    print("PROBLEM: Exponential Recursion Without Caching")
    print("=" * 70)

    print("\n[1] How many times is each value calculated?")
    print("\nfib(10) requires how many function calls?")

    result, calls = count_calls_fibonacci(10)
    print(f"  Result: {result}")
    print(f"  Function calls: {calls:,}")

    print("\nfib(30) requires how many function calls?")
    result, calls = count_calls_fibonacci(30)
    print(f"  Result: {result}")
    print(f"  Function calls: {calls:,}  ← 2 MILLION calls!")

    print("\nfib(40) requires how many function calls?")
    result, calls = count_calls_fibonacci(40)
    print(f"  Result: {result}")
    print(f"  Function calls: {calls:,}  ← 330 MILLION calls!")

    # Performance impact
    print("\n[2] Performance impact (time to calculate):")
    print("\nWithout cache:")

    test_cases = [20, 25, 30]
    for n in test_cases:
        start = time()
        result = fibonacci_no_cache(n)
        elapsed = (time() - start) * 1000  # Convert to milliseconds

        print(f"  fib({n:2d}) = {result:>10,}  took {elapsed:>8.2f}ms")

        if elapsed > 2000:  # If over 2 seconds, stop (too slow)
            print(f"  ⚠️  fib(31+) would take too long, skipping...")
            break


# ============================================================================
# PART 2: THE SOLUTION - @lru_cache
# ============================================================================

@lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    """
    Calculate Fibonacci number WITH caching.

    @lru_cache decorator:
    - LRU = Least Recently Used
    - maxsize=128: Keep last 128 results in memory
    - If same n called again, return cached result instantly

    This converts exponential time to linear time!
    """
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def demonstrate_cache_solution():
    """
    Show how @lru_cache solves the problem.
    """
    print("\n" + "=" * 70)
    print("SOLUTION: @lru_cache Decorator")
    print("=" * 70)

    print("\n[1] What is @lru_cache?")
    print("  @lru_cache is a decorator that:")
    print("    - Remembers results of function calls")
    print("    - If called again with same arguments → return cached result")
    print("    - Maxsize: keep last N results")
    print("    - When full, discard least recently used")

    print("\n[2] Performance comparison:")
    print(f"  {'n':<5} {'Without Cache':>25} {'With Cache':>25} {'Speedup':>10}")
    print(f"  {'-'*5} {'-'*25} {'-'*25} {'-'*10}")

    # Clear cache before tests
    fibonacci_cached.cache_clear()

    for n in [10, 15, 20, 25, 30]:
        # Without cache
        start = time()
        result_uncached = fibonacci_no_cache(n)
        time_uncached = (time() - start) * 1000

        # With cache
        start = time()
        result_cached = fibonacci_cached(n)
        time_cached = (time() - start) * 1000

        speedup = time_uncached / time_cached if time_cached > 0 else 999999

        print(
            f"  {n:<5} {time_uncached:>20.2f}ms {time_cached:>20.6f}ms "
            f"{speedup:>8.0f}x"
        )

    # Show cache statistics
    print("\n[3] Cache statistics:")
    info = fibonacci_cached.cache_info()
    print(f"  Hits: {info.hits:,} (returned from cache)")
    print(f"  Misses: {info.misses:,} (had to calculate)")
    print(f"  Maxsize: {info.maxsize}")
    print(f"  Currsize: {info.currsize}")
    print(f"  Hit rate: {info.hits / (info.hits + info.misses) * 100:.1f}%")


# ============================================================================
# PART 3: HOW @lru_cache WORKS (DETAILED)
# ============================================================================

def lru_cache_mechanics():
    """
    Explain how LRU cache actually works step by step.
    """
    print("\n" + "=" * 70)
    print("HOW @lru_cache WORKS: Step by Step")
    print("=" * 70)

    @lru_cache(maxsize=3)
    def example(n):
        """Simple function to trace caching."""
        print(f"    [COMPUTE] example({n})")
        return n * 2

    print("\n[Example with maxsize=3]")
    print("\nStep 1: Call example(1)")
    result = example(1)
    print(f"  Result: {result}, Cache: {[(1, 2)]}")

    print("\nStep 2: Call example(2)")
    result = example(2)
    print(f"  Result: {result}, Cache: {[(1, 2), (2, 4)]}")

    print("\nStep 3: Call example(1) again")
    result = example(1)
    print(f"  ✓ CACHED! Result: {result}, Cache: {[(2, 4), (1, 2)]}")

    print("\nStep 4: Call example(3)")
    result = example(3)
    print(f"  Result: {result}, Cache: {[(1, 2), (3, 6)]}")

    print("\nStep 5: Call example(4)")
    result = example(4)
    print(f"  Result: {result}, Cache FULL (3 items), LRU(2) evicted")
    print(f"  Cache: {[(1, 2), (3, 6), (4, 8)]}")

    print("\nStep 6: Call example(2) - not in cache anymore")
    result = example(2)
    print(f"  [COMPUTE] because 2 was evicted as least recently used")
    print(f"  Cache: {[(3, 6), (4, 8), (2, 4)]}")

    print("\n💡 LRU = when cache full, remove least recently used item")


# ============================================================================
# PART 4: PRACTICAL EXAMPLE - RECOMMENDATION ENGINE
# ============================================================================

class ProductRecommender:
    """
    Simple recommendation engine with caching.

    Real recommenders (Netflix, Amazon) cache:
    - User profiles (expensive ML computation)
    - Product recommendations
    - Similarity scores
    """

    def __init__(self):
        """Initialize with sample products."""
        self.products = {
            "laptop": ["electronics", "expensive", "productivity"],
            "book": ["education", "cheap", "entertainment"],
            "phone": ["electronics", "expensive", "communication"],
            "headphones": ["electronics", "moderate", "audio"],
            "coffee": ["food", "cheap", "daily"],
            "desk": ["furniture", "expensive", "productivity"],
        }

    @lru_cache(maxsize=128)
    def calculate_similarity(self, product_a: str, product_b: str) -> Decimal:
        """
        Calculate similarity between two products.

        This is expensive computation (simulated).
        Caching saves huge amount of computation.

        In real recommender:
        - Extract features from 1000+ products
        - Compute ML embeddings
        - Calculate similarity using cosine distance
        """
        # Simulate expensive computation
        import time
        time.sleep(0.001)  # 1ms simulated computation

        if product_a not in self.products or product_b not in self.products:
            return Decimal("0")

        # Simple similarity: matching attributes
        attrs_a = set(self.products[product_a])
        attrs_b = set(self.products[product_b])

        if not attrs_a or not attrs_b:
            return Decimal("0")

        intersection = len(attrs_a & attrs_b)
        union = len(attrs_a | attrs_b)
        similarity = Decimal(intersection) / Decimal(union)

        return similarity

    def recommend(self, product: str, top_n: int = 3) -> List[Tuple[str, Decimal]]:
        """
        Recommend similar products.

        Uses caching: if same product recommended again,
        use cached similarities instead of recalculating.
        """
        if product not in self.products:
            return []

        similarities = [
            (other, self.calculate_similarity(product, other))
            for other in self.products
            if other != product
        ]

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_n]

    def print_cache_stats(self):
        """Print cache statistics."""
        info = self.calculate_similarity.cache_info()
        print(f"\n  Cache Stats:")
        print(f"    Hits: {info.hits}")
        print(f"    Misses: {info.misses}")
        print(f"    Hit rate: {info.hits / (info.hits + info.misses) * 100:.1f}%")


def recommendation_engine_demo():
    """
    Demonstrate caching in recommendation engine.
    """
    print("\n" + "=" * 70)
    print("PRACTICAL: Recommendation Engine with Caching")
    print("=" * 70)

    recommender = ProductRecommender()

    print("\n[1] First recommendation for 'laptop':")
    start = time()
    results = recommender.recommend("laptop", top_n=3)
    elapsed = (time() - start) * 1000

    print(f"  Time: {elapsed:.2f}ms (includes similarity calculations)")
    for product, similarity in results:
        print(f"    - {product}: {similarity:.2%}")

    print("\n[2] Second recommendation for 'laptop' (should be instant):")
    start = time()
    results = recommender.recommend("laptop", top_n=3)
    elapsed = (time() - start) * 1000

    print(f"  Time: {elapsed:.2f}ms (from cache!)")
    for product, similarity in results:
        print(f"    - {product}: {similarity:.2%}")

    print("\n[3] Recommendation for different product 'book':")
    start = time()
    results = recommender.recommend("book", top_n=3)
    elapsed = (time() - start) * 1000

    print(f"  Time: {elapsed:.2f}ms (new calculations)")
    for product, similarity in results:
        print(f"    - {product}: {similarity:.2%}")

    print("\n[4] Second recommendation for 'book' (from cache):")
    start = time()
    results = recommender.recommend("book", top_n=3)
    elapsed = (time() - start) * 1000

    print(f"  Time: {elapsed:.2f}ms (from cache!)")
    for product, similarity in results:
        print(f"    - {product}: {similarity:.2%}")

    # Show final stats
    recommender.print_cache_stats()

    print("\n💡 Real Netflix/Amazon:")
    print("  - Cache 1M user profiles")
    print("  - Cache product similarities")
    print("  - Save billions of computations daily")


# ============================================================================
# PART 5: WHEN TO USE CACHING
# ============================================================================

def caching_best_practices():
    """
    Explain when and when NOT to use caching.
    """
    print("\n" + "=" * 70)
    print("WHEN TO USE @lru_cache")
    print("=" * 70)

    print("\n✓ GOOD CANDIDATES FOR CACHING:")
    print("  1. Pure functions (same input → same output)")
    print("     Example: fibonacci(n), sqrt(x), similarity(a, b)")
    print("")
    print("  2. Expensive computations")
    print("     Example: ML predictions, complex calculations")
    print("")
    print("  3. Repeated calls with same arguments")
    print("     Example: recommendations for same user")
    print("")
    print("  4. Deterministic (no side effects)")
    print("     Example: NOT file I/O, NOT random numbers")

    print("\n✗ BAD CANDIDATES FOR CACHING:")
    print("  1. Functions with side effects")
    print("     Bad: send_email(), write_file(), print()")
    print("     Why: calling once vs calling from cache = different!")
    print("")
    print("  2. Non-deterministic functions")
    print("     Bad: random.random(), datetime.now()")
    print("     Why: same args → different results → cache wrong!")
    print("")
    print("  3. Functions with mutable arguments")
    print("     Bad: modify lists, dicts passed as arguments")
    print("     Why: unhashable types can't be cache keys")
    print("")
    print("  4. Frequently changing data")
    print("     Bad: caching current stock prices")
    print("     Why: cached values become outdated")

    print("\n📊 CACHE SIZING:")
    print("  maxsize=128   ← Default, good for most cases")
    print("  maxsize=1000  ← More memory, larger hit rate")
    print("  maxsize=32    ← Less memory, smaller hit rate")
    print("")
    print("  Tip: Monitor cache_info() to optimize maxsize")

    print("\n🎯 REAL-WORLD CACHING STRATEGIES:")
    print("  Tier 1: @lru_cache (in-process, <0.1ms)")
    print("  Tier 2: Redis (distributed, 1-5ms)")
    print("  Tier 3: Database (persistent, 50-100ms)")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def run_demo():
    """Run all caching demonstrations."""
    print("\n" + "=" * 70)
    print("BEGINNER EDITION - LESSON 4: @lru_cache")
    print("=" * 70)

    demonstrate_fibonacci_problem()
    demonstrate_cache_solution()
    lru_cache_mechanics()
    recommendation_engine_demo()
    caching_best_practices()


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM LESSON 4:
============================

1. @lru_cache = Remember function results:
   @lru_cache(maxsize=128)
   def expensive_function(x):
       return complex_calculation(x)

2. Performance impact:
   fib(30) without cache: 130ms
   fib(30) with cache:    0.00002ms
   Speedup: 6,500,000x

3. How it works:
   Call 1: Calculate, store in cache
   Call 2: Same args → return cached result (instant!)
   When full: Remove least recently used item

4. Requirements for caching:
   ✓ Pure function (same input = same output)
   ✓ Deterministic (no randomness)
   ✓ Expensive computation
   ✓ Hashable arguments (can be dict keys)
   ✗ Side effects (printing, file I/O)
   ✗ Mutable arguments

5. Monitoring cache:
   cache_info() → shows hits, misses, hit rate
   cache_clear() → clears cache (when data changes)

REAL-WORLD IMPACT:
==================
- Netflix: Caches user preferences (save 10,000+ seconds daily)
- Google: Caches search results (same queries repeat 30% of time)
- PayPal: Caches ML fraud detection models
- Amazon: Caches product recommendations

NEXT STEP:
==========
Learn OOP (classes, inheritance, composition)
Combine functional programming (decorators, generators) with OOP
"""

if __name__ == "__main__":
    run_demo()
