"""
BEGINNER EDITION: Lesson 3 - map/filter/lambda for Data Transformation
=======================================================================

PROBLEM:
--------
Data cleaning requires many loops and temporary variables.
Manual loops are verbose, hard to understand, and error-prone.

SOLUTION:
---------
Use functional transformations:
- map(): Transform each item
- filter(): Keep only matching items
- lambda: Quick anonymous functions for simple operations

WHY IT MATTERS:
---------------
- Data science: 80% of work is cleaning dirty data
- Every company has messy data
- Functional approach = cleaner, composable, testable code
- Better performance (optimized internally)

This lesson shows:
1. The problem with manual loops
2. How map() transforms data
3. How filter() selects data
4. Using lambda for quick functions
5. Composing transformations together
"""

import re
from decimal import Decimal
from typing import List, Callable, Generator
from datetime import datetime
from config import DATA_CLEANING_CONFIG, LOGGING_CONFIG


# ============================================================================
# PART 1: THE PROBLEM - MANUAL LOOPS
# ============================================================================

class DirtyDataExample:
    """
    Real-world messy data (from web scraping, user input, logs, etc).
    """

    # Sample dirty data
    raw_data = [
        {"date": "2024-01-15", "type": "PURCHASE", "amount": " 45.99 ", "category": "Groceries", "notes": ""},
        {"date": "2024-01-16", "type": "refund", "amount": "-25.50", "category": "groceries", "notes": None},
        {"date": "2024-01-17", "type": "purchase", "amount": "invalid", "category": "ENTERTAINMENT", "notes": "Movie"},
        {"date": "2024-01-18", "type": "withdrawal", "amount": "100.00", "category": "", "notes": "ATM"},
        {"date": "invalid-date", "type": "DEPOSIT", "amount": "500.00", "category": "salary", "notes": "Paycheck"},
        {"date": "2024-01-20", "type": "transfer", "amount": "0.00", "category": "other", "notes": ""},
        {"date": "2024-01-21", "type": "purchase", "amount": "75.25", "category": "unknown_category", "notes": ""},
    ]

    VALID_TYPES = ["purchase", "refund", "withdrawal", "deposit", "transfer"]
    VALID_CATEGORIES = ["groceries", "utilities", "entertainment", "transport", "healthcare", "salary", "other"]


def demonstrate_manual_loop():
    """
    Show the painful way: manual loops with lots of code.

    This is what most beginners write, and it's hard to read.
    """
    print("\n" + "=" * 70)
    print("PROBLEM: Manual Data Cleaning (Verbose and Hard to Understand)")
    print("=" * 70)

    data = DirtyDataExample.raw_data
    cleaned = []

    print("\n❌ Imperative (manual loops):")
    print("""
    cleaned = []
    for row in data:
        # Type validation
        if row["type"].lower() not in VALID_TYPES:
            continue

        # Amount validation
        try:
            amount = Decimal(row["amount"].strip())
            if amount < 0 or amount > 1000000:
                continue
        except:
            continue

        # Category validation
        category = row["category"].lower()
        if category not in VALID_CATEGORIES:
            continue

        # Date validation
        try:
            date = datetime.strptime(row["date"], "%Y-%m-%d")
        except:
            continue

        # Build cleaned record
        cleaned_row = {
            "date": date,
            "type": row["type"].lower(),
            "amount": amount,
            "category": category,
            "notes": row.get("notes", "") or "",
        }
        cleaned.append(cleaned_row)
    """)

    # Actually do it
    for row in data:
        try:
            # Type validation
            if row["type"].lower() not in DirtyDataExample.VALID_TYPES:
                continue

            # Amount validation
            try:
                amount = Decimal(row["amount"].strip())
                if amount <= 0 or amount > Decimal("1000000"):
                    continue
            except:
                continue

            # Category validation
            category = row["category"].lower()
            if category not in DirtyDataExample.VALID_CATEGORIES:
                continue

            # Date validation
            try:
                date = datetime.strptime(row["date"], "%Y-%m-%d")
            except:
                continue

            # Build cleaned record
            cleaned_row = {
                "date": date,
                "type": row["type"].lower(),
                "amount": amount,
                "category": category,
                "notes": row.get("notes", "") or "",
            }
            cleaned.append(cleaned_row)
        except:
            pass

    print(f"\nResult: {len(cleaned)} valid records from {len(data)} raw")
    for record in cleaned:
        print(f"  {record['date'].date()} | {record['type']:10} | ${record['amount']:>8.2f} | {record['category']}")


