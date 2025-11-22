"""
Модуль 4.3: Data Parsing та очищення - Professional Edition
=============================================================

Це продвинутий модуль для парсингу та очищення реальних даних.
Включає приклади з:
- Парсингу неструктурованих даних
- Очищення та валідації даних
- Робота з помилками та аномаліями
- Entity extraction з текстів
- Батч обробки великих наборів даних

Ключові концепції:
- Defensive programming при роботі з невідомими даними
- Type hints та Pydantic для валідації
- Streaming обробка для великих файлів
- Логування та моніторинг проблем
- Пошук та нормалізація паттернів

Це версія для Senior engineers - готова до production.
"""

import re
import json
import csv
import logging
from typing import List, Dict, Tuple, Optional, Generator
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import io

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

print("=" * 70)
print("МОДУЛЬ 4.3: DATA PARSING ТА ОЧИЩЕННЯ - PROFESSIONAL EDITION")
print("=" * 70)

# ============================================================================
# 1. ПАРСИНГ НЕСТРУКТУРОВАНИХ ЛОГІВ
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: ПАРСИНГ ЛОГІВ - EXTRACT INFORMATION")
print("=" * 70)

# Типова задача: разобрати лог файл та витягнути інформацію
# Формат: YYYY-MM-DD HH:MM:SS [LEVEL] [MODULE] Message

