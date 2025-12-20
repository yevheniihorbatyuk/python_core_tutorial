# Module 6: Beginner Edition
## Functional Programming & Object-Oriented Programming for Everyone

**Duration:** 3-4 hours
**Level:** Beginner to Intermediate
**Prerequisites:** Module 1-5 (Python basics)

---

## 🎯 What You'll Learn

### Part 1: Functional Programming (2 hours)
Master the four fundamental functional programming techniques used in every real project.

| Lesson | Topic | What You'll Do | Real Impact |
|--------|-------|----------------|------------|
| 1️⃣ | **Decimal** | Build a complete banking system with precise money handling | Banks process $100B+ daily with Decimal |
| 2️⃣ | **Generators** | Process millions of CSV rows with minimal memory | Netflix streams without loading entire file |
| 3️⃣ | **map/filter** | Clean messy data from web scraping and APIs | Data science = 80% data cleaning |
| 4️⃣ | **@lru_cache** | Optimize functions 10,000x faster with caching | Google caches search results for instant responses |

### Part 2: Object-Oriented Programming (1-2 hours)
Design real systems using classes and inheritance.

| Lesson | Topic | What You'll Do | Real Impact |
|--------|-------|----------------|------------|
| 5️⃣ | **Classes & Inheritance** | Build a user management system from scratch | Every web app (Flask, Django) uses this |
| | **Composition** | Add flexible features without code duplication | Netflix uses composition for 1000+ feature types |
| | **Polymorphism** | Same method, different behavior for different types | Enables flexible, maintainable code |

---

## 📁 File Structure

```
beginner_edition/
├── config.py                           # Configuration for all lessons
├── 01_decimal_banking.py              # Lesson 1: Decimal & Banking
├── 02_generators_csv_processing.py    # Lesson 2: Generators & CSV
├── 03_map_filter_data_cleaning.py     # Lesson 3: map/filter & Data Cleaning
├── 04_lru_cache_recommendations.py    # Lesson 4: Caching & Performance
├── 05_classes_user_management.py      # Lesson 5: Classes & OOP
├── README_beginner.md                 # This file
└── data/                              # Sample data (created by lessons)
```

---

## 🚀 Quick Start

### Run All Lessons
```bash
# Lesson 1: Decimal for Banking (10 minutes)
python3 01_decimal_banking.py

# Lesson 2: Generators for CSV (15 minutes)
python3 02_generators_csv_processing.py

# Lesson 3: map/filter for Data Cleaning (15 minutes)
python3 03_map_filter_data_cleaning.py

# Lesson 4: @lru_cache for Performance (10 minutes)
python3 04_lru_cache_recommendations.py

# Lesson 5: Classes for User Management (15 minutes)
python3 05_classes_user_management.py
```

### Expected Output
Each lesson prints:
- ✅ Theory explanation
- ✅ Problem demonstration
- ✅ Solution explanation
- ✅ Practical working example
- ✅ Real-world impact
- ✅ Performance metrics

---

## 📚 Lesson Summaries

### Lesson 1: Decimal ➡️ Financial Precision

**Problem:** Float arithmetic fails for money
```python
0.1 + 0.2 = 0.30000000000000004  # ❌ Wrong!
```

**Solution:** Use Decimal for exact calculations
```python
Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # ✅ Correct!
```

**What You Learn:**
- Why float fails (binary representation)
- How Decimal solves it (exact decimal strings)
- Building a banking system with accounts and transactions
- Interest calculations, fees, transfers

**Real Impact:**
- Banks process $100+ billion daily using Decimal
- One penny error repeated = millions in discrepancies
- IRS uses Decimal for tax calculations

---

### Lesson 2: Generators ➡️ Process Big Data Efficiently

**Problem:** Loading large files crashes
```python
# 1 billion rows × 1KB per row = 1,000,000 MB RAM needed
# Most computers have 8-16 GB max → CRASH!
all_data = load_entire_file()  # ❌ Out of memory
```

**Solution:** Process one row at a time with generators
```python
def read_file():
    for row in file:
        yield row  # Give to caller, pause execution

for row in read_file():  # ✓ Only 1 row in memory
    process(row)
```

**What You Learn:**
- Memory comparison: list vs generator
- How yield works (pause and resume)
- Reading CSV files with generators
- Chaining generators for data pipelines
- Streaming analysis (online algorithms)

**Real Impact:**
- YouTube streams billions of videos (1KB chunks)
- Netflix processes user logs without loading all to RAM
- Twitter handles real-time tweet stream
- Data science pipelines handle terabytes

---

### Lesson 3: map/filter/lambda ➡️ Transform Data Elegantly

**Problem:** Manual data cleaning is verbose
```python
cleaned = []
for row in data:
    if is_valid(row):
        cleaned.append(normalize(row))  # ❌ Lots of code
```

