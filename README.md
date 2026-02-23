# Python Core — Комплексний курс від нуля до робочих навичок

> Структурований курс Python із послідовними модулями, де кожен будує на попередніх знаннях.

---

## Про курс

Матеріали розроблені для студентів, які вивчають Python з нуля, і для викладачів, яким потрібні готові сценарії занять. Курс використовує **двотрачну систему** — кожен завершений модуль має окремі треки для новачків та для досвідчених розробників (DS/DE/Senior).

**Цілі курсу:**
- Вивчити основи та ООП Python
- Набути практичних навичок для розв'язання реальних задач
- Підготуватися до розробки веб-додатків та автоматизації

---

## Структура курсу

| Модуль | Тема | Статус | Папка |
|--------|------|--------|-------|
| 1 | Основи Python (типи даних, змінні, I/O) | ⏳ Заплановано | — |
| **2** | **Контроль потоку та функції** | ✅ Готово | [`_02/`](_02/) |
| 3 | Структури даних (list, dict, set, tuple) | ⏳ Заплановано | — |
| **4** | **Файли, модулі, datetime, regex** | ✅ Готово | [`_04/`](_04/) |
| 5 | ООП: класи, спадкування, поліморфізм | ⏳ Заплановано | — |
| **6** | **Функціональне програмування та ООП** | ✅ Готово | [`_06/`](_06/) |
| 7 | Обробка помилок та логування | ⏳ Заплановано | — |
| **8** | **Серіалізація та копіювання об'єктів** | ✅ Готово | [`_08/`](_08/) |

---

## Модулі

### Модуль 2 — Контроль потоку та функції [`_02/`](_02/)

- Умовні оператори (`if/elif/else`), цикли (`for`, `while`)
- Функції, параметри, область видимості
- Рядки та методи
- Debugging у VSCode (breakpoints, watch, call stack)
- Git та GitHub для початківців

**Двотрачна система:** beginner + DS-орієнтований трек (`07_practice_ds_tasks.py`)
**Jupyter:** `fundamentals_notebook.ipynb`

---

### Модуль 4 — Файли, модулі та обробка даних [`_04/`](_04/)

- `datetime` — роботи з датами та часом
- `math` / `statistics` — математичні операції та A/B-тести
- Регулярні вирази (regex) — пошук, валідація, парсинг
- Файли (TXT, CSV, JSON)
- Модулі та пакети (`import`, `pip`, `venv`)

**Beginner edition** — 6 модулів (~3 300 рядків):

```
beginner_edition/
├── 01_datetime_basics.py       (~650 рядків)
├── 02_math_basics.py           (~650 рядків)
├── 03_regex_basics.py          (~580 рядків)
├── 04_files_basics.py          (~450 рядків)
├── 05_modules_packages.py      (~450 рядків)
└── 06_practice_tasks.py        (~430 рядків, 5 проектів)
```

**Pro edition** — production-патерни для Senior/DS/DE (4/6 завершено):

```
pro_edition/
├── 01_datetime_professional.py     ✅
├── 02_statistics_ab_testing.py     ✅
├── 03_data_parsing.py              ✅
├── 04_data_processing.py           ✅
├── 05_architecture.py              ⏳ В розробці
└── 06_real_projects.py             ⏳ В розробці
```

**Jupyter:** `Module_4_Complete_Guide.ipynb`

---

### Модуль 6 — Функціональне програмування та ООП [`_06/`](_06/)

- `Decimal` для фінансової точності
- Генератори та lazy evaluation
- `map` / `filter` / `lambda`
- `@lru_cache` — мемоізація
- Класи, спадкування, MRO, композиція

**Beginner edition:**
```
beginner_edition/
├── 01_decimal_banking.py
├── 02_generators_csv_processing.py
├── 03_map_filter_data_cleaning.py
├── 04_lru_cache_recommendations.py
└── 05_classes_user_management.py
```

**Advanced edition:**
```
advanced_edition/
├── 01_big_data_analytics.py
└── 02_oop_advanced.py
```

**Jupyter:** `Module_6_Complete_Course.ipynb`

---

### Модуль 8 — Серіалізація та копіювання об'єктів [`_08/`](_08/)

- Інкапсуляція та безпечні сеттери
- Pickle (бінарний формат), JSON, CSV
- `__getstate__` / `__setstate__` для контролю серіалізації
- Shallow vs deep copy (`copy` module)
- Pydantic та dataclasses (сучасний підхід)

**Beginner edition:**
```
beginner_edition/
├── 01_oop_encapsulation_basics.py
├── 02_pickle_basics.py
├── 03_json_csv_basics.py
├── 04_copying_basics.py
├── 05_practice_tasks_beginner.py
└── 06_mini_projects_beginner.py
```

**Advanced edition:**
```
advanced_edition/
├── 01_modern_encapsulation.py
├── 02_pickle_production.py
├── 03_modern_serialization.py
├── 04_copying_performance.py
└── 05_pydantic_dataclasses.py
```

**Jupyter:** `Module_8_Complete_Guide.ipynb`

---

## Швидкий старт

### Студенту

```bash
# 1. Перевірте Python 3.8+
python3 --version

# 2. Оберіть модуль і прочитайте START_HERE.md
cd _04/
cat START_HERE.md

# Beginner track:
cd beginner_edition/
python3 01_datetime_basics.py

# Pro track:
cd ../pro_edition/
python3 01_datetime_professional.py
```

### Викладачу

```bash
# Детальний план уроку
cat _04/00_lesson_plan.md

# Стан розробки
cat _04/docs/CONTENT_MAP.md
```

---

## Принципи курсу

1. **Навчання через робочий код** — всі приклади запускаються без змін. Розкоментовуйте, експериментуйте.
2. **Від простого до складного** — модулі послідовні. Починайте з Модуля 2.
3. **70% практики** — пишіть код, не читайте теорію.
4. **Debugger з першого дня** — Модуль 2 одразу вчить VSCode debugger.
5. **Реальні приклади** — валідація email, A/B-тести, фінансові розрахунки.

---

## Технічні вимоги

- **Python** 3.8+ (рекомендовано 3.11+)
- **VSCode** — розширення: Python, Pylance, IntelliCode
- **Jupyter** (опціонально): `pip install notebook`

```bash
# Розширення VSCode через консоль
code --install-extension ms-python.python
code --install-extension ms-python.pylance
```

---

## Оцінювання

| Складність | Бали |
|-----------|------|
| Легке завдання | 5 |
| Середнє завдання | 10 |
| Складне завдання | 15 |
| Бонус (PLUS) | +5 |

**Критерії:** код виконується без помилок, результати правильні, код читабельний, використані потрібні концепції.

---

## Ресурси

| Ресурс | Посилання |
|--------|-----------|
| Офіційна документація | https://docs.python.org |
| Real Python | https://realpython.com |
| Python Tutor (візуалізація) | https://pythontutor.com |
| Stack Overflow | https://stackoverflow.com |

---

**Версія:** 2.1 · **Оновлено:** 2026-02-21
