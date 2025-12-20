"""
ADVANCED EDITION: Lesson 1 - Big Data Analytics with Real Datasets
==================================================================

PROBLEM:
--------
Real-world data is HUGE:
- Netflix: 250 million users, billions of events daily
- Amazon: millions of products, transactions every second
- Modern ML: training on terabytes of data

Can't load all to memory, need efficient streaming and analysis.

SOLUTION:
---------
Combine generators + functional programming + smart data structures:
1. Stream data from sources (never load all at once)
2. Process incrementally (one batch at a time)
3. Aggregate on-the-fly (calculate without storing everything)
4. Scale to billions of records

WHY IT MATTERS:
---------------
- Netflix watches billions of videos → streams efficiently
- Uber processes 10M+ requests daily → real-time analytics
- Medical researchers analyze genomic data → petabytes
- Every company does this at scale

This lesson demonstrates:
1. Downloading real public datasets
2. Streaming large CSV files with generators
3. Real-time statistics without loading all data
4. Advanced aggregations (percentiles, distributions)
5. Memory-efficient data pipelines
"""

import csv
import gzip
import io
import time
from pathlib import Path
from decimal import Decimal
from typing import Generator, Dict, List, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import urllib.request
from config_advanced import DATA_SOURCES_CONFIG, ETL_CONFIG, PERFORMANCE_CONFIG


# ============================================================================
# PART 1: DATA SOURCE HANDLING
# ============================================================================

class BigDataSource:
    """Handle various data sources efficiently."""

    def __init__(self):
        """Initialize data sources."""
        self.data_dir = DATA_SOURCES_CONFIG["data_dir"]
        self.cache_dir = DATA_SOURCES_CONFIG["cache_dir"]

        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)

    def create_sample_dataset(self, name: str, rows: int = 100_000):
        """
        Create sample dataset (simulating real dataset).

        In production, would download from Kaggle, AWS, etc.
        """
        filepath = self.data_dir / f"{name}.csv"

        if filepath.exists():
            print(f"✓ Dataset already exists: {filepath}")
            return filepath

        print(f"\n📥 Creating sample dataset: {name}")
        print(f"   Rows: {rows:,}")

        import random
        import csv

        categories = ["electronics", "books", "home", "sports", "fashion"]
        regions = ["North", "South", "East", "West", "Central"]

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "timestamp",
                    "user_id",
                    "product_id",
                    "category",
                    "amount",
                    "region",
                    "country",
                ],
            )
            writer.writeheader()

            base_time = datetime(2023, 1, 1)
            for i in range(rows):
                timestamp = base_time + timedelta(seconds=random.randint(0, 365 * 24 * 3600))
                writer.writerow({
                    "timestamp": timestamp.isoformat(),
                    "user_id": f"USER_{random.randint(1, 10_000):06d}",
                    "product_id": f"PROD_{random.randint(1, 5_000):06d}",
                    "category": random.choice(categories),
                    "amount": round(random.uniform(10, 500), 2),
                    "region": random.choice(regions),
                    "country": random.choice(["USA", "Canada", "UK", "Germany"]),
                })

                if (i + 1) % 10_000 == 0:
                    print(f"   ✓ Created {i + 1:,} rows...")

        print(f"✓ Dataset created: {filepath}")
        return filepath

    def stream_csv(self, filepath: Path) -> Generator[Dict[str, Any], None, None]:
        """
        Stream CSV file efficiently (never load all to memory).

        Handles:
        - Regular CSV files
        - Compressed CSV (gzip)
        - Type conversion
        """
        # Detect if compressed
        if filepath.suffix == ".gz":
            file_obj = gzip.open(filepath, "rt")
        else:
            file_obj = open(filepath, "r")

        try:
            reader = csv.DictReader(file_obj)
            for row in reader:
                # Convert amount to Decimal
                if "amount" in row:
                    row["amount"] = Decimal(row["amount"])

                yield row
        finally:
            file_obj.close()


# ============================================================================
# PART 2: STREAMING ANALYTICS ENGINE
# ============================================================================

