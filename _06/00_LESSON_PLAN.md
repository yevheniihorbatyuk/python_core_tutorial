# Module 6: Functional Programming and Object-Oriented Programming
## Comprehensive Lesson Plan with Real-World Examples

**Duration:** 4-5 hours
**Level:** Intermediate (after modules 1-5)
**Format:** Theory + Live Coding + Practical Projects
**Target Audience:** Developers who want to understand why FP and OOP matter

---

## 🎯 Learning Objectives

After this lesson, students will be able to:

✅ Understand the difference between procedural, functional, and object-oriented programming
✅ Write clean functional code (@lru_cache, map, filter, lambda, generators)
✅ Design classes with proper architecture
✅ Use inheritance and composition effectively
✅ Apply these concepts in real-world projects (Data Science, Web, Systems)
✅ Understand MRO (Method Resolution Order) and its importance

---

## 📚 Lesson Structure

### PART 1: Functional Programming (70 minutes)

#### 1.1 What is Functional Programming? (10 min)

**Theory:**

Functional Programming (FP) is a programming paradigm where:
- Functions are first-class citizens (can be passed as arguments)
- Data is immutable (doesn't change after creation)
- Computation is about transforming data, not mutating state

**The Problem with Procedural Code:**

```python
# ❌ PROCEDURAL CODE (mutates state)
scores = [85, 92, 78, 95]
total = 0
for score in scores:
    total += score
average = total / len(scores)

# PROBLEMS:
# - total changes multiple times
# - Hard to test (dependent on order)
# - Hard to parallelize (needs synchronization)
```

**Solution with FP:**

```python
# ✅ FUNCTIONAL CODE (pure, immutable)
scores = [85, 92, 78, 95]
average = sum(scores) / len(scores)

# BENEFITS:
# - No side effects
# - Easy to test (same input → same output)
# - Easy to parallelize
# - Easy to refactor
```

**Key FP Principles:**

```
1. Pure Functions
   ├─ Same input → Same output
   ├─ No side effects
   └─ Don't depend on global state

2. Immutability
   ├─ Data doesn't change in place
   ├─ Create new structures instead
   └─ Original remains untouched

3. Higher-Order Functions
   ├─ Functions can take functions as arguments
   ├─ Functions can return functions
   └─ Enables composition and reusability

4. Recursion
   ├─ Instead of iterative loops
   ├─ Each call handles one part
   └─ Base case stops recursion
```

#### 1.2 Decimal and Precision in Calculations (15 min)

**Theory: Why is 0.1 + 0.2 ≠ 0.3?**

```python
# ❌ PROBLEM: Floating Point Precision
print(0.1 + 0.2)  # 0.30000000000000004 (ERROR!)
print(0.1 + 0.2 == 0.3)  # False (!)

# REASON: 0.1 and 0.2 cannot be exactly represented in binary
# 0.1 in binary = 0.0001100110011... (infinite)
# Computer truncates → rounding error

# CONSEQUENCES:
# - Financial transactions give wrong results
# - Scientific calculations accumulate errors
# - Legal/financial problems ($0.0000000004!)
```

**Solution: Decimal Module**

```python
from decimal import Decimal

# ✅ EXACT CALCULATIONS
result = Decimal('0.1') + Decimal('0.2')
print(result)  # 0.3 (exactly!)
print(result == Decimal('0.3'))  # True (correct!)

# BENEFITS:
# - Precise financial calculations
# - Can define precision (decimal places)
# - Protection from cumulative errors
```

#### 1.3 Generators and yield (20 min)

**Theory: Why Are Generators Important?**

```
Scenario: Read 1 million lines from a file
┌─────────────────────────────────────────────┐
│ Approach 1: Read ALL into memory (list)    │
├─────────────────────────────────────────────┤
│ data = [line for line in open('big.txt')] │
│ RAM needed: 1M lines × 100 bytes = 100MB   │
│ Time to first line: long (read everything) │
│ PROBLEM: Small devices will crash!         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Approach 2: Generator (yield)              │
├─────────────────────────────────────────────┤
│ def read_big_file(file_path):              │
│     for line in open(file_path):           │
│         yield line  # Lazy evaluation      │
│                                             │
│ RAM needed: 1 line × 100 bytes = 0.1KB     │
│ Time to first line: instant!               │
│ BENEFITS: Works on small devices           │
└─────────────────────────────────────────────┘
```

**Real-World Impact:**
- YouTube reads video chunks as generators (not whole file)
- Netflix streams video (doesn't download everything)
- Pandas reads CSV files in chunks with generators

#### 1.4 map, filter, lambda (15 min)

**Transforming Data Functionally:**

```python
# PROBLEM: Transform a list
numbers = [1, 2, 3, 4, 5]

# ❌ Procedural (verbose, loop)
squared = []
for n in numbers:
    squared.append(n ** 2)

# ✅ Functional (declarative)
squared = list(map(lambda n: n ** 2, numbers))
# or
squared = [n ** 2 for n in numbers]  # Pythonic
```

#### 1.5 Decorators and @lru_cache (10 min)

**Decorators modify function behavior:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# fib(30): 1 billion operations (1+ sec) → 31 operations (0.0001 sec)
# 10,000x SPEEDUP!
```

---

### PART 2: Object-Oriented Programming (100 minutes)

#### 2.1 Basics: Classes and Objects (20 min)

**Theory: What is a Class?**

A class is a blueprint (template) for creating objects.

```
┌──────────────────────────────────────┐
│ Real World                           │
├──────────────────────────────────────┤
│ Blueprint: Car                       │
│   ├─ Brand: Toyota                   │
│   ├─ Model: Camry                    │
│   ├─ Color: Black                    │
│   └─ Methods: drive(), park(), refuel│
│                                      │
│ Instance: My Car (specific)          │
│   ├─ Brand: Toyota                   │
│   ├─ Model: Camry                    │
│   ├─ Color: Black                    │
│   └─ Actions: drive to work          │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ Python Code                          │
├──────────────────────────────────────┤
│ class Car:  # Blueprint              │
│     def __init__(self, brand):       │
│         self.brand = brand           │
│                                      │
│ my_car = Car("Toyota")  # Instance   │
└──────────────────────────────────────┘
```

#### 2.2 Inheritance: Reusing Code (30 min)

**Without Inheritance (DRY violation):**
```
Person class:          Employee class:        Student class:
- name                 - name  (DUPLICATE!)   - name  (DUPLICATE!)
- age                  - age   (DUPLICATE!)   - age   (DUPLICATE!)
- info()               - salary               - school
                       - info() (DUPLICATE!)  - info() (DUPLICATE!)
```

**With Inheritance (DRY):**
```
        Person class (one source of truth)
        - name, age, info()
        /              \
    Employee        Student
    - salary        - school
    - info()        - info()
    (override)      (override)
```

**Benefits:**
- Reduce code duplication
- Easier to maintain
- Changes in one place affect all subclasses
- Clear logical hierarchy

#### 2.3 Composition vs Inheritance (20 min)

**When to use what:**

```
INHERITANCE ("IS-A"):
  Employee IS-A Person
  ├─ Logical hierarchy
  ├─ Shares behavior
  └─ Fragile with deep hierarchies

COMPOSITION ("HAS-A"):
  Person HAS-A Address
  ├─ More flexible
  ├─ Easier to change
  └─ Recommended in modern OOP
```

#### 2.4 Method Resolution Order (MRO) (15 min)

**Multiple Inheritance Problem:**

```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Pet(Dog, Cat):  # Which speak()? Dog's or Cat's?
    pass

pet = Pet()
print(pet.speak())  # Dog's speak() - MRO is Dog → Cat → Animal

# MRO (Method Resolution Order):
print(Pet.mro())
# [Pet, Dog, Cat, Animal, object]
```

---

### PART 3: Integration and Real-World Examples (50 minutes)

#### 3.1 Real-World: Data Science Project

**User Segmentation System:**
- User base class with purchase history
- Different user types (Regular, Premium)
- Calculate spending, discounts, lifetime value

#### 3.2 Real-World: Web Framework

**Simple Flask-like Framework:**
- Route class for HTTP endpoints
- WebApp class for managing routes
- Decorator pattern for route registration

---

## 🏁 Homework Assignments

### Assignment 1: Project Management System

Build a system for managing projects and tasks:
- Project class with task list
- Task class with difficulty levels
- Developer class with skill levels
- Assign tasks to developers
- Calculate project completion time

### Assignment 2: Functional Data Pipeline

Transform data functionally:
1. Filter even numbers
2. Square them
3. Filter > 50
4. Calculate sum

Implement using:
1. filter() and map()
2. List comprehension
3. Functional pipeline class

### Assignment 3: Real-World Project (Choose One)

**A) Data Science:** User segmentation and churn prediction
**B) Web:** Simple API with routing and middleware
**C) Finance:** Personal finance management system

---

## 🔗 Connection to Future Modules

### Module 7 (Data Structures):
- Classes form the basis for data structures (LinkedList, Tree, Graph)
- Composition used for nested structures

### Module 8 (Files & APIs):
- Classes for file handling and API interactions
- Decorators for validation and logging

### Module 9+ (Web Development):
- OOP is the foundation of all web frameworks (Flask, Django)
- Inheritance for models and controllers
- Decorators for routing and middleware

### Data Science:
- @lru_cache for caching expensive computations
- Classes for models (sklearn, pandas use OOP extensively)
- Functional style for data pipelines

---

## 📊 Success Metrics

Student knows this module if they can:

- [ ] Write pure functions without side effects
- [ ] Use decorators to modify function behavior
- [ ] Design class hierarchies without code duplication
- [ ] Choose between inheritance and composition
- [ ] Trace MRO to understand which method executes
- [ ] Combine FP and OOP in a real project
- [ ] Understand what previously seemed like "black magic"

---

**Lesson Complete!** ✅