# ============================================================================
# PART 2: DECLARATIVE APPROACH WITH map/filter
# ============================================================================

def map_demo():
    """
    Show map(): Transform each element.

    map(function, iterable) → apply function to each item
    """
    print("\n" + "=" * 70)
    print("SOLUTION 1: map() - Transform Each Element")
    print("=" * 70)

    # Simple example
    print("\n[1] Simple transformation with map():")
    numbers = [1, 2, 3, 4, 5]

    print(f"\nSquare numbers:")
    print(f"  Imperative: squared = [x**2 for x in numbers]")
    squared_imperative = [x**2 for x in numbers]
    print(f"  Result: {squared_imperative}")

    print(f"\n  Functional: squared = map(lambda x: x**2, numbers)")
    squared_functional = list(map(lambda x: x**2, numbers))
    print(f"  Result: {squared_functional}")

    # Data cleaning example
    print("\n[2] Normalize data with map():")
    raw_amounts = [" 45.99 ", "-25.50", "100.00"]

    print(f"\nClean whitespace and convert to Decimal:")
    print(f"  amounts = map(lambda s: Decimal(s.strip()), raw_amounts)")

    amounts = list(map(lambda s: Decimal(s.strip()), raw_amounts))
    for original, cleaned in zip(raw_amounts, amounts):
        print(f"  '{original}' → {cleaned}")

    # Using named function
    print("\n[3] Using named function with map():")

    def normalize_type(type_str: str) -> str:
        """Convert type to lowercase."""
        return type_str.lower()

    types = ["PURCHASE", "Refund", "WITHDRAWAL"]
    print(f"  types = {types}")
    print(f"  normalized = map(normalize_type, types)")
    normalized = list(map(normalize_type, types))
    print(f"  Result: {normalized}")


def filter_demo():
    """
    Show filter(): Keep only matching elements.

    filter(predicate, iterable) → keep items where predicate(item) is True
    """
    print("\n" + "=" * 70)
    print("SOLUTION 2: filter() - Keep Only Matching Items")
    print("=" * 70)

    # Simple example
    print("\n[1] Simple filtering with filter():")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print(f"\nKeep only even numbers:")
    print(f"  Imperative: evens = [x for x in numbers if x % 2 == 0]")
    evens_imperative = [x for x in numbers if x % 2 == 0]
    print(f"  Result: {evens_imperative}")

    print(f"\n  Functional: evens = filter(lambda x: x % 2 == 0, numbers)")
    evens_functional = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"  Result: {evens_functional}")

    # Data validation
    print("\n[2] Validate data with filter():")

    def is_valid_amount(amount_str: str) -> bool:
        """Check if amount string is valid decimal."""
        try:
            amount = Decimal(amount_str.strip())
            return Decimal("0") < amount <= Decimal("1000000")
        except:
            return False

    amounts = [" 45.99 ", "invalid", "-25.50", "100.00", "0.00"]
    print(f"  amounts = {amounts}")
    print(f"  valid = filter(is_valid_amount, amounts)")

    valid_amounts = list(filter(is_valid_amount, amounts))
    print(f"  Valid: {valid_amounts}")

    # Using lambda
    print("\n[3] Complex filtering with lambda:")
    transactions = [
        {"type": "purchase", "amount": 45.99, "category": "groceries"},
        {"type": "refund", "amount": 25.50, "category": "groceries"},
        {"type": "purchase", "amount": 5.00, "category": "transport"},
        {"type": "withdrawal", "amount": 100.00, "category": "other"},
    ]

    print(f"\nKeep only purchases over $20:")
    print(f"  result = filter(lambda t: t['type']=='purchase' and t['amount']>20, txns)")

    large_purchases = list(filter(
        lambda t: t["type"] == "purchase" and t["amount"] > 20,
        transactions
    ))

    for txn in large_purchases:
        print(f"  {txn['type']} - ${txn['amount']:.2f} ({txn['category']})")


