"""
Модуль 2.2: Сучасні функції та патерни для DS/DE
=================================================

Advanced function patterns для Data Science/Engineering
Python 3.10+ features
"""

from functools import wraps, lru_cache, partial
from time import time, sleep
from typing import Callable, Any
from dataclasses import dataclass
import statistics

# ============================================================================
# 1. ДЕКОРАТОРИ - TIMING ДЛЯ DATA PIPELINES
# ============================================================================

print("=" * 70)
print("1. ДЕКОРАТОРИ - ВИМІРЮВАННЯ ЧАСУ ВИКОНАННЯ")
print("=" * 70)

def timing_decorator(func: Callable) -> Callable:
    """
    Декоратор для вимірювання часу виконання функції
    Критично важливо для ML pipelines та ETL
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        
        execution_time = end_time - start_time
        print(f"⏱️  {func.__name__} виконано за {execution_time:.4f}s")
        
        return result
    return wrapper


@timing_decorator
def process_large_dataset(n: int) -> int:
    """Симуляція обробки великого датасету"""
    sleep(0.1)  # Симулюємо обробку
    return sum(range(n))


# Тест
result = process_large_dataset(1_000_000)
print(f"Результат: {result:,}")


# ============================================================================
# 2. ДЕКОРАТОР ДЛЯ ЛОГУВАННЯ
# ============================================================================

print("\n" + "=" * 70)
print("2. ДЕКОРАТОР ДЛЯ ЛОГУВАННЯ ВИКЛИКІВ")
print("=" * 70)

def log_calls(func: Callable) -> Callable:
    """
    Логує виклики функцій з аргументами
    Корисно для debugging ML pipelines
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        print(f"📞 Виклик {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} повернув {result!r}")
        
        return result
    return wrapper


@log_calls
def calculate_average(numbers: list[float]) -> float:
    """Обчислює середнє значення"""
    return sum(numbers) / len(numbers) if numbers else 0.0


# Тест
avg = calculate_average([10, 20, 30, 40, 50])


# ============================================================================
# 3. CACHING/MEMOIZATION - ОПТИМІЗАЦІЯ
# ============================================================================

print("\n" + "=" * 70)
print("3. LRU CACHE - ОПТИМІЗАЦІЯ ДОРОГИХ ОБЧИСЛЕНЬ")
print("=" * 70)

@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    """
    Дорога операція з кешуванням
    
    lru_cache кешує результати - критично для:
    - Feature engineering
    - Повторювані обчислення в ML
    - API calls
    """
    print(f"  🔄 Обчислюю для {n}... (це дорого!)")
    sleep(0.1)  # Симуляція важкої операції
    return n ** 2 + n * 10


# Перший виклик - обчислення
print("Перший виклик:")
result1 = expensive_calculation(100)
print(f"Результат: {result1}")

# Другий виклик - з кешу!
print("\nДругий виклик (з кешу):")
result2 = expensive_calculation(100)
print(f"Результат: {result2}")

# Інформація про кеш
print(f"\nСтатистика кешу: {expensive_calculation.cache_info()}")


# ============================================================================
# 4. ГЕНЕРАТОРИ - ДЛЯ ВЕЛИКИХ ДАТАСЕТІВ
# ============================================================================

print("\n" + "=" * 70)
print("4. ГЕНЕРАТОРИ - РОБОТА З ВЕЛИКИМИ ДАНИМИ")
print("=" * 70)

def read_large_file_bad(n: int) -> list[int]:
    """
    ПОГАНИЙ спосіб - завантажує все в пам'ять
    ❌ Не підходить для великих файлів
    """
    return [i for i in range(n)]


def read_large_file_good(n: int):
    """
    ДОБРИЙ спосіб - генератор
    ✅ Обробляє по одному елементу
    ✅ Не займає всю пам'ять
    """
    for i in range(n):
        yield i


# Порівняння
print("Генератор vs список:")
large_n = 1_000_000

# Генератор - створюється миттєво
gen = read_large_file_good(large_n)
print(f"✅ Генератор створено миттєво: {gen}")

# Обробка перших 5 елементів
print("Перші 5 елементів:")
for i, value in enumerate(gen):
    if i >= 5:
        break
    print(f"  {value}")


