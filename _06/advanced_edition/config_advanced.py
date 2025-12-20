"""
Configuration for Advanced Edition - Module 6
==============================================

Production-grade configuration for real-world scenarios:
- Big data processing (millions of records)
- Distributed systems and caching
- Machine learning pipelines
- API servers and web frameworks

PRINCIPLE: "Make it work, then optimize" - but this is optimized from the start.
"""

import os
from pathlib import Path
from decimal import Decimal
from typing import Dict, List, Any

# ============================================================================
# [DATABASE & DATA SOURCES]
# ============================================================================

DATA_SOURCES_CONFIG = {
    # Public dataset sources (examples)
    "datasets": {
        "kaggle_transactions": {
            "url": "https://example.com/transactions_1m.csv.gz",
            "rows": 1_000_000,
            "compressed": True,
            "description": "1M financial transactions (sample)",
        },
        "ecommerce_events": {
            "url": "https://example.com/events_10m.parquet",
            "rows": 10_000_000,
            "compressed": True,
            "description": "10M e-commerce user events",
        },
        "user_behavior": {
            "url": "https://example.com/user_behavior.csv",
            "rows": 500_000,
            "compressed": False,
            "description": "User behavior data",
        },
    },

    # Local storage for downloaded data
    "data_dir": Path(__file__).parent / "data",
    "cache_dir": Path(__file__).parent / "cache",

    # Streaming config
    "chunk_size": 100_000,  # Process 100K rows at a time
    "buffer_size": 10_000,  # Buffer size for streaming
}

# ============================================================================
# [FINANCIAL SYSTEM - PRODUCTION GRADE]
# ============================================================================

FINANCIAL_CONFIG = {
    # Account types with different rules
    "account_types": {
        "checking": {
            "interest_rate": Decimal("0.001"),
            "withdrawal_limit": Decimal("10000.00"),
            "transaction_limit": 1000,
            "min_balance": Decimal("100.00"),
        },
        "savings": {
            "interest_rate": Decimal("0.025"),
            "withdrawal_limit": Decimal("5000.00"),
            "transaction_limit": 6,  # Federal limit
            "min_balance": Decimal("500.00"),
        },
        "money_market": {
            "interest_rate": Decimal("0.045"),
            "withdrawal_limit": Decimal("50000.00"),
            "transaction_limit": 3,
            "min_balance": Decimal("2500.00"),
        },
    },

    # Tiered fees
    "fee_schedule": {
        "base_transaction": Decimal("0.50"),
        "international_transfer": Decimal("25.00"),
        "wire_transfer": Decimal("15.00"),
        "atm_outofnetwork": Decimal("2.50"),
        "overdraft": Decimal("35.00"),
    },

    # Compliance settings
    "decimal_places": 4,  # Internal precision (higher for calculations)
    "display_places": 2,  # Display precision (USD standard)
    "daily_volume_limit": Decimal("100000.00"),  # AML compliance
    "suspicious_amount": Decimal("10000.00"),  # Flag for reporting
}

# ============================================================================
# [MACHINE LEARNING & RECOMMENDATION ENGINE]
# ============================================================================

ML_CONFIG = {
    # Feature engineering
    "features": {
        "user_based": ["age", "tenure", "purchase_frequency", "avg_spend"],
        "behavior_based": ["category_preferences", "time_of_day", "device"],
        "engagement_based": ["click_rate", "conversion_rate", "return_rate"],
    },

    # Caching strategy (3-tier)
    "cache_tiers": {
        "tier1_lru": {
            "type": "in_process",
            "maxsize": 10_000,
            "ttl_seconds": 3600,  # 1 hour
        },
        "tier2_redis": {
            "type": "distributed",
            "host": "localhost",
            "port": 6379,
            "ttl_seconds": 86400,  # 24 hours
        },
        "tier3_database": {
            "type": "persistent",
            "retention_days": 30,
        },
    },

    # Model parameters
    "model_config": {
        "min_history_size": 10,  # Need 10+ purchases for recommendations
        "similarity_threshold": 0.7,
        "top_n": 10,
        "diversity_weight": 0.3,  # Mix in diverse items
    },

    # Segmentation
    "segments": {
        "DORMANT": {"days_inactive": 90, "target_reactivation": True},
        "ACTIVE": {"purchase_freq_days": 30, "target_retention": True},
        "VIP": {"lifetime_value_percentile": 0.95, "target_grow": True},
        "AT_RISK": {"churn_probability": 0.5, "target_save": True},
    },
}

# ============================================================================
# [WEB FRAMEWORK SIMULATION - OOP ARCHITECTURE]
# ============================================================================

