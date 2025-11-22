"""
Модуль 4.1: Робота з датами та часом - Professional Edition
===========================================================

Це продвинутий модуль для роботи з датами у реальних Data Science проектах.
Включає приклади з:
- Часових рядів для аналітики
- Обробки логів у production системах
- Обчислення метрик в аналізі даних
- Синхронізації в розподілених системах

Ключові концепції:
- Datetime як фундамент для часових рядів
- UTC vs локальний час (critical для інтеграцій)
- Правильна обробка часових зон
- Оптимізація для великих обсягів даних
"""

from datetime import datetime, timedelta, date, timezone
from typing import List, Tuple
import time

print("=" * 70)
print("МОДУЛЬ 4.1: РОБОТА З ДАТАМИ - DATA SCIENCE EDITION")
print("=" * 70)

# ============================================================================
# 1. ЧАСОВІ РЯДИ: РЕАЛЬНА ЗАДАЧА - АНАЛІЗ ТРАФІКУ САЙТУ
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: ЧАСОВІ РЯДИ - АНАЛІЗ ТРАФІКУ")
print("=" * 70)

# Сценарій: Є логи з трафіком. Потрібно знайти пікові години
# Це реальна задача у web analytics

log_entries = [
    {"timestamp": "2024-11-21 08:15:30", "user": "user1", "status": 200},
    {"timestamp": "2024-11-21 08:16:45", "user": "user2", "status": 200},
    {"timestamp": "2024-11-21 12:30:00", "user": "user3", "status": 200},
    {"timestamp": "2024-11-21 12:31:15", "user": "user4", "status": 500},
    {"timestamp": "2024-11-21 12:32:00", "user": "user5", "status": 200},
    {"timestamp": "2024-11-21 18:45:30", "user": "user6", "status": 200},
    {"timestamp": "2024-11-21 18:46:00", "user": "user7", "status": 200},
]

print("\n1. АНАЛІЗ ЛОГІВ - ПІКОВІ ГОДИНИ")
print("-" * 70)

# Парсимо лог та групуємо по годинам
hour_counts = {}
for entry in log_entries:
    # Парсинг дати
    log_time = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
    hour_key = log_time.strftime("%Y-%m-%d %H:00")  # Округлення до години

    hour_counts[hour_key] = hour_counts.get(hour_key, 0) + 1

print("Трафік по годинах:")
for hour, count in sorted(hour_counts.items()):
    print(f"  {hour}: {count} запитів")

# Знайти пікову годину
peak_hour = max(hour_counts, key=hour_counts.get)
print(f"\nПікова година: {peak_hour} ({hour_counts[peak_hour]} запитів)")
print()

# ============================================================================
# 2. ОБЧИСЛЕННЯ МЕТРИК: RETENTION, CHURN, DAU (Daily Active Users)
# ============================================================================

print("=" * 70)
print("PART 2: МЕТРИКИ АНАЛІТИКИ - РАСЧЁТ DAU, MAU, RETENTION")
print("=" * 70)

# Реальна задача: Розраховувати метрики активності користувачів
user_events = [
    {"date": "2024-11-19", "user_id": 1, "action": "login"},
    {"date": "2024-11-19", "user_id": 2, "action": "login"},
    {"date": "2024-11-20", "user_id": 1, "action": "login"},  # User 1 вернувся
    {"date": "2024-11-20", "user_id": 3, "action": "login"},
    {"date": "2024-11-21", "user_id": 2, "action": "login"},
    {"date": "2024-11-21", "user_id": 3, "action": "login"},
]

print("\n1. ОБЧИСЛЕННЯ DAU (Daily Active Users)")
print("-" * 70)

# Розраховуємо DAU для кожного дня
daily_users = {}
for event in user_events:
    date_str = event["date"]
    user_id = event["user_id"]

    if date_str not in daily_users:
        daily_users[date_str] = set()

    daily_users[date_str].add(user_id)

