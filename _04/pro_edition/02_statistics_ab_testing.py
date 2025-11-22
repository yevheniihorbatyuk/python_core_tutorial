"""
Модуль 4.2: Статистика та експериментирование - Professional Edition
=====================================================================

Це продвинутий модуль для роботи зі статистикою у Data Science проектах.
Включає приклади з:
- A/B тестування для product decisions
- Розрахунку статистичної значущості
- Генерування синтетичних даних
- Monte Carlo симуляцій
- Простої кластеризації

Ключові концепції:
- Статистика як основа для decision making
- P-value та confidence intervals
- Симуляції для валідації гіпотез
- Правильний дизайн експериментів
"""

import random
import statistics
from typing import List, Tuple
from dataclasses import dataclass
import math

print("=" * 70)
print("МОДУЛЬ 4.2: СТАТИСТИКА ТА ЕКСПЕРИМЕНТИ - DATA SCIENCE EDITION")
print("=" * 70)

# ============================================================================
# 1. A/B ТЕСТУВАННЯ - НАЙПОПУЛЯРНІШИЙ USE CASE У PRODUCT
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: A/B ТЕСТУВАННЯ - REAL PRODUCT DECISION")
print("=" * 70)

# Реальна задача: На сайту 2 версії кнопки. Яка краща для конверсії?
# Версія A (control): старий дизайн
# Версія B (treatment): новий дизайн

print("\nСценарій: Менеджер хоче перевірити нову кнопку на сайті")
print("- Version A (control): 3000 користувачів, 150 покупок (5% conversion)")
print("- Version B (new):     3200 користувачів, 192 покупок (6% conversion)")
print()

# Параметри A/B тесту
class ABTest:
    """Клас для аналізу A/B тесту."""

    def __init__(self, control_users: int, control_conversions: int,
                 treatment_users: int, treatment_conversions: int):
        self.control_users = control_users
        self.control_conversions = control_conversions
        self.treatment_users = treatment_users
        self.treatment_conversions = treatment_conversions

        # Розраховуємо conversion rates
        self.control_rate = control_conversions / control_users
        self.treatment_rate = treatment_conversions / treatment_users
        self.uplift = (self.treatment_rate - self.control_rate) / self.control_rate * 100

    def print_summary(self):
        print("📊 A/B TEST RESULTS:")
        print("-" * 70)
        print(f"Control (A):  {self.control_conversions}/{self.control_users} = {self.control_rate*100:.2f}%")
        print(f"Treatment(B): {self.treatment_conversions}/{self.treatment_users} = {self.treatment_rate*100:.2f}%")
        print(f"Uplift: {self.uplift:.1f}%")
        print()

    def simple_statistical_test(self):
        """Простий тест - чи різниця більше ніж 3%?"""
        print("✓ SIMPLE TEST (diff > 3%):")

        min_difference = 0.03  # 3% мінімальна різниця для значущості

        if abs(self.treatment_rate - self.control_rate) > min_difference:
            print(f"  ✅ SIGNIFICANT: різниця {abs(self.treatment_rate - self.control_rate)*100:.1f}% > 3%")
            print(f"  Рекомендація: Запустити Treatment (B) для 100% користувачів")
        else:
            print(f"  ❌ NOT SIGNIFICANT: різниця {abs(self.treatment_rate - self.control_rate)*100:.1f}% <= 3%")
            print(f"  Рекомендація: Збільшити sample size або відмовитись від зміни")
        print()

# Тест 1: Успішний тест (Treatment краще)
test1 = ABTest(control_users=3000, control_conversions=150,
               treatment_users=3200, treatment_conversions=192)
test1.print_summary()
test1.simple_statistical_test()

# Тест 2: Неудачний тест (різниці немає)
test2 = ABTest(control_users=3000, control_conversions=150,
               treatment_users=3000, treatment_conversions=158)
test2.print_summary()
test2.simple_statistical_test()

# ============================================================================
# 2. СИМУЛЯЦІЇ (MONTE CARLO) - ВАЛІДАЦІЯ ГІПОТЕЗ
# ============================================================================

print("=" * 70)
print("PART 2: MONTE CARLO СИМУЛЯЦІЯ - ВАЛІДАЦІЯ ГІПОТЕЗ")
print("=" * 70)

# Реальна задача: Якою буде conversion rate якщо ми запустимо тест на 10k користувачів?

print("\n1. СИМУЛЯЦІЯ CONVERSION RATE")
print("-" * 70)

def simulate_conversions(conversion_rate: float, sample_size: int, simulations: int = 1000) -> List[float]:
    """Симулює conversion rates для певного розміру вибірки."""
    results = []

    for _ in range(simulations):
        # Генеруємо випадкові 0/1 для конверсій
        conversions = sum(random.random() < conversion_rate for _ in range(sample_size))
        rate = conversions / sample_size
        results.append(rate)

    return results

# Симулюємо конверсію 5% на 1000 користувачів (1000 раз)
true_rate = 0.05
sample_size = 1000
simulations = 1000

simulated_rates = simulate_conversions(true_rate, sample_size, simulations)