@dataclass
class LogEntry:
    """Структурований запис логу з валідацією."""
    timestamp: datetime
    level: str
    module: str
    message: str

    def __post_init__(self):
        """Валідація після ініціалізації."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.level not in valid_levels:
            raise ValueError(f"Invalid log level: {self.level}")

# Сирові логи (як вони приходять із сервера)
raw_logs = """2024-01-15 10:23:45 [INFO] [AUTH] User admin logged in from 192.168.1.100
2024-01-15 10:24:12 [WARNING] [API] Slow response time: 2.5s for /users endpoint
2024-01-15 10:25:33 [ERROR] [DATABASE] Connection timeout after 30s
2024-01-15 10:26:01 [INFO] [API] Request completed: GET /users - 200 - 145ms
2024-01-15 10:27:45 [CRITICAL] [PAYMENT] Payment gateway unavailable
Некорректна лінія без формату
2024-01-15 10:28:15 [ERROR] [API] Invalid input: null value in required field"""

def parse_log_line(line: str) -> Optional[LogEntry]:
    """Парс одної лінії логу з обробкою помилок."""
    # Regex для матчення формату: YYYY-MM-DD HH:MM:SS [LEVEL] [MODULE] Message
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\[([A-Z]+)\]\s+\[([\w]+)\]\s+(.+)$'

    match = re.match(pattern, line.strip())
    if not match:
        logger.warning(f"Could not parse line: {line[:50]}...")
        return None

    try:
        timestamp_str, level, module, message = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return LogEntry(timestamp, level, module, message)
    except (ValueError, TypeError) as e:
        logger.error(f"Error parsing log entry: {e}")
        return None

print("\n1. PARSING СТРУКТУРОВАНИХ ЛОГІВ:")
print("-" * 70)

parsed_logs = []
for line in raw_logs.strip().split('\n'):
    entry = parse_log_line(line)
    if entry:
        parsed_logs.append(entry)

print(f"Спарсено {len(parsed_logs)} з {len(raw_logs.split(chr(10)))} логів")
print("\nПерші 3 запису:")
for entry in parsed_logs[:3]:
    print(f"  {entry.timestamp} [{entry.level}] [{entry.module}] {entry.message}")

print()

print("\n2. АНАЛІТИКА ЛОГІВ:")
print("-" * 70)

# Групування по рівню серйозності
level_counts = defaultdict(int)
module_errors = defaultdict(int)

for entry in parsed_logs:
    level_counts[entry.level] += 1
    if entry.level in {"ERROR", "CRITICAL"}:
        module_errors[entry.module] += 1

print("Розподіл за рівнями:")
for level in sorted(level_counts.keys()):
    count = level_counts[level]
    print(f"  {level:8s}: {count}")

if module_errors:
    print("\nМодулі з помилками:")
    for module, count in sorted(module_errors.items()):
        print(f"  {module}: {count} помилок")

print()

# ============================================================================
# 2. ОЧИЩЕННЯ ДАНИХ ДЛЯ DATA SCIENCE
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: ОЧИЩЕННЯ ДАНИХ - DATA CLEANING")
print("=" * 70)

# Типова задача: користувацькі дані з різними проблемами
# - Пропуски (missing values)
# - Неправильні типи
# - Дублікати
# - Аномалії

@dataclass
class UserData:
    """Очищена та валідна дані користувача."""
    user_id: int
    email: str
    age: int
    country: str
    spending: float

    @classmethod
    def from_raw(cls, raw_data: Dict) -> Optional['UserData']:
        """Фабрика для створення з невалідних даних."""
        try:
            # Валідація user_id
            user_id = int(raw_data.get('id', 0))
            if user_id <= 0:
                return None

            # Очищення та валідація email
            email = raw_data.get('email', '').strip().lower()
            if not re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email):
                logger.warning(f"Invalid email for user {user_id}: {email}")
                return None

            # Валідація age
            age = int(raw_data.get('age', 0))
            if not (13 <= age <= 120):
                logger.warning(f"Invalid age for {email}: {age}")
                return None

            # Нормалізація country
            country_raw = raw_data.get('country', 'unknown')
            if country_raw is None:
                country_raw = 'unknown'
            country = country_raw.strip().upper()

            # Валідація spending
            spending = float(raw_data.get('spending', 0))
            if spending < 0:
                logger.warning(f"Negative spending for {email}: {spending}")
                spending = 0

            return cls(user_id, email, age, country, spending)

        except (ValueError, TypeError) as e:
            logger.error(f"Failed to parse user data: {e}")
            return None

# Сирові дані (як часто трапляється в реальності)
raw_users = [
    {'id': 1, 'email': 'john@example.com', 'age': 28, 'country': 'usa', 'spending': '150.50'},
    {'id': 2, 'email': 'jane@EXAMPLE.COM', 'age': 35, 'country': 'UK', 'spending': '200'},
    {'id': 0, 'email': 'invalid', 'age': 25, 'country': 'DE', 'spending': '100'},  # Invalid ID
    {'id': 3, 'email': 'bob@test.com', 'age': 150, 'country': 'FR', 'spending': '-50'},  # Bad age, negative spending
    {'id': 4, 'email': 'alice@company.co.uk', 'age': 42, 'country': 'UK', 'spending': '300.75'},
    {'id': 5, 'email': 'charlie@mail.com', 'age': 22, 'country': None, 'spending': 'invalid'},  # Bad country/spending
]

print("\n1. ОЧИЩЕННЯ ДАНИХ:")
print("-" * 70)

cleaned_users: List[UserData] = []
invalid_count = 0

for raw_user in raw_users:
    user = UserData.from_raw(raw_user)
    if user:
        cleaned_users.append(user)
    else:
        invalid_count += 1

print(f"Вхідні дані: {len(raw_users)} користувачів")
print(f"Очищені дані: {len(cleaned_users)} валідних користувачів")
print(f"Відкинуті: {invalid_count} невалідних записів")

print("\nОчищені користувачі:")
for user in cleaned_users:
    print(f"  {user.email}: age={user.age}, country={user.country}, spent=${user.spending:.2f}")

print()

# ============================================================================
# 3. ВИТЯГНЕННЯ ІНФОРМАЦІЇ (ENTITY EXTRACTION)
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: ВИТЯГНЕННЯ СУТНОСТЕЙ - ENTITY EXTRACTION")
print("=" * 70)

@dataclass
class ExtractedEntities:
    """Витягнуті сутності з тексту."""
    emails: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    phone_numbers: List[str] = field(default_factory=list)
    prices: List[float] = field(default_factory=list)
    dates: List[str] = field(default_factory=list)

def extract_entities(text: str) -> ExtractedEntities:
    """Витягує всі сутності з тексту."""
    entities = ExtractedEntities()

    # Email адреси
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    entities.emails = re.findall(email_pattern, text)

    # URLs
    url_pattern = r'https?://[^\s]+'
    entities.urls = re.findall(url_pattern, text)

    # Телефонні номери (різні формати)
    phone_pattern = r'\+?\d{1,3}[-.\s]?\(?[\d]{2,3}\)?[-.\s]?[\d]{3}[-.\s]?[\d]{4}'
    entities.phone_numbers = re.findall(phone_pattern, text)

    # Ціни ($ або грн)
    price_pattern = r'\$[\d,]+\.?\d*|\d+\.?\d*\s*(?:грн|₴|USD|UAH)'
    price_matches = re.findall(price_pattern, text)
    for match in price_matches:
        # Спроба витягнути числу
        num_match = re.search(r'[\d,]+\.?\d*', match)
        if num_match:
            price_str = num_match.group().replace(',', '')
            try:
                entities.prices.append(float(price_str))
            except ValueError:
                pass

    # Дати (YYYY-MM-DD або DD.MM.YYYY)
    date_pattern = r'\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4}'
    entities.dates = re.findall(date_pattern, text)

    return entities

# Тестовий текст (як його можна знайти на веб-сайті або в email)
test_text = """
Привіт! Я залишив мої контакти: john.doe@company.com і також
можешь написати на +38(050)123-4567.

