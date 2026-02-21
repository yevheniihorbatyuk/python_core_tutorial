# Content Map (Canonical)

This is the source of truth for file roles in `python_core/_02`.

```mermaid
graph TD
    A[README.md Canonical Hub] --> B[START_HERE.md Quick Start]
    A --> C[docs/LEARNING_PATHS.md]
    A --> D[docs/TEACHING_FLOW.md]
    A --> E[docs/ARCHITECTURE.md]
    A --> F[docs/CONTENT_MAP.md]

    C --> G[Beginner path]
    C --> H[Advanced DS/DE path]

    G --> I[03_input_output.py]
    G --> J[04_functions.py]
    G --> K[05_strings.py]
    G --> L[07_practice_tasks.py]

    H --> M[03_modern_input_output.py]
    H --> N[04_modern_functions.py]
    H --> O[05_modern_strings.py]
    H --> P[07_practice_ds_tasks.py]

    D --> Q[00_lesson_plan.md]
    D --> R[01_git_github_guide.md]
    D --> S[02_vscode_setup_guide.md]
    D --> T[06_debugging.py]

    A --> U[fundamentals_notebook.ipynb Primary]
    A --> V[notebook.ipynb Legacy Optional]

    W[README_MODERN.md Redirect] --> C
    X[COMPARISON.md Chooser] --> C
```

## File role matrix
- `README.md`: single canonical entrypoint
- `START_HERE.md`: minimal quick start only
- `docs/LEARNING_PATHS.md`: canonical path sequencing and expected outcomes
- `docs/TEACHING_FLOW.md`: canonical class flow/timing
- `docs/ARCHITECTURE.md`: DRY policy and ownership rules
- `README_MODERN.md`: redirect page
- `COMPARISON.md`: short chooser page
- `fundamentals_notebook.ipynb`: primary notebook for delivery
- `notebook.ipynb`: legacy/optional notebook

## Version policy
- Required baseline: Python 3.10-3.12
- Python 3.13 topics: optional appendix-level context only
