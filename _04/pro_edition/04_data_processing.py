"""
Модуль 4.4: Data Processing та ETL - Professional Edition
===========================================================

Це продвинутий модуль для обробки великих наборів даних.
Включає приклади з:
- Обробка CSV та JSON файлів у production
- ETL (Extract-Transform-Load) pipeline
- Memory-efficient обробка великих файлів
- Балансування точності та швидкості
- Паралельна обробка (multi-threading)
- Кешування та оптимізація
- Обробка помилок та логування

Ключові концепції:
- Streaming обробка (не завантажуємо все в пам'ять)
- Chunks обробка для балансу
- Type hints та validation на всіх етапах
- Метрики та моніторинг обробки
- Graceful degradation при помилках

Це версія для Senior engineers - production-ready.
"""

import csv
import json
import os
import time
import logging
from typing import List, Dict, Optional, Generator, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

print("=" * 70)
print("МОДУЛЬ 4.4: DATA PROCESSING ТА ETL - PROFESSIONAL EDITION")
print("=" * 70)

# ============================================================================
# 1. STREAMING CSV ОБРОБКА
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: STREAMING CSV ОБРОБКА - MEMORY EFFICIENT")
print("=" * 70)

@dataclass
class CSVMetrics:
    """Метрики для CSV обробки."""
    total_rows: int = 0
    processed_rows: int = 0
    skipped_rows: int = 0
    error_rows: int = 0
    processing_time: float = 0.0
    throughput: float = 0.0

class CSVProcessor:
    """Production-ready CSV обробник з streaming та кешуванням."""

    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.metrics = CSVMetrics()
        self._cache = {}

    def process_csv_streaming(
        self, filepath: str, row_processor
    ) -> CSVMetrics:
        """Обробляє CSV файл streaming способом (chunks)."""
        start_time = time.time()
        chunk = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    self.metrics.total_rows += 1

                    try:
                        processed = row_processor(row)
                        if processed:
                            chunk.append(processed)
                            self.metrics.processed_rows += 1
                        else:
                            self.metrics.skipped_rows += 1

                    except Exception as e:
                        logger.warning(f"Row error: {e}")
                        self.metrics.error_rows += 1

                    # Батч обробка
                    if len(chunk) >= self.chunk_size:
                        self._process_batch(chunk)
                        chunk = []

                # Обробити залишок
                if chunk:
                    self._process_batch(chunk)

        except IOError as e:
            logger.error(f"File read error: {e}")

        self.metrics.processing_time = time.time() - start_time
        self.metrics.throughput = (
            self.metrics.processed_rows / self.metrics.processing_time
            if self.metrics.processing_time > 0 else 0
        )

        return self.metrics

    def _process_batch(self, batch: List[Dict]) -> None:
        """Обробляє батч (можна розширити для DB запису, etc)."""
        # Placeholder для батч обробки (наприклад, DB insert)
        pass

# Генеруємо тестовий CSV файл
test_csv = "sales_data.csv"
with open(test_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'product', 'quantity', 'price', 'date'])
    writer.writeheader()
    for i in range(100):
        writer.writerow({
            'id': i,
            'product': f'Product_{i % 10}',
            'quantity': 10 + (i % 50),
            'price': 99.99 + i,
            'date': '2024-01-15'
        })

print("\n1. STREAMING CSV ОБРОБКА:")
print("-" * 70)

def validate_sales_row(row: Dict) -> Optional[Dict]:
    """Валідує та нормалізує рядок продажу."""
    try:
        quantity = int(row['quantity'])
        price = float(row['price'])

        if quantity <= 0 or price <= 0:
            return None

        return {
            'product': row['product'].strip(),
            'quantity': quantity,
            'price': price,
            'total': quantity * price
        }
    except (ValueError, KeyError):
        return None

processor = CSVProcessor(chunk_size=25)
metrics = processor.process_csv_streaming(test_csv, validate_sales_row)

