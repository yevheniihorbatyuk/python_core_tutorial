# Module 8: Serialization and Object Copying
# Detailed Lesson Plan

## 📋 General Info

**Duration:** 3 - 4 hours
**Format:** Theory + Live Coding + Practice
**Target Audience:** Intermediate (after Modules 4 and 6)

---

## 🎯 Learning Outcomes

By the end of this lesson, students will:

✅ Build safe classes with encapsulation
✅ Understand what serialization is and why it exists
✅ Use `pickle` for internal object persistence
✅ Control serialization with `__getstate__` / `__setstate__`
✅ Serialize objects to JSON with custom encoding
✅ Use CSV for interchange and reporting
✅ Avoid shared mutable state with correct copying

---

## 🧭 Lesson Structure

### Part 1: Encapsulation and Object Safety (40 min)

#### 1.1 Why Encapsulation Matters (10 min)
- Passwords, tokens, API keys must be protected
- Properties allow validation and controlled access
- Name mangling is not security, only a convention

#### 1.2 Live Coding: User Class (30 min)

- `User` with email and password
- Password setter hashes input
- Getter hides raw password
- Demonstrate `_User__password` access
- Show constants via `Enum` and `Final`

**Discussion:**
- Why we never store raw passwords in real systems
- How modern systems use KMS and secret managers

---

### Part 2: Serialization Fundamentals (60 min)

#### 2.1 Why Serialization Exists (10 min)
- Persist objects
- Send objects over network
- Cache expensive computations

#### 2.2 Pickle (25 min)
- Dump/load objects
- Tradeoff: Python-specific + unsafe on untrusted data
- Use-case: internal caching, offline artifacts

#### 2.3 Live Coding: `__getstate__` / `__setstate__` (25 min)
- Add `Address` to `User`
- Remove sensitive fields before serialization
- Inject user_id into email on deserialization

**Real-World Example:**
- Caching data processing pipeline state

---

### Part 3: JSON and CSV (50 min)

#### 3.1 JSON for APIs (20 min)
- Convert objects to dicts
- Use `default` encoder or `object_hook`
- Demonstrate round-trip: object -> JSON -> object

#### 3.2 CSV for Reporting (15 min)
- Use `csv.DictWriter` and `csv.DictReader`
- Store analytics results for Excel/BI

#### 3.3 Modern Practices (15 min)
- Schema-first JSON (Pydantic, Marshmallow)
- Binary formats for big data (Parquet, Avro)
- Versioning and metadata alongside artifacts

---

### Part 4: Copying Objects Safely (40 min)

#### 4.1 Shallow vs Deep Copy (15 min)
- Shallow copy = shared nested state
- Deep copy = independent nested objects

#### 4.2 Live Coding: Copy Pitfalls (25 min)
- Config dict with nested lists
- Pipeline object with steps
- Compare behavior of `copy.copy` vs `copy.deepcopy`

**Real-World Example:**
- ML experiment configs (mutations leak between runs)

---

### Part 5: Practice (30-40 min)

**Guided Task:**
- Serialize `User` to JSON and CSV
- Deserialize back to objects

**Independent Tasks:**
1. Build a class with secure setters
2. Build `to_dict` / `from_dict` for nested objects
3. Implement a safe copy function for pipelines

---

## 🏁 Homework Ideas

1. **Model Artifact Packager**
   - Save model metadata to JSON
   - Save evaluation metrics to CSV
   - Store binary artifact with pickle (trusted only)

2. **User Export Tool**
   - Export to CSV
   - Export to JSON
   - Load and validate objects

3. **Config Cloner**
   - Copy nested config safely
   - Mutate without affecting the source

---

## 🔗 Connections to Future Modules

- Error handling for failed deserialization
- Web APIs require strict JSON contracts
- Data pipelines need reproducibility via serialized artifacts

---

## ✅ Success Indicators

Students can:

- Explain serialization tradeoffs
- Use pickle safely and with custom state
- Serialize objects to JSON and reconstruct them
- Avoid mutable shared state bugs
- Apply patterns to real engineering problems

---

**End of lesson.** ✅
