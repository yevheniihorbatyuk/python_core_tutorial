"""
Модуль 2.3: Робота з рядками для Data Science/Engineering
==========================================================

String processing, regex, data cleaning patterns
"""

import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import unicodedata
from typing import Any

# ============================================================================
# 1. REGEX - DATA CLEANING
# ============================================================================

print("=" * 70)
print("1. РЕГУЛЯРНІ ВИРАЗИ - DATA CLEANING")
print("=" * 70)

def clean_phone_number(phone: str) -> str | None:
    """
    Очищує та нормалізує телефонний номер
    
    Patterns:
        +380501234567
        050-123-45-67
        (050) 123 45 67
        0501234567
    
    Returns:
        +380501234567 або None
    """
    # Видаляємо всі нечислові символи крім +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Українські номери
    pattern = r'^(\+380|380|0)(\d{9})$'
    match = re.match(pattern, cleaned)
    
    if match:
        prefix, number = match.groups()
        return f"+380{number}"
    
    return None


# Тести
test_phones = [
    "+380501234567",
    "050-123-45-67",
    "(050) 123 45 67",
    "0501234567",
    "invalid"
]

print("Нормалізація телефонних номерів:")
for phone in test_phones:
    cleaned = clean_phone_number(phone)
    status = "✅" if cleaned else "❌"
    print(f"  {status} '{phone}' → {cleaned}")


def extract_emails(text: str) -> list[str]:
    """
    Витягує email адреси з тексту
    Корисно для: web scraping, log analysis
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)


text_sample = """
Контакти:
john.doe@example.com
support@company.co.uk
admin@test-server.com
invalid@email (це не email)
"""

emails = extract_emails(text_sample)
print(f"\nЗнайдені email адреси: {emails}")


# ============================================================================
# 2. DATA NORMALIZATION - CLEANING USER INPUT
# ============================================================================

print("\n" + "=" * 70)
print("2. НОРМАЛІЗАЦІЯ ДАНИХ")
print("=" * 70)

def normalize_company_name(name: str) -> str:
    """
    Нормалізує назви компаній для дедуплікації
    
    Корисно для:
    - Data matching
    - Entity resolution
    - Deduplication
    """
    # Lowercase
    normalized = name.lower()
    
    # Видаляємо юридичні форми
    legal_forms = [
        r'\b(llc|ltd|inc|corp|gmbh|sa|ag|nv|bv|plc)\b\.?',
        r'\b(limited|incorporated|corporation)\b',
        r'\b(товариство з обмеженою відповідальністю|тов|тзов)\b'
    ]
    for pattern in legal_forms:
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    
    # Видаляємо спецсимволи та зайві пробіли
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = ' '.join(normalized.split())
    
    return normalized.strip()


# Тести
companies = [
    "Apple Inc.",
    "Apple Incorporated",
    "APPLE",
    "Google LLC",
    "Google",
    "Microsoft Corporation",
    "Microsoft Corp."
]

print("Нормалізація назв компаній:")
for company in companies:
    normalized = normalize_company_name(company)
    print(f"  '{company}' → '{normalized}'")


# ============================================================================
# 3. PARSING STRUCTURED STRINGS
# ============================================================================

print("\n" + "=" * 70)
print("3. ПАРСИНГ СТРУКТУРОВАНИХ РЯДКІВ")
print("=" * 70)

def parse_log_line(log: str) -> dict | None:
    """
    Парсить рядок з лог файлу
    
    Format: [timestamp] LEVEL: message
    Example: [2024-10-23 14:30:45] ERROR: Database connection failed
    """
    pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+): (.+)'
    match = re.match(pattern, log)
    
    if match:
        timestamp_str, level, message = match.groups()
        return {
            'timestamp': datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'),
            'level': level,
            'message': message
        }
    return None


# Тести
log_lines = [
    "[2024-10-23 14:30:45] ERROR: Database connection failed",
    "[2024-10-23 14:31:12] INFO: Processing batch 1000",
    "[2024-10-23 14:32:00] WARNING: High memory usage",
    "Invalid log line"
]

print("Парсинг log файлів:")
for log in log_lines:
    parsed = parse_log_line(log)
    if parsed:
        print(f"  ✅ {parsed['level']}: {parsed['message'][:30]}...")
    else:
        print(f"  ❌ Не вдалося розпарсити: {log}")


def parse_url_query(url: str) -> dict:
    """
    Парсить параметри з URL
    Корисно для: API logs, web analytics
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    # Конвертуємо list значення в single values
    return {k: v[0] if len(v) == 1 else v for k, v in params.items()}