Предмет: Спеціальна пропозиція від 2024-01-15

Дивись деякі з наших інших продуктів на https://shop.example.com/products

Ціни:
- Базова версія: $99.99
- Преміум версія: 5000 грн
- Корпоративна: $1,299.50

Для зв'язку: support@company.com або +1-800-555-0123

Дата締切: 31.12.2024
"""

print("\n1. ВИТЯГНЕННЯ СУТНОСТЕЙ З ТЕКСТУ:")
print("-" * 70)

entities = extract_entities(test_text)

print("Email адреси:")
for email in entities.emails:
    print(f"  - {email}")

print("\nURLs:")
for url in entities.urls:
    print(f"  - {url}")

print("\nТелефонні номери:")
for phone in entities.phone_numbers:
    print(f"  - {phone}")

print("\nЦіни:")
for price in entities.prices:
    print(f"  - ${price:.2f}")

print("\nДати:")
for date in entities.dates:
    print(f"  - {date}")

print()

# ============================================================================
# 4. CSV ОБРОБКА - STREAMING
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: CSV ОБРОБКА ДЛЯ ВЕЛИКИХ ФАЙЛІВ - STREAMING")
print("=" * 70)

# Генеруємо CSV дані в пам'яті (як приклад великого файлу)
csv_data = """user_id,timestamp,event_type,value
1,2024-01-15 10:00:00,page_view,/home
1,2024-01-15 10:05:12,click,button_subscribe
2,2024-01-15 10:03:45,page_view,/products
1,2024-01-15 10:10:22,purchase,product_xyz
2,2024-01-15 10:12:33,page_view,/checkout
3,2024-01-15 10:15:00,page_view,/about"""

@dataclass
class UserEvent:
    """Подія користувача."""
    user_id: int
    timestamp: datetime
    event_type: str
    value: str

def stream_csv_events(csv_text: str) -> Generator[UserEvent, None, None]:
    """Generator для обробки CSV без завантаження всього в пам'ять."""
    reader = csv.DictReader(io.StringIO(csv_text))

    for row in reader:
        try:
            event = UserEvent(
                user_id=int(row['user_id']),
                timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"),
                event_type=row['event_type'],
                value=row['value']
            )
            yield event
        except (ValueError, KeyError) as e:
            logger.warning(f"Skipped invalid event: {e}")
            continue

print("\n1. STREAMING ОБРОБКА CSV:")
print("-" * 70)

# Аналізуємо евенти користувача на льоту (streaming)
user_sessions: Dict[int, List[UserEvent]] = defaultdict(list)
event_counts = defaultdict(int)

for event in stream_csv_events(csv_data):
    user_sessions[event.user_id].append(event)
    event_counts[event.event_type] += 1