for date_str, users in sorted(daily_users.items()):
    print(f"  {date_str}: {len(users)} DAU (користувачів: {users})")

print("\n2. ОБЧИСЛЕННЯ RETENTION (дні, які користувачі повернулись)")
print("-" * 70)

# День 1: {1, 2}, День 2: {1, 3}, День 3: {2, 3}
# Retention = користувачі що були в День N і День N+1

for day_num in range(len(daily_users) - 1):
    days_sorted = sorted(daily_users.keys())
    day_current = days_sorted[day_num]
    day_next = days_sorted[day_num + 1]

    users_current = daily_users[day_current]
    users_next = daily_users[day_next]

    # Хто повернувся?
    returned = users_current & users_next
    retention_rate = (len(returned) / len(users_current)) * 100

    print(f"  {day_current} -> {day_next}: {len(returned)}/{len(users_current)} користувачів повернулись ({retention_rate:.1f}%)")

print()

# ============================================================================
# 3. ЧАСОВІ ЗОНИ (CRITICAL для міжнародних систем)
# ============================================================================

print("=" * 70)
print("PART 3: ЧАСОВІ ЗОНИ - UTC VS ЛОКАЛЬНИЙ ЧАС")
print("=" * 70)

print("\n⚠️  ВАЖЛИВО ДЛЯ PRODUCTION:")
print("  - Завжди зберігайте дати в UTC у БД")
print("  - Конвертуйте в локальний час тільки для виведення")
print("  - Це запобігає помилкам при DST (літній час)")
print()

# Приклад: Часові мітки з різних часових зон
from datetime import timezone as tz

# UTC час (ЗАВЖДИ використовуйте для storage)
now_utc = datetime.now(tz.utc)
print(f"Поточна дата/час UTC: {now_utc}")
print(f"ISO формат (для APIs): {now_utc.isoformat()}")
print()

# Коли конвертуємо у локальний час (наприклад для звіту)
local_timestamp = now_utc.timestamp()  # Секунди від 1970
print(f"Unix timestamp (для APIs): {local_timestamp}")

# ============================================================================
# 4. WINDOW FUNCTIONS - АНАЛІЗ ПОСЛІДОВНОСТЕЙ
# ============================================================================

print("=" * 70)
print("PART 4: АНАЛІЗ ЧАСОВИХ ПОСЛІДОВНОСТЕЙ - ROLLING WINDOWS")
print("=" * 70)

# Реальна задача: Розраховувати середньою по скользящему вікну (як у pandas)
# Це важливо для згладжування шуму в часових рядах

timestamps = [
    "2024-11-21 10:00:00",
    "2024-11-21 10:01:00",
    "2024-11-21 10:02:00",
    "2024-11-21 10:03:00",
    "2024-11-21 10:04:00",
]

# Дані: кількість запитів за кожну хвилину
requests = [100, 110, 95, 120, 105]

print("\n1. РОЗРАХОВУЄМО КОВЗАЮЧУ СЕРЕДНЮ (3-хвилинне вікно)")
print("-" * 70)

window_size = 3
moving_avg = []

for i in range(len(requests) - window_size + 1):
    window = requests[i:i + window_size]
    avg = sum(window) / len(window)
    moving_avg.append(avg)

    start_time = timestamps[i]
    print(f"  Вікно {i+1}: {window} -> середня {avg:.1f} запитів/хв")

print()

# ============================================================================
# 5. ПРАКТИЧНИЙ ПРИКЛАД: SLA MONITORING
# ============================================================================

print("=" * 70)
print("PART 5: PRODUCTION МОНІТОРИНГ - SLA (Service Level Agreement)")
print("=" * 70)

# Реальна задача: Перевіряти чи система була доступна 99.9% часу
# (SLA часто вимагає 99.9% uptime)