# Тест
url = "https://api.example.com/search?q=python&category=programming&limit=10&tags=ml&tags=ai"
params = parse_url_query(url)

print(f"\nURL: {url}")
print("Параметри:")
for key, value in params.items():
    print(f"  {key}: {value}")


# ============================================================================
# 4. TEXT PREPROCESSING - NLP BASICS
# ============================================================================

print("\n" + "=" * 70)
print("4. TEXT PREPROCESSING ДЛЯ NLP")
print("=" * 70)

def preprocess_text(text: str, lowercase: bool = True) -> dict:
    """
    Базовий preprocessing тексту
    
    Steps:
    1. Lowercase (optional)
    2. Remove punctuation
    3. Remove extra whitespace
    4. Tokenize
    5. Remove short words
    """
    result = {}
    
    # Original
    result['original'] = text
    
    # Lowercase
    if lowercase:
        text = text.lower()
    result['lowercased'] = text
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    result['no_urls'] = text
    
    # Remove mentions and hashtags (для соц мереж)
    text = re.sub(r'@\w+|#\w+', '', text)
    result['no_mentions'] = text
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    result['no_punctuation'] = text
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    result['cleaned'] = text
    
    # Tokenize
    tokens = text.split()
    result['tokens'] = tokens
    
    # Remove short words (< 3 chars)
    long_tokens = [t for t in tokens if len(t) >= 3]
    result['filtered_tokens'] = long_tokens
    
    # Stats
    result['word_count'] = len(tokens)
    result['unique_words'] = len(set(tokens))
    
    return result


# Тест
tweet = """
Check out this amazing #Python tutorial! 🚀
https://example.com/tutorial @DataScience
It's really helpful for ML beginners!!!
"""

processed = preprocess_text(tweet)

print("Text Preprocessing:")
print(f"Original: {processed['original'][:50]}...")
print(f"Cleaned: {processed['cleaned']}")
print(f"Tokens: {processed['tokens'][:5]}...")
print(f"Word count: {processed['word_count']}")
print(f"Unique words: {processed['unique_words']}")


# ============================================================================
# 5. DATA VALIDATION WITH REGEX
# ============================================================================

print("\n" + "=" * 70)
print("5. ВАЛІДАЦІЯ ДАНИХ")
print("=" * 70)