print(f"✅ CSV обробка завершена")
print(f"  Total rows: {metrics.total_rows}")
print(f"  Processed: {metrics.processed_rows}")
print(f"  Skipped: {metrics.skipped_rows}")
print(f"  Errors: {metrics.error_rows}")
print(f"  Time: {metrics.processing_time:.3f}s")
print(f"  Throughput: {metrics.throughput:.0f} rows/sec")

print()

# ============================================================================
# 2. JSON STREAMING ОБРОБКА
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: JSON STREAMING - HANDLING LARGE FILES")
print("=" * 70)

# Генеруємо тестовий JSON файл (JSONL - одна JSON об'єкт на рядок)
test_jsonl = "events.jsonl"
with open(test_jsonl, 'w', encoding='utf-8') as f:
    for i in range(50):
        event = {
            'id': i,
            'user_id': i % 10,
            'event_type': ['page_view', 'click', 'purchase'][i % 3],
            'timestamp': '2024-01-15T10:00:00Z',
            'value': 10.0 + (i % 100)
        }
        f.write(json.dumps(event) + '\n')

def stream_jsonl_events(filepath: str) -> Generator[Dict, None, None]:
    """Streaming обробка JSONL файлу."""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                yield json.loads(line.strip())
            except json.JSONDecodeError as e:
                logger.warning(f"Line {line_num} JSON error: {e}")
                continue

print("\n1. JSONL STREAMING ОБРОБКА:")
print("-" * 70)

event_stats = defaultdict(lambda: {'count': 0, 'total_value': 0})
total_events = 0

for event in stream_jsonl_events(test_jsonl):
    total_events += 1
    event_type = event.get('event_type', 'unknown')
    event_stats[event_type]['count'] += 1
    event_stats[event_type]['total_value'] += event.get('value', 0)

print(f"✅ Оброблено {total_events} евентів")
print(f"\nСтатистика по типам:")
for event_type in sorted(event_stats.keys()):
    stats = event_stats[event_type]
    print(f"  {event_type:12s}: {stats['count']:3d} events, ${stats['total_value']:8.2f}")

print()

# ============================================================================
# 3. ДЕДУ­ПЛІ­КА­ЦІЯ та ОЧИЩЕННЯ
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: ДЕДУБЛІКАЦІЯ ТА НОРМАЛІЗАЦІЯ")
print("=" * 70)

@dataclass
class UserRecord:
    """Нормалізований користувацький запис."""
    user_id: str
    email: str
    name: str
    country: str

    def get_hash(self) -> str:
        """Отримує хеш для дедублікації."""
        content = f"{self.user_id}|{self.email}|{self.name}|{self.country}"
        return hashlib.md5(content.encode()).hexdigest()

class DuplicateEliminator:
    """Видаляє дублікати з потоку даних."""

    def __init__(self):
        self.seen_hashes = set()
        self.duplicate_count = 0

    def add_record(self, record: UserRecord) -> Optional[UserRecord]:
        """Додає запис, повертає None якщо дублікат."""
        record_hash = record.get_hash()

        if record_hash in self.seen_hashes:
            self.duplicate_count += 1
            return None

        self.seen_hashes.add(record_hash)
        return record

# Тестові користувачі з дублікатами
test_users = [
    UserRecord('u1', 'john@example.com', 'John', 'USA'),
    UserRecord('u2', 'jane@example.com', 'Jane', 'UK'),
    UserRecord('u1', 'john@example.com', 'John', 'USA'),  # Дублікат
    UserRecord('u3', 'bob@example.com', 'Bob', 'USA'),
    UserRecord('u2', 'jane@example.com', 'Jane', 'UK'),  # Дублікат
]

print("\n1. ДЕДУБЛІКАЦІЯ:")
print("-" * 70)

dedup = DuplicateEliminator()
unique_users = []

for user in test_users:
    unique = dedup.add_record(user)
    if unique:
        unique_users.append(unique)

print(f"Вхідні записи: {len(test_users)}")
print(f"Унікальні: {len(unique_users)}")
print(f"Дублікати видалено: {dedup.duplicate_count}")

print("\nУнікальні користувачі:")
for user in unique_users:
    print(f"  {user.user_id}: {user.name} ({user.email})")

print()

