# 🚀 Модуль 2: Сучасний Python для Data Science/Engineering

## 📚 Про модуль (оновлена версія)

Цей модуль навчає **сучасним практикам Python** з акцентом на **реальні задачі Data Science/Engineering**. Матеріали включають найновіші фічі Python 3.10-3.13 та industry best practices.

---

## ✨ Що нового в цій версії?

### 🆕 Сучасні Python features:

- **Python 3.10+**: Union types (`int | float`), Match-case
- **Python 3.11**: Improved error messages, faster execution
- **Python 3.12**: F-string improvements
- **Python 3.13 preview**: Template strings (T-strings) concepts

### 💼 DS/DE Focus:

- Реальні приклади з data science
- Production-ready patterns
- Industry best practices
- Practical ML/DE scenarios

### 🎯 Прикладні завдання:

- Data cleaning pipelines
- Feature engineering
- Statistical analysis
- Time series basics
- Customer segmentation (RFM)

---

## 📂 Структура матеріалів

```
module-2-modern/
│
├── START_HERE.md                    # 🎯 Почніть звідси!
├── README.md                        # Цей файл
│
├── 00_lesson_plan.md                # План заняття
├── 01_git_github_guide.md           # Git/GitHub
├── 02_vscode_setup_guide.md         # VSCode
│
├── 03_modern_input_output.py        # 🆕 Сучасний I/O + data validation
├── 04_modern_functions.py           # 🆕 Advanced functions + decorators
├── 05_modern_strings.py             # 🆕 String processing + regex
├── 06_debugging.py                  # Debugging (базовий)
│
└── 07_practice_ds_tasks.py          # 🆕 Real-world DS/DE challenges
```

---

## 🎓 Ключові теми

### 1️⃣ Сучасний Input/Output (03_modern_input_output.py)

**Що нового:**
```python
# F-strings з = для debugging (Python 3.8+)
x = 42
print(f"{x=}")  # x=42

# Union types без typing import (Python 3.10+)
def func(value: int | float) -> str:
    pass

# Walrus operator := (Python 3.8+)
if (n := len(data)) > 100:
    print(f"Large dataset: {n} records")

# Type hints в сучасному стилі
def process(data: list[dict[str, int | float]]) -> dict[str, Any]:
    pass
```

**Практичні приклади:**
- Data validation patterns
- JSON operations
- ETL-like transformations
- Pathlib (замість os.path)
- Professional logging
- Data quality checks

### 2️⃣ Advanced Functions (04_modern_functions.py)

**Що нового:**
```python
# Декоратори для timing
@timing_decorator
def process_data():
    pass

# LRU Cache для оптимізації
@lru_cache(maxsize=128)
def expensive_calculation(n):
    pass

# Generators для великих даних
def read_large_file():
    for line in file:
        yield process(line)

# Match-case (Python 3.10+)
match data:
    case {"type": "csv", "path": path}:
        process_csv(path)
    case {"type": "json", "path": path}:
        process_json(path)

# Dataclasses (Python 3.7+)
@dataclass
class ModelMetrics:
    accuracy: float
    f1_score: float
```

**Практичні приклади:**
- Decorator patterns (timing, logging, caching)
- Generator functions для stream processing
- Pattern matching для data routing
- Dataclasses для структур даних
- Функціональне програмування (map, filter, reduce)
- Pipeline patterns

### 3️⃣ String Processing (05_modern_strings.py)

**Що нового:**
```python
# Regex для data cleaning
import re

def clean_phone(phone: str) -> str | None:
    pattern = r'^(\+380|380|0)(\d{9})$'
    match = re.match(pattern, phone)
    return f"+380{match.group(2)}" if match else None

# Unicode handling
def remove_accents(text: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

# String similarity (Levenshtein distance)
def fuzzy_match(s1: str, s2: str) -> float:
    pass
```

**Практичні приклади:**
- Regex для data extraction
- Data normalization
- Text preprocessing (NLP basics)
- Validation patterns
- String similarity для deduplication
- Unicode handling
- Log parsing