def lambda_demo():
    """
    Show lambda: Anonymous functions for quick operations.

    lambda args: expression
    """
    print("\n" + "=" * 70)
    print("SOLUTION 3: lambda - Anonymous Quick Functions")
    print("=" * 70)

    print("\n[1] Why lambda?")
    print("\nWithout lambda (need to define function):")
    print("""
    def add(a, b):
        return a + b

    result = map(add, [1, 2, 3], [10, 20, 30])
    """)

    print("\nWith lambda (inline, concise):")
    print("""
    result = map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])
    """)

    # Examples
    print("\n[2] Lambda examples:")

    # Single argument
    print("\n  Square: lambda x: x**2")
    square = lambda x: x**2
    print(f"    square(5) = {square(5)}")

    # Multiple arguments
    print("\n  Add: lambda a, b: a + b")
    add = lambda a, b: a + b
    print(f"    add(3, 7) = {add(3, 7)}")

    # With dict
    print("\n  Get amount: lambda t: t['amount']")
    get_amount = lambda t: t["amount"]
    txn = {"type": "purchase", "amount": 50.00}
    print(f"    get_amount(txn) = {get_amount(txn)}")

    # Conditional
    print("\n  Is positive: lambda x: x > 0")
    is_positive = lambda x: x > 0
    print(f"    is_positive(5) = {is_positive(5)}")
    print(f"    is_positive(-3) = {is_positive(-3)}")

    print("\n[3] When to use lambda:")
    print("  ✓ Simple functions (1-2 lines)")
    print("  ✓ Used only once")
    print("  ✓ Callbacks for map/filter/sorted")
    print("  ✗ Complex logic (use def)")
    print("  ✗ Reused multiple times (use def)")


# ============================================================================
# PART 3: PRACTICAL DATA CLEANING WITH map/filter
# ============================================================================

def practical_data_cleaning():
    """
    Clean dirty data using functional approach.

    Step 1: Define validation functions
    Step 2: Chain map/filter operations
    Step 3: Result is clean data
    """
    print("\n" + "=" * 70)
    print("PRACTICAL: Clean Messy Data with map/filter")
    print("=" * 70)

    data = DirtyDataExample.raw_data

    print(f"\n[Input] {len(data)} raw records with various issues")
    print("  - Wrong case (UPPERCASE, MixedCase)")
    print("  - Whitespace in amounts")
    print("  - Invalid amounts (negative, zero, non-numeric)")
    print("  - Invalid categories")
    print("  - Invalid dates")
    print("  - Empty notes")

    # Step 1: Type validation and normalization
    print(f"\n[Step 1] Filter by type and normalize...")

    def is_valid_type(row):
        return row["type"].lower() in DirtyDataExample.VALID_TYPES

    def normalize_type(row):
        row["type"] = row["type"].lower()
        return row

    data = list(filter(is_valid_type, data))
    data = list(map(normalize_type, data))
    print(f"  After filtering: {len(data)} records")

    # Step 2: Amount validation
    print(f"\n[Step 2] Validate and normalize amounts...")

    def is_valid_amount(row):
        try:
            amount = Decimal(row["amount"].strip())
            return Decimal("0") < amount <= Decimal("1000000")
        except:
            return False

    def convert_amount(row):
        row["amount"] = Decimal(row["amount"].strip())
        return row

    data = list(filter(is_valid_amount, data))
    data = list(map(convert_amount, data))
    print(f"  After filtering: {len(data)} records")

    # Step 3: Category validation and normalization
    print(f"\n[Step 3] Validate and normalize categories...")

    def is_valid_category(row):
        return row["category"].lower() in DirtyDataExample.VALID_CATEGORIES

    def normalize_category(row):
        row["category"] = row["category"].lower()
        return row

    data = list(filter(is_valid_category, data))
    data = list(map(normalize_category, data))
    print(f"  After filtering: {len(data)} records")

    # Step 4: Date validation
    print(f"\n[Step 4] Validate dates...")

    def is_valid_date(row):
        try:
            datetime.strptime(row["date"], "%Y-%m-%d")
            return True
        except:
            return False

    def parse_date(row):
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
        return row

    data = list(filter(is_valid_date, data))
    data = list(map(parse_date, data))
    print(f"  After filtering: {len(data)} records")

    # Step 5: Clean notes
    print(f"\n[Step 5] Clean notes field...")

    def clean_notes(row):
        row["notes"] = (row.get("notes") or "").strip()
        return row

    data = list(map(clean_notes, data))

    # Show results
    print(f"\n[Output] {len(data)} clean records")
    print(f"  {'Date':<12} {'Type':<12} {'Amount':>10} {'Category':<15} {'Notes'}")
    print(f"  {'-'*12} {'-'*12} {'-'*10} {'-'*15} {'---'}")

    for record in data:
        date_str = record["date"].strftime("%Y-%m-%d")
        print(
            f"  {date_str:<12} {record['type']:<12} "
            f"${record['amount']:>8.2f} {record['category']:<15} {record['notes']}"
        )


