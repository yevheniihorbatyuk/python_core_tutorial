# 🆚 Базова vs Modern версія - Що обрати?

## 📦 У вас є 2 версії матеріалів

### 📘 Базова версія (для всіх)
```
03_input_output.py
04_functions.py
05_strings.py
06_debugging.py
07_practice_tasks.py
```

### 🚀 Modern версія (DS/DE focus)
```
03_modern_input_output.py
04_modern_functions.py
05_modern_strings.py
07_practice_ds_tasks.py
```

---

## 🤔 Яку версію обрати?

### ✅ Базову версію, якщо:

- Студенти **початківці** в програмуванні
- Потрібні **прості, зрозумілі приклади**
- Фокус на **основах Python**


**Приклади з базової версії:**
```python
# Проста функція привітання
def greet(name):
    print(f"Привіт, {name}!")

# Пошук літери в тексті
def find_letter(text, letter):
    return letter in text

# Площа трикутника
def triangle_area(base, height):
    return (base * height) / 2
```

### 🚀 Modern версію, якщо:

- Студенти **мають базу програмування**
- Цільова аудиторія: **майбутні DS/DE**
- Потрібні **прикладні, реальні задачі**
- Студенти **технічного профілю**


**Приклади з modern версії:**
```python
# Data validation з type hints
def validate_email(email: str) -> tuple[bool, str]:
    if '@' not in email:
        return False, "Missing @ symbol"
    return True, "Valid email"

# Decorator для timing
@timing_decorator
def process_large_dataset(n: int) -> int:
    return sum(range(n))

# RFM Analysis для customer segmentation
def calculate_rfm_score(transactions: list[dict]) -> dict[int, dict]:
    # Real business logic
    pass
```

---

## 📊 Детальне порівняння

| Аспект | Базова версія | Modern версія |
|--------|---------------|---------------|
| **Рівень** | Початківці | Середній |
| **Приклади** | Абстрактні (площа, привітання) | Реальні (data cleaning, RFM) |
| **Python features** | 3.8+ basics | 3.10+ modern (match-case, \| types) |
| **Type hints** | Мінімальні | Обов'язкові всюди |
| **Задачі** | Прості алгоритми | DS/DE challenges |
| **Фокус** | Синтаксис | Практичне застосування |
| **Складність** | ⭐⭐ | ⭐⭐⭐⭐ |

---

## 📖 Приклади по темах

### 1️⃣ Input/Output

**Базова:**
```python
# Простий input/output
name = input("Ваше ім'я: ")
print(f"Привіт, {name}!")

# Калькулятор
num1 = float(input("Перше число: "))
num2 = float(input("Друге число: "))
result = num1 + num2
print(f"Результат: {result}")
```

**Modern:**
```python
# F-strings debugging (Python 3.8+)
user_id = 12345
print(f"{user_id=}")  # user_id=12345

# Data validation
def validate_age(age: int | str) -> tuple[bool, int | None, str]:
    try:
        age_int = int(age)
        if age_int < 0:
            return False, None, "Negative age"
        return True, age_int, "Valid"
    except ValueError:
        return False, None, "Not a number"

# ETL-like transformation
def clean_salary_string(salary: str) -> float:
    cleaned = salary.replace(',', '').replace('$', '')
    if 'k' in cleaned.lower():
        return float(cleaned.replace('k', '')) * 1000
    return float(cleaned)
```

### 2️⃣ Functions

**Базова:**
```python
# Проста функція
def add_numbers(a, b):
    return a + b

# Функція з параметром за замовчуванням
def greet(name, greeting="Привіт"):
    print(f"{greeting}, {name}!")

# Повернення декількох значень
def divide_with_remainder(a, b):
    return a // b, a % b
```

**Modern:**
```python
# Декоратор для timing
@timing_decorator
def process_data(data: list[int]) -> dict:
    return {"sum": sum(data), "count": len(data)}

# Generator для великих даних
def read_large_file(n: int):
    for i in range(n):
        yield process_line(i)

# Match-case (Python 3.10+)
def route_data(data: dict) -> str:
    match data:
        case {"type": "csv", "path": path}:
            return f"Processing CSV: {path}"
        case {"type": "json", "path": path}:
            return f"Processing JSON: {path}"

# Dataclass
@dataclass
class ModelMetrics:
    accuracy: float
    f1_score: float
    
    @property
    def is_good(self) -> bool:
        return self.f1_score > 0.8
```

