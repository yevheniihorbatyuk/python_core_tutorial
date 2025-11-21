"""
Модуль 2.1: Сучасний Input/Output та робота з даними
=====================================================

Прикладні приклади для Data Science/Engineering
Python 3.10+ features
"""

from pathlib import Path
from datetime import datetime
import json

# ============================================================================
# 1. СУЧАСНІ F-STRINGS ТА DEBUGGING
# ============================================================================

print("=" * 70)
print("1. СУЧАСНІ F-STRINGS (Python 3.8+)")
print("=" * 70)

# F-strings з = для debugging (Python 3.8+)
# Автоматично показує змінну та її значення
user_id = 12345
username = "data_scientist"
records_processed = 1_500_000  # Underscore для читабельності

print(f"{user_id=}")  # user_id=12345
print(f"{username=}")  # username='data_scientist'
print(f"{records_processed=}")  # records_processed=1500000

# Форматування в debugging mode
price = 1234.56789
print(f"{price=:.2f}")  # price=1234.57

# Вирази в f-strings з =
data_size_mb = 2048
print(f"{data_size_mb / 1024=:.2f}")  # data_size_mb / 1024=2.00

# Багаторядкові f-strings для звітів
model_name = "Random Forest"
accuracy = 0.9543
training_time = 125.7

report = f"""
Model Performance Report
{'=' * 40}
Model: {model_name}
Accuracy: {accuracy:.2%}
Training Time: {training_time:.1f}s
Timestamp: {datetime.now():%Y-%m-%d %H:%M:%S}
"""
print(report)


# ============================================================================
# 2. РОБОТА З РЕАЛЬНИМИ ДАНИМИ - CSV PARSING
# ============================================================================

print("\n" + "=" * 70)
print("2. ОБРОБКА ДАНИХ З INPUT")
print("=" * 70)

def parse_csv_row(row: str) -> dict:
    """
    Парсить рядок CSV в словник
    
    Args:
        row: Рядок формату "name,age,city,salary"
    
    Returns:
        dict: Структуровані дані
    
    Example:
        >>> parse_csv_row("John,30,Kyiv,50000")
        {'name': 'John', 'age': 30, 'city': 'Kyiv', 'salary': 50000.0}
    """
    parts = row.strip().split(',')
    
    return {
        'name': parts[0],
        'age': int(parts[1]),
        'city': parts[2],
        'salary': float(parts[3])
    }

# Демонстрація
sample_data = "Alice,28,Lviv,45000"
parsed = parse_csv_row(sample_data)
print(f"Вхідні дані: {sample_data}")
print(f"Розпарсені: {parsed}")
print(f"Тип: {type(parsed)}")


# ============================================================================
# 3. DATA VALIDATION - ПРИКЛАДНИЙ ПРИКЛАД
# ============================================================================

print("\n" + "=" * 70)
print("3. ВАЛІДАЦІЯ ДАНИХ")
print("=" * 70)

def validate_age(age: int | str) -> tuple[bool, int | None, str]:
    """
    Валідує вік користувача
    
    Args:
        age: Вік як число або рядок
    
    Returns:
        tuple: (валідність, значення, повідомлення)
        
    Note:
        Використовує | для union types (Python 3.10+)
    """
    try:
        age_int = int(age)
        
        if age_int < 0:
            return False, None, "Вік не може бути від'ємним"
        elif age_int > 150:
            return False, None, "Вік занадто великий"
        elif age_int < 18:
            return False, age_int, "Потрібно бути 18+"
        else:
            return True, age_int, "Валідний вік"
            
    except ValueError:
        return False, None, "Вік повинен бути числом"


# Тестування
test_ages = ["25", "150", "-5", "abc", "17"]

for age in test_ages:
    is_valid, value, message = validate_age(age)
    status = "✅" if is_valid else "❌"
    print(f"{status} Вік '{age}': {message} (значення: {value})")