class DataValidator:
    """Валідатор для різних типів даних"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Валідація email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Валідація IP адреси"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        # Перевірка діапазону
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    @staticmethod
    def is_valid_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Валідація дати"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_credit_card(card: str) -> bool:
        """Валідація номера картки (Luhn algorithm)"""
        # Видаляємо пробіли та дефіси
        card = re.sub(r'[\s-]', '', card)
        
        if not card.isdigit() or len(card) not in [13, 15, 16]:
            return False
        
        # Luhn algorithm
        def luhn_checksum(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10
        
        return luhn_checksum(int(card)) == 0


# Тести
validator = DataValidator()

test_data = {
    'emails': ['valid@example.com', 'invalid@', 'no-at-sign.com'],
    'ips': ['192.168.1.1', '255.255.255.255', '256.1.1.1', '192.168'],
    'dates': ['2024-10-23', '2024-13-45', '10/23/2024'],
    'cards': ['4532015112830366', '1234567890123456', '4532-0151-1283-0366']
}

print("Email валідація:")
for email in test_data['emails']:
    valid = validator.is_valid_email(email)
    print(f"  {'✅' if valid else '❌'} {email}")

print("\nIP адреса валідація:")
for ip in test_data['ips']:
    valid = validator.is_valid_ip(ip)
    print(f"  {'✅' if valid else '❌'} {ip}")

print("\nДата валідація:")
for date in test_data['dates']:
    valid = validator.is_valid_date(date)
    print(f"  {'✅' if valid else '❌'} {date}")


# ============================================================================
# 6. STRING SIMILARITY - DATA MATCHING
# ============================================================================

print("\n" + "=" * 70)
print("6. STRING SIMILARITY - DATA MATCHING")
print("=" * 70)

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Обчислює Levenshtein distance між рядками
    Використовується для:
    - Fuzzy matching
    - Spell checking
    - Record linkage
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity_ratio(s1: str, s2: str) -> float:
    """
    Обчислює similarity ratio [0, 1]
    1.0 = identical, 0.0 = completely different
    """
    distance = levenshtein_distance(s1.lower(), s2.lower())
    max_len = max(len(s1), len(s2))
    
    if max_len == 0:
        return 1.0
    
    return 1 - (distance / max_len)


# Тести
print("String Similarity (Fuzzy Matching):")

# Знаходження дублікатів компаній
companies = [
    "Microsoft",
    "Microsft",  # Typo
    "Microsoft Corp",
    "Apple Inc",
    "Apple Incorporated"
]

threshold = 0.8
print(f"\nПошук схожих назв (threshold={threshold}):")

for i, company1 in enumerate(companies):
    for company2 in companies[i+1:]:
        similarity = similarity_ratio(company1, company2)
        if similarity >= threshold:
            print(f"  ⚠️  '{company1}' ≈ '{company2}' (similarity: {similarity:.2f})")


# ============================================================================
# 7. UNICODE HANDLING - INTERNATIONALIZATION
# ============================================================================

print("\n" + "=" * 70)
print("7. UNICODE ТА МІЖНАРОДНІ ТЕКСТИ")
print("=" * 70)

def normalize_unicode(text: str) -> str:
    """
    Нормалізує Unicode текст
    Вирішує проблеми з різними представленнями символів
    """
    # NFKD normalization - розкладає складні символи
    normalized = unicodedata.normalize('NFKD', text)
    
    # Видаляємо combining characters (діакритичні знаки)
    ascii_text = ''.join(c for c in normalized if not unicodedata.combining(c))
    
    return ascii_text


def remove_accents(text: str) -> str:
    """
    Видаляє акценти (для пошуку)
    café → cafe
    """
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


# Тести
international_texts = [
    "Café",
    "naïve",
    "Zürich",
    "Москва",
    "日本",  # Японська
    "العربية"  # Арабська
]

print("Unicode normalization:")
for text in international_texts:
    normalized = remove_accents(text)
    print(f"  '{text}' → '{normalized}'")


# ============================================================================
# 8. STRING FORMATTING - REPORTS AND OUTPUTS
# ============================================================================

print("\n" + "=" * 70)
print("8. ФОРМАТУВАННЯ ДЛЯ ЗВІТІВ")
print("=" * 70)

def format_table(data: list[dict], columns: list[str]) -> str:
    """
    Форматує дані в ASCII таблицю
    Корисно для CLI tools та звітів
    """
    if not data:
        return "No data"
    
    # Знаходимо максимальну ширину для кожної колонки
    col_widths = {col: len(col) for col in columns}
    
    for row in data:
        for col in columns:
            value = str(row.get(col, ''))
            col_widths[col] = max(col_widths[col], len(value))
    
    # Створюємо роздільник
    separator = "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+"
    
    # Заголовок
    header = "|" + "|".join(f" {col:{col_widths[col]}} " for col in columns) + "|"
    
    # Рядки
    rows = []
    for row in data:
        row_str = "|" + "|".join(
            f" {str(row.get(col, '')):{col_widths[col]}} " for col in columns
        ) + "|"
        rows.append(row_str)
    
    # Збираємо таблицю
    table = [separator, header, separator]
    table.extend(rows)
    table.append(separator)
    
    return "\n".join(table)


# Приклад використання
metrics_data = [
    {"model": "Random Forest", "accuracy": "0.92", "f1": "0.89"},
    {"model": "XGBoost", "accuracy": "0.94", "f1": "0.91"},
    {"model": "Neural Net", "accuracy": "0.96", "f1": "0.94"},
]

table = format_table(metrics_data, ["model", "accuracy", "f1"])
print("\nModel Performance Table:")
print(table)


def format_bytes(bytes_size: int) -> str:
    """Форматує розмір в читабельний вигляд"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


# Тест
sizes = [500, 1500, 1_500_000, 1_500_000_000, 1_500_000_000_000]
print("\nРозміри файлів:")
for size in sizes:
    print(f"  {size:>15,} bytes = {format_bytes(size)}")


# ============================================================================
# 9. TEMPLATE STRINGS - DYNAMIC CONTENT
# ============================================================================

print("\n" + "=" * 70)
print("9. STRING TEMPLATES - ДИНАМІЧНИЙ КОНТЕНТ")
print("=" * 70)

