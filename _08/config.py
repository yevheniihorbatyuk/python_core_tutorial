"""
Module 8 Configuration and Constants
====================================

Centralized configuration for serialization examples and demonstrations.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Final

# Module paths
MODULE_ROOT = Path(__file__).parent
BEGINNER_DIR = MODULE_ROOT / "beginner_edition"
ADVANCED_DIR = MODULE_ROOT / "advanced_edition"
DATA_DIR = MODULE_ROOT / "data"
SOLUTIONS_DIR = MODULE_ROOT / "solutions"
EXERCISES_DIR = MODULE_ROOT / "exercises"

# Create directories if they don't exist
for directory in [DATA_DIR, SOLUTIONS_DIR, EXERCISES_DIR]:
    directory.mkdir(exist_ok=True)

# Serialization settings
DEFAULT_ENCODING: Final = "utf-8"
JSON_INDENT: Final = 2
PICKLE_PROTOCOL: Final = 5

# Validation constants
MIN_PASSWORD_LENGTH: Final = 8
MAX_PASSWORD_LENGTH: Final = 128
MIN_BATCH_SIZE: Final = 1
MAX_BATCH_SIZE: Final = 100000
MIN_TIMEOUT: Final = 0.1
MAX_TIMEOUT: Final = 300.0


class SerializationFormat(Enum):
    """Supported serialization formats."""
    JSON = "json"
    CSV = "csv"
    PICKLE = "pickle"
    MSGPACK = "msgpack"
    PARQUET = "parquet"


class DataPipelineStage(Enum):
    """Data pipeline processing stages."""
    INPUT = "input"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    AGGREGATION = "aggregation"
    OUTPUT = "output"


class Environment(Enum):
    """Deployment environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# Sample data
SAMPLE_USER_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve",
    "Frank", "Grace", "Henry", "Ivy", "Jack"
]

SAMPLE_CITIES = [
    "Kyiv", "Lviv", "Kharkiv", "Dnipro", "Odesa",
    "Warsaw", "Berlin", "Prague", "Budapest", "Vienna"
]

SAMPLE_COUNTRIES = [
    "Ukraine", "Poland", "Germany", "Czech Republic", "Hungary",
    "Austria", "Slovakia", "Romania", "Bulgaria", "Serbia"
]