**Solution:** Use functional transformations
```python
cleaned = list(map(normalize, filter(is_valid, data)))  # ✓ Concise
```

**What You Learn:**
- `map()`: Transform each element
- `filter()`: Keep only matching elements
- `lambda`: Quick anonymous functions
- Composing transformations together
- Data validation and normalization

**Real Impact:**
- Data science: 80% of work is cleaning messy data
- Every company has dirty data from web scraping
- Data pipelines transform terabytes daily
- Functional approach = cleaner, testable code

---

### Lesson 4: @lru_cache ➡️ Optimize 10,000x Faster

**Problem:** Expensive functions called repeatedly
```python
fib(30)  # Takes 1 second (1 billion operations)
fib(30)  # Takes 1 second again (recalculated!)
```

**Solution:** Cache results with @lru_cache
```python
@lru_cache(maxsize=128)
def fib(n):
    ...

fib(30)  # Takes 1 second (calculated)
fib(30)  # Takes 0.00002ms (from cache!) ← 50,000x faster!
```

**What You Learn:**
- How caching works (LRU = Least Recently Used)
- When to use caching (pure functions, expensive computation)
- Monitoring cache hits/misses
- When NOT to use caching (side effects, random numbers)
- 3-tier caching strategy (in-process, distributed, database)

**Real Impact:**
- Netflix saves 10,000+ seconds daily with caching
- Google caches search results (30% queries repeat)
- ML systems cache predictions for same users
- Database queries use caching internally

---

### Lesson 5: Classes & OOP ➡️ Build Scalable Systems

**Problem:** Functions don't scale for complex data
```python
def create_user(user_id, name, email, role, status, ...):  # Too many params!
    ...

def validate_user(user):  # Need validation in every function!
    ...

def change_status(user, new_status):  # No enforcement!
    ...
```

**Solution:** Use classes to organize data + behavior
```python
class User:
    def __init__(self, user_id, name, email, role):
        self.validate()  # ✓ Automatic validation

    def change_status(self, new_status):
        if not self.can_change():
            raise ValueError()  # ✓ Enforced rules
```

**What You Learn:**
- Class basics: attributes (data), methods (behavior)
- Inheritance: Employee(User) reuses code
- Composition: User HAS-A Address (flexible)
- Polymorphism: Same method, different behavior
- Encapsulation: Hide internal details

**Real Impact:**
- Every web framework (Flask, Django) uses classes
- Every database ORM (SQLAlchemy) models data as classes
- Every REST API returns class instances
- All modern software architecture uses OOP

---

## 💡 Key Concepts Quick Reference

### Decimal (Precision)
```python
from decimal import Decimal

# ✓ Do this
balance = Decimal("1000.00")  # From string!
amount = Decimal("0.01")
new_balance = balance - amount

# ✗ Don't do this
balance = Decimal(1000.0)  # From float!
```

### Generators (Memory Efficiency)
```python
# ✓ Efficient
def read_csv():
    for row in file:
        yield row

# ✗ Wasteful
rows = list(file.readlines())  # All in memory!
```

### map/filter (Transformations)
```python
# ✓ Functional
squared = map(lambda x: x**2, numbers)
evens = filter(lambda x: x % 2 == 0, numbers)

# ✓ Pythonic (preferred)
squared = [x**2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
```

### @lru_cache (Performance)
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(n):
    # This is cached!
    return complex_calculation(n)

# Cache info
info = expensive_function.cache_info()
print(f"Hits: {info.hits}, Misses: {info.misses}")

# Clear cache when data changes
expensive_function.cache_clear()
```

### Classes (Organization)
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def login(self):
        return f"Welcome {self.name}"

# Inheritance
class Employee(User):
    def __init__(self, name, email, salary):
        super().__init__(name, email)
        self.salary = salary

# Use it
user = Employee("Alice", "alice@example.com", 80000)
print(user.login())  # Inherits from User
```

---

## ✅ Self-Assessment Checklist

After each lesson, you should understand:

### Lesson 1: Decimal
- [ ] Why float fails for money (binary representation)
- [ ] How Decimal solves the problem (exact decimals)
- [ ] When to use Decimal (always for money!)
- [ ] Real-world impact (banks, healthcare, law)

### Lesson 2: Generators
- [ ] Memory comparison (list vs generator)
- [ ] How yield works (pause and resume)
- [ ] When to use generators (big data, streams)
- [ ] Generator chaining (pipeline pattern)

### Lesson 3: map/filter/lambda
- [ ] What map does (transform each element)
- [ ] What filter does (select matching elements)
- [ ] When lambda is useful (quick, one-time functions)
- [ ] When to use functional vs list comprehension