# ============================================================================
# PART 4: COMPOSING TRANSFORMATIONS
# ============================================================================

def composition_demo():
    """
    Show how to compose multiple transformations.

    This is the power of functional programming:
    Chain operations together, each doing one thing well.
    """
    print("\n" + "=" * 70)
    print("COMPOSITION: Chain Transformations Together")
    print("=" * 70)

    words = ["apple", "pie", "python", "ai", "excellence"]

    print(f"\n[Input] {words}")

    # Method 1: Multiple loops (imperative)
    print(f"\n[Method 1] Multiple loops (hard to follow):")
    print("""
    # Filter words > 3 chars
    long_words = [w for w in words if len(w) > 3]
    # Uppercase
    uppered = [w.upper() for w in long_words]
    # Add length
    with_len = [(w, len(w)) for w in uppered]
    """)

    long_words = [w for w in words if len(w) > 3]
    uppered = [w.upper() for w in long_words]
    with_len = [(w, len(w)) for w in uppered]

    print(f"  Result: {with_len}")

    # Method 2: Composition (functional, chainable)
    print(f"\n[Method 2] Composition (clean and readable):")
    print("""
    result = (
        words
        |> filter(len > 3)      # Keep long words
        |> map(str.upper)       # Uppercase
        |> map(lambda w: (w, len(w)))  # Add length
    )
    """)

    print(f"  Python equivalent:")
    result = list(map(
        lambda w: (w, len(w)),
        map(str.upper, filter(lambda w: len(w) > 3, words))
    ))
    print(f"  Result: {result}")

    print(f"\n[Method 3] Using list comprehension (Pythonic):")
    result = [(w.upper(), len(w)) for w in words if len(w) > 3]
    print(f"  Result: {result}")

    print(f"\n💡 All three methods work! Python developers often prefer list comprehensions.")
    print(f"   But understanding map/filter helps you code in other languages (JavaScript, etc)")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def run_demo():
    """Run all data transformation demonstrations."""
    print("\n" + "=" * 70)
    print("BEGINNER EDITION - LESSON 3: map/filter/lambda")
    print("=" * 70)

    demonstrate_manual_loop()
    map_demo()
    filter_demo()
    lambda_demo()
    practical_data_cleaning()
    composition_demo()


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM LESSON 3:
============================

1. map() transforms each element:
   - Apply function to each item
   - Returns transformed items in same order
   - Lazy (doesn't execute immediately)

2. filter() selects matching elements:
   - Keep items where predicate(item) is True
   - Remove everything else
   - Lazy (doesn't execute immediately)

3. lambda defines quick anonymous functions:
   - One-liner functions
   - Used for map/filter callbacks
   - More readable than 5-line def

4. When to use functional vs imperative:
   ✓ Functional:
     - Data transformation pipelines
     - Composing operations
     - Functional languages (Haskell, Lisp)
   ✓ Imperative:
     - Complex control flow
     - Multiple branches
     - Mutating state

5. Python style (Pythonic):
   List comprehensions are preferred:
     [x**2 for x in numbers]  ← better than map
     [x for x in numbers if x > 0]  ← better than filter

   But understanding map/filter helps you:
   - Code in other languages
   - Understand functional programming
   - Optimize performance (lazy evaluation)

REAL-WORLD IMPACT:
==================
- Data Science: pandas uses map/filter internally
- Web Dev: JavaScript uses map/filter on arrays
- Data cleaning: 80% of data science work
- ETL pipelines: Transform terabytes of data

NEXT STEP:
==========
Learn @lru_cache to speed up functions 10,000x
Functional transformations + memoization = powerful optimization
"""

if __name__ == "__main__":
    run_demo()