### 3️⃣ Strings

**Базова:**
```python
# Базові методи
text = "Hello World"
print(text.upper())
print(text.lower())
print(text.find("o"))

# Проста заміна
text = text.replace("World", "Python")

# Split та join
words = text.split()
joined = "-".join(words)
```

**Modern:**
```python
# Regex для data cleaning
import re

def clean_phone(phone: str) -> str | None:
    pattern = r'^(\+380|380|0)(\d{9})$'
    match = re.match(pattern, phone)
    return f"+380{match.group(2)}" if match else None

# Text preprocessing для NLP
def preprocess_text(text: str) -> dict:
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Tokenize
    tokens = text.lower().split()
    return {"tokens": tokens, "count": len(tokens)}

# String similarity (fuzzy matching)
def levenshtein_distance(s1: str, s2: str) -> int:
    # Використовується для deduplication
    pass

# Unicode handling
def remove_accents(text: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])
```

### 4️⃣ Practice Tasks

**Базова:**
```python
# Пошук літери
def find_letter(text: str, letter: str) -> bool:
    return letter in text

# Площа фігур
def triangle_area(base: float, height: float) -> float:
    return (base * height) / 2

# Калькулятор ІМТ
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)

# Паліндром
def is_palindrome(text: str) -> bool:
    return text == text[::-1]
```

**Modern:**
```python
# Data quality check
def check_missing_values(data: list[dict]) -> dict:
    # Аналізує missing values по колонках
    # Повертає статистику
    pass

# Min-Max normalization
def normalize_data(values: list[float]) -> list[float]:
    min_val, max_val = min(values), max(values)
    return [(v - min_val) / (max_val - min_val) for v in values]

# Feature engineering
def create_age_groups(ages: list[int]) -> dict[str, list[int]]:
    # Binning ages into categories
    pass

# Outlier detection
def detect_outliers_iqr(data: list[float]) -> dict:
    # IQR method для виявлення outliers
    pass

# Time series
def calculate_moving_average(values: list[float], window: int) -> list[float]:
    # Moving average для згладжування
    pass

# Customer segmentation
def calculate_rfm_score(transactions: list[dict]) -> dict[int, dict]:
    # RFM analysis для customer analytics
    pass
```

---

## 🎯 Рекомендації

### Для викладача курсу Python:

**Варіант 1: Базова версія**
- ✅ Аудиторія: початківці
- ✅ Фокус: основи синтаксису
- ✅ Після курсу: веб-розробка, автоматизація

**Варіант 2: Modern версія**
- ✅ Аудиторія: студенти технічних вузів
- ✅ Фокус: DS/DE практики
- ✅ Після курсу: data science, ML, DE

**Варіант 3: Гібрид**
- ✅ Базова версія (основи)
- ✅ Modern версія (поглиблення)
- ✅ Найкращий варіант для змішаної аудиторії!


**Якщо ви новачок:**
1. Почніть з базової версії
2. Виконайте всі завдання
3. Переходьте до modern версії

**Якщо маєте досвід:**
1. Одразу до modern версії
2. Базову як reference

---

## 📁 Як використовувати обидві версії?

### Структура навчання:

```
 1: Git + VSCode + Python basics
├── 01_git_github_guide.md
├── 02_vscode_setup_guide.md
└── 03_input_output.py (базова)

 2: Functions basics
├── 04_functions.py (базова)
└── 06_debugging.py

 3: Modern approaches (якщо є час)
├── 03_modern_input_output.py
├── 04_modern_functions.py
└── 05_modern_strings.py

 4: Practice
├── 07_practice_tasks.py (базова)
└── 07_practice_ds_tasks.py (modern)
```

---

## 💡 Поради

### Якщо обираєте базову:
- ✅ Додайте більше часу на практику
- ✅ Дайте більше simple exercises
- ✅ Фокус на debugging skills
- ✅ Заохочуйте експерименти

### Якщо обираєте modern:
- ✅ Переконайтесь що Python 3.10+
- ✅ Поясніть чому type hints важливі
- ✅ Покажіть реальні use cases
- ✅ Дайте проєктні завдання

---

## 🎓 Висновок

**Базова версія** = 📘 Міцний фундамент  
**Modern версія** = 🚀 Прикладні навички

**Обидві версії важливі!** Ідеально - пройти обидві. 💯

---

**Успіхів у навчанні! 📚💻**