# Статистика симуляцій
mean_rate = statistics.mean(simulated_rates)
std_rate = statistics.stdev(simulated_rates)
min_rate = min(simulated_rates)
max_rate = max(simulated_rates)

print(f"True conversion rate: {true_rate*100}%")
print(f"Sample size: {sample_size}")
print(f"\nСимуляція {simulations} експериментів:")
print(f"  Mean: {mean_rate*100:.2f}%")
print(f"  Std Dev: {std_rate*100:.2f}%")
print(f"  95% Confidence Interval: [{(mean_rate - 1.96*std_rate)*100:.2f}%, {(mean_rate + 1.96*std_rate)*100:.2f}%]")
print(f"  Range: {min_rate*100:.2f}% - {max_rate*100:.2f}%")
print()

print("💡 Інсайти:")
print("  - Simulation показує реальну variability")
print("  - 95% CI говорить де буде результат у 95% випадків")
print("  - Більший sample size = меньша variability")
print()

# ============================================================================
# 3. ГЕНЕРУВАННЯ СИНТЕТИЧНИХ ДАНИХ
# ============================================================================

print("=" * 70)
print("PART 3: СИНТЕТИЧНІ ДАНІ - КОЛИ НА REAL DATA НЕ ВИСТАЧАЄ")
print("=" * 70)

# Реальна задача: Потрібно тестати модель, але real data обмежена/приватна

print("\n1. ГЕНЕРУВАННЯ КОРИСТУВАЦЬКИХ ПРОФІЛІВ")
print("-" * 70)

@dataclass
class UserProfile:
    user_id: int
    age: int
    country: str
    spending: float  # USD per month
    purchase_count: int

    def __repr__(self):
        return f"User({self.user_id}, age={self.age}, country={self.country}, spend=${self.spending:.0f})"

def generate_synthetic_users(count: int) -> List[UserProfile]:
    """Генерує синтетичних користувачів з реалістичним розподілом."""
    countries = ["US", "UK", "DE", "FR", "UA"]
    users = []

    for i in range(count):
        # Age: нормальний розподіл (25-55)
        age = int(random.gauss(40, 10))
        age = max(18, min(70, age))  # Constraints

        # Country: рівномірний розподіл
        country = random.choice(countries)

        # Spending: log-normal (більшість витрачає мало, деякі - багато)
        spending = random.lognormvariate(4.5, 0.8)

        # Purchase count: залежить від spending
        purchase_count = int(spending / random.uniform(50, 150))

        users.append(UserProfile(
            user_id=i,
            age=age,
            country=country,
            spending=spending,
            purchase_count=purchase_count
        ))

    return users

# Генеруємо 5 користувачів для демонстрації
synthetic_users = generate_synthetic_users(5)
print("Синтетичні користувачі:")
for user in synthetic_users:
    print(f"  {user}")

print()

# Статистика по синтетичних даних
all_users = generate_synthetic_users(1000)
ages = [u.age for u in all_users]
spending_list = [u.spending for u in all_users]

print(f"\nСтатистика на 1000 синтетичних користувачах:")
print(f"  Age: mean={statistics.mean(ages):.0f}, std={statistics.stdev(ages):.0f}")
print(f"  Spending: mean=${statistics.mean(spending_list):.0f}, median=${statistics.median(spending_list):.0f}")
print()

# ============================================================================
# 4. СТАТИСТИЧНІ РОЗПОДІЛИ
# ============================================================================

print("=" * 70)
print("PART 4: РОЗПОДІЛИ ДАНИХ - РОЗУМІННЯ PATTERNS")
print("=" * 70)

print("\n1. НОРМАЛЬНИЙ РОЗПОДІЛ (Normal Distribution)")
print("-" * 70)

# Генеруємо нормально розподілені дані (наприклад, час відповіді сервера)
response_times = [random.gauss(100, 15) for _ in range(1000)]  # 100ms avg, 15ms std

mean_rt = statistics.mean(response_times)
median_rt = statistics.median(response_times)
stdev_rt = statistics.stdev(response_times)

print(f"Response times (ms):")
print(f"  Mean: {mean_rt:.1f}ms")
print(f"  Median: {median_rt:.1f}ms")
print(f"  Std Dev: {stdev_rt:.1f}ms")
print(f"  95th percentile: {sorted(response_times)[int(0.95*len(response_times))]:.1f}ms")
print()

print("💡 Інсайти:")
print("  - Mean ≈ Median означає нормальний розподіл")
print("  - 95th percentile важливий для SLA")
print("  - Видаліть outliers перед аналізом")
print()

# ============================================================================
# 5. КЛАСТЕРИЗАЦІЯ - ПРОСТИЙ МЕТОД
# ============================================================================

print("=" * 70)
print("PART 5: ПРОСТИЙ K-MEANS (Manual Implementation)")
print("=" * 70)

# Реальна задача: Поділити користувачів на 3 群=ру за spending

print("\n1. ВЕКТОР КЛАСТЕРИЗАЦІЇ (1D CASE - spending)")
print("-" * 70)