print(f"Оброблено {sum(len(v) for v in user_sessions.values())} евентів")
print(f"Унікальних користувачів: {len(user_sessions)}")

print("\nРозподіл типів евентів:")
for event_type, count in sorted(event_counts.items()):
    print(f"  {event_type}: {count}")

print("\nСесії користувачів:")
for user_id, events in sorted(user_sessions.items()):
    print(f"  User {user_id}: {len(events)} евентів")
    for event in events:
        print(f"    - {event.event_type:12s} → {event.value}")

print()

# ============================================================================
# 5. БАТЧ ОБРОБКА ТА ДЕДУБЛІКАЦІЯ
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: БАТЧ ОБРОБКА - DEDUPE ТА НОРМАЛІЗАЦІЯ")
print("=" * 70)

@dataclass
class ProductRecord:
    """Нормалізований запис продукту."""
    product_id: str
    name: str
    price: float
    category: str

def normalize_product_name(name: str) -> str:
    """Нормалізує назву продукту."""
    # Видаляємо додаткові пробіли, конвертуємо у title case
    name = ' '.join(name.split())
    name = name.title()
    # Видаляємо спеціальні символи
    name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
    return name

def process_products_batch(raw_products: List[Dict]) -> List[ProductRecord]:
    """Обробляє батч продуктів з дедублікацією."""
    seen_ids = set()
    processed = []

    for raw in raw_products:
        try:
            product_id = str(raw.get('id', '')).strip()

            # Пропускаємо дублікати
            if product_id in seen_ids:
                logger.info(f"Duplicate product skipped: {product_id}")
                continue

            seen_ids.add(product_id)

            product = ProductRecord(
                product_id=product_id,
                name=normalize_product_name(raw.get('name', 'unknown')),
                price=float(raw.get('price', 0)),
                category=raw.get('category', '').strip().upper()
            )
            processed.append(product)

        except (ValueError, KeyError):
            logger.warning(f"Invalid product record: {raw}")
            continue

    return processed

raw_products = [
    {'id': 'p001', 'name': '  laptop computer  ', 'price': '999.99', 'category': 'electronics'},
    {'id': 'p002', 'name': 'mouse @ pad', 'price': '25.50', 'category': 'accessories'},
    {'id': 'p001', 'name': 'laptop', 'price': '999', 'category': 'electronics'},  # Дублікат
    {'id': 'p003', 'name': 'keyboard!!!', 'price': '75.00', 'category': 'electronics'},
    {'id': 'p004', 'name': 'monitor', 'price': 'invalid', 'category': 'electronics'},  # Bad price
]

print("\n1. БАТЧ ОБРОБКА З ДЕДУБЛІКАЦІЄЮ:")
print("-" * 70)

products = process_products_batch(raw_products)

print(f"Вхідні дані: {len(raw_products)} записів")
print(f"Оброблено: {len(products)} унікальних продуктів")

print("\nОброблені продукти:")
for product in products:
    print(f"  {product.product_id}: {product.name:20s} ${product.price:7.2f} ({product.category})")

print()

# ============================================================================
# 6. ОБРОБКА JSON З ВКЛАДЕНОЮ СТРУКТУРОЮ
# ============================================================================

print("\n" + "=" * 70)
print("PART 6: JSON ПАРСИНГ - ВКЛАДЕНА СТРУКТУРА")
print("=" * 70)

@dataclass
class APIResponse:
    """Структурована API відповідь."""
    status: str
    user_id: int
    transactions: List[Dict]

    def total_spent(self) -> float:
        """Обчислює загальну суму витрат."""
        return sum(float(t.get('amount', 0)) for t in self.transactions)

def parse_api_response(json_str: str) -> Optional[APIResponse]:
    """Безпечно парсить API JSON відповідь."""
    try:
        data = json.loads(json_str)

        # Валідація обов'язкових полів
        if not all(k in data for k in ['status', 'user_id', 'transactions']):
            raise ValueError("Missing required fields")

        # Валідація типів
        if not isinstance(data['transactions'], list):
            raise TypeError("Transactions must be a list")

        return APIResponse(
            status=data['status'],
            user_id=int(data['user_id']),
            transactions=data['transactions']
        )

    except (json.JSONDecodeError, ValueError, TypeError) as e:
        logger.error(f"Failed to parse API response: {e}")
        return None

