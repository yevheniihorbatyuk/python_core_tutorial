"""
Module 8.6: Mini Projects - Real-World Applications
====================================================

Three complete projects combining all concepts from this module.
Each project demonstrates serialization and object copying in practice.

Estimated time: 4-5 hours (1-2 hours per project)
Difficulty: ⭐⭐⭐ (Advanced Beginner)
"""

from __future__ import annotations

import csv
import json
import os
import pickle
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Final, Optional

# ==============================================================================
# PROJECT 1: TASK TRACKER WITH JSON PERSISTENCE
# ==============================================================================

print("=" * 80)
print("PROJECT 1: TASK TRACKER WITH JSON PERSISTENCE")
print("=" * 80)

print("""
Description:
Build a task management system that persists tasks to JSON.
Users can add tasks, mark complete, and save/load from file.

Requirements:
✓ Task class with title, description, completion status, created_at
✓ TaskTracker class to manage multiple tasks
✓ JSON serialization (to_dict/from_dict)
✓ Load/save to file with error handling
✓ Display tasks with formatting
""")


@dataclass
class Task:
    """Represents a single task."""
    title: str
    description: str
    completed: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        """Deserialize from dict."""
        return cls(
            title=data["title"],
            description=data["description"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
        )

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.completed = True
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        status = "✅" if self.completed else "⏳"
        return f"{status} {self.title}: {self.description[:30]}..."


class TaskTracker:
    """Manages a collection of tasks with persistence."""

    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: list[Task] = []
        self.load()

    def add_task(self, title: str, description: str) -> None:
        """Add a new task."""
        task = Task(title=title, description=description)
        self.tasks.append(task)
        print(f"✅ Added: {task}")

    def complete_task(self, task_index: int) -> None:
        """Mark task as complete."""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_complete()
            print(f"✅ Completed: {self.tasks[task_index].title}")

    def list_tasks(self) -> None:
        """Display all tasks."""
        if not self.tasks:
            print("No tasks yet!")
            return

        print(f"\n📋 Tasks ({len(self.tasks)}):")
        for i, task in enumerate(self.tasks):
            print(f"  {i}. {task}")

    def save(self) -> None:
        """Save tasks to JSON file."""
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved {len(self.tasks)} tasks to {self.filename}")

    def load(self) -> None:
        """Load tasks from JSON file."""
        if not os.path.exists(self.filename):
            print(f"ℹ️  No tasks file found ({self.filename})")
            return

        with open(self.filename, "r") as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        print(f"✅ Loaded {len(self.tasks)} tasks from {self.filename}")


# Run Project 1
print("\nRunning Project 1 Demo:")
tracker = TaskTracker("project1_tasks.json")
tracker.add_task("Learn Serialization", "Complete Module 8 lessons")
tracker.add_task("Build Data Pipeline", "Practice with real data")
tracker.add_task("Code Review", "Review teammate's PR")
tracker.list_tasks()
tracker.complete_task(0)
tracker.list_tasks()
tracker.save()

print("\n✅ Project 1 Complete!\n")


# ==============================================================================
# PROJECT 2: CONFIGURATION MANAGER WITH VALIDATION
# ==============================================================================

print("=" * 80)
print("PROJECT 2: CONFIGURATION MANAGER WITH VALIDATION")
print("=" * 80)

print("""
Description:
Build a configuration system for ML model training.
Support loading from file, validation, and environment overrides.

Requirements:
✓ Config dataclass with model parameters
✓ Validation in __post_init__
✓ JSON serialization
✓ Environment variable override
✓ Deep copy for experiment variations
✓ Pretty printing
""")


@dataclass
class ModelConfig:
    """Configuration for ML model training."""
    name: str
    learning_rate: float
    batch_size: int
    epochs: int
    optimizer: str = "adam"
    validation_split: float = 0.2

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not 0.0 < self.learning_rate < 1.0:
            raise ValueError("Learning rate must be between 0 and 1")
        if self.batch_size <= 0:
            raise ValueError("Batch size must be positive")
        if self.epochs <= 0:
            raise ValueError("Epochs must be positive")
        if not 0.0 <= self.validation_split < 1.0:
            raise ValueError("Validation split must be between 0 and 1")

    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {
            "name": self.name,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "epochs": self.epochs,
            "optimizer": self.optimizer,
            "validation_split": self.validation_split,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ModelConfig:
        """Deserialize from dict."""
        return cls(**data)

    @classmethod
    def from_file(cls, filename: str) -> ModelConfig:
        """Load configuration from JSON file."""
        with open(filename, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def save(self, filename: str) -> None:
        """Save configuration to JSON file."""
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"✅ Saved config to {filename}")

    def create_variant(self, **overrides) -> ModelConfig:
        """Create a copy with some parameters changed (for experiments)."""
        import copy
        data = copy.deepcopy(self.to_dict())
        data.update(overrides)
        return ModelConfig.from_dict(data)

    def __repr__(self) -> str:
        return f"ModelConfig(name={self.name!r}, lr={self.learning_rate}, batch={self.batch_size}, epochs={self.epochs})"


# Run Project 2
print("\nRunning Project 2 Demo:")

# Create base config
base_config = ModelConfig(
    name="bert_classifier",
    learning_rate=0.001,
    batch_size=32,
    epochs=10
)
print(f"Base config: {base_config}")

# Create variants for hyperparameter tuning
configs = [
    base_config,
    base_config.create_variant(learning_rate=0.0001),
    base_config.create_variant(learning_rate=0.01, batch_size=64),
    base_config.create_variant(epochs=20),
]

print("\nExperiment variants:")
for i, config in enumerate(configs):
    print(f"  {i+1}. {config}")

# Save one config
configs[0].save("project2_config.json")
loaded_config = ModelConfig.from_file("project2_config.json")
print(f"\nLoaded config: {loaded_config}")

print("\n✅ Project 2 Complete!\n")


# ==============================================================================
# PROJECT 3: DATA BACKUP UTILITY
# ==============================================================================

print("=" * 80)
print("PROJECT 3: DATA BACKUP UTILITY")
print("=" * 80)

print("""
Description:
Build a backup system that exports data in multiple formats.
Support creating backups, listing them, and comparing versions.

Requirements:
✓ Data model (list of records)
✓ Export to JSON, CSV, and Pickle
✓ Backup metadata (timestamp, format, file size)
✓ Backup listing and management
✓ Data comparison across formats
""")


@dataclass
class Record:
    """A single data record."""
    id: int
    name: str
    value: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class BackupMetadata:
    """Information about a backup."""
    filename: str
    format: str  # "json", "csv", or "pickle"
    timestamp: datetime
    record_count: int
    file_size: int  # bytes

    def __repr__(self) -> str:
        return f"Backup({self.format.upper()}, {self.record_count} records, {self.file_size} bytes)"


class BackupManager:
    """Manages backups of data in multiple formats."""

    def __init__(self, data_dir: str = "backups"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.backups: list[BackupMetadata] = []

    def backup_json(self, records: list[Record]) -> None:
        """Backup data as JSON."""
        filename = f"{self.data_dir}/backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        data = [r.to_dict() for r in records]
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        self._register_backup(filename, "json", len(records))

    def backup_csv(self, records: list[Record]) -> None:
        """Backup data as CSV."""
        filename = f"{self.data_dir}/backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "value", "created_at"])
            writer.writeheader()
            for record in records:
                writer.writerow(record.to_dict())
        self._register_backup(filename, "csv", len(records))

    def backup_pickle(self, records: list[Record]) -> None:
        """Backup data as Pickle."""
        filename = f"{self.data_dir}/backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.pkl"
        with open(filename, "wb") as f:
            pickle.dump(records, f, protocol=5)
        self._register_backup(filename, "pickle", len(records))

    def _register_backup(self, filename: str, format_type: str, record_count: int) -> None:
        """Register a backup."""
        file_size = os.path.getsize(filename)
        metadata = BackupMetadata(
            filename=os.path.basename(filename),
            format=format_type,
            timestamp=datetime.now(timezone.utc),
            record_count=record_count,
            file_size=file_size
        )
        self.backups.append(metadata)
        print(f"✅ Backed up: {metadata}")

    def list_backups(self) -> None:
        """List all backups."""
        if not self.backups:
            print("No backups yet!")
            return

        print(f"\n📦 Backups ({len(self.backups)}):")
        for backup in self.backups:
            print(f"  - {backup}")

    def compare_sizes(self) -> None:
        """Compare file sizes across formats."""
        if len(self.backups) < 2:
            print("Need at least 2 backups to compare")
            return

        print("\n📊 Backup Size Comparison:")
        for backup in self.backups:
            print(f"  {backup.format.upper():8s}: {backup.file_size:6d} bytes")

        sizes = [b.file_size for b in self.backups]
        print(f"  Smallest: {min(sizes)} bytes")
        print(f"  Largest:  {max(sizes)} bytes")


# Run Project 3
print("\nRunning Project 3 Demo:")

# Create sample data
sample_records = [
    Record(1, "Alice", 95.5),
    Record(2, "Bob", 87.3),
    Record(3, "Charlie", 92.1),
    Record(4, "Diana", 88.9),
]

# Create backups in different formats
backup_manager = BackupManager()
print("\nCreating backups...")
backup_manager.backup_json(sample_records)
backup_manager.backup_csv(sample_records)
backup_manager.backup_pickle(sample_records)

backup_manager.list_backups()
backup_manager.compare_sizes()

print("\n✅ Project 3 Complete!\n")


# ==============================================================================
# SUMMARY AND NEXT STEPS
# ==============================================================================

print("=" * 80)
print("SUMMARY")
print("=" * 80)

summary = """
✅ COMPLETED 3 MINI PROJECTS:

1. Task Tracker
   - JSON persistence
   - CRUD operations
   - Date/time handling

2. Configuration Manager
   - Validation
   - Deep copy for variants
   - File I/O

3. Data Backup Utility
   - Multiple formats (JSON, CSV, Pickle)
   - File metadata management
   - Comparison and analysis

💡 KEY PATTERNS LEARNED:
   - to_dict() / from_dict() for serialization
   - dataclasses with validation
   - Context managers for file I/O
   - Deep copy for creating variations
   - Metadata tracking

🎯 NEXT STEPS:
   1. Combine these projects (config-driven task tracker)
   2. Add error handling (try/except)
   3. Add logging (who did what, when)
   4. Move to advanced_edition for:
      - Pydantic validation
      - Async I/O
      - Database integration
      - Production patterns

🚀 REAL-WORLD APPLICATIONS:
   - Task Tracker → Project management tools, todo apps
   - Config Manager → ML training scripts, microservice configs
   - Backup Utility → Data warehouses, ETL pipelines
"""

print(summary)