def process_data_stream(data_generator, batch_size: int = 100):
    """
    Обробляє дані батчами з генератора
    Типовий паттерн для ML training
    """
    batch = []
    processed = 0
    
    for item in data_generator:
        batch.append(item)
        
        if len(batch) >= batch_size:
            # Обробка батчу
            batch_sum = sum(batch)
            processed += len(batch)
            print(f"  Оброблено батч: {len(batch)} елементів, сума: {batch_sum}")
            batch = []
    
    # Обробка останнього батчу
    if batch:
        processed += len(batch)
        print(f"  Останній батч: {len(batch)} елементів")
    
    return processed


print("\nОбробка stream даних:")
data_stream = read_large_file_good(350)
total = process_data_stream(data_stream, batch_size=100)
print(f"Всього оброблено: {total} елементів")


# ============================================================================
# 5. MATCH-CASE - PATTERN MATCHING (Python 3.10+)
# ============================================================================

print("\n" + "=" * 70)
print("5. MATCH-CASE - STRUCTURAL PATTERN MATCHING (Python 3.10+)")
print("=" * 70)

def route_data_by_type(data: dict) -> str:
    """
    Роутинг даних по типу - сучасний спосіб
    Замінює складні if-elif-else
    """
    match data:
        case {"type": "csv", "path": path}:
            return f"📄 Обробка CSV: {path}"
        
        case {"type": "json", "path": path, "encoding": enc}:
            return f"📋 Обробка JSON: {path} ({enc})"
        
        case {"type": "parquet", "path": path}:
            return f"🗂️  Обробка Parquet: {path}"
        
        case {"type": "api", "url": url, "method": method}:
            return f"🌐 API запит: {method} {url}"
        
        case {"type": str(type_name)}:
            return f"⚠️  Невідомий тип: {type_name}"
        
        case _:
            return "❌ Невалідні дані"


# Тести
test_cases = [
    {"type": "csv", "path": "data/train.csv"},
    {"type": "json", "path": "config.json", "encoding": "utf-8"},
    {"type": "parquet", "path": "data/features.parquet"},
    {"type": "api", "url": "https://api.example.com/data", "method": "GET"},
    {"type": "unknown"},
    {"invalid": "data"}
]

print("Роутинг різних типів даних:")
for data in test_cases:
    result = route_data_by_type(data)
    print(f"  {result}")


def process_ml_result(result: dict) -> str:
    """
    Обробка результатів ML моделі з pattern matching
    """
    match result:
        case {"success": True, "predictions": list(preds), "confidence": float(conf)} if conf > 0.9:
            return f"✅ Високоточний результат: {len(preds)} передбачень (confidence: {conf:.2%})"
        
        case {"success": True, "predictions": list(preds), "confidence": float(conf)} if conf > 0.7:
            return f"⚠️  Середня точність: {len(preds)} передбачень (confidence: {conf:.2%})"
        
        case {"success": True, "predictions": list(preds)}:
            return f"⚠️  Низька точність: {len(preds)} передбачень"
        
        case {"success": False, "error": str(error)}:
            return f"❌ Помилка: {error}"
        
        case _:
            return "❌ Невалідний результат"


# Тести
ml_results = [
    {"success": True, "predictions": [1, 0, 1], "confidence": 0.95},
    {"success": True, "predictions": [0, 0, 1], "confidence": 0.75},
    {"success": False, "error": "Model not found"},
]

print("\nОбробка результатів ML:")
for result in ml_results:
    print(f"  {process_ml_result(result)}")


# ============================================================================
# 6. DATACLASSES - СТРУКТУРОВАНІ ДАНІ (Python 3.7+)
# ============================================================================

print("\n" + "=" * 70)
print("6. DATACLASSES - СУЧАСНІ DATA STRUCTURES")
print("=" * 70)

@dataclass
class DatasetInfo:
    """
    Інформація про датасет
    
    Dataclass автоматично генерує:
    - __init__
    - __repr__
    - __eq__
    """
    name: str
    rows: int
    columns: int
    size_mb: float
    features: list[str]
    
    @property
    def density(self) -> float:
        """Густина даних"""
        return self.rows * self.columns
    
    def summary(self) -> str:
        """Короткий опис датасету"""
        return f"{self.name}: {self.rows:,} rows × {self.columns} cols = {self.density:,} cells ({self.size_mb:.1f} MB)"


# Створення екземпляру - чисто та зрозуміло
dataset = DatasetInfo(
    name="Customer Churn",
    rows=100_000,
    columns=25,
    size_mb=12.5,
    features=["age", "tenure", "monthly_charges", "churn"]
)

print(f"Dataset: {dataset}")
print(f"Summary: {dataset.summary()}")