api_response_json = """{
    "status": "success",
    "user_id": 12345,
    "transactions": [
        {"id": "tx001", "amount": "150.50", "date": "2024-01-15", "type": "purchase"},
        {"id": "tx002", "amount": "75.00", "date": "2024-01-14", "type": "refund"},
        {"id": "tx003", "amount": "299.99", "date": "2024-01-13", "type": "purchase"}
    ]
}"""

print("\n1. ПАРСИНГ JSON СТРУКТУРИ:")
print("-" * 70)

response = parse_api_response(api_response_json)

if response:
    print(f"Status: {response.status}")
    print(f"User ID: {response.user_id}")
    print(f"Транзакції ({len(response.transactions)}): ")

    for tx in response.transactions:
        print(f"  - {tx.get('type', 'unknown'):8s}: ${tx.get('amount', '0'):7s} ({tx.get('date', 'N/A')})")

    print(f"\nОбщо витрачено: ${response.total_spent():.2f}")

print()

# ============================================================================
# 7. ПРАКТИЧНІ ЗАВДАННЯ
# ============================================================================

print("\n" + "=" * 70)
print("PART 7: ПРАКТИЧНІ ЗАВДАННЯ")
print("=" * 70)

print("""
ЗАВДАННЯ 1 (ЛЕГКО): Парс простого CSV
  Дано CSV: "name,age,city\\nAlice,30,NYC\\nBob,25,LA"
  Знайти: Скільки людей старше 27 років?

ЗАВДАННЯ 2 (СЕРЕДНЬО): Дедублікація email-ів
  Дано список email-ів з дублікатами (разних регістрів)
  Нормалізувати та знайти унікальні
  Методика: .lower(), .strip(), set()

ЗАВДАННЯ 3 (СЕРЕДНЬО): Витяг цін із тексту
  Дано текст з різними форматами цін ($100, 500 грн, €75)
  Витягнути всі ціни та конвертувати в одну валюту
  Підказка: regex + словник для конверсії

ЗАВДАННЯ 4 (СКЛАДНО): Валідація та нормалізація адрес
  Дано список адрес з опечатками та різним форматом
  Нормалізувати в стандартний формат
  Валідувати наявність необхідних полів
  Методика: regex + dataclass + from_raw()

ЗАВДАННЯ 5 (СКЛАДНО): Streaming обробка великого файлу
  Реалізувати generator для чтення файлу за частинами
  Обробити кожен рядок без завантаження всього в пам'ять
  Накопичити статистику (COUNT, SUM, AVG)

Розв'яжіть завдання перед дивіттям рішення!
""")

print("\n" + "=" * 70)
print("ИТОГИ")
print("=" * 70)

print("""
✅ Що ви дізналися:
  1. Парсинг неструктурованих даних (логи, текст)
  2. Очищення даних з валідацією та обробкою помилок
  3. Entity extraction з допомогою regex
  4. Streaming обробка для великих файлів (memory efficient)
  5. Батч обробка з дедублікацією
  6. JSON парсинг з вкладеною структурою

🔑 Key insights для Senior Data Engineer:
  - Завжди обробляйте помилки при парсингу (0% даних = 100% чисті дані)
  - Валідуйте дані при вхідні (fail fast, fail clear)
  - Використовуйте dataclasses для структурування
  - Streaming для великих наборів (memory efficiency)
  - Логування для дебаґування проблем в production

⚠️  Частії помилки:
  - Недостатня валідація (garbage in = garbage out)
  - Завантаження всіх даних в пам'ять (OOM errors)
  - Не логування проблеми при парсингу (неможливо дебаґити)
  - Использування простих regex без тестування

🚀 Наступне: Data processing - CSV, JSON, Parquet обробка
""")
