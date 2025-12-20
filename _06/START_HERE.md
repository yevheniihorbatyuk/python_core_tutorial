# Module 6: START HERE 🚀

## What Is This Module About?

This module teaches you **how professional developers write code** using two fundamental approaches:

1. **Functional Programming (FP)** - Write clean, fast, precise functions
2. **Object-Oriented Programming (OOP)** - Organize code into reusable, maintainable classes

---

## 📊 Quick Overview

### Part 1: Functional Programming (1.5 hours)

Learn to write functions that are **fast, clean, and precise**.

| Topic | Problem | Solution | Impact |
|-------|---------|----------|--------|
| Decimal | `0.1 + 0.2 = 0.30000000004` ❌ | `Decimal('0.1') + Decimal('0.2') = 0.3` ✅ | Penny-perfect money |
| Generators | Read 1M lines → 100MB RAM | Read 1M lines → 0.1KB RAM | 1000x less memory |
| map/filter | Manual loops, verbose code | Functional transforms | Cleaner code |
| @lru_cache | fib(30) = 1000ms | fib(30) = 0.00001ms | 10,000x faster |

**Run it:** `python3 01_functional_programming.py`

### Part 2: Object-Oriented Programming (2 hours)

Learn to structure code using **classes and inheritance**.

| Topic | What You Learn | Real Example |
|-------|----------------|--------------|
| Classes | Objects with data + methods | Person(name, age) |
| Inheritance | Reuse code (DRY) | Employee inherits Person |
| Composition | Flexible combining | Person HAS-A Address |
| Polymorphism | Same name, different behavior | speak() for Dog, Cat |
| MRO | Method lookup order | Which speak() runs? |

**Run it:** `python3 02_oop_classes.py`

---

## 🎯 Why This Matters

### Web Development
```python
# Flask (web framework) = OOP classes
from flask import Flask

app = Flask(__name__)  # app is an object of Flask class

@app.route('/home')  # decorator (FP concept!)
def home():
    return "Hello"
```

### Data Science
```python
# sklearn = OOP classes
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()  # model is an object
model.fit(X, y)  # call method
prediction = model.predict(X_test)  # call another method
```

### Finance
```python
# Banks use Decimal for precision
from decimal import Decimal

balance = Decimal('1000.00')
balance += Decimal('50.50')
# Exactly correct, no floating point errors!
```

---

## 🚀 Getting Started

### Step 1: Read the Lesson Plan
```bash
cat 00_LESSON_PLAN.md
```

### Step 2: Run Part 1 (Functional Programming)
```bash
python3 01_functional_programming.py
```

You'll see:
- Why floating point is dangerous
- How generators save memory
- Performance benchmarks
- Practical examples

### Step 3: Run Part 2 (OOP)
```bash
python3 02_oop_classes.py
```

You'll see:
- How classes organize code
- Why inheritance prevents duplication
- Real-world web and data science examples
- Method resolution order explained

---

## 💡 Key Insights

### Functional Programming
- **Write pure functions** (no side effects)
- **Use generators** for large data (memory efficient)
- **Use @lru_cache** for expensive computations (speed)
- **Use Decimal** for money (accuracy)

### Object-Oriented Programming
- **Use classes** to organize related data and behavior
- **Use inheritance** to avoid repeating code
- **Use composition** for flexibility
- **Understand MRO** to know which method runs

---

## 📈 Learning Path

```
Foundation (Modules 1-5)
        ↓
THIS MODULE: Learn FP and OOP ← YOU ARE HERE
        ↓
Module 7: Apply OOP to Data Structures (LinkedList, Tree)
        ↓
Module 8: Use both concepts in File I/O and APIs
        ↓
Module 9+: Web Development (100% OOP frameworks)
        ↓
Professional: Can read and write ANY Python code
```

---

## 🎓 Quick Check

**You understand Functional Programming when you can answer:**
- [ ] Why is Decimal better than float for money?
- [ ] What does `yield` do in a generator?
- [ ] How does `@lru_cache` make code faster?
- [ ] What's the difference between `map()` and a for loop?

**You understand OOP when you can answer:**
- [ ] What is a class and what is an object?
- [ ] Why does inheritance prevent code duplication?
- [ ] When should you use composition instead of inheritance?
- [ ] What does MRO determine?

---

## 📚 Complete Contents

1. **00_LESSON_PLAN.md** - Detailed lesson plan (4-5 hours)
2. **01_functional_programming.py** - FP concepts with code
3. **02_oop_classes.py** - OOP concepts with code
4. **README.md** - Complete guide with exercises

---

## ⚡ Pro Tips

1. **Run the code** - Don't just read it, execute it and see the output
2. **Modify examples** - Change numbers, add print statements, break things!
3. **Compare approaches** - See the difference between procedural vs functional vs OOP
4. **Benchmark** - Notice the actual performance improvements
5. **Apply immediately** - Use these concepts in your next project

---

## 🏆 What You'll Be Able To Do

After this module, you can:

✅ Write fast, clean functions that don't crash on precision
✅ Handle massive datasets without running out of memory
✅ Design classes that solve real problems
✅ Build applications using inheritance properly
✅ Understand almost any Python code you see
✅ Start learning web frameworks (Flask, Django)
✅ Read data science code (sklearn, pandas)
✅ Be confident in advanced Python concepts

---

## 🎯 Next Steps

1. Run `python3 01_functional_programming.py` NOW
2. Run `python3 02_oop_classes.py` NOW
3. Read the complete `00_LESSON_PLAN.md`
4. Try the exercises in `README.md`
5. Build your own project combining both

---

**Let's code! 🚀**

Questions? Check `README.md` for detailed explanations.
