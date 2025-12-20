"""
BEGINNER EDITION: Lesson 2 - Generators for Efficient Data Processing
======================================================================

PROBLEM:
--------
Loading entire files into memory fails for big data:
- 1 billion rows × 1KB per row = 1 million MB (1 TB!) of RAM
- Most computers have 8-16 GB RAM max
- Reading all at once = app crashes

SOLUTION:
---------
Use Generators: Process data in chunks, keep only current chunk in memory.
Think: "Lazy evaluation" - compute only what you need.

WHY IT MATTERS:
---------------
- YouTube streams billions of videos (not downloaded all at once)
- Netflix processes user logs without loading all to RAM
- Data science pipelines handle terabytes of data
- Real-time analytics process streams

This lesson shows:
1. Memory comparison: list vs generator
2. What yield does in generators
3. Processing CSV with generator
4. Chaining generators for pipelines
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Generator, List, Tuple
from decimal import Decimal
from config import CSV_PROCESSING_CONFIG, LOGGING_CONFIG


# ============================================================================
# PART 1: MEMORY COMPARISON - LIST VS GENERATOR
# ============================================================================

def create_sample_csv():
    """
    Create a sample CSV file for demonstration.

    In real world, this would be millions of rows.
    """
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    csv_file = data_dir / "sample_transactions.csv"

    # Create sample transaction data
    categories = ["groceries", "utilities", "entertainment", "transport", "healthcare"]
    types = ["purchase", "refund", "withdrawal"]

    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["date", "type", "amount", "category", "description"]
        )
        writer.writeheader()

        # Generate 10,000 sample transactions
        start_date = datetime(2024, 1, 1)
        for i in range(10000):
            date = start_date + timedelta(hours=i)
            writer.writerow({
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": random.choice(types),
                "amount": round(random.uniform(1, 500), 2),
                "category": random.choice(categories),
                "description": f"Transaction {i}",
            })

    return csv_file


def demonstrate_list_memory():
    """
    Show memory usage when loading entire file into list.
    (We'll simulate with smaller data for demo)
    """
    print("\n" + "=" * 70)
    print("MEMORY USAGE: List (load all at once)")
    print("=" * 70)

    csv_file = create_sample_csv()

    # Load all into list
    print(f"\n⚠️  Loading all {10_000:,} rows into memory...")
    rows = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)  # ← ALL IN MEMORY NOW

    print(f"Loaded: {len(rows):,} rows")
    print(f"Approx memory: {len(rows) * 500 / (1024**2):.2f} MB")  # ~500 bytes per row
    print(f"Problem: If 1 billion rows, need 500+ GB RAM! ❌")

    # To use this data, we'd do:
    print(f"\nTo sum amounts:")
    total = sum(Decimal(row["amount"]) for row in rows)
    print(f"  Total: ${total:.2f}")


def demonstrate_generator_memory():
    """
    Show memory usage with generator (process chunk by chunk).
    """
    print("\n" + "=" * 70)
    print("MEMORY USAGE: Generator (lazy evaluation)")
    print("=" * 70)

    csv_file = Path(__file__).parent / "data" / "sample_transactions.csv"

    def read_csv_generator(filepath: Path) -> Generator[dict, None, None]:
        """
        Generator function to read CSV row by row.

        Key: Uses 'yield' instead of 'return'
        - yield: gives control back to caller, remembers state
        - Only keeps 1 row in memory at a time
        """
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row  # ← Pause here, give row to caller

    print(f"\n✓ Processing {10_000:,} rows with generator...")
    print(f"Memory usage: ~1 KB (just 1 row at a time)")
    print(f"Works with 1 billion rows! ✓")

    # To use generator:
    print(f"\nTo sum amounts:")
    total = Decimal("0")
    for row in read_csv_generator(csv_file):
        total += Decimal(row["amount"])

    print(f"  Total: ${total:.2f}")
    print(f"  ✓ Only 1 row in memory at a time!")


# ============================================================================
# PART 2: UNDERSTANDING YIELD
# ============================================================================

def simple_generator_demo():
    """
    Show how yield works step by step.

    The key: yield pauses the function and returns a value.
    The next time you ask for a value, it resumes from where it left off.
    """
    print("\n" + "=" * 70)
    print("HOW YIELD WORKS")
    print("=" * 70)

    def count_up_to(n: int) -> Generator[int, None, None]:
        """
        Generator that counts from 0 to n.

        Without yield (return all): wasteful
        With yield (one at a time): efficient
        """
        print("\n>>> count_up_to(5) called")
        for i in range(n):
            print(f"    >>> About to yield {i}")
            yield i  # ← Pause here. Caller gets i, function sleeps.
            print(f"    >>> Resumed after yielding {i}")

    print("\nCalling generator...")
    gen = count_up_to(3)  # ← Create generator (doesn't execute yet!)

    print(f"Type: {type(gen)}")
    print(f"Generator is lazy: {gen}")

    print("\n--- Calling next() three times ---")
    print(f"next(gen) = {next(gen)}")  # Execute until first yield
    print(f"next(gen) = {next(gen)}")  # Resume, execute until next yield
    print(f"next(gen) = {next(gen)}")  # Resume, execute until next yield

    print("\nUsing in for loop:")
    gen = count_up_to(3)
    for value in gen:
        print(f"  Got: {value}")


# ============================================================================
# PART 3: PROCESSING CSV WITH GENERATORS
# ============================================================================

def filter_by_category(
    csv_gen: Generator, category: str
) -> Generator[dict, None, None]:
    """
    Filter transactions by category.

    Args:
        csv_gen: Generator yielding transaction dicts
        category: Which category to keep

    Yields:
        Only rows matching the category
    """
    for row in csv_gen:
        if row["category"] == category:
            yield row


def aggregate_by_category(
    csv_gen: Generator,
) -> Generator[Tuple[str, Decimal, int], None, None]:
    """
    Aggregate transactions by category (sum and count).

    Yields:
        (category, total_amount, count) tuples
    """
    categories = {}

    for row in csv_gen:
        cat = row["category"]
        amount = Decimal(row["amount"])

        if cat not in categories:
            categories[cat] = {"total": Decimal("0"), "count": 0}

        categories[cat]["total"] += amount
        categories[cat]["count"] += 1

    # Yield results
    for cat, data in sorted(categories.items()):
        yield (cat, data["total"], data["count"])


def read_csv_generator(filepath: Path) -> Generator[dict, None, None]:
    """Read CSV file row by row."""
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def csv_processing_demo():
    """
    Demonstrate practical CSV processing with generators.
    """
    print("\n" + "=" * 70)
    print("PRACTICAL: CSV Processing Pipeline")
    print("=" * 70)

    csv_file = Path(__file__).parent / "data" / "sample_transactions.csv"

    # Pipeline 1: Read all and sum
    print("\n[1] Reading CSV and calculating statistics...")
    total_amount = Decimal("0")
    total_rows = 0

    for row in read_csv_generator(csv_file):
        total_amount += Decimal(row["amount"])
        total_rows += 1

    print(f"  Total transactions: {total_rows:,}")
    print(f"  Total amount: ${total_amount:.2f}")
    print(f"  Average: ${total_amount / total_rows:.2f}")

    # Pipeline 2: Filter by category
    print("\n[2] Finding all 'groceries' transactions...")
    groceries = list(filter_by_category(read_csv_generator(csv_file), "groceries"))
    print(f"  Found {len(groceries)} groceries transactions")
    if groceries:
        print(f"  First: {groceries[0]}")

    # Pipeline 3: Aggregate by category
    print("\n[3] Summary by category...")
    print(f"  {'Category':<15} {'Total':>12} {'Count':>8} {'Average':>12}")
    print(f"  {'-'*15} {'-'*12} {'-'*8} {'-'*12}")

    for category, total, count in aggregate_by_category(read_csv_generator(csv_file)):
        avg = total / count
        print(f"  {category:<15} ${total:>10.2f} {count:>8} ${avg:>10.2f}")


# ============================================================================
# PART 4: CHAINING GENERATORS
# ============================================================================

def generator_chaining_demo():
    """
    Show how generators can be chained together.

    Each generator does one thing, pass output to next.
    This is functional programming! (next lesson)
    """
    print("\n" + "=" * 70)
    print("ADVANCED: Chaining Generators (Pipeline)")
    print("=" * 70)

    csv_file = Path(__file__).parent / "data" / "sample_transactions.csv"

    def read_csv(filepath):
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def filter_category(gen, category):
        """Keep only specific category."""
        for row in gen:
            if row["category"] == category:
                yield row

    def filter_type(gen, transaction_type):
        """Keep only specific type."""
        for row in gen:
            if row["type"] == transaction_type:
                yield row

    def map_to_amount(gen):
        """Transform to just amounts."""
        for row in gen:
            yield Decimal(row["amount"])

    # Chain them together
    print("\nFinding all 'groceries' PURCHASES:")
    pipeline = read_csv(csv_file)
    pipeline = filter_category(pipeline, "groceries")
    pipeline = filter_type(pipeline, "purchase")
    pipeline = map_to_amount(pipeline)

    # Process results
    total = Decimal("0")
    count = 0
    for amount in pipeline:
        total += amount
        count += 1

    print(f"  Count: {count}")
    print(f"  Total: ${total:.2f}")
    avg = total / count if count > 0 else Decimal("0")
    print(f"  Average: ${avg:.2f}")

    print("\n💡 Pipeline explanation:")
    print("  1. read_csv: Generate all rows")
    print("  2. filter_category: Keep only 'groceries'")
    print("  3. filter_type: Keep only 'purchase' type")
    print("  4. map_to_amount: Transform to decimal amounts")
    print("  5. for loop: Consume results, calculate sum")
    print("\n  Each step is separate, reusable, memory efficient!")


# ============================================================================
# PART 5: STREAMING ANALYSIS
# ============================================================================

def streaming_statistics_demo():
    """
    Demonstrate streaming analysis (online algorithm).

    Calculate mean and variance without loading all data.
    Uses Welford's online algorithm.
    """
    print("\n" + "=" * 70)
    print("STREAMING ANALYSIS: Calculate stats without loading all data")
    print("=" * 70)

    csv_file = Path(__file__).parent / "data" / "sample_transactions.csv"

    # Welford's online algorithm for mean/variance
    n = 0
    mean = Decimal("0")
    m2 = Decimal("0")  # For variance calculation

    for row in read_csv_generator(csv_file):
        amount = Decimal(row["amount"])

        # Update statistics
        n += 1
        delta = amount - mean
        mean += delta / n
        delta2 = amount - mean
        m2 += delta * delta2

    variance = m2 / n if n > 0 else Decimal("0")
    std_dev = variance.sqrt()

    print(f"\nStatistics (calculated streaming, never loaded all data):")
    print(f"  Count: {n:,}")
    print(f"  Mean: ${mean:.2f}")
    print(f"  Variance: {variance:.4f}")
    print(f"  Std Dev: {std_dev:.2f}")
    print(f"\n✓ Worked with {n:,} rows, only 1 in memory!")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def run_demo():
    """Run all generator demonstrations."""
    print("\n" + "=" * 70)
    print("BEGINNER EDITION - LESSON 2: GENERATORS")
    print("=" * 70)

    # Create sample data
    print("\n[Setup] Creating sample CSV with 10,000 transactions...")
    create_sample_csv()

    # Memory comparison
    demonstrate_list_memory()
    demonstrate_generator_memory()

    # How yield works
    simple_generator_demo()

    # Practical CSV processing
    csv_processing_demo()

    # Chaining generators
    generator_chaining_demo()

    # Streaming analysis
    streaming_statistics_demo()


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM LESSON 2:
============================

1. Generators are LAZY:
   - Don't execute until you ask for value
   - Use 'yield' instead of 'return'
   - Only keep 1 item in memory at a time

2. When to use generators:
   ✓ Large files (millions of rows)
   ✓ Streams (unlimited data)
   ✓ Real-time processing
   ✓ Data pipelines
   ✗ Need random access (use list)
   ✗ Small data (overhead not worth it)

3. Memory comparison:
   List:      1M rows × 1KB = 1 GB RAM
   Generator: 1M rows = 1 KB RAM  ← 1,000x less!

4. Pipeline pattern:
   read() → filter() → transform() → aggregate()
   Each is a separate generator, chainable, testable

5. Using generators:
   - for value in generator: ← most common
   - next(generator) ← manual control
   - list(generator) ← convert to list (use carefully!)

REAL-WORLD IMPACT:
==================
- YouTube: Streams videos (not downloaded all at once)
- Netflix: Processes logs for recommendations
- Twitter: Handles real-time tweets
- Healthcare: Analyzes patient data streams

NEXT STEP:
==========
Learn map/filter/lambda to transform data more elegantly.
Generators handle volume, map/filter handle transformation.
"""

if __name__ == "__main__":
    run_demo()