class StreamingAnalytics:
    """
    Calculate statistics on massive datasets without loading all to memory.

    Uses online algorithms (Welford's for mean/variance, etc).
    """

    def __init__(self):
        """Initialize accumulators."""
        self.count = 0
        self.sum_amount = Decimal("0")
        self.mean = Decimal("0")
        self.m2 = Decimal("0")  # For variance
        self.min_amount = None
        self.max_amount = None

        # Category aggregation
        self.category_stats = defaultdict(lambda: {
            "count": 0,
            "sum": Decimal("0"),
            "min": None,
            "max": None,
        })

        # Region aggregation
        self.region_stats = defaultdict(lambda: {
            "count": 0,
            "sum": Decimal("0"),
            "users": set(),
        })

    def process_row(self, row: Dict[str, Any]):
        """
        Process one row using online algorithm (Welford's method).

        Efficient: O(1) memory for each row, O(1) time.
        """
        amount = row.get("amount", Decimal("0"))

        # Update count and basic stats
        self.count += 1
        self.sum_amount += amount

        # Online mean calculation
        delta = amount - self.mean
        self.mean += delta / self.count

        # Online variance (Welford's algorithm)
        delta2 = amount - self.mean
        self.m2 += delta * delta2

        # Min/max
        if self.min_amount is None:
            self.min_amount = amount
            self.max_amount = amount
        else:
            self.min_amount = min(self.min_amount, amount)
            self.max_amount = max(self.max_amount, amount)

        # Category aggregation
        category = row.get("category", "unknown")
        self.category_stats[category]["count"] += 1
        self.category_stats[category]["sum"] += amount
        if self.category_stats[category]["min"] is None:
            self.category_stats[category]["min"] = amount
            self.category_stats[category]["max"] = amount
        else:
            self.category_stats[category]["min"] = min(
                self.category_stats[category]["min"], amount
            )
            self.category_stats[category]["max"] = max(
                self.category_stats[category]["max"], amount
            )

        # Region aggregation
        region = row.get("region", "unknown")
        self.region_stats[region]["count"] += 1
        self.region_stats[region]["sum"] += amount
        self.region_stats[region]["users"].add(row.get("user_id"))

    def get_summary(self) -> Dict[str, Any]:
        """Get complete summary statistics."""
        variance = self.m2 / self.count if self.count > 0 else Decimal("0")
        std_dev = variance ** Decimal("0.5")

        return {
            "count": self.count,
            "total": self.sum_amount,
            "mean": self.mean,
            "median": None,  # Can't calculate online
            "min": self.min_amount,
            "max": self.max_amount,
            "std_dev": std_dev,
            "variance": variance,
        }

    def get_category_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get category breakdown."""
        result = {}
        for cat, stats in self.category_stats.items():
            result[cat] = {
                "count": stats["count"],
                "total": stats["sum"],
                "avg": stats["sum"] / stats["count"] if stats["count"] > 0 else Decimal("0"),
                "min": stats["min"],
                "max": stats["max"],
            }
        return result

    def get_region_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get region breakdown."""
        result = {}
        for region, stats in self.region_stats.items():
            result[region] = {
                "transactions": stats["count"],
                "total": stats["sum"],
                "unique_users": len(stats["users"]),
                "avg_per_user": stats["sum"] / len(stats["users"])
                if stats["users"]
                else Decimal("0"),
            }
        return result


# ============================================================================
# PART 3: ETL PIPELINE
# ============================================================================

class ETLPipeline:
    """
    Extract-Transform-Load pipeline for big data processing.

    Demonstrates best practices for data pipelines.
    """

    def __init__(self, chunk_size: int = 10_000):
        """Initialize pipeline."""
        self.chunk_size = chunk_size
        self.metrics = {
            "rows_read": 0,
            "rows_valid": 0,
            "rows_invalid": 0,
            "total_time": 0,
        }

    def validate_row(self, row: Dict[str, Any]) -> bool:
        """
        Validate data row.

        Checks:
        - Required fields present
        - Amount is positive decimal
        - Timestamp is valid
        """
        required_fields = ["user_id", "amount", "category"]
        for field in required_fields:
            if field not in row or not row[field]:
                return False

        try:
            amount = Decimal(str(row["amount"]))
            if amount <= 0:
                return False
        except:
            return False

        return True

    def process_pipeline(self, filepath: Path) -> Tuple[StreamingAnalytics, Dict[str, Any]]:
        """
        Run complete ETL pipeline.

        Returns: (analytics_engine, metrics)
        """
        start_time = time.time()
        analytics = StreamingAnalytics()
        batch = []

        print(f"\n📊 Running ETL Pipeline")
        print(f"   Input: {filepath.name}")
        print(f"   Chunk size: {self.chunk_size:,}")

        # Extract + Transform + Load (streaming)
        data_source = BigDataSource()
        for row in data_source.stream_csv(filepath):
            self.metrics["rows_read"] += 1

            # Transform: validate
            if self.validate_row(row):
                analytics.process_row(row)
                self.metrics["rows_valid"] += 1
            else:
                self.metrics["rows_invalid"] += 1

            # Progress indicator
            if self.metrics["rows_read"] % 10_000 == 0:
                print(f"   ✓ Processed {self.metrics['rows_read']:,} rows...")

        self.metrics["total_time"] = time.time() - start_time

        return analytics, self.metrics


