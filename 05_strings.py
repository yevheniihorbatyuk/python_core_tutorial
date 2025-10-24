"""
Модуль 2.3: Робота з рядками в Python
======================================

Цей модуль показує різні способи роботи з рядками та їх методи
"""

# ============================================================================
# 1. ОСНОВИ РЯДКІВ
# ============================================================================

print("=" * 60)
print("1. ОСНОВИ РЯДКІВ (STRINGS)")
print("=" * 60)

# Створення рядків
text1 = "Привіт"
text2 = 'Світ'
text3 = """Багаторядковий
текст"""

print(text1)
print(text2)
print(text3)

# Рядки - це послідовності символів
word = "Python"
print(f"Перший символ: {word[0]}")   # P
print(f"Другий символ: {word[1]}")   # y
print(f"Останній символ: {word[-1]}")  # n
print(f"Передостанній: {word[-2]}")    # o


# ============================================================================
# 2. ОПЕРАЦІЇ З РЯДКАМИ
# ============================================================================

print("\n" + "=" * 60)
print("2. БАЗОВІ ОПЕРАЦІЇ")
print("=" * 60)

# Конкатенація (об'єднання)
first_name = "Іван"
last_name = "Петренко"
full_name = first_name + " " + last_name
print(f"Повне ім'я: {full_name}")

# Повторення
print("=" * 30)
print("Ha" * 5)  # HaHaHaHaHa

# Довжина рядка
text = "Python Programming"
print(f"Довжина рядка: {len(text)}")

# Перевірка входження (in)
sentence = "Я вивчаю мову Python"
print(f"'Python' у реченні: {'Python' in sentence}")
print(f"'Java' у реченні: {'Java' in sentence}")


# ============================================================================
# 3. ІНДЕКСАЦІЯ ТА ЗРІЗИ (SLICING)
# ============================================================================

print("\n" + "=" * 60)
print("3. ІНДЕКСАЦІЯ ТА ЗРІЗИ")
print("=" * 60)

text = "Python Programming"
#       0123456789...

# Отримання одного символу
print(f"text[0] = {text[0]}")
print(f"text[7] = {text[7]}")

# Зрізи: text[start:end:step]
print(f"Перші 6 символів: {text[0:6]}")  # Python
print(f"Те саме: {text[:6]}")  # Python
print(f"З 7-го до кінця: {text[7:]}")  # Programming
print(f"Останні 11 символів: {text[-11:]}")  # Programming

# Кожен другий символ
print(f"Кожен другий: {text[::2]}")  # Pto rgamn

# Реверс рядка
print(f"Задом наперед: {text[::-1]}")


# ============================================================================
# 4. ВАЖЛИВІ МЕТОДИ РЯДКІВ
# ============================================================================

print("\n" + "=" * 60)
print("4. МЕТОДИ РЯДКІВ - ЗМІНА РЕГІСТРУ")
print("=" * 60)

text = "hello World"

# Зміна регістру
print(f"Оригінал: {text}")
print(f"upper(): {text.upper()}")      # HELLO WORLD
print(f"lower(): {text.lower()}")      # hello world
print(f"capitalize(): {text.capitalize()}")  # Hello world
print(f"title(): {text.title()}")      # Hello World
print(f"swapcase(): {text.swapcase()}")  # HELLO wORLD

print("\n" + "-" * 60)
print("5. МЕТОДИ - ПОШУК ТА ПЕРЕВІРКА")
print("-" * 60)

sentence = "Python is awesome"

# Пошук підрядка
print(f"find('is'): {sentence.find('is')}")  # 7 (індекс початку)
print(f"find('Java'): {sentence.find('Java')}")  # -1 (не знайдено)

# Перевірка початку/кінця
print(f"startswith('Python'): {sentence.startswith('Python')}")  # True
print(f"endswith('awesome'): {sentence.endswith('awesome')}")  # True

# Підрахунок входжень
print(f"count('o'): {sentence.count('o')}")  # 2

print("\n" + "-" * 60)
print("6. МЕТОДИ - ПЕРЕВІРКА ТИПУ")
print("-" * 60)

# Перевірка типу символів
print(f"'123'.isdigit(): {'123'.isdigit()}")  # True
print(f"'abc'.isalpha(): {'abc'.isalpha()}")  # True
print(f"'abc123'.isalnum(): {'abc123'.isalnum()}")  # True
print(f"'   '.isspace(): {'   '.isspace()}")  # True

text1 = "HELLO"
text2 = "hello"
text3 = "Hello World"

print(f"'HELLO'.isupper(): {text1.isupper()}")  # True
print(f"'hello'.islower(): {text2.islower()}")  # True
print(f"'Hello World'.istitle(): {text3.istitle()}")  # True


# ============================================================================
# 7. ВИДАЛЕННЯ ПРОБІЛІВ
# ============================================================================

print("\n" + "=" * 60)
print("7. ВИДАЛЕННЯ ПРОБІЛІВ")
print("=" * 60)

text = "   Python Programming   "

