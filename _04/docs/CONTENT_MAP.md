# Content Map (Canonical) — Module 4

```mermaid
graph TD
  A[README.md Canonical Hub] --> B[START_HERE.md]
  A --> C[docs/LEARNING_PATHS.md]
  A --> D[docs/TEACHING_FLOW.md]
  A --> E[docs/ARCHITECTURE.md]
  A --> F[docs/legacy/README.md]

  C --> G[Beginner route]
  C --> H[Advanced/Pro route]

  G --> G1[beginner_edition/01_datetime_basics.py]
  G --> G2[beginner_edition/02_math_basics.py]
  G --> G3[beginner_edition/03_regex_basics.py]
  G --> G4[beginner_edition/04_files_basics.py]
  G --> G5[beginner_edition/05_modules_packages.py]
  G --> G6[beginner_edition/06_practice_tasks.py]

  H --> H1[pro_edition/01_datetime_professional.py]
  H --> H2[pro_edition/02_statistics_ab_testing.py]
  H --> H3[pro_edition/03_data_parsing.py]
  H --> H4[pro_edition/04_data_processing.py]

  A --> N[Module_4_Complete_Guide.ipynb Primary]
```

## Ролі файлів
- `README.md`: єдиний вхід
- `START_HERE.md`: коротка стартова інструкція
- `docs/LEARNING_PATHS.md`: порядок вивчення
- `docs/TEACHING_FLOW.md`: таймінг заняття
- `docs/ARCHITECTURE.md`: DRY-правила