# ============================================================================
# 4. СТРУКТУРОВАНІ ДАНІ - JSON ОПЕРАЦІЇ
# ============================================================================

print("\n" + "=" * 70)
print("4. РОБОТА З JSON (типові DS/DE операції)")
print("=" * 70)

def create_data_record(
    user_id: int,
    features: list[float],
    label: str,
    metadata: dict | None = None
) -> dict:
    """
    Створює запис даних для ML pipeline
    
    Args:
        user_id: ID користувача
        features: Feature vector
        label: Цільова змінна
        metadata: Додаткова інформація
    
    Returns:
        dict: Структурований запис
    """
    record = {
        'user_id': user_id,
        'features': features,
        'label': label,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    }
    
    if metadata:
        record['metadata'] = metadata
    
    return record


# Створення прикладу
record = create_data_record(
    user_id=1001,
    features=[0.5, 0.8, 0.3, 0.9],
    label='positive',
    metadata={'source': 'api', 'confidence': 0.95}
)

print("Створений запис:")
print(json.dumps(record, indent=2, ensure_ascii=False))


# ============================================================================
# 5. ETL-LIKE ПРИКЛАД: ТРАНСФОРМАЦІЯ ДАНИХ
# ============================================================================

print("\n" + "=" * 70)
print("5. ПРОСТИЙ ETL PIPELINE")
print("=" * 70)

def clean_salary_string(salary_str: str) -> float:
    """
    Очищує та конвертує зарплату з різних форматів
    
    Examples:
        >>> clean_salary_string("$50,000")
        50000.0
        >>> clean_salary_string("45000 грн")
        45000.0
        >>> clean_salary_string("1.5k USD")
        1500.0
    """
    # Видаляємо все крім цифр, крапки та k
    cleaned = salary_str.replace(',', '').replace('$', '').replace('грн', '').replace('USD', '').strip()
    
    # Обробка k (thousands)
    if 'k' in cleaned.lower():
        cleaned = cleaned.lower().replace('k', '')
        return float(cleaned) * 1000
    
    return float(cleaned)


def transform_salary_data(raw_salaries: list[str]) -> dict:
    """
    Трансформує сирі дані зарплат в аналітичний формат
    
    Returns:
        dict: Статистика по зарплатам
    """
    cleaned_salaries = []
    
    for salary in raw_salaries:
        try:
            cleaned = clean_salary_string(salary)
            cleaned_salaries.append(cleaned)
        except ValueError as e:
            print(f"⚠️  Помилка обробки '{salary}': {e}")
            continue
    
    if not cleaned_salaries:
        return {'error': 'Немає валідних даних'}
    
    return {
        'count': len(cleaned_salaries),
        'min': min(cleaned_salaries),
        'max': max(cleaned_salaries),
        'avg': sum(cleaned_salaries) / len(cleaned_salaries),
        'total': sum(cleaned_salaries)
    }


# Тестування з реальними даними
raw_data = [
    "$50,000",
    "45000 грн",
    "1.5k USD",
    "$75,000",
    "invalid",
    "60000"
]

stats = transform_salary_data(raw_data)
print("\nВхідні дані:", raw_data)
print("\nСтатистика:")
for key, value in stats.items():
    if isinstance(value, float):
        print(f"  {key}: ${value:,.2f}")
    else:
        print(f"  {key}: {value}")


# ============================================================================
# 6. PATHLIB - СУЧАСНА РОБОТА З ФАЙЛАМИ
# ============================================================================

print("\n" + "=" * 70)
print("6. PATHLIB - СУЧАСНИЙ СПОСІБ (замість os.path)")
print("=" * 70)

