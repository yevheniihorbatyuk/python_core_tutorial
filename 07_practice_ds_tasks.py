"""
Модуль 2.5: Практичні завдання для DS/DE
==========================================

Real-world Data Science/Engineering challenges
"""

from typing import Any
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# БЛОК 1: DATA CLEANING & VALIDATION
# ============================================================================

print("=" * 70)
print("БЛОК 1: DATA CLEANING & VALIDATION")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 1.1: Email Validator
# ----------------------------------------------------------------------------

def validate_email(email: str) -> tuple[bool, str]:
    """
    Валідує email адресу
    
    Requirements:
    - Має містити @ та .
    - Домен має бути після @
    - TLD (top-level domain) має бути після .
    
    Args:
        email: Email для валідації
    
    Returns:
        tuple: (is_valid, message)
    
    Examples:
        >>> validate_email("user@example.com")
        (True, "Valid email")
        >>> validate_email("invalid@")
        (False, "Missing domain")
    """
    # TODO: Реалізуйте валідацію
    
    # Базова перевірка
    if '@' not in email:
        return False, "Missing @ symbol"
    
    if email.count('@') > 1:
        return False, "Multiple @ symbols"
    
    local, domain = email.split('@')
    
    if not local:
        return False, "Missing local part"
    
    if not domain:
        return False, "Missing domain"
    
    if '.' not in domain:
        return False, "Missing TLD"
    
    return True, "Valid email"


# Тести
print("\n--- Завдання 1.1: Email Validator ---")
test_emails = [
    "valid@example.com",
    "user.name@company.co.uk",
    "invalid@",
    "@nodomain.com",
    "no-at-sign.com",
    "multiple@@at.com"
]

for email in test_emails:
    is_valid, message = validate_email(email)
    status = "✅" if is_valid else "❌"
    print(f"{status} {email:30s} → {message}")


# ----------------------------------------------------------------------------
# Завдання 1.2: Data Quality Checker
# ----------------------------------------------------------------------------

def check_missing_values(data: list[dict]) -> dict[str, Any]:
    """
    Аналізує missing values в датасеті
    
    Args:
        data: Список словників з даними
    
    Returns:
        dict: Статистика по missing values
    
    Example:
        >>> data = [
        ...     {"name": "John", "age": 30, "city": None},
        ...     {"name": "Jane", "age": None, "city": "Kyiv"}
        ... ]
        >>> check_missing_values(data)
        {'total_rows': 2, 'columns': {...}}
    """
    # TODO: Реалізуйте аналіз missing values
    
    if not data:
        return {"error": "Empty dataset"}
    
    # Отримуємо всі унікальні ключі
    all_keys = set()
    for record in data:
        all_keys.update(record.keys())
    
    # Аналіз по кожній колонці
    columns_stats = {}
    
    for key in all_keys:
        missing = 0
        none_count = 0
        empty_string = 0
        
        for record in data:
            value = record.get(key)
            if value is None:
                missing += 1
                none_count += 1
            elif value == '':
                missing += 1
                empty_string += 1
        
        columns_stats[key] = {
            'total_missing': missing,
            'missing_pct': (missing / len(data)) * 100,
            'none_count': none_count,
            'empty_string': empty_string
        }
    
    return {
        'total_rows': len(data),
        'total_columns': len(all_keys),
        'columns': columns_stats
    }


# Тест
print("\n--- Завдання 1.2: Data Quality Checker ---")
sample_data = [
    {"id": 1, "name": "Alice", "age": 25, "city": "Kyiv", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "age": None, "city": "Lviv", "email": ""},
    {"id": 3, "name": "Charlie", "age": 30, "city": None, "email": "charlie@example.com"},
    {"id": 4, "name": "", "age": 28, "city": "Kharkiv", "email": None},
]

quality_report = check_missing_values(sample_data)
print(f"Total rows: {quality_report['total_rows']}")
print(f"Total columns: {quality_report['total_columns']}")
print("\nMissing values per column:")
for col, stats in quality_report['columns'].items():
    if stats['total_missing'] > 0:
        print(f"  {col}: {stats['total_missing']} ({stats['missing_pct']:.1f}%) - None: {stats['none_count']}, Empty: {stats['empty_string']}")


# ============================================================================
# БЛОК 2: DATA TRANSFORMATION
# ============================================================================