### 4️⃣ Practical DS/DE Tasks (07_practice_ds_tasks.py)

**Real-world challenges:**

1. **Data Cleaning & Validation**
   - Email validation
   - Data quality checks
   - Missing values analysis

2. **Data Transformation**
   - Min-Max normalization
   - Feature engineering (binning)
   - Data preprocessing

3. **Statistical Analysis**
   - Descriptive statistics
   - Outlier detection (IQR)
   - Distribution analysis

4. **Time Series Basics**
   - Moving averages
   - Growth rates
   - Trend analysis

5. **Data Aggregation**
   - GroupBy operations
   - Aggregation functions
   - Data summarization

6. **Advanced Challenge**
   - RFM Analysis (Customer segmentation)
   - Business metrics
   - Customer analytics

---

## 🆕 Python 3.13 Preview: Template Strings

**Примітка:** Template strings (PEP 750) - це нова фіча в Python 3.13 (preview).

### Що таке T-strings?

T-strings (Template strings) - це новий тип рядків для безпечної інтерполяції:

```python
# Поточні f-strings (можуть бути небезпечні для SQL/HTML)
user_input = "'; DROP TABLE users; --"
query = f"SELECT * FROM users WHERE name = '{user_input}'"  # ❌ SQL injection!

# T-strings (Python 3.13+) - автоматичне екранування
query = t"SELECT * FROM users WHERE name = {user_input}"  # ✅ Безпечно!

# HTML templates
html = t"<div>{user_content}</div>"  # ✅ Auto-escaping

# Custom interpolators
sql = sql_t"SELECT {columns} FROM {table} WHERE {condition}"
```

### Переваги T-strings:

- 🛡️ **Безпека**: Автоматичне екранування
- 🎯 **Type-safe**: Перевірка типів на compile time
- 🔧 **Extensible**: Власні інтерполятори
- 📝 **Clear**: Явна вказівка контексту

### Коли використовувати:

- ✅ SQL queries (з автоматичним escaping)
- ✅ HTML templates
- ✅ Shell commands
- ✅ API endpoints
- ✅ Log messages з structured logging

**На даний момент (Python 3.12):**
- Використовуйте parameterized queries для SQL
- Використовуйте template engines для HTML
- T-strings будуть доступні в Python 3.13+

---

## 🛠️ Необхідне програмне забезпечення

### Рекомендовано:
- **Python 3.10+** (для union types та match-case)
- Python 3.11+ (для кращої продуктивності)
- Python 3.12+ (для останніх improvements)

### Мінімальні вимоги:
- Python 3.8+ (для walrus operator та f-string =)

### Додатково:
- Git
- VSCode
- GitHub акаунт

---

## 🎯 Для кого цей курс?

### ✅ Ідеально підходить для:

- Початківців в Python з амбіціями в DS/DE
- Студентів data science
- Тих, хто хоче вивчити сучасний Python

### 💡 Ви навчитесь:

- Писати **production-ready** код
- Використовувати **сучасні Python features**
- Розв'язувати **реальні DS/DE задачі**
- Працювати з **великими даними** (generators)
- Проводити **data analysis**
- Створювати **data pipelines**

---

## 🚀 Швидкий старт

### Для студента:

```bash
# 1. Перевірте версію Python
python --version  # Має бути 3.8+, рекомендовано 3.10+

# 2. Запустіть модулі
python 03_modern_input_output.py
python 04_modern_functions.py
python 05_modern_strings.py

# 3. Виконайте практичні завдання
python 07_practice_ds_tasks.py
```

### Для викладача:

```bash
# 1. Ознайомтесь з планом
open 00_lesson_plan.md

# 2. Перегляньте всі модулі
# 3. Підготуйте live coding примери
# 4. Готові до заняття!
```

---

## 📖 Порядок вивчення

### Тиждень 1: Основи
```
День 1-2: Git/GitHub + VSCode setup
День 3-4: Modern Input/Output (03_modern_input_output.py)
День 5-7: Практика з input/output
```

