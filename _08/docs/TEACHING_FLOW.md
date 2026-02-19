# Teaching Flow (Canonical) — Module 8

```mermaid
flowchart TD
  A[Setup and Context 10-15m] --> B[Encapsulation 35-45m]
  B --> C[Serialization 60-75m]
  C --> D[Copying 30-45m]
  D --> E[Practice and Wrap-up 30-45m]

  B --> B1[Beginner or Advanced]
  C --> C1[Beginner or Advanced]
  D --> D1[Beginner or Advanced]
  E --> E1[Track-specific practice]
```

## Правила
1. Один primary route на конкретну сесію.
2. Другий route залишається optional/self-study.
3. Акцент на безпеку: `pickle` лише для trusted inputs.