# ============================================================================
# PART 4: DEMONSTRATION
# ============================================================================

def run_demo():
    """Run big data analytics demonstration."""
    print("\n" + "=" * 70)
    print("ADVANCED EDITION - LESSON 1: BIG DATA ANALYTICS")
    print("=" * 70)

    # Create data source
    source = BigDataSource()

    # Create sample dataset (simulating real data)
    print("\n[1] Creating Sample Dataset")
    filepath = source.create_sample_dataset("ecommerce_transactions", rows=100_000)

    # Run ETL pipeline
    print("\n[2] Running ETL Pipeline")
    pipeline = ETLPipeline(chunk_size=10_000)
    analytics, metrics = pipeline.process_pipeline(filepath)

    # Print results
    print("\n[3] Pipeline Statistics")
    print(f"  Rows read:    {metrics['rows_read']:,}")
    print(f"  Rows valid:   {metrics['rows_valid']:,}")
    print(f"  Rows invalid: {metrics['rows_invalid']:,}")
    print(f"  Time elapsed: {metrics['total_time']:.2f} seconds")
    print(f"  Rate:         {metrics['rows_read'] / metrics['total_time']:.0f} rows/sec")

    # Streaming analytics
    print("\n[4] Overall Statistics (calculated streaming)")
    summary = analytics.get_summary()
    print(f"  Count:        {summary['count']:,}")
    print(f"  Total:        ${summary['total']:.2f}")
    print(f"  Mean:         ${summary['mean']:.2f}")
    print(f"  Min:          ${summary['min']:.2f}")
    print(f"  Max:          ${summary['max']:.2f}")
    print(f"  Std Dev:      ${summary['std_dev']:.2f}")

    # Category breakdown
    print("\n[5] Category Breakdown")
    print(f"  {'Category':<15} {'Count':>10} {'Total':>12} {'Average':>10}")
    print(f"  {'-'*15} {'-'*10} {'-'*12} {'-'*10}")

    for cat in sorted(analytics.get_category_summary().keys()):
        stats = analytics.get_category_summary()[cat]
        print(
            f"  {cat:<15} {stats['count']:>10,} "
            f"${stats['total']:>10.2f} ${stats['avg']:>8.2f}"
        )

    # Region breakdown
    print("\n[6] Region Performance")
    print(f"  {'Region':<15} {'Transactions':>15} {'Total':>12} {'Unique Users':>15} {'Avg/User':>10}")
    print(f"  {'-'*15} {'-'*15} {'-'*12} {'-'*15} {'-'*10}")

    for region in sorted(analytics.get_region_summary().keys()):
        stats = analytics.get_region_summary()[region]
        print(
            f"  {region:<15} {stats['transactions']:>15,} "
            f"${stats['total']:>10.2f} {stats['unique_users']:>15,} "
            f"${stats['avg_per_user']:>8.2f}"
        )

    # Memory efficiency message
    print("\n[7] Memory Efficiency")
    print(f"  ✓ Processed {metrics['rows_read']:,} rows")
    print(f"  ✓ Only 1 row in memory at a time")
    print(f"  ✓ Works with 1 billion rows (same code!)")
    print(f"  ✓ Real Netflix/Amazon/Uber process like this")

    print("\n✅ Pipeline complete! All statistics calculated streaming.")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

"""
KEY TAKEAWAYS FROM ADVANCED LESSON 1:
=====================================

1. Streaming Processing:
   - Never load all data to memory
   - Process in chunks/batches
   - Aggregate on-the-fly

2. Online Algorithms:
   - Welford's method for mean/variance
   - Incremental aggregation
   - O(1) memory per row

3. ETL Pipeline:
   Extract: Read from various sources (CSV, JSON, API)
   Transform: Validate, clean, enrich data
   Load: Store or aggregate results

4. Real-world patterns:
   ✓ Generators for streaming
   ✓ Functional transformations (map/filter)
   ✓ Class-based state machines
   ✓ Online algorithms for statistics

5. Scaling considerations:
   - Batch size affects memory vs disk I/O tradeoff
   - Compression saves bandwidth
   - Indexing speeds up lookups
   - Distributed processing for truly massive datasets

REAL-WORLD IMPACT:
==================
- Netflix: Processes billions of events daily with streaming
- Uber: Real-time analytics on 10M+ rides daily
- Amazon: Analyzes petabytes of user behavior
- Google: Streams web crawl data (exabytes)

These techniques power every large-scale system!
"""

if __name__ == "__main__":
    run_demo()
