# Module 8: Serialization and Object Copying
# START HERE

Welcome to Module 8. This module teaches how to **persist Python objects**, safely serialize data, and **copy complex structures** without bugs.

---

## ✅ Prerequisites

- Module 4 (files, JSON, CSV)
- Module 6 (OOP basics)

---

## 📂 Files in this module

```
_08/
├── 00_lesson_plan.md
├── 01_user_class_encapsulation.py
├── 02_pickle_serialization.py
├── 03_json_csv_serialization.py
├── 04_copying_objects.py
├── 05_practice_tasks.py
├── START_HERE.md
└── README.md
```

---

## 🚀 Quick Start

```bash
# From python_core/
cd _08/

# 1) Encapsulation and password handling
python3 01_user_class_encapsulation.py

# 2) Pickle serialization with getstate/setstate
python3 02_pickle_serialization.py

# 3) JSON + CSV serialization
python3 03_json_csv_serialization.py

# 4) Shallow vs deep copy
python3 04_copying_objects.py

# 5) Practice tasks
python3 05_practice_tasks.py
```

---

## 🧭 How to study this module

1. Run each file and read the printed output.
2. Pause and explain **why** the output looks that way.
3. Modify examples (change fields, add nested data) and re-run.
4. Solve tasks in `05_practice_tasks.py`.

---

## ⚠️ Important Notes

- **Pickle is unsafe for untrusted data.** Only load pickle from trusted sources.
- JSON is **safe and interoperable**, but needs custom encoding for objects.
- Copying mistakes cause **shared mutable state** bugs in production.

---

If you only have 30 minutes, run `02_pickle_serialization.py` and `04_copying_objects.py` first.