### Тиждень 2: Functions
```
День 1-3: Modern Functions (04_modern_functions.py)
День 4-5: Декоратори та generators
День 6-7: Match-case та dataclasses
```

### Тиждень 3: Strings
```
День 1-3: String Processing (05_modern_strings.py)
День 4-5: Regex та validation
День 6-7: Text preprocessing
```

### Тиждень 4: Practice
```
День 1-7: Practice DS Tasks (07_practice_ds_tasks.py)
         - Виконання всіх завдань
         - Code review
         - Оптимізація
```

---

## 💻 Код-стиль та Best Practices

### Type Hints (обов'язково!)
```python
# ✅ Good
def process_data(values: list[float]) -> dict[str, float]:
    pass

# ❌ Bad
def process_data(values):
    pass
```

### Docstrings (обов'язково!)
```python
# ✅ Good
def calculate_mean(numbers: list[float]) -> float:
    """
    Обчислює середнє арифметичне.
    
    Args:
        numbers: Список чисел
    
    Returns:
        Середнє значення
    
    Example:
        >>> calculate_mean([1, 2, 3])
        2.0
    """
    return sum(numbers) / len(numbers)
```

### Error Handling
```python
# ✅ Good
def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        logger.error(f"Division by zero: {a} / {b}")
        return None

# ❌ Bad
def divide(a, b):
    return a / b  # Може впасти!
```

---

## 🎓 Критерії успішного завершення

### Обов'язково:
- ✅ Знає сучасний синтаксис Python 3.10+
- ✅ Розуміє decorators та generators
- ✅ Вміє писати type hints
- ✅ Використовує match-case
- ✅ Знає regex basics
- ✅ Може провести data validation
- ✅ Розуміє основи statistics

### Додатково:
- ✅ Використовує dataclasses
- ✅ Знає functional programming patterns
- ✅ Може написати data pipeline
- ✅ Розуміє time series basics
- ✅ Вміє проводити RFM analysis

---

## 📚 Додаткові ресурси

### Офіційна документація:
- [Python 3.12 What's New](https://docs.python.org/3.12/whatsnew/3.12.html)
- [Python 3.13 What's New](https://docs.python.org/3.13/whatsnew/3.13.html)
- [PEP 750 - Template Strings](https://peps.python.org/pep-0750/)
- [Type Hints](https://docs.python.org/3/library/typing.html)

### Для Data Science:
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Real Python - Data Science Tutorials](https://realpython.com/tutorials/data-science/)
- [Kaggle Learn](https://www.kaggle.com/learn)

### Практика:
- [LeetCode](https://leetcode.com) - Алгоритми
- [HackerRank](https://www.hackerrank.com) - Python challenges
- [DataLemur](https://datalemur.com) - DS/DE задачі

---

## 🔥 Що робити після курсу?

### Наступні кроки:

1. **Pandas & NumPy**
   - Data manipulation
   - Numerical computing

2. **Data Visualization**
   - Matplotlib
   - Seaborn
   - Plotly

3. **Machine Learning**
   - Scikit-learn
   - Feature engineering
   - Model training

4. **SQL & Databases**
   - PostgreSQL
   - Database design
   - Query optimization

5. **Big Data Tools**
   - Spark (PySpark)
   - Airflow
   - dbt

---

## 🤝 Внесок та фідбек

### Як покращити матеріали:

- 📝 Створіть issue з пропозиціями
- 🐛 Повідомте про помилки
- ✨ Запропонуйте нові приклади
- 📖 Додайте документацію

### Фідбек:

Напишіть нам:
- Що сподобалось?
- Що складно?
- Чого не вистачає?
- Які приклади додати?

---

## ⚖️ Ліцензія

Матеріали створені для навчальних цілей та можуть бути вільно використані.

---

**Успіхів у вивченні сучасного Python! 🚀💻🐍**

*Версія: 2.0 (Modern DS/DE Edition)*  
*Оновлено: Жовтень 2025*  
*Python: 3.10-3.13*