print("\n" + "=" * 70)
print("БЛОК 2: DATA TRANSFORMATION")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 2.1: Data Normalizer
# ----------------------------------------------------------------------------

def normalize_numerical_data(values: list[float]) -> list[float]:
    """
    Нормалізує дані до діапазону [0, 1]
    Min-Max normalization
    
    Formula: (x - min) / (max - min)
    
    Args:
        values: Список числових значень
    
    Returns:
        list: Нормалізовані значення
    
    Example:
        >>> normalize_numerical_data([10, 20, 30, 40, 50])
        [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    # TODO: Реалізуйте Min-Max normalization
    
    if not values:
        return []
    
    min_val = min(values)
    max_val = max(values)
    
    if max_val == min_val:
        return [0.5] * len(values)  # Всі однакові
    
    normalized = [(v - min_val) / (max_val - min_val) for v in values]
    
    return normalized


# Тест
print("\n--- Завдання 2.1: Data Normalizer ---")
raw_values = [10, 25, 50, 75, 100]
normalized = normalize_numerical_data(raw_values)

print("Оригінал → Нормалізовані:")
for orig, norm in zip(raw_values, normalized):
    print(f"  {orig:6.1f} → {norm:.3f}")


# ----------------------------------------------------------------------------
# Завдання 2.2: Feature Engineering
# ----------------------------------------------------------------------------

def create_age_groups(ages: list[int]) -> dict[str, list[int]]:
    """
    Групує віки за категоріями (feature binning)
    
    Categories:
    - youth: 0-17
    - young_adult: 18-35
    - adult: 36-55
    - senior: 56+
    
    Args:
        ages: Список віків
    
    Returns:
        dict: Словник з категоріями
    
    Example:
        >>> create_age_groups([15, 25, 45, 65])
        {'youth': [15], 'young_adult': [25], 'adult': [45], 'senior': [65]}
    """
    # TODO: Реалізуйте binning
    
    groups = {
        'youth': [],
        'young_adult': [],
        'adult': [],
        'senior': []
    }
    
    for age in ages:
        if age < 18:
            groups['youth'].append(age)
        elif age <= 35:
            groups['young_adult'].append(age)
        elif age <= 55:
            groups['adult'].append(age)
        else:
            groups['senior'].append(age)
    
    return groups


# Тест
print("\n--- Завдання 2.2: Feature Engineering (Age Groups) ---")
test_ages = [15, 22, 28, 35, 40, 52, 60, 70, 8, 45]
age_groups = create_age_groups(test_ages)

for group, ages in age_groups.items():
    if ages:
        print(f"  {group:15s}: {len(ages)} people - {ages}")


# ============================================================================
# БЛОК 3: STATISTICAL ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("БЛОК 3: STATISTICAL ANALYSIS")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 3.1: Basic Statistics
# ----------------------------------------------------------------------------

def calculate_statistics(numbers: list[float]) -> dict[str, float]:
    """
    Обчислює базову статистику
    
    Metrics:
    - mean (середнє)
    - median (медіана)
    - std (стандартне відхилення)
    - variance (дисперсія)
    - min, max
    - range (розмах)
    
    Args:
        numbers: Список чисел
    
    Returns:
        dict: Статистичні метрики
    """
    # TODO: Реалізуйте обчислення статистики
    
    if not numbers:
        return {"error": "Empty list"}
    
    n = len(numbers)
    
    # Mean
    mean = sum(numbers) / n
    
    # Median
    sorted_nums = sorted(numbers)
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # Variance and Std
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std = variance ** 0.5
    
    # Min, Max, Range
    min_val = min(numbers)
    max_val = max(numbers)
    range_val = max_val - min_val
    
    return {
        'count': n,
        'mean': mean,
        'median': median,
        'std': std,
        'variance': variance,
        'min': min_val,
        'max': max_val,
        'range': range_val
    }


# Тест
print("\n--- Завдання 3.1: Basic Statistics ---")
test_numbers = [10, 15, 20, 25, 30, 35, 40, 45, 50]
stats = calculate_statistics(test_numbers)

print("Статистика для:", test_numbers)
for metric, value in stats.items():
    if metric != 'count':
        print(f"  {metric:10s}: {value:.2f}")
    else:
        print(f"  {metric:10s}: {value}")


# ----------------------------------------------------------------------------
# Завдання 3.2: Outlier Detection
# ----------------------------------------------------------------------------

def detect_outliers_iqr(data: list[float]) -> dict[str, Any]:
    """
    Виявляє outliers методом IQR (Interquartile Range)
    
    Method:
    - Q1 = 25th percentile
    - Q3 = 75th percentile
    - IQR = Q3 - Q1
    - Lower bound = Q1 - 1.5 * IQR
    - Upper bound = Q3 + 1.5 * IQR
    
    Args:
        data: Список числових значень
    
    Returns:
        dict: Інформація про outliers
    """
    # TODO: Реалізуйте IQR метод
    
    if not data:
        return {"error": "Empty data"}
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # Calculate Q1 and Q3
    q1_idx = n // 4
    q3_idx = 3 * n // 4
    
    q1 = sorted_data[q1_idx]
    q3 = sorted_data[q3_idx]
    
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # Find outliers
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    normal = [x for x in data if lower_bound <= x <= upper_bound]
    
    return {
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers,
        'outlier_count': len(outliers),
        'outlier_percentage': (len(outliers) / len(data)) * 100,
        'normal_count': len(normal)
    }


# Тест
print("\n--- Завдання 3.2: Outlier Detection ---")
# Дані з outliers
test_data = [10, 12, 15, 18, 20, 22, 25, 28, 30, 100, 150]  # 100 і 150 - outliers

outlier_analysis = detect_outliers_iqr(test_data)

print("Дані:", test_data)
print(f"\nIQR Analysis:")
print(f"  Q1: {outlier_analysis['q1']}")
print(f"  Q3: {outlier_analysis['q3']}")
print(f"  IQR: {outlier_analysis['iqr']}")
print(f"  Bounds: [{outlier_analysis['lower_bound']:.1f}, {outlier_analysis['upper_bound']:.1f}]")
print(f"  Outliers: {outlier_analysis['outliers']} ({outlier_analysis['outlier_percentage']:.1f}%)")


# ============================================================================
# БЛОК 4: TIME SERIES BASICS
# ============================================================================

print("\n" + "=" * 70)
print("БЛОК 4: TIME SERIES BASICS")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 4.1: Moving Average
# ----------------------------------------------------------------------------

def calculate_moving_average(values: list[float], window: int) -> list[float]:
    """
    Обчислює moving average (ковзне середнє)
    
    Використовується для:
    - Згладжування даних
    - Trend detection
    - Noise reduction
    
    Args:
        values: Часовий ряд
        window: Розмір вікна
    
    Returns:
        list: Moving averages
    
    Example:
        >>> calculate_moving_average([1, 2, 3, 4, 5], 3)
        [2.0, 3.0, 4.0]
    """
    # TODO: Реалізуйте moving average
    
    if len(values) < window:
        return []
    
    moving_averages = []
    
    for i in range(len(values) - window + 1):
        window_values = values[i:i + window]
        avg = sum(window_values) / window
        moving_averages.append(avg)
    
    return moving_averages


# Тест
print("\n--- Завдання 4.1: Moving Average ---")
time_series = [10, 15, 13, 17, 20, 18, 22, 25, 23, 28]
window_size = 3

ma = calculate_moving_average(time_series, window_size)

print(f"Original series: {time_series}")
print(f"Moving average (window={window_size}): {[f'{v:.1f}' for v in ma]}")


# ----------------------------------------------------------------------------
# Завдання 4.2: Growth Rate Calculator
# ----------------------------------------------------------------------------

def calculate_growth_rates(values: list[float]) -> list[float]:
    """
    Обчислює growth rate (темп зростання) між послідовними значеннями
    
    Formula: ((new - old) / old) * 100
    
    Args:
        values: Список значень в часі
    
    Returns:
        list: Growth rates (%)
    
    Example:
        >>> calculate_growth_rates([100, 110, 121])
        [10.0, 10.0]
    """
    # TODO: Реалізуйте обчислення growth rate
    
    if len(values) < 2:
        return []
    
    growth_rates = []
    
    for i in range(1, len(values)):
        old_value = values[i-1]
        new_value = values[i]
        
        if old_value == 0:
            growth_rates.append(float('inf') if new_value > 0 else 0)
        else:
            growth_rate = ((new_value - old_value) / old_value) * 100
            growth_rates.append(growth_rate)
    
    return growth_rates


# Тест
print("\n--- Завдання 4.2: Growth Rate ---")
revenue = [100, 110, 125, 120, 135, 150]
growth = calculate_growth_rates(revenue)

print("Revenue progression:")
for i, (rev, rate) in enumerate(zip(revenue[1:], growth), 1):
    print(f"  Period {i}: ${rev} (growth: {rate:+.1f}%)")


# ============================================================================
# БЛОК 5: DATA AGGREGATION
# ============================================================================

print("\n" + "=" * 70)
print("БЛОК 5: DATA AGGREGATION")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 5.1: Group By and Aggregate
# ----------------------------------------------------------------------------

def group_and_aggregate(
    data: list[dict],
    group_by: str,
    agg_column: str,
    agg_func: str = 'sum'
) -> dict[Any, float]:
    """
    Групує дані та агрегує
    
    Args:
        data: Список словників
        group_by: Колонка для групування
        agg_column: Колонка для агрегації
        agg_func: Функція агрегації ('sum', 'avg', 'count', 'max', 'min')
    
    Returns:
        dict: Згруповані та агреговані дані
    
    Example:
        >>> data = [
        ...     {'city': 'Kyiv', 'sales': 100},
        ...     {'city': 'Kyiv', 'sales': 150},
        ...     {'city': 'Lviv', 'sales': 200}
        ... ]
        >>> group_and_aggregate(data, 'city', 'sales', 'sum')
        {'Kyiv': 250, 'Lviv': 200}
    """
    # TODO: Реалізуйте groupby та aggregation
    
    # Групуємо дані
    groups = {}
    
    for record in data:
        key = record.get(group_by)
        value = record.get(agg_column)
        
        if key is None or value is None:
            continue
        
        if key not in groups:
            groups[key] = []
        
        groups[key].append(value)
    
    # Агрегуємо
    result = {}
    
    for key, values in groups.items():
        if agg_func == 'sum':
            result[key] = sum(values)
        elif agg_func == 'avg':
            result[key] = sum(values) / len(values)
        elif agg_func == 'count':
            result[key] = len(values)
        elif agg_func == 'max':
            result[key] = max(values)
        elif agg_func == 'min':
            result[key] = min(values)
        else:
            result[key] = sum(values)  # default
    
    return result


# Тест
print("\n--- Завдання 5.1: Group By and Aggregate ---")
sales_data = [
    {'city': 'Kyiv', 'product': 'A', 'sales': 100},
    {'city': 'Kyiv', 'product': 'B', 'sales': 150},
    {'city': 'Lviv', 'product': 'A', 'sales': 200},
    {'city': 'Lviv', 'product': 'B', 'sales': 120},
    {'city': 'Kharkiv', 'product': 'A', 'sales': 180},
]

# Group by city
city_sales = group_and_aggregate(sales_data, 'city', 'sales', 'sum')
print("Total sales by city:")
for city, total in city_sales.items():
    print(f"  {city}: ${total}")

# Average sales by product
product_avg = group_and_aggregate(sales_data, 'product', 'sales', 'avg')
print("\nAverage sales by product:")
for product, avg in product_avg.items():
    print(f"  Product {product}: ${avg:.2f}")


# ============================================================================
# БЛОК 6: ADVANCED CHALLENGE
# ============================================================================

print("\n" + "=" * 70)
print("БЛОК 6: ADVANCED CHALLENGE - RFM ANALYSIS")
print("=" * 70)

# ----------------------------------------------------------------------------
# Завдання 6: RFM Score Calculator (Customer Segmentation)
# ----------------------------------------------------------------------------

def calculate_rfm_score(transactions: list[dict]) -> dict[int, dict]:
    """
    Обчислює RFM (Recency, Frequency, Monetary) score для сегментації клієнтів
    
    RFM метрики:
    - Recency: Скільки днів назад була остання покупка
    - Frequency: Скільки покупок зробив клієнт
    - Monetary: Загальна сума покупок
    
    Args:
        transactions: Список транзакцій з полями:
            - customer_id
            - date (YYYY-MM-DD)
            - amount
    
    Returns:
        dict: RFM scores по клієнтам
    
    Example:
        >>> transactions = [
        ...     {'customer_id': 1, 'date': '2024-10-20', 'amount': 100},
        ...     {'customer_id': 1, 'date': '2024-10-22', 'amount': 150},
        ...     {'customer_id': 2, 'date': '2024-09-15', 'amount': 200}
        ... ]
        >>> calculate_rfm_score(transactions)
        {1: {'recency': 1, 'frequency': 2, 'monetary': 250}, ...}
    """
    # TODO: Реалізуйте RFM аналіз
    
    from datetime import datetime
    
    # Сьогоднішня дата (для розрахунку recency)
    today = datetime(2024, 10, 23)
    
    # Групуємо транзакції по клієнтам
    customer_data = {}
    
    for transaction in transactions:
        customer_id = transaction['customer_id']
        date = datetime.strptime(transaction['date'], '%Y-%m-%d')
        amount = transaction['amount']
        
        if customer_id not in customer_data:
            customer_data[customer_id] = {
                'dates': [],
                'amounts': []
            }
        
        customer_data[customer_id]['dates'].append(date)
        customer_data[customer_id]['amounts'].append(amount)
    
    # Обчислюємо RFM
    rfm_scores = {}
    
    for customer_id, data in customer_data.items():
        # Recency: днів з останньої покупки
        last_purchase = max(data['dates'])
        recency = (today - last_purchase).days
        
        # Frequency: кількість покупок
        frequency = len(data['dates'])
        
        # Monetary: загальна сума
        monetary = sum(data['amounts'])
        
        rfm_scores[customer_id] = {
            'recency': recency,
            'frequency': frequency,
            'monetary': monetary
        }
    
    return rfm_scores


# Тест
print("\n--- Завдання 6: RFM Analysis ---")
customer_transactions = [
    {'customer_id': 1, 'date': '2024-10-22', 'amount': 100},
    {'customer_id': 1, 'date': '2024-10-20', 'amount': 150},
    {'customer_id': 1, 'date': '2024-10-15', 'amount': 200},
    
    {'customer_id': 2, 'date': '2024-10-23', 'amount': 300},
    {'customer_id': 2, 'date': '2024-10-10', 'amount': 250},
    
    {'customer_id': 3, 'date': '2024-09-15', 'amount': 500},
]

rfm_results = calculate_rfm_score(customer_transactions)

print("RFM Analysis Results:")
print(f"{'Customer':<12} {'Recency':<10} {'Frequency':<12} {'Monetary':<12}")
print("-" * 50)

for customer_id, scores in rfm_results.items():
    print(f"{customer_id:<12} {scores['recency']:<10} {scores['frequency']:<12} ${scores['monetary']:<11}")

# Сегментація
print("\nCustomer Segments:")
for customer_id, scores in rfm_results.items():
    if scores['recency'] <= 7 and scores['frequency'] >= 2 and scores['monetary'] >= 300:
        segment = "VIP Customer"
    elif scores['recency'] <= 14:
        segment = "Active Customer"
    elif scores['recency'] <= 30:
        segment = "At Risk"
    else:
        segment = "Lost Customer"
    
    print(f"  Customer {customer_id}: {segment}")


# ============================================================================
# ПІДСУМОК ТА ОЦІНЮВАННЯ
# ============================================================================

print("\n" + "=" * 70)
print("ПІДСУМОК")
print("=" * 70)

summary = """
✅ ВИ ПОПРАКТИКУВАЛИ:

БЛОК 1 - Data Cleaning & Validation:
  - Email validation
  - Data quality checks
  - Missing values analysis

БЛОК 2 - Data Transformation:
  - Min-Max normalization
  - Feature engineering (binning)
  - Data preprocessing

БЛОК 3 - Statistical Analysis:
  - Descriptive statistics
  - Outlier detection (IQR method)
  - Distribution analysis

БЛОК 4 - Time Series:
  - Moving averages
  - Growth rates
  - Trend analysis

БЛОК 5 - Data Aggregation:
  - GroupBy operations
  - Aggregation functions
  - Data summarization

БЛОК 6 - Advanced:
  - RFM Analysis
  - Customer segmentation
  - Business metrics

🎯 РЕАЛЬНІ DS/DE НАВИЧКИ:
  - Data validation patterns
  - Feature engineering
  - Statistical analysis
  - Time series basics
  - Customer analytics
  - Production-ready code

📚 ЩО ДАЛІ:
  - Pandas для data manipulation
  - NumPy для numerical computing
  - Scikit-learn для ML
  - SQL для баз даних
"""

print(summary)

print("\n✨ Ви готові до роботи з реальними даними! ✨\n")
