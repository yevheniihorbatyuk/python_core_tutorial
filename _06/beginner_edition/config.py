"""
Configuration for Beginner Edition - Module 6
==============================================

This file centralizes all configuration parameters used across
beginner-level examples. Easy to adjust for different scenarios.

PRINCIPLE: "Explicit is better than implicit" (PEP 20)
All magic numbers and paths defined here, not scattered in code.
"""

import os
from pathlib import Path
from decimal import Decimal

# ============================================================================
# [1] DECIMAL: Banking System Configuration
# ============================================================================

BANKING_CONFIG = {
    # Starting balances for accounts
    "initial_balance": Decimal("1000.00"),

    # Transaction fees (in dollars)
    "withdrawal_fee": Decimal("0.50"),
    "transfer_fee": Decimal("1.00"),
    "atm_fee": Decimal("2.50"),

    # Interest rates (annual percentage)
    "savings_rate": Decimal("0.025"),  # 2.5% per year
    "checking_rate": Decimal("0.001"),  # 0.1% per year

    # Limits
    "daily_withdrawal_limit": Decimal("500.00"),
    "monthly_transaction_limit": 100,

    # Currency precision (important!)
    "decimal_places": 2,  # Always 2 decimal places for USD
}

# ============================================================================
# [2] GENERATORS: CSV Processing Configuration
# ============================================================================

CSV_PROCESSING_CONFIG = {
    # Sample CSV file (we'll create this in examples)
    "sample_csv_filename": "sample_transactions.csv",
    "sample_csv_path": Path(__file__).parent / "data" / "sample_transactions.csv",

    # Chunk size for streaming (rows per batch)
    "chunk_size": 1000,

    # For demonstrating memory efficiency
    "demo_rows": 10000,  # Demonstrate with 10K rows

    # Column names expected in CSV
    "csv_columns": ["date", "type", "amount", "category", "description"],
}

# ============================================================================
# [3] MAP/FILTER: Data Cleaning Configuration
# ============================================================================

DATA_CLEANING_CONFIG = {
    # Valid transaction types
    "valid_types": ["purchase", "refund", "withdrawal", "deposit", "transfer"],

    # Amount validation
    "min_amount": Decimal("0.01"),
    "max_amount": Decimal("1000000.00"),

    # Date format
    "date_format": "%Y-%m-%d",

    # Valid categories
    "valid_categories": [
        "groceries", "utilities", "entertainment", "transport",
        "healthcare", "other", "salary", "bonus"
    ],
}

# ============================================================================
# [4] @lru_cache: Recommendation System Configuration
# ============================================================================

CACHE_CONFIG = {
    # LRU Cache size (max items to cache)
    "cache_maxsize": 128,

    # Recommendation settings
    "recommendation_threshold": 0.7,  # Similarity score 0.7+
    "top_n_recommendations": 5,

    # Categories for mock recommendations
    "product_categories": ["electronics", "books", "home", "sports", "fashion"],
    "demo_products": {
        "electronics": ["laptop", "phone", "headphones", "tablet"],
        "books": ["python_guide", "data_science", "clean_code", "algorithms"],
        "home": ["pillow", "bed_sheets", "lamp", "desk"],
        "sports": ["running_shoes", "yoga_mat", "dumbbell", "bike"],
        "fashion": ["t_shirt", "jeans", "jacket", "socks"],
    },
}

# ============================================================================
# [5] CLASSES & OOP: User Management Configuration
# ============================================================================

USER_MANAGEMENT_CONFIG = {
    # User roles and their permissions
    "user_roles": {
        "admin": ["read", "write", "delete", "manage_users"],
        "manager": ["read", "write", "delete"],
        "user": ["read", "write"],
        "guest": ["read"],
    },

    # Password validation
    "min_password_length": 8,
    "require_special_chars": True,
    "require_numbers": True,

    # Account status
    "valid_statuses": ["active", "inactive", "suspended", "deleted"],

    # Demo data
    "demo_users": [
        {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
        {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
        {"name": "Carol Davis", "email": "carol@example.com", "age": 42},
    ],
}

# ============================================================================
# [LOGGING & OUTPUT]
# ============================================================================

LOGGING_CONFIG = {
    "verbose": True,  # Print detailed output
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "color_output": True,  # Use ANSI colors in terminal
}

# ============================================================================
# [UTILITY FUNCTIONS]
# ============================================================================

def get_config_value(section, key, default=None):
    """
    Safely get config value from any section.

    Usage:
        amount = get_config_value("BANKING_CONFIG", "initial_balance")
        cache_size = get_config_value("CACHE_CONFIG", "cache_maxsize")
    """
    configs = {
        "BANKING": BANKING_CONFIG,
        "CSV": CSV_PROCESSING_CONFIG,
        "CLEANING": DATA_CLEANING_CONFIG,
        "CACHE": CACHE_CONFIG,
        "USER": USER_MANAGEMENT_CONFIG,
        "LOGGING": LOGGING_CONFIG,
    }

    if section not in configs:
        raise KeyError(f"Unknown config section: {section}")

    section_config = configs[section]
    return section_config.get(key, default)


def validate_decimal_precision(value, places=2):
    """Ensure Decimal has correct precision for financial calculations."""
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    # Round to correct places
    quantize_str = "0." + "0" * places
    return value.quantize(Decimal(quantize_str))


if __name__ == "__main__":
    # Quick config test
    print("=" * 70)
    print("BEGINNER EDITION - CONFIGURATION TEST")
    print("=" * 70)

    print("\n[Banking Config]")
    print(f"  Initial Balance: {BANKING_CONFIG['initial_balance']}")
    print(f"  Savings Rate: {BANKING_CONFIG['savings_rate'] * 100}%")

    print("\n[CSV Config]")
    print(f"  Chunk Size: {CSV_PROCESSING_CONFIG['chunk_size']} rows")

    print("\n[Cache Config]")
    print(f"  Max Size: {CACHE_CONFIG['cache_maxsize']} items")

    print("\n[User Config]")
    print(f"  Roles: {list(USER_MANAGEMENT_CONFIG['user_roles'].keys())}")

    print("\n✅ All configurations loaded successfully!")
