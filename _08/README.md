# Module 8: Serialization and Object Copying
## Practical Persistence and Safe Object Handling

This module covers **how Python objects become data**, how to **restore them safely**, and how to **copy complex structures without hidden bugs**.

---

## 🎯 Learning Objectives

After this module, students will be able to:

✅ Build classes with encapsulation and safe password handling
✅ Explain what serialization is and why it matters
✅ Serialize objects with `pickle` and control state via `__getstate__`/`__setstate__`
✅ Serialize objects to JSON and re-create real objects via `object_hook`
✅ Work with CSV for data interchange
✅ Choose between shallow and deep copy correctly
✅ Apply modern practices: schema-first JSON, versioned artifacts, safe storage

---

## 📂 Files

| File | Purpose |
|------|---------|
| `00_lesson_plan.md` | Detailed lesson plan (3-4 hours) |
| `01_user_class_encapsulation.py` | Encapsulation, password hashing, name mangling, Enum constants |
| `02_pickle_serialization.py` | Pickle + `__getstate__` / `__setstate__` |
| `03_json_csv_serialization.py` | JSON object hooks + CSV export/import |
| `04_copying_objects.py` | Shallow vs deep copy | 
| `05_practice_tasks.py` | Exercises and mini-projects |
| `START_HERE.md` | 3-minute onboarding |

---

## 🧠 Why This Matters (Real World)

**Data Science / ML**
- Persist model metadata + feature schemas
- Cache expensive preprocessing results
- Store experiment artifacts with versioning

**Data Engineering**
- Exchange datasets as JSON/CSV
- Move data across services (ETL)
- Create immutable snapshots for reproducibility

**Backend / Web**
- JSON is the de-facto API format
- Serialization shapes contracts between services
- Copying bugs cause subtle production issues

---

## 🚀 Quick Start

```bash
cd _08/
python3 01_user_class_encapsulation.py
python3 02_pickle_serialization.py
python3 03_json_csv_serialization.py
python3 04_copying_objects.py
python3 05_practice_tasks.py
```

---

## 🔗 Connections to Other Modules

**Previous:**
- Module 4: Files, CSV, JSON basics
- Module 6: OOP and class design

**Next (Future Use):**
- Error handling and logging (safe deserialization)
- Web APIs (JSON contracts, DTOs)
- Data pipelines (artifact versioning, caching)

---

## 🧪 Exercises (Summary)

### Easy
- Encapsulate a password field with a property
- Export simple objects to CSV

### Medium
- Build `to_dict` / `from_dict` for nested objects
- Deserialize JSON into a real class via `object_hook`

### Hard
- Design a versioned serialized artifact (model + metadata)
- Implement safe copy strategies for a pipeline object

---

## ✅ Self-Assessment Checklist

- [ ] I know when to use pickle vs JSON
- [ ] I can explain why pickle is unsafe for untrusted data
- [ ] I can reconstruct objects from JSON using `object_hook`
- [ ] I can serialize nested objects without leaking secrets
- [ ] I can choose between shallow and deep copy correctly

---

## 📖 Further Reading

- Python `pickle` docs: https://docs.python.org/3/library/pickle.html
- Python `json` docs: https://docs.python.org/3/library/json.html
- Python `copy` docs: https://docs.python.org/3/library/copy.html
- Python `csv` docs: https://docs.python.org/3/library/csv.html

---

**Ready to make your data portable and your objects safe?** 🚀
