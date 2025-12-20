# Module 6: Functional Programming and OOP
## Complete Guide with Real-World Applications

Welcome to Module 6! This is where you learn the **two fundamental paradigms** that power all modern software: Functional Programming (FP) and Object-Oriented Programming (OOP).

---

## 📚 What You'll Learn

### Part 1: Functional Programming (Lesson 1)
- **Decimal** - Financial precision for banking systems
- **Generators** - Lazy evaluation for handling millions of records
- **map/filter/lambda** - Functional data transformations
- **@lru_cache** - Optimize code with 1000x+ speedups

### Part 2: Object-Oriented Programming (Lesson 2)
- **Classes** - Design blueprints for your systems
- **Inheritance** - Reuse code without duplication (DRY)
- **Composition** - Flexible object combining (HAS-A)
- **Polymorphism** - One interface, many implementations
- **MRO** - Understand method resolution order

---

## 🎯 Why This Matters

### Real-World Impact

**Functional Programming:**
- YouTube watches billions of videos → uses generators to stream chunks
- Netflix processes user data → @lru_cache speeds up recommendations
- Banks handle trillions → Decimal ensures penny-perfect transactions
- Data Science pipelines → map/filter transform datasets

**Object-Oriented Programming:**
- **Every web framework** (Flask, Django) is built on OOP classes
- **All data science libraries** (sklearn, pandas, TensorFlow) use OOP
- **Financial systems** model instruments as classes
- **Modern systems** architect with inheritance and composition

---

## 📂 Files

| File | Purpose |
|------|---------|
| `00_LESSON_PLAN.md` | Complete lesson plan (4-5 hours) |
| `01_functional_programming.py` | Decimal, generators, map/filter, @lru_cache |
| `02_oop_classes.py` | Classes, inheritance, composition, MRO |

---

## 🚀 Quick Start

### Run the Code

```bash
# Part 1: Functional Programming
python3 01_functional_programming.py

# Part 2: Object-Oriented Programming
python3 02_oop_classes.py
```

### What You'll See

Both files include:
- ✅ Theory explanations
- ✅ Code demonstrations
- ✅ Performance benchmarks
- ✅ Real-world examples
- ✅ Key takeaways

---

## 📊 Learning Progression

### Functional Programming

```
Decimal:        0.1 + 0.2 = 0.3 exactly (not 0.30000000004)
                ↓
Generators:     Read 1M lines with 0.1KB RAM (not 100MB)
                ↓
map/filter:     Transform data without loops
                ↓
@lru_cache:     fib(30) in 0.00001ms (not 1000ms)
                ↓
RESULT:         Faster, cleaner, more precise code
```

### Object-Oriented Programming

```
Classes:        Blueprint → Objects (real things)
                ↓
Inheritance:    Employee inherits from Person (DRY)
                ↓
Composition:    Person HAS-A Address (flexible)
                ↓
Polymorphism:   Same method name, different behavior
                ↓
MRO:            Understand which method actually runs
                ↓
RESULT:         Maintainable, scalable, professional code
```

---

## 💡 Key Concepts

### Functional Programming

**Pure Functions:**
- Same input → always same output
- No side effects
- Easy to test and parallelize

**Immutability:**
- Data doesn't change
- Create new structures instead
- Safer, easier to reason about

**Higher-Order Functions:**
- Functions take functions as arguments
- Functions return functions
- Enables composition and reusability

### Object-Oriented Programming

**Encapsulation:**
- Bundle data and behavior together
- Hide internal details
- Control how things are used

**Inheritance:**
- Parent → Child relationships
- Child has parent's methods + adds own
- Reduces code duplication

**Composition:**
- Objects contain other objects
- More flexible than inheritance
- Recommended in modern design

---

## 🔗 Connections to Other Modules

### Previous Modules
- Module 1-5: Built foundation for this material
- Used functions, loops, conditions to understand FP concepts

### Next Modules
- **Module 7**: Data structures (LinkedList, Tree, Graph) use OOP classes
- **Module 8**: File handling and APIs use classes and decorators
- **Module 9+**: Web development (Flask, Django) is 100% OOP
- **Data Science**: All libraries (sklearn, pandas) use OOP extensively