outages = [
    {"start": "2024-11-21 08:00:00", "end": "2024-11-21 08:15:00"},  # 15 хвилин
    {"start": "2024-11-21 14:30:00", "end": "2024-11-21 14:35:00"},  # 5 хвилин
]

print("\n1. РОЗРАХУНОК UPTIME")
print("-" * 70)

# Загальний час дня
day_start = datetime.strptime("2024-11-21 00:00:00", "%Y-%m-%d %H:%M:%S")
day_end = datetime.strptime("2024-11-21 23:59:59", "%Y-%m-%d %H:%M:%S")

total_seconds = (day_end - day_start).total_seconds()

# Час простоїв
downtime_seconds = 0
for outage in outages:
    start = datetime.strptime(outage["start"], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(outage["end"], "%Y-%m-%d %H:%M:%S")
    downtime = (end - start).total_seconds()
    downtime_seconds += downtime

    minutes = downtime / 60
    print(f"  Простій: {outage['start']} до {outage['end']} ({minutes:.1f} хв)")

uptime_percent = ((total_seconds - downtime_seconds) / total_seconds) * 100
print(f"\nUptime: {uptime_percent:.4f}%")
print(f"Вимога SLA: 99.9% (мак. простій: {(24 * 60 - 24 * 60 * 0.999):.1f} хвилин)")
print(f"Статус: {'✅ PASSED' if uptime_percent >= 99.9 else '❌ FAILED'}")
print()

# ============================================================================
# 6. ОПТИМІЗАЦІЯ ДЛЯ ВЕЛИКИХ ОБСЯГІВ ДАНИХ
# ============================================================================

print("=" * 70)
print("PART 6: ОПТИМІЗАЦІЯ - ОБРОБКА МІЛЬЙОНІВ ЗАПИСІВ")
print("=" * 70)

print("\n1. ПОРІВНЯННЯ ШВИДКОСТІ:")
print("-" * 70)

# Метод 1: Базовий (повільний для великих даних)
def parse_dates_basic(dates: List[str]) -> List[datetime]:
    return [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]

# Метод 2: Кешований format (швидший)
date_format = "%Y-%m-%d %H:%M:%S"
def parse_dates_optimized(dates: List[str]) -> List[datetime]:
    return [datetime.strptime(d, date_format) for d in dates]

# Тест на малому наборі (для демонстрації)
test_dates = ["2024-11-21 10:00:00"] * 1000

start = time.time()
parse_dates_basic(test_dates)
time_basic = time.time() - start

start = time.time()
parse_dates_optimized(test_dates)
time_optimized = time.time() - start

print(f"  Базовий метод: {time_basic*1000:.2f} мс")
print(f"  Оптимізований: {time_optimized*1000:.2f} мс")
print(f"  Прискорення: {time_basic/time_optimized:.1f}x")

print("\n💡 Поради для production:")
print("  - Кешуйте format strings")
print("  - Використовуйте iloc для pandas DataFrames")
print("  - Розглядайте pd.to_datetime() замість strptime")
print("  - Паралелізуйте обробку (multiprocessing)")
print()

# ============================================================================
# 7. ПРАКТИЧНІ ШАБЛОНИ (TEMPLATES)
# ============================================================================

print("=" * 70)
print("PART 7: ШАБЛОНИ КОДУ ДЛЯ REAL-WORLD ЗАДАЧ")
print("=" * 70)

# Шаблон 1: Парсинг дати з error handling
print("\n1. SAFE DATE PARSING (з обробкою помилок):")
print("-" * 70)

def safe_parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime | None:
    """Безпечно парсить дату, повертає None якщо помилка."""
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError as e:
        print(f"  ⚠️ Помилка при парсингу '{date_str}': {e}")
        return None

test_dates = [
    "2024-11-21 10:00:00",      # OK
    "2024-11-21",                # Помилка - неправильний формат
    "invalid date",              # Помилка - невалідна дата
]

print("Тестування:")
for date_str in test_dates:
    result = safe_parse_datetime(date_str)
    status = "✅ OK" if result else "❌ SKIPPED"
    print(f"  '{date_str}' -> {status}")

print()

# Шаблон 2: Лог-парсер для production систем
print("2. LOG PARSER (реальний приклад з production логу):")
print("-" * 70)

class LogEvent:
    """Структура для логу (краще ніж dict для type safety)."""
    def __init__(self, timestamp: datetime, level: str, message: str):
        self.timestamp = timestamp
        self.level = level
        self.message = message

    def __repr__(self):
        return f"LogEvent({self.timestamp}, {self.level}, '{self.message[:30]}...')"

def parse_log_line(line: str) -> LogEvent | None:
    """Парсить лог у форматі: 2024-11-21 10:00:00 ERROR Something happened"""
    try:
        parts = line.split(" ", 3)  # Розділяємо перші 3 слова
        if len(parts) < 4:
            return None

        date_str = f"{parts[0]} {parts[1]}"
        timestamp = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        level = parts[2]
        message = parts[3]

        return LogEvent(timestamp, level, message)
    except Exception:
        return None

log_lines = [
    "2024-11-21 10:00:00 ERROR Connection failed",
    "2024-11-21 10:01:00 WARNING High memory usage",
    "2024-11-21 10:02:00 INFO Service restarted",
    "invalid log line",  # Буде пропущена
]

print("Парсинг логів:")
events = []
for line in log_lines:
    event = parse_log_line(line)
    if event:
        events.append(event)
        print(f"  ✅ {event}")
    else:
        print(f"  ❌ SKIPPED: {line}")

print()

# ============================================================================
# 8. ЗАВДАННЯ ДЛЯ ПРАКТИКИ
# ============================================================================

print("=" * 70)
print("PART 8: ПРАКТИЧНІ ЗАВДАННЯ")
print("=" * 70)

print("""
ЗАВДАННЯ 1 (ЛЕГКО): Обчислити DAU (Daily Active Users)
  Вхід: список подій з датами та user_id
  Вихід: кількість унікальних користувачів на день
  💡 Підказка: set() для unique값

ЗАВДАННЯ 2 (СЕРЕДНЬО): Розрахувати retention (якій % повернулись)
  Вхід: користувачи дня N та дня N+1
  Вихід: % користувачів що повернулись
  💡 Підказка: intersection (&) для перетину множин

ЗАВДАННЯ 3 (СКЛАДНО): Побудувати утилітний клас DateRange для аналізу
  Методи:
  - __init__(start_date, end_date)
  - days_in_range() -> int
  - hours_in_range() -> int
  - is_business_day(date) -> bool
  - week_of_year(date) -> int

  Використання:
  dr = DateRange("2024-01-01", "2024-12-31")
  print(dr.days_in_range())  # 366 днів

ЗАВДАННЯ 4 (БОНУС): Реалізувати функцію для аналізу SLA
  def calculate_sla(outages: List[dict]) -> float
  Повертає: % uptime за період

Розв'яжіть на папері перед тим як писати код!
""")

print("\n" + "=" * 70)
print("ИТОГИ")
print("=" * 70)

print("""
✅ Що ви дізналися:
  1. Час як основа для аналізу (DAU, MAU, retention)
  2. Важливість UTC для міжнародних систем
  3. Оптимізація для великих обсягів даних
  4. Шаблони для production код (error handling, logging)
  5. Структурована обробка часових рядів

🔑 Key insights для Senior Data Engineer:
  - Дата/час є ОСНОВОЮ для всіх временных рядів
  - Неправильне обробка часу = дорогі помилки
  - Оптимізація важлива при роботі з 1M+ записів
  - Type hints (datetime | None) - профі підхід
  - Dataclass > dict для логів та событий

🚀 Наступне: Обробка великих файлів (CSV з датами)
""")
