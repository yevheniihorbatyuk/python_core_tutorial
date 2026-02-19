# Documentation Architecture — Module 8

## Canonical ownership
- Entry: `README.md`
- Learning order: `docs/LEARNING_PATHS.md`
- Timing: `docs/TEACHING_FLOW.md`
- File map: `docs/CONTENT_MAP.md`
- Legacy index: `docs/legacy/README.md`

## DRY rules
1. `START_HERE.md` не дублює повні траєкторії.
2. Зміни маршрутів — спочатку у `LEARNING_PATHS`.
3. Зміни таймінгу — спочатку у `TEACHING_FLOW`.
4. Root docs мають відповідати реальним шляхам файлів.

## Notebook policy
- Primary notebook: `Module_8_Complete_Guide.ipynb`

## Data policy
- Великі/бінарні артефакти (`.pkl`, `.parquet`) не модифікуються в межах doc-overhaul.