### Real Applications
```
Web Development:
  Django/Flask = OOP classes for models, views, controllers
  Decorators = @app.route() for URL routing

Data Science:
  sklearn = Classifier, Regressor classes (inheritance)
  @lru_cache = speed up predictions for same inputs

Finance:
  Classes for Stock, Bond, Portfolio (inheritance)
  Decimal for all price calculations
  Generators for processing huge transaction logs
```

---

## 📋 Exercises

### Exercise 1: Banking System
Build a banking system with:
- Account class (balance, transactions)
- SavingsAccount (inheritance, has interest rate)
- TransactionLogger (composition)
- Use Decimal for all calculations

### Exercise 2: E-commerce
Create an e-commerce system with:
- User class (registration, purchases)
- RegularUser and PremiumUser (inheritance)
- Product and CartItem (composition)
- @lru_cache for product recommendations

### Exercise 3: Data Pipeline
Build a data transformation pipeline:
- Use generators to read large CSV files
- Transform with map/filter
- Calculate statistics without loading everything in memory
- Compare performance: list vs generator

---

## 🎓 Self-Assessment

You understand this module when you can:

- [ ] Write pure functions without side effects
- [ ] Explain why Decimal matters for money
- [ ] Use generators to handle large datasets efficiently
- [ ] Transform data with map/filter/lambda
- [ ] Measure performance improvements with @lru_cache
- [ ] Design a class hierarchy without duplication
- [ ] Choose between inheritance and composition
- [ ] Trace MRO to understand method execution
- [ ] Explain polymorphism and method overriding
- [ ] Build a real application using both FP and OOP

---

## 📖 Further Reading

### Python Documentation
- [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
- [Classes](https://docs.python.org/3/tutorial/classes.html)
- [functools - lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- [decimal - Decimal arithmetic](https://docs.python.org/3/library/decimal.html)

### Best Practices
- Clean Code by Robert C. Martin
- Design Patterns by Gang of Four
- Python Design Patterns book

---

## 🎯 Performance Impact Examples

### From This Module

**@lru_cache:**
```
Without: fib(30) = 1 billion operations = 1000ms
With:    fib(30) = 31 operations = 0.00001ms
Result:  10,000x faster!
```

**Generators:**
```
Without: Read 1M lines = 100MB RAM
With:    Read 1M lines = 0.1KB RAM
Result:  1,000,000x less memory!
```

**Decimal:**
```
Without: 0.1 + 0.2 = 0.30000000004 (WRONG!)
With:    0.1 + 0.2 = 0.3 (CORRECT!)
Result:  Financial accuracy, legal compliance!
```

---

## 🏆 Project Ideas

### Beginner
- Bank account management system
- Simple e-commerce store
- Data CSV transformer

### Intermediate
- Multi-level authentication system (inheritance)
- Recommendation engine with @lru_cache
- Game character hierarchy (inheritance)

### Advanced
- Machine learning pipeline (generators + classes)
- Multi-layer caching system
- Framework with decorators and routing

---

## 📞 Getting Help

Concepts that seem confusing at first:
- **Inheritance**: Draw diagrams (parent → child relationships)
- **MRO**: Use Python's `Class.mro()` to see the order
- **Composition**: Think "HAS-A" (Person HAS-A Address)
- **Generators**: Think "lazy" (create on-the-fly, not all at once)
- **Decorators**: Think "wrapper" (wrap function without changing code)

---

## ✅ Summary

| Concept | What It Is | Why It Matters | Real Example |
|---------|-----------|----------------|--------------|
| **Decimal** | Exact arithmetic | Money is precise | Bank balance $100.00 |
| **Generator** | Lazy evaluation | Save memory | Read 1M file lines |
| **map/filter** | Data transform | Clean code | Analyze user data |
| **@lru_cache** | Function caching | Speed up code | ML predictions |
| **Classes** | Object blueprint | Organize code | Person, Employee |
| **Inheritance** | Code reuse | DRY principle | Child inherits parent |
| **Composition** | Object combining | Flexibility | Person HAS Address |
| **Polymorphism** | Same interface | Flexible code | speak() different animals |
| **MRO** | Method lookup order | Understand execution | Which method runs? |

---

**Ready to become a better Python developer!** 🚀

Go ahead - run the code, do the exercises, build something awesome!