print(f"Оригінал: '{text}'")
print(f"strip(): '{text.strip()}'")    # Видалити з обох боків
print(f"lstrip(): '{text.lstrip()}'")  # Видалити зліва
print(f"rstrip(): '{text.rstrip()}'")  # Видалити справа


# ============================================================================
# 8. ЗАМІНА ПІДРЯДКІВ
# ============================================================================

print("\n" + "=" * 60)
print("8. ЗАМІНА ПІДРЯДКІВ")
print("=" * 60)

text = "Я вивчаю Java. Java це круто!"

# Замінити всі входження
new_text = text.replace("Java", "Python")
print(f"Оригінал: {text}")
print(f"Після заміни: {new_text}")

# Замінити тільки перше входження
new_text2 = text.replace("Java", "Python", 1)
print(f"Замінити 1 раз: {new_text2}")


# ============================================================================
# 9. РОЗДІЛЕННЯ ТА ОБ'ЄДНАННЯ
# ============================================================================

print("\n" + "=" * 60)
print("9. РОЗДІЛЕННЯ ТА ОБ'ЄДНАННЯ")
print("=" * 60)

# split() - розділити рядок на список
sentence = "Python is easy to learn"
words = sentence.split()  # За пробілами
print(f"Слова: {words}")

csv_data = "Іван,25,Київ"
data = csv_data.split(",")  # За комами
print(f"Дані: {data}")

# join() - об'єднати список в рядок
words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(f"Речення: {sentence}")

# Різні роздільники
print("-".join(words))  # Python-is-awesome
print(" | ".join(words))  # Python | is | awesome


# ============================================================================
# 10. ПРАКТИЧНІ ПРИКЛАДИ
# ============================================================================

print("\n" + "=" * 60)
print("10. ПРАКТИЧНІ ПРИКЛАДИ")
print("=" * 60)

# Приклад 1: Пошук літери у тексті (простий спосіб)
def find_letter_simple(text, letter):
    """
    Перевіряє чи є літера у тексті
    
    Args:
        text (str): Текст для пошуку
        letter (str): Літера для пошуку
    
    Returns:
        bool: True якщо літера є у тексті
    """
    return letter in text

result = find_letter_simple("Hello World", "o")
print(f"Літера 'o' у 'Hello World': {result}")


# Приклад 2: Пошук літери через цикл
def find_letter_loop(text, letter):
    """
    Знаходить позиції всіх входжень літери
    
    Args:
        text (str): Текст для пошуку
        letter (str): Літера для пошуку
    
    Returns:
        list: Список позицій де знайдено літеру
    """
    positions = []
    for i in range(len(text)):
        if text[i] == letter:
            positions.append(i)
    return positions

positions = find_letter_loop("Hello World", "o")
print(f"Позиції 'o': {positions}")


# Приклад 3: Підрахунок літер
def count_letter(text, letter):
    """
    Рахує кількість входжень літери
    
    Args:
        text (str): Текст
        letter (str): Літера
    
    Returns:
        int: Кількість входжень
    """
    count = 0
    for char in text:
        if char.lower() == letter.lower():
            count += 1
    return count

# Або простіше через метод:
def count_letter_method(text, letter):
    """Рахує літери через метод count()"""
    return text.lower().count(letter.lower())

text = "Hello World"
print(f"Літера 'l' зустрічається {count_letter(text, 'l')} рази")
print(f"Літера 'l' зустрічається {count_letter_method(text, 'l')} рази")


# Приклад 4: Перетворення до великої літери
def to_uppercase(text):
    """Перетворює перший символ на велику літеру"""
    if len(text) == 0:
        return text
    return text[0].upper() + text[1:]

print(f"'hello' -> '{to_uppercase('hello')}'")

# Або через метод:
print(f"'hello' -> '{'hello'.capitalize()}'")


# Приклад 5: Всі слова з великої літери
def title_case(text):
    """Кожне слово з великої літери"""
    words = text.split()
    capitalized = []
    for word in words:
        capitalized.append(word.capitalize())
    return " ".join(capitalized)

text = "привіт світ python"
print(f"Title case: {title_case(text)}")

# Або простіше:
print(f"Title case (метод): {text.title()}")


# ============================================================================
# 11. ФОРМАТУВАННЯ РЯДКІВ
# ============================================================================

print("\n" + "=" * 60)
print("11. РІЗНІ СПОСОБИ ФОРМАТУВАННЯ")
print("=" * 60)

name = "Олександр"
age = 25

# 1. Конкатенація (старий спосіб)
print("Мене звати " + name + ", мені " + str(age) + " років")

# 2. format() метод
print("Мене звати {}, мені {} років".format(name, age))
print("Мене звати {0}, мені {1} років. {0} любить Python".format(name, age))

# 3. f-strings (сучасний спосіб - РЕКОМЕНДУЄТЬСЯ)
print(f"Мене звати {name}, мені {age} років")

# f-strings з виразами
print(f"Через 5 років мені буде {age + 5} років")

# f-strings з форматуванням
price = 1234.56789
print(f"Ціна: {price:.2f} грн")  # 2 знаки після коми


# ============================================================================
# 12. СПЕЦІАЛЬНІ СИМВОЛИ ТА ЕКРАНУВАННЯ
# ============================================================================