def get_data_file_info(filename: str) -> dict:
    """
    Отримує інформацію про файл даних
    
    Args:
        filename: Назва файлу
    
    Returns:
        dict: Інформація про файл
    """
    # Pathlib - сучасний спосіб (Python 3.4+)
    filepath = Path(filename)
    
    return {
        'filename': filepath.name,
        'extension': filepath.suffix,
        'stem': filepath.stem,  # Назва без розширення
        'parent': str(filepath.parent),
        'absolute': str(filepath.absolute()),
        'exists': filepath.exists(),
        'is_csv': filepath.suffix == '.csv',
        'is_json': filepath.suffix == '.json'
    }


# Приклади з різними файлами
files = [
    'data/train.csv',
    'models/random_forest.pkl',
    'configs/settings.json'
]

for file in files:
    info = get_data_file_info(file)
    print(f"\n📁 {info['filename']}:")
    print(f"   Тип: {info['extension']}")
    print(f"   CSV: {info['is_csv']}, JSON: {info['is_json']}")


# ============================================================================
# 7. WALRUS OPERATOR - СУЧАСНИЙ PYTHON (3.8+)
# ============================================================================

print("\n" + "=" * 70)
print("7. WALRUS OPERATOR := (Python 3.8+)")
print("=" * 70)

def process_data_batch(data: list[int], threshold: int = 100) -> dict:
    """
    Обробляє batch даних з використанням walrus operator
    
    Walrus operator (:=) дозволяє присвоєння в виразах
    """
    results = []
    
    # Старий спосіб:
    # filtered_data = [x for x in data if x > threshold]
    # if len(filtered_data) > 0:
    #     results = filtered_data
    
    # Новий спосіб з walrus:
    if (n := len([x for x in data if x > threshold])) > 0:
        print(f"✅ Знайдено {n} записів > {threshold}")
        results = [x for x in data if x > threshold]
    else:
        print(f"❌ Немає записів > {threshold}")
    
    # Walrus в list comprehension
    return {
        'total': len(data),
        'mean': (total := sum(data)) / len(data),  # Walrus!
        'sum': total,  # Можемо використати знову
        'filtered': len(results)
    }


# Тест
sample_data = [50, 150, 200, 30, 175, 80, 250]
result = process_data_batch(sample_data, threshold=100)
print(f"\nРезультати: {result}")


# ============================================================================
# 8. TYPE HINTS - СУЧАСНА ПРАКТИКА
# ============================================================================

print("\n" + "=" * 70)
print("8. TYPE HINTS (Python 3.5+ / 3.10+ для unions)")
print("=" * 70)

def calculate_metrics(
    predictions: list[int | float],
    actuals: list[int | float]
) -> dict[str, float]:
    """
    Обчислює метрики моделі
    
    Args:
        predictions: Передбачення моделі
        actuals: Реальні значення
    
    Returns:
        Словник з метриками
        
    Note:
        - list[int | float] - Python 3.10+ синтаксис
        - Замість Union[int, float] з typing
    """
    if len(predictions) != len(actuals):
        raise ValueError("Різна кількість елементів")
    
    # Mean Absolute Error
    mae = sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(predictions)
    
    # Mean Squared Error
    mse = sum((p - a) ** 2 for p, a in zip(predictions, actuals)) / len(predictions)
    
    # R² Score (simplified)
    mean_actual = sum(actuals) / len(actuals)
    ss_tot = sum((a - mean_actual) ** 2 for a in actuals)
    ss_res = sum((a - p) ** 2 for a, p in zip(actuals, predictions))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': mse ** 0.5,
        'r2': r2
    }


# Тест
y_pred = [100, 150, 200, 250]
y_true = [110, 145, 210, 240]

metrics = calculate_metrics(y_pred, y_true)
print("\nМетрики моделі:")
for metric, value in metrics.items():
    print(f"  {metric.upper()}: {value:.4f}")


# ============================================================================
# 9. ПРАКТИЧНИЙ ПРИКЛАД: DATA QUALITY CHECK
# ============================================================================

print("\n" + "=" * 70)
print("9. DATA QUALITY CHECKER")
print("=" * 70)