@dataclass
class MLModelMetrics:
    """Метрики ML моделі"""
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time_sec: float
    
    @property
    def is_good_performance(self) -> bool:
        """Чи модель має хороші показники"""
        return self.f1_score > 0.8 and self.accuracy > 0.85
    
    def compare_with(self, other: 'MLModelMetrics') -> str:
        """Порівняння з іншою моделлю"""
        if self.f1_score > other.f1_score:
            return f"✅ {self.model_name} краща за {other.model_name}"
        else:
            return f"❌ {other.model_name} краща за {self.model_name}"


# Порівняння моделей
model_a = MLModelMetrics("Random Forest", 0.92, 0.89, 0.91, 0.90, 125.5)
model_b = MLModelMetrics("XGBoost", 0.94, 0.92, 0.93, 0.925, 98.3)

print(f"\nМодель A: {model_a.model_name}")
print(f"  F1 Score: {model_a.f1_score:.3f}")
print(f"  Good performance: {model_a.is_good_performance}")

print(f"\nМодель B: {model_b.model_name}")
print(f"  F1 Score: {model_b.f1_score:.3f}")
print(f"  Good performance: {model_b.is_good_performance}")

print(f"\nПорівняння: {model_a.compare_with(model_b)}")


# ============================================================================
# 7. ФУНКЦІЇ ВИЩОГО ПОРЯДКУ - MAP, FILTER, REDUCE
# ============================================================================

print("\n" + "=" * 70)
print("7. ФУНКЦІЇ ВИЩОГО ПОРЯДКУ - ФУНКЦІОНАЛЬНЕ ПРОГРАМУВАННЯ")
print("=" * 70)

# Дані для обробки
raw_data = [
    {"id": 1, "value": 100, "category": "A"},
    {"id": 2, "value": 250, "category": "B"},
    {"id": 3, "value": 150, "category": "A"},
    {"id": 4, "value": 300, "category": "C"},
    {"id": 5, "value": 200, "category": "B"},
]

# Map - трансформація
print("MAP - трансформація даних:")
enriched = list(map(
    lambda x: {**x, "value_squared": x["value"] ** 2},
    raw_data
))
print(f"  Додано value_squared:")
for item in enriched[:2]:
    print(f"    ID {item['id']}: {item['value']} → {item['value_squared']}")

# Filter - фільтрація
print("\nFILTER - відбір даних:")
high_value = list(filter(
    lambda x: x["value"] > 150,
    raw_data
))
print(f"  Записів з value > 150: {len(high_value)}")
for item in high_value:
    print(f"    ID {item['id']}: value={item['value']}")

# Combine - chain operations
print("\nCOMBINE - ланцюг операцій:")
result = list(
    map(
        lambda x: x["value"] * 1.1,  # Збільшити на 10%
        filter(
            lambda x: x["category"] == "A",  # Тільки категорія A
            raw_data
        )
    )
)
print(f"  Category A зі збільшенням: {result}")


# ============================================================================
# 8. PARTIAL FUNCTIONS - СПЕЦІАЛІЗАЦІЯ ФУНКЦІЙ
# ============================================================================

print("\n" + "=" * 70)
print("8. PARTIAL FUNCTIONS - СПЕЦІАЛІЗАЦІЯ")
print("=" * 70)

def calculate_discount(price: float, discount_pct: float, tax_pct: float) -> float:
    """Розрахунок ціни з знижкою та податком"""
    discounted = price * (1 - discount_pct / 100)
    final_price = discounted * (1 + tax_pct / 100)
    return final_price


# Створюємо спеціалізовані функції
black_friday_price = partial(calculate_discount, discount_pct=30, tax_pct=20)
regular_price = partial(calculate_discount, discount_pct=0, tax_pct=20)
member_price = partial(calculate_discount, discount_pct=15, tax_pct=20)

# Використання
prices = [100, 250, 500]

print("Спеціалізовані функції ціноутворення:")
for price in prices:
    print(f"\n  Базова ціна: ${price}")
    print(f"    Regular: ${regular_price(price):.2f}")
    print(f"    Member: ${member_price(price):.2f}")
    print(f"    Black Friday: ${black_friday_price(price):.2f}")


# ============================================================================
# 9. ERROR HANDLING PATTERNS
# ============================================================================

print("\n" + "=" * 70)
print("9. ПРОФЕСІЙНА ОБРОБКА ПОМИЛОК")
print("=" * 70)

class DataValidationError(Exception):
    """Custom exception для валідації даних"""
    pass