def simple_kmeans_1d(data: List[float], k: int, iterations: int = 10):
    """Простий K-means для 1D даних."""

    # Ініціалізуємо центроїди випадково
    centroids = sorted(random.sample(data, k))

    for iteration in range(iterations):
        # Assign points to nearest centroid
        clusters = [[] for _ in range(k)]

        for point in data:
            nearest_centroid = min(range(k),
                                   key=lambda i: abs(point - centroids[i]))
            clusters[nearest_centroid].append(point)

        # Update centroids
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroids.append(statistics.mean(cluster))
            else:
                new_centroids.append(random.choice(data))

        centroids = sorted(new_centroids)

    return clusters, centroids

# Генеруємо 100 users та кластеризуємо по spending
spending_data = [random.lognormvariate(4.5, 0.8) for _ in range(100)]

clusters, centroids = simple_kmeans_1d(spending_data, k=3)

print(f"Розподіл користувачів на 3 群:")
for i, cluster in enumerate(clusters):
    if cluster:
        mean_spend = statistics.mean(cluster)
        print(f"  Cluster {i+1}: {len(cluster)} users, avg spend ${mean_spend:.0f}")

print(f"\nЦентроїди: {[f'${c:.0f}' for c in centroids]}")
print()

print("💡 Застосування:")
print("  - Сегментація користувачів")
print("  - Виявлення аномалій (outlier cluster)")
print("  - Price optimization (різні ціни для різних群)")
print()

# ============================================================================
# 6. ПРАКТИЧНІ ШАБЛОНИ
# ============================================================================

print("=" * 70)
print("PART 6: ПРАКТИЧНІ ШАБЛОНИ ДЛЯ PRODUCTION")
print("=" * 70)

print("\n1. CONFIDENCE INTERVAL CALCULATOR")
print("-" * 70)

def calculate_ci(samples: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Розраховує confidence interval для даних."""
    n = len(samples)
    mean = statistics.mean(samples)
    std = statistics.stdev(samples)

    # T-distribution для малих выборок
    # За простоту використаємо 1.96 (z-score для 95%)
    margin_of_error = 1.96 * std / math.sqrt(n)

    return (mean - margin_of_error, mean + margin_of_error)

# Приклад: розраховуємо CI для тривалості сесії
session_durations = [random.expovariate(1/300) for _ in range(50)]  # Avg 5 min

ci_lower, ci_upper = calculate_ci(session_durations)
mean_duration = statistics.mean(session_durations)

print(f"Session duration analysis (50 sessions):")
print(f"  Mean: {mean_duration:.0f}s")
print(f"  95% CI: [{ci_lower:.0f}s, {ci_upper:.0f}s]")
print(f"  Interpretation: 95% confident that true mean is in this range")
print()

# ============================================================================
# 7. ЗАВДАННЯ ДЛЯ ПРАКТИКИ
# ============================================================================

print("=" * 70)
print("PART 7: ПРАКТИЧНІ ЗАВДАННЯ")
print("=" * 70)

print("""
ЗАВДАННЯ 1 (ЛЕГКО): Розрахувати power analysis
  Дано: control conversion = 5%, expected lift = 10%
  Знайти: який sample size потрібен для significance?
  💡 Підказка: більший lift = менший потрібен sample size

ЗАВДАННЯ 2 (СЕРЕДНЬО): Реалізувати sequential testing
  - Тест працює поки не буде 100 conversions у обох версіях
  - Зупинити якщо різниця > 10%
  - Зупинити якщо sample size > 10k

ЗАВДАННЯ 3 (СКЛАДНО): Bayesian A/B testing
  Замість p-values, розраховувати posterior probability що B краще ніж A
  - Prior: обидва мають 50% шанс
  - Update з даних
  - Повернути P(B > A)

ЗАВДАННЯ 4 (БОНУС): Multi-armed bandit
  Реалізувати epsilon-greedy алгоритм:
  - 10% часу випробовуємо random button
  - 90% часу використовуємо найкращий button
  - Показати convergence до найкращої версії

Розв'яжіть на папері перед кодингом!
""")

print("\n" + "=" * 70)
print("ИТОГИ")
print("=" * 70)

print("""
✅ Що ви дізналися:
  1. A/B тестування як основа для product decisions
  2. Статистична значущість та confidence intervals
  3. Симуляції для валідації гіпотез
  4. Синтетичні дані для тестування
  5. Базова кластеризація та сегментація

🔑 Key insights для Senior Data Engineer:
  - A/B тесту без правильного дизайну експериментів = марна праця
  - Симуляції > теорія для практичних гіпотез
  - Синтетичні дані дозволяють тестувати fast
  - Segmentation дозволяє персоналізовану стратегію
  - Завжди думайте про sample size та power

⚠️  Частії помилки:
  - Пикінг winners під час тесту (p-hacking)
  - Неправильна sample size (занадто малий)
  -Ignoring seasonality у даних
  - Не фіксуючи конфаундинг змінні

🚀 Наступне: Парсинг та очищення реальних даних
""")