def generate_sql_query(
    table: str,
    columns: list[str],
    conditions: dict[str, Any] | None = None
) -> str:
    """
    Генерує SQL запит (simple templating)
    
    ВАЖЛИВО: У production використовуйте parameterized queries!
    """
    cols = ", ".join(columns)
    query = f"SELECT {cols} FROM {table}"
    
    if conditions:
        where_clauses = []
        for key, value in conditions.items():
            if isinstance(value, str):
                where_clauses.append(f"{key} = '{value}'")
            else:
                where_clauses.append(f"{key} = {value}")
        
        query += " WHERE " + " AND ".join(where_clauses)
    
    return query + ";"


# Приклад
query = generate_sql_query(
    table="users",
    columns=["id", "name", "email"],
    conditions={"age": 25, "city": "Kyiv"}
)
print("Generated SQL:")
print(f"  {query}")


def generate_email_template(name: str, product: str, discount: int) -> str:
    """
    Генерує email template
    """
    template = f"""
    Привіт, {name}!
    
    Маємо для вас спеціальну пропозицію на {product}!
    Знижка {discount}% діє тільки сьогодні.
    
    Не пропустіть!
    
    З повагою,
    Команда Store
    """
    return template.strip()


email = generate_email_template("Олександр", "Python Course", 30)
print("\nEmail Template:")
print(email)


# ============================================================================
# 10. PRACTICAL: DATA CLEANING PIPELINE
# ============================================================================

print("\n" + "=" * 70)
print("10. ПРАКТИКА: DATA CLEANING PIPELINE")
print("=" * 70)

def clean_text_pipeline(text: str) -> dict[str, Any]:
    """
    Повний pipeline очищення тексту
    """
    steps = {}
    
    # 1. Original
    steps['original'] = text
    steps['original_length'] = len(text)
    
    # 2. Strip whitespace
    text = text.strip()
    steps['stripped'] = text
    
    # 3. Normalize whitespace
    text = ' '.join(text.split())
    steps['whitespace_normalized'] = text
    
    # 4. Remove special characters (keep letters, numbers, spaces)
    text = re.sub(r'[^a-zA-Zа-яА-ЯіІїЇєЄ0-9\s]', '', text)
    steps['special_chars_removed'] = text
    
    # 5. Lowercase
    text = text.lower()
    steps['lowercased'] = text
    
    # 6. Remove extra spaces again
    text = ' '.join(text.split())
    steps['final'] = text
    steps['final_length'] = len(text)
    
    # Stats
    steps['length_reduction'] = steps['original_length'] - steps['final_length']
    steps['reduction_pct'] = (steps['length_reduction'] / steps['original_length'] * 100) if steps['original_length'] > 0 else 0
    
    return steps


# Тест
dirty_text = """
    !!!  Hello   World!!!  
    This   is   a    TEST  @#$%  
    With  MANY    spaces!!!
"""

result = clean_text_pipeline(dirty_text)

print("Data Cleaning Pipeline:")
print(f"Original: '{result['original'][:50]}...'")
print(f"Final: '{result['final']}'")
print(f"Length: {result['original_length']} → {result['final_length']}")
print(f"Reduction: {result['reduction_pct']:.1f}%")


# ============================================================================
# ПІДСУМОК
# ============================================================================

print("\n" + "=" * 70)
print("ПІДСУМОК: STRING PROCESSING ДЛЯ DS/DE")
print("=" * 70)

summary = """
✅ REGEX PATTERNS:
   - Data extraction
   - Validation
   - Cleaning

✅ DATA NORMALIZATION:
   - Company names
   - Phone numbers
   - Addresses

✅ TEXT PREPROCESSING:
   - Tokenization
   - Cleaning
   - NLP готовність

✅ VALIDATION:
   - Email, IP, dates
   - Credit cards (Luhn)
   - Custom validators

✅ STRING SIMILARITY:
   - Levenshtein distance
   - Fuzzy matching
   - Deduplication

✅ UNICODE:
   - Internationalization
   - Accent removal
   - Normalization

✅ FORMATTING:
   - Tables
   - Reports
   - Templates

✅ PRACTICAL PIPELINES:
   - End-to-end cleaning
   - Multi-step processing
   - Production-ready

🎯 ЗАСТОСУВАННЯ В DS/DE:
   - Data cleaning pipelines
   - Entity resolution
   - Log parsing
   - Text preprocessing
   - Data validation
   - Report generation
"""

print(summary)

print("\n✨ String processing - основа data engineering! ✨\n")