### Lesson 4: @lru_cache
- [ ] How caching works (remember results)
- [ ] Performance impact (100x-10,000x speedup)
- [ ] When to cache (pure functions, expensive computations)
- [ ] When NOT to cache (side effects, non-deterministic)

### Lesson 5: Classes & OOP
- [ ] Class vs object (blueprint vs instance)
- [ ] Why classes (organize data + behavior)
- [ ] Inheritance (code reuse, IS-A)
- [ ] Composition (flexible combining, HAS-A)
- [ ] Polymorphism (same method, different behavior)

---

## 🎓 Exercises (Homework)

### Exercise 1: Banking System
Extend 01_decimal_banking.py:
```python
# Add new features:
1. Create 3 accounts
2. Transfer between accounts
3. Calculate account balances with interest
4. Print statement showing all transactions
5. Calculate total assets across all accounts

# Make sure:
- All calculations use Decimal
- All amounts are precise to the cent
- Validate all inputs
```

### Exercise 2: Data Cleaning Pipeline
Extend 03_map_filter_data_cleaning.py:
```python
# Create a CSV file with messy data:
1. Different case (UPPERCASE, lowercase, MixedCase)
2. Whitespace in amounts
3. Invalid categories
4. Missing values
5. Duplicate rows

# Write a cleaning pipeline that:
- Normalizes all data
- Removes duplicates
- Validates all fields
- Produces clean output
```

### Exercise 3: Recommendation System with Caching
Extend 04_lru_cache_recommendations.py:
```python
# Add new features:
1. Load recommendations from file
2. Cache recommendations by user
3. Monitor cache hit rate
4. Implement cache timeout (TTL)
5. Compare performance: with/without cache

# Measure:
- Time to get recommendations (first vs second call)
- Cache hit rate
- Memory usage
```

### Exercise 4: User Management Extension
Extend 05_classes_user_management.py:
```python
# Add new classes:
1. Manager (extends Employee, manages other users)
2. AdminUser (extends User, special privileges)
3. Team (composition: has many users)
4. Department (composition: has teams)

# Add functionality:
- Promote user to manager
- Assign users to teams
- Teams report to departments
- Display organizational chart
```

---

## 📖 Additional Resources

### Python Documentation
- [Decimal Module](https://docs.python.org/3/library/decimal.html)
- [Generators](https://docs.python.org/3/howto/functional.html)
- [functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- [Classes](https://docs.python.org/3/tutorial/classes.html)

### Recommended Reading
- Clean Code (Robert C. Martin) - Chapter on Functions
- Design Patterns (Gang of Four)
- Fluent Python (Luciano Ramalho) - Excellent OOP coverage

### Related Modules
- Module 4: Data Structures & Collections
- Module 7: Advanced Data Structures (LinkedList, Tree, Graph) - Uses Classes heavily
- Module 8: File I/O & APIs - Uses Generators and Classes
- Module 9+: Web Development - 100% OOP frameworks

---

## 🚀 Next Steps After This Module

1. **Practice:** Do all exercises above
2. **Extend:** Add features not covered here
3. **Combine:** Mix FP and OOP (e.g., @lru_cache on class methods)
4. **Real Project:** Build a small project using what you learned
5. **Advanced Edition:** See ../advanced_edition/ for real-world scenarios

---

## 💬 Common Questions

**Q: Should I memorize all the code?**
A: No! Understand concepts and look up syntax. Re-read the explanations until concepts click.

**Q: When should I use functions vs classes?**
A: Functions for simple calculations, Classes for complex data with related behavior.

**Q: Is functional or OOP better?**
A: Both! Use functional for data transformation, OOP for system architecture.

**Q: Do I need to understand MRO (Method Resolution Order)?**
A: Not for Beginner Edition. See Advanced Edition for MRO details.

**Q: How do I know if my cache maxsize is right?**
A: Monitor cache_info() and adjust based on hit rate (target 70%+).

---

## 🎯 Success Criteria

You've completed Beginner Edition when you can:

✅ Write a banking system using Decimal with multiple accounts
✅ Process a 1 million row CSV with <1KB memory using generators
✅ Clean messy data using map/filter
✅ Speed up a function 100+ times using @lru_cache
✅ Design a class hierarchy with inheritance and composition
✅ Implement polymorphism (different methods with same name)
✅ Combine all concepts in a real project

---

## 📞 Getting Help

If you're stuck:
1. Re-read the lesson introduction
2. Check the "KEY TAKEAWAYS" section
3. Look at the practical example
4. Try modifying the example
5. Check Python documentation
6. See Advanced Edition for more complex examples

---

**Ready to level up? After mastering Beginner Edition, move on to Advanced Edition!**

🎉 **You're learning the fundamental skills that power every professional Python developer!**