def validate_and_process(
    data: list[dict]
) -> tuple[list[dict], list[str]]:
    """
    Валідує та обробляє дані з proper error handling
    
    Returns:
        tuple: (valid_data, errors)
    """
    valid_data = []
    errors = []
    
    for i, record in enumerate(data):
        try:
            # Валідація структури
            if "value" not in record:
                raise DataValidationError(f"Missing 'value' field")
            
            # Валідація типу
            if not isinstance(record["value"], (int, float)):
                raise DataValidationError(f"'value' must be numeric")
            
            # Валідація діапазону
            if record["value"] < 0:
                raise DataValidationError(f"'value' must be positive")
            
            # Валідація пройдена
            valid_data.append(record)
            
        except DataValidationError as e:
            errors.append(f"Record {i}: {e}")
        except Exception as e:
            errors.append(f"Record {i}: Unexpected error - {e}")
    
    return valid_data, errors


# Тест з різними даними
test_data = [
    {"id": 1, "value": 100},      # OK
    {"id": 2, "name": "test"},    # Missing value
    {"id": 3, "value": "abc"},    # Wrong type
    {"id": 4, "value": -50},      # Negative
    {"id": 5, "value": 200},      # OK
]

valid, errors = validate_and_process(test_data)

print(f"Валідні записи: {len(valid)}")
print(f"Помилки: {len(errors)}")
if errors:
    print("\nДеталі помилок:")
    for error in errors:
        print(f"  ❌ {error}")


# ============================================================================
# 10. КОМПОЗИЦІЯ ФУНКЦІЙ - PIPELINE PATTERN
# ============================================================================

print("\n" + "=" * 70)
print("10. PIPELINE PATTERN - КОМПОЗИЦІЯ ФУНКЦІЙ")
print("=" * 70)

def compose(*functions):
    """
    Композиція функцій - функціональний підхід до pipelines
    """
    def inner(arg):
        result = arg
        for func in functions:
            result = func(result)
        return result
    return inner


# Функції для pipeline
def extract_values(data: list[dict]) -> list[float]:
    """Extract: витягуємо значення"""
    return [item["value"] for item in data if "value" in item]


def transform_scale(values: list[float]) -> list[float]:
    """Transform: нормалізація [0, 1]"""
    if not values:
        return []
    min_val, max_val = min(values), max(values)
    if max_val == min_val:
        return [0.5] * len(values)
    return [(v - min_val) / (max_val - min_val) for v in values]


def load_statistics(values: list[float]) -> dict:
    """Load: обчислюємо статистику"""
    if not values:
        return {"error": "No data"}
    return {
        "count": len(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0
    }


# Створюємо ETL pipeline
etl_pipeline = compose(
    extract_values,
    transform_scale,
    load_statistics
)

# Тест pipeline
input_data = [
    {"id": 1, "value": 100},
    {"id": 2, "value": 200},
    {"id": 3, "value": 150},
    {"id": 4, "value": 300},
]

result = etl_pipeline(input_data)
print("ETL Pipeline результат:")
for key, value in result.items():
    if isinstance(value, float):
        print(f"  {key}: {value:.4f}")
    else:
        print(f"  {key}: {value}")


# ============================================================================
# ПІДСУМОК
# ============================================================================

print("\n" + "=" * 70)
print("ПІДСУМОК: СУЧАСНІ ПАТТЕРНИ ФУНКЦІЙ")
print("=" * 70)

summary = """
✅ ДЕКОРАТОРИ:
   - @timing_decorator - профілювання
   - @lru_cache - оптимізація
   - @log_calls - debugging

✅ ГЕНЕРАТОРИ:
   - yield для великих даних
   - Обробка stream даних
   - Батч processing

✅ MATCH-CASE (Python 3.10+):
   - Pattern matching
   - Data routing
   - Чистіше за if-elif-else

✅ DATACLASSES:
   - Структуровані дані
   - Auto-generated methods
   - Type hints

✅ ФУНКЦІОНАЛЬНЕ ПРОГРАМУВАННЯ:
   - map, filter, reduce
   - Partial functions
   - Function composition

✅ ERROR HANDLING:
   - Custom exceptions
   - Proper error messages
   - Validation patterns

✅ PIPELINE PATTERN:
   - Function composition
   - ETL workflows
   - Чистий та читабельний код

🎯 ДЛЯ DATA SCIENCE/ENGINEERING:
   - Оптимізація через caching
   - Stream processing для великих даних
   - Професійна обробка помилок
   - Декоратори для моніторингу
   - Dataclasses для структур даних
"""

print(summary)

print("\n✨ Тепер ви знаєте advanced паттерни Python! ✨\n")
