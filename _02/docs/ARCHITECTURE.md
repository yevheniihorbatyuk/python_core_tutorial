# Documentation Architecture and DRY Rules

## Purpose
Prevent duplicate instructions and conflicting guidance across Module 2 docs.

## Canonical ownership
- Entrypoint owner: `README.md`
- Learning route owner: `docs/LEARNING_PATHS.md`
- Teaching timing/flow owner: `docs/TEACHING_FLOW.md`
- File-role mapping owner: `docs/CONTENT_MAP.md`
- DRY policy owner: `docs/ARCHITECTURE.md`

## DRY rules
1. Do not duplicate full path descriptions in `START_HERE.md`, `README_MODERN.md`, `COMPARISON.md`.
2. Redirect/chooser pages must link to canonical docs instead of re-explaining details.
3. Version policy must be stated consistently as Python 3.10-3.12 baseline.
4. Notebook policy must remain stable:
- Primary: `fundamentals_notebook.ipynb`
- Secondary: `notebook.ipynb` (legacy/optional)

## Change policy
1. If learning order changes: update `docs/LEARNING_PATHS.md` first.
2. If session timing changes: update `docs/TEACHING_FLOW.md` first.
3. If file roles change: update `docs/CONTENT_MAP.md` first.
4. Then update `README.md` and `START_HERE.md` links only if needed.

## Non-goals for this iteration
- No full rewrite of `03/04/05/07*.py` materials
- No migration to a new folder taxonomy for module sources