# ============================================================================
# 4. ПАРАЛЕЛЬНА ОБРОБКА (THREAD POOL)
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: ПАРАЛЕЛЬНА ОБРОБКА - THREAD POOL")
print("=" * 70)

def process_heavy_task(item: Dict) -> Dict:
    """Імітує тяжку обробку (напр., API виклик)."""
    time.sleep(0.01)  # Імітація затримки
    return {
        'item_id': item['id'],
        'result': item['value'] * 2,
        'processed_at': time.time()
    }

items = [{'id': i, 'value': i * 10} for i in range(10)]

print("\n1. ПОСЛІДОВНА ОБРОБКА (базлайн):")
print("-" * 70)

start = time.time()
sequential_results = [process_heavy_task(item) for item in items]
sequential_time = time.time() - start

print(f"✅ Послідовна обробка {len(items)} items: {sequential_time:.3f}s")

print("\n2. ПАРАЛЕЛЬНА ОБРОБКА (THREAD POOL):")
print("-" * 70)

start = time.time()
parallel_results = []

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(process_heavy_task, item): item for item in items}

    for future in as_completed(futures):
        try:
            result = future.result()
            parallel_results.append(result)
        except Exception as e:
            logger.error(f"Task failed: {e}")

parallel_time = time.time() - start
speedup = sequential_time / parallel_time

print(f"✅ Паралельна обробка {len(items)} items: {parallel_time:.3f}s")
print(f"   Speedup: {speedup:.1f}x")

print()

# ============================================================================
# 5. INCREMENTAL AGGREGATION (Статистика на льоту)
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: INCREMENTAL AGGREGATION - STATISTICS ON THE FLY")
print("=" * 70)

class IncrementalStats:
    """Обчислює статистику без зберігання всіх даних."""

    def __init__(self):
        self.count = 0
        self.sum = 0
        self.min = float('inf')
        self.max = float('-inf')
        self.sum_of_squares = 0

    def add(self, value: float) -> None:
        """Додає значення та оновлює статистику."""
        self.count += 1
        self.sum += value
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.sum_of_squares += value ** 2

    def mean(self) -> float:
        """Середнє значення."""
        return self.sum / self.count if self.count > 0 else 0

    def variance(self) -> float:
        """Дисперсія."""
        if self.count == 0:
            return 0
        return (self.sum_of_squares / self.count) - (self.mean() ** 2)

    def std_dev(self) -> float:
        """Стандартне відхилення."""
        return self.variance() ** 0.5

print("\n1. INCREMENTAL СТАТИСТИКА:")
print("-" * 70)

# Імітуємо потік значень
stream_values = [10, 20, 15, 30, 25, 22, 28, 18, 24, 26]

stats = IncrementalStats()

print(f"Потік значень: {stream_values}\n")

for value in stream_values:
    stats.add(value)

print(f"✅ Статистика без зберігання всих даних:")
print(f"  Count: {stats.count}")
print(f"  Min: {stats.min}")
print(f"  Max: {stats.max}")
print(f"  Mean: {stats.mean():.2f}")
print(f"  Std Dev: {stats.std_dev():.2f}")

print()

# ============================================================================
# 6. ТРАНСФОРМАЦІЯ ДАНИХ (ETL PIPELINE)
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: ETL PIPELINE - EXTRACT -> TRANSFORM -> LOAD")
print("=" * 70)

@dataclass
class TransformMetrics:
    """Метрики трансформації."""
    extracted: int = 0
    transformed: int = 0
    loaded: int = 0
    errors: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: float = 0

    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time > 0 else 0

