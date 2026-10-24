---
mode: agent
description: Write a pytest suite for the selected function, happy path plus named edge cases.
---
Write pytest unit tests for the selected code.

Cover:
1. The happy path with realistic values from `data/sensors_short.csv`.
2. These edge cases: empty input, window larger than data, window of zero or negative, non-numeric values.

Constraints: pytest only, no mocks, one behavior per test, descriptive names. Follow `.github/copilot-instructions.md`.
Output: a single test file under `tests/`, no explanation unless a test encodes a non-obvious assumption.