WEB_CONFIG = {
    # Server settings
    "server": {
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 4,
        "timeout": 30,
    },

    # HTTP settings
    "http": {
        "max_request_size": 100 * 1024 * 1024,  # 100MB
        "max_connections": 1000,
        "keepalive_timeout": 60,
    },

    # Authentication
    "auth": {
        "jwt_secret": "your-secret-key-change-in-production",
        "token_expiry_minutes": 60,
        "refresh_token_expiry_days": 30,
        "algorithm": "HS256",
    },

    # Rate limiting
    "rate_limit": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "burst_size": 10,
    },

    # Middleware order (this is important for execution)
    "middleware": [
        "logging",
        "authentication",
        "rate_limiting",
        "compression",
        "error_handling",
    ],

    # Routes configuration
    "routes": {
        "/api/users": {
            "methods": ["GET", "POST"],
            "auth_required": True,
            "cache_ttl": 300,
        },
        "/api/recommendations": {
            "methods": ["GET"],
            "auth_required": True,
            "cache_ttl": 3600,
        },
        "/api/analytics": {
            "methods": ["GET"],
            "auth_required": True,
            "admin_only": True,
        },
    },
}

# ============================================================================
# [ETL PIPELINE CONFIGURATION]
# ============================================================================

ETL_CONFIG = {
    # Extract settings
    "extract": {
        "sources": ["csv", "json", "parquet", "api"],
        "batch_size": 100_000,
        "parallel_downloads": 4,
        "retry_attempts": 3,
    },

    # Transform settings
    "transform": {
        "validation": {
            "schema_check": True,
            "null_check": True,
            "type_coercion": True,
        },
        "deduplication": {
            "enabled": True,
            "key_fields": ["id", "timestamp"],
        },
        "enrichment": {
            "add_computed_fields": True,
            "add_timestamps": True,
        },
    },

    # Load settings
    "load": {
        "destination": "database",  # or "data_warehouse"
        "batch_size": 100_000,
        "transaction_size": 10_000,
        "error_handling": "quarantine",  # vs "skip" or "fail"
    },

    # Pipeline monitoring
    "monitoring": {
        "log_level": "INFO",
        "metrics_enabled": True,
        "alert_on_error": True,
    },
}

# ============================================================================
# [PERFORMANCE TUNING]
# ============================================================================

PERFORMANCE_CONFIG = {
    # Memory management
    "memory": {
        "max_per_process": "4GB",
        "gc_threshold": 10_000,  # Run GC after N objects
    },

    # Multiprocessing
    "parallel": {
        "enabled": True,
        "num_workers": 4,
        "chunk_per_worker": 100_000,
    },

    # Compression
    "compression": {
        "enabled": True,
        "algorithm": "gzip",  # or "snappy", "zstd"
        "level": 6,  # 1-9, higher = more compression
    },

    # Benchmarking
    "benchmarking": {
        "enabled": True,
        "sample_size": 0.01,  # Profile 1% of operations
        "output_format": "json",
    },
}

# ============================================================================
# [LOGGING & MONITORING]
# ============================================================================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "console": {"enabled": True},
        "file": {"enabled": True, "path": "logs/app.log"},
        "sentry": {"enabled": False, "dsn": ""},
    },

    "metrics": {
        "enabled": True,
        "export_interval": 60,  # seconds
        "backend": "prometheus",
    },
}

# ============================================================================
# [UTILITY FUNCTIONS FOR ADVANCED CONFIG]
# ============================================================================

def get_config_section(section_name: str) -> Dict[str, Any]:
    """Get entire configuration section."""
    sections = {
        "data_sources": DATA_SOURCES_CONFIG,
        "financial": FINANCIAL_CONFIG,
        "ml": ML_CONFIG,
        "web": WEB_CONFIG,
        "etl": ETL_CONFIG,
        "performance": PERFORMANCE_CONFIG,
        "logging": LOGGING_CONFIG,
    }
    if section_name not in sections:
        raise ValueError(f"Unknown section: {section_name}")
    return sections[section_name]


def get_config_value(section: str, key: str, default: Any = None) -> Any:
    """Get nested config value safely."""
    try:
        section_config = get_config_section(section)
        keys = key.split(".")
        value = section_config
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default


def validate_data_source(dataset_name: str) -> bool:
    """Check if dataset is properly configured."""
    return dataset_name in DATA_SOURCES_CONFIG["datasets"]


def estimate_memory_usage(num_rows: int, avg_row_bytes: int = 1000) -> str:
    """Estimate memory for dataset."""
    bytes_total = num_rows * avg_row_bytes
    gb = bytes_total / (1024 ** 3)
    return f"{gb:.2f} GB"


if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED EDITION - CONFIGURATION VALIDATION")
    print("=" * 70)

    print("\n[Financial Accounts]")
    for acc_type, settings in FINANCIAL_CONFIG["account_types"].items():
        print(f"  {acc_type}: {settings['interest_rate']}% interest")

    print("\n[ML Caching Tiers]")
    for tier, config in ML_CONFIG["cache_tiers"].items():
        print(f"  {tier}: {config['type']}")

    print("\n[Dataset Sources]")
    for name, dataset in DATA_SOURCES_CONFIG["datasets"].items():
        rows = f"{dataset['rows']:,}"
        print(f"  {name}: {rows} rows")

    print("\n✅ Advanced configuration validated!")