def check_data_quality(data: dict[str, list]) -> dict:
    """
    Перевіряє якість датасету
    
    Args:
        data: Словник з колонками та їх значеннями
    
    Returns:
        Звіт про якість даних
    """
    report = {
        'total_columns': len(data),
        'columns': {}
    }
    
    for column_name, values in data.items():
        # Підрахунок missing values
        none_count = values.count(None)
        empty_count = sum(1 for v in values if v == '')
        missing_count = none_count + empty_count
        
        # Статистика
        report['columns'][column_name] = {
            'total': len(values),
            'missing': missing_count,
            'missing_pct': (missing_count / len(values) * 100) if values else 0,
            'filled': len(values) - missing_count,
            'unique': len(set(v for v in values if v not in [None, '']))
        }
    
    return report


# Приклад з реальними даними
dataset = {
    'user_id': [1, 2, 3, 4, 5],
    'age': [25, None, 30, 28, None],
    'city': ['Kyiv', 'Lviv', '', 'Kharkiv', 'Odesa'],
    'salary': [50000, 45000, None, 60000, 55000]
}

quality_report = check_data_quality(dataset)

print("\n📊 Data Quality Report:")
print(f"Загальна кількість колонок: {quality_report['total_columns']}")
print("\nДеталі по колонках:")

for col, stats in quality_report['columns'].items():
    print(f"\n  {col}:")
    print(f"    Заповнено: {stats['filled']}/{stats['total']}")
    print(f"    Відсутні: {stats['missing']} ({stats['missing_pct']:.1f}%)")
    print(f"    Унікальні: {stats['unique']}")


# ============================================================================
# 10. LOGGING BASICS - ПРОФЕСІЙНИЙ ПІДХІД
# ============================================================================

print("\n" + "=" * 70)
print("10. ЛОГУВАННЯ ЗАМІСТЬ PRINT (професійний підхід)")
print("=" * 70)

import logging

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def process_data_with_logging(data: list[int]) -> dict:
    """
    Обробляє дані з професійним логуванням
    
    Замість print() використовуємо logging для production code
    """
    logger.info(f"Початок обробки {len(data)} записів")
    
    # Валідація
    if not data:
        logger.warning("Отримано пустий список")
        return {'error': 'Empty data'}
    
    # Обробка
    try:
        result = {
            'count': len(data),
            'sum': sum(data),
            'avg': sum(data) / len(data)
        }
        logger.info(f"Оброблено успішно. Середнє: {result['avg']:.2f}")
        return result
        
    except Exception as e:
        logger.error(f"Помилка обробки: {e}")
        raise


# Тест
try:
    result = process_data_with_logging([10, 20, 30, 40, 50])
    print(f"\nРезультат: {result}")
except Exception as e:
    print(f"Помилка: {e}")


# ============================================================================
# ПІДСУМОК
# ============================================================================

print("\n" + "=" * 70)
print("ПІДСУМОК: СУЧАСНІ ПРАКТИКИ PYTHON")
print("=" * 70)

summary = """
✅ F-strings з = для debugging:
   print(f"{variable=}")

✅ Type hints (Python 3.10+):
   def func(x: int | float) -> dict[str, float]

✅ Walrus operator :=
   if (n := len(data)) > 10:

✅ Pathlib замість os.path:
   path = Path("data.csv")

✅ Logging замість print для production:
   logger.info("Processing data...")

✅ Data validation patterns:
   - Return tuple (is_valid, value, message)
   - Early returns для помилок

✅ JSON для структурованих даних:
   - API responses
   - Конфігурації
   - ML pipelines

✅ Docstrings з типами:
   - Args, Returns, Examples
   - Google/NumPy style

🎯 Для Data Science/Engineering:
   - Валідація даних
   - ETL patterns
   - Quality checks
   - Metrics calculation
   - Professional logging
"""

print(summary)

print("\n✨ Тепер ви знаєте сучасні практики Python! ✨\n")