print("\n" + "=" * 60)
print("12. СПЕЦІАЛЬНІ СИМВОЛИ")
print("=" * 60)

# \n - новий рядок
print("Рядок 1\nРядок 2\nРядок 3")

# \t - табуляція
print("Колонка1\tКолонка2\tКолонка3")

# \\ - зворотній слеш
print("Шлях: C:\\Users\\Documents")

# \' та \" - лапки
print("Він сказав: \"Привіт!\"")
print('It\'s a wonderful day!')

# Raw strings (r"...") - не обробляють спеціальні символи
print(r"C:\Users\Documents\new")  # Виведе як є


# ============================================================================
# 13. КОРИСНІ ВЛАСТИВОСТІ РЯДКІВ
# ============================================================================

print("\n" + "=" * 60)
print("13. ВАЖЛИВІ ВЛАСТИВОСТІ")
print("=" * 60)

print("✅ Рядки незмінні (immutable)")
text = "Hello"
# text[0] = "h"  # ❌ Помилка! Не можна змінити символ

# Потрібно створити новий рядок:
new_text = "h" + text[1:]
print(f"Оригінал: {text}")
print(f"Новий: {new_text}")

print("\n✅ Порівняння рядків")
print(f"'apple' == 'apple': {'apple' == 'apple'}")
print(f"'apple' < 'banana': {'apple' < 'banana'}")  # Лексикографічне
print(f"'A' < 'a': {'A' < 'a'}")  # За ASCII кодом


# ============================================================================
# ПІДСУМОК
# ============================================================================

print("\n" + "=" * 60)
print("ПІДСУМОК - ОСНОВНІ МЕТОДИ РЯДКІВ")
print("=" * 60)

summary = """
ЗМІНА РЕГІСТРУ:
  .upper()       - ВСІ ВЕЛИКІ
  .lower()       - всі маленькі
  .capitalize()  - Перша велика
  .title()       - Кожне Слово З Великої

ПОШУК ТА ПЕРЕВІРКА:
  .find(sub)         - знайти індекс підрядка (-1 якщо немає)
  .count(sub)        - підрахувати входження
  .startswith(sub)   - чи починається з...
  .endswith(sub)     - чи закінчується на...
  
  'sub' in text      - чи містить підрядок

ПЕРЕВІРКА ТИПУ:
  .isdigit()     - чи тільки цифри
  .isalpha()     - чи тільки літери
  .isalnum()     - літери або цифри
  .isspace()     - чи тільки пробіли
  .isupper()     - чи всі великі
  .islower()     - чи всі маленькі

ОЧИЩЕННЯ:
  .strip()       - видалити пробіли з обох боків
  .lstrip()      - видалити пробіли зліва
  .rstrip()      - видалити пробіли справа

ЗАМІНА:
  .replace(old, new)       - замінити підрядок
  .replace(old, new, n)    - замінити n разів

РОЗДІЛЕННЯ/ОБ'ЄДНАННЯ:
  .split(sep)    - розділити на список
  sep.join(list) - об'єднати список в рядок

ІНДЕКСАЦІЯ:
  text[i]        - отримати символ
  text[i:j]      - зріз від i до j
  text[::-1]     - реверс рядка
  len(text)      - довжина рядка
"""

print(summary)


# ============================================================================
# ПРАКТИЧНІ ЗАВДАННЯ
# ============================================================================

print("\n" + "=" * 60)
print("ЗАВДАННЯ ДЛЯ ПРАКТИКИ")
print("=" * 60)

tasks = """
1. Напишіть функцію, яка перевіряє чи є слово паліндромом
   (читається однаково з обох боків, наприклад: "шалаш")

2. Напишіть функцію, яка рахує кількість голосних у тексті

3. Напишіть функцію, яка видаляє всі пробіли з тексту

4. Напишіть функцію, яка перевертає слова у реченні
   ("Привіт світ" -> "світ Привіт")

5. Напишіть функцію, яка перевіряє чи є рядок валідною 
   email адресою (спрощена перевірка: має містити @ та .)
"""

print(tasks)

print("\n✨ Модуль завершено! Практикуйтесь з рядками! ✨\n")


# ============================================================================
# ШАБЛОНИ ДЛЯ ПРАКТИКИ
# ============================================================================

"""
# Завдання 1: Паліндром
def is_palindrome(text):
    # Підказка: порівняйте text з text[::-1]
    # Не забудьте привести до нижнього регістру
    pass

# Завдання 2: Підрахунок голосних
def count_vowels(text):
    vowels = "аеєиіїоуюя"  # для української
    # Ваш код
    pass

# Завдання 3: Видалити пробіли
def remove_spaces(text):
    # Підказка: використайте replace() або join() з split()
    pass

# Завдання 4: Реверс слів
def reverse_words(sentence):
    # Підказка: використайте split(), reverse або [::-1], join()
    pass

# Завдання 5: Перевірка email
def is_valid_email(email):
    # Підказка: перевірте чи є @ та .
    # і чи @ йде перед .
    pass
"""