class SimpleETLPipeline:
    """Простий ETL pipeline."""

    def __init__(self):
        self.metrics = TransformMetrics()

    def extract(self, source_file: str) -> Generator[Dict, None, None]:
        """Extract: читаємо дані."""
        with open(source_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    self.metrics.extracted += 1
                    yield data
                except json.JSONDecodeError:
                    self.metrics.errors += 1

    def transform(self, data: Dict) -> Optional[Dict]:
        """Transform: очищуємо та нормалізуємо."""
        try:
            return {
                'id': int(data['id']),
                'value': float(data['value']) * 1.1,  # 10% markup
                'status': 'processed'
            }
        except (KeyError, ValueError):
            self.metrics.errors += 1
            return None

    def load(self, data: List[Dict], output_file: str) -> None:
        """Load: записуємо результати."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
                self.metrics.loaded += 1

    def run(self, source_file: str, output_file: str) -> TransformMetrics:
        """Запускає ETL pipeline."""
        transformed_data = []

        for raw_data in self.extract(source_file):
            transformed = self.transform(raw_data)
            if transformed:
                transformed_data.append(transformed)
                self.metrics.transformed += 1

        self.load(transformed_data, output_file)
        self.metrics.end_time = time.time()

        return self.metrics

print("\n1. ETL PIPELINE:")
print("-" * 70)

pipeline = SimpleETLPipeline()
etl_metrics = pipeline.run(test_jsonl, "processed_events.jsonl")

print(f"✅ ETL Pipeline завершений")
print(f"  Extracted: {etl_metrics.extracted}")
print(f"  Transformed: {etl_metrics.transformed}")
print(f"  Loaded: {etl_metrics.loaded}")
print(f"  Errors: {etl_metrics.errors}")
print(f"  Duration: {etl_metrics.duration():.3f}s")

print()

# ============================================================================
# 7. ПРАКТИЧНІ ЗАВДАННЯ
# ============================================================================

print("\n" + "=" * 70)
print("PART 7: ПРАКТИЧНІ ЗАВДАННЯ")
print("=" * 70)

print("""
ЗАВДАННЯ 1 (ЛЕГКО): Streaming підрахунок рядків
  - Реалізуйте generator що читає CSV файл
  - Поверніть загальну кількість рядків
  - Не завантажуйте весь файл в пам'ять

ЗАВДАННЯ 2 (СЕРЕДНЬО): Фільтрація та агрегація
  - Прочитайте JSON файл
  - Відфільтруйте записи за критерієм (напр. value > 50)
  - Агрегуйте (sum, count, average)

ЗАВДАННЯ 3 (СЕРЕДНЬО): Дедублікація за кількома полями
  - Реалізуйте дедублікацію по composite key (id + email)
  - Розпечатайте кількість дублікатів видалено
  - Збережіть унікальні записи

ЗАВДАННЯ 4 (СКЛАДНО): Паралельна обробка з лімітом
  - Реалізуйте ThreadPoolExecutor для обробки
  - Додайте обробку помилок (retry, fallback)
  - Вимірюйте throughput

ЗАВДАННЯ 5 (СКЛАДНО): Multi-stage ETL pipeline
  - Extract з CSV
  - Transform (очищення + валідація)
  - Load в JSON з метриками

Розв'яжіть завдання перед дивіттям рішення!
""")

print("\n" + "=" * 70)
print("ИТОГИ")
print("=" * 70)

print("""
✅ Що ви дізналися:
  1. Streaming обробка для memory efficiency
  2. Батч обробка для оптимізації
  3. JSONL формат для великих файлів
  4. Дедублікація з хешуванням
  5. Паралельна обробка з ThreadPoolExecutor
  6. Incremental aggregation без зберігання даних
  7. ETL pipeline архітектура

🔑 Key patterns для Senior Data Engineer:
  - Streaming vs. Batch: знайти баланс за memory vs. latency
  - Дедублікація: використовуйте hashing для масштабованості
  - Паралелізм: ThreadPool для I/O, multiprocessing для CPU
  - Метрики: завжди вимірюйте throughput, latency, error rate
  - Graceful degradation: обробляйте помилки, не зупиняйте pipeline

⚠️  Частії помилки:
  - Завантажувати все в пам'ять (OOM for large files)
  - Не обробляти помилки (зупиняється на першій помилці)
  - Недостатня логування (неможливо дебаґити в production)
  - Без метрик (не знаєте де вузькі місця)
  - Синхронна обробка замість паралельної (марнується час)

🚀 Наступне: Architecture patterns - design for scale
""")

# Очистка тестових файлів
for file in [test_csv, test_jsonl, "processed_events.jsonl"]:
    if os.path.exists(file):
        os.remove(file)
