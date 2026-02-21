# Модуль 2: Контроль потоку та функції
# Оновлений план заняття (узгоджено з `docs/TEACHING_FLOW.md`)

## 1. Загальна інформація
- Тривалість: 2.5-3 години
- Формат: live coding + guided practice + Q&A
- Baseline: Python 3.10-3.12
- Аудиторія: beginner або advanced DS/DE (обираємо один primary track на сесію)

## 2. Принцип проведення
- Не проводимо два повних треки паралельно в межах однієї короткої сесії.
- Обираємо primary track (beginner або advanced DS/DE).
- Другий трек даємо як follow-up/self-study.
- Python 3.13 preview теми (за потреби) лише як optional context.

## 3. Канонічні джерела
- Вхідна точка модуля: `README.md`
- Карта матеріалів: `docs/CONTENT_MAP.md`
- Траєкторії: `docs/LEARNING_PATHS.md`
- Канонічний flow: `docs/TEACHING_FLOW.md`
- Правила DRY: `docs/ARCHITECTURE.md`
- Primary notebook: `fundamentals_notebook.ipynb`

## 4. Таймінг заняття (канонічний)

### Block A. Setup and Context (10-15 хв)
- Що буде на занятті, expected outcomes
- Перевірка середовища (Python, VSCode, terminal)
- Фіксація primary track на цю групу

### Block B. Git/GitHub (20-25 хв)
- Мінімальний workflow: `clone -> add -> commit -> push`
- Пояснення типових помилок (`not a git repo`, auth, merge conflicts)
- Короткий live-demo

### Block C. VSCode Setup (15-20 хв)
- Interpreter, terminal, extensions (`Python`, `Pylance`)
- Базовий debugging workflow (breakpoint, step over, variables)

### Block D. Core Python Block (60-80 хв)

#### Варіант D1: Beginner path
1. `03_input_output.py`
2. `04_functions.py`
3. `05_strings.py`

Фокус:
- `input/print`, type conversion, форматування
- функції: параметри, `return`, default args
- базові рядкові методи і проста обробка тексту

#### Варіант D2: Advanced DS/DE path
1. `03_modern_input_output.py`
2. `04_modern_functions.py`
3. `05_modern_strings.py`

Фокус:
- валідація/трансформація даних
- composable functions, reusable patterns
- regex/string cleaning для реалістичних задач

### Block E. Debugging Block (15-20 хв)
- Єдиний файл для обох треків: `06_debugging.py`
- Показати: breakpoint, step-by-step, inspect variables

### Block F. Practice Block (25-35 хв)
- Beginner: `07_practice_tasks.py`
- Advanced DS/DE: `07_practice_ds_tasks.py`
- Формат: 1-2 задачі разом + 1 задача самостійно

### Block G. Q&A and Wrap-up (10-15 хв)
- Підсумок ключових патернів
- Розбір типових запитань
- Місток до наступних модулів (`_04`, `_06`)

## 5. Практичний сценарій проведення

### Перед заняттям (чекліст)
1. Перевірити запуск файлів primary треку
2. Перевірити `06_debugging.py`
3. Підготувати короткий git-demo репозиторій
4. Відкрити `fundamentals_notebook.ipynb` як основний сценарій

### Під час заняття
1. Не виходити за канонічний таймінг
2. Тримати фокус на одному primary track
3. Фіксувати питання студентів для wrap-up блоку

### Після заняття
1. Видати домашню практику за активним треком
2. Дати optional задачі з другого треку
3. Зібрати фідбек про темп і складність

## 6. Expected outcomes
Після заняття студент повинен:
- розуміти базовий Git workflow
- впевнено запускати та дебажити Python-код у VSCode
- вирішувати базові задачі на функції/рядки або data-oriented задачі (залежно від треку)
- пояснити різницю між навчальним і production-minded підходом на прикладах модуля

## 7. Що не робимо в межах цього модуля
- Не робимо Python 3.13 preview частиною обов'язкової програми
- Не намагаємось пройти beginner + advanced трек повністю за одну сесію
- Не дублюємо детальні інструкції з canonical docs у кількох файлах
