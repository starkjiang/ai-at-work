# Live Demo 2 — copy-paste prompts

Two columns throughout: what the instructor types into **GitHub Copilot Chat** in VS Code, and
the equivalent for **any chat assistant** (ChatGPT, Claude, Gemini, Copilot Chat in the browser).
The only difference is context: Copilot sees your open files automatically; a chat tool needs
you to paste them. Everything else, including the mistakes, is the same.

> In a chat tool, start **one conversation** for the whole demo and keep it open. Each step builds on the last.

## Step 0 — Give your assistant the standards (chat tool only)

Copilot reads `.github/copilot-instructions.md` on every request. In a chat tool, paste it once as your first message:

```
I am going to work on a small Python project with you. Follow these rules for everything you write:

# Copilot instructions for this repository

You are assisting engineers at <ORGANIZATION>. Follow these rules on every request.

## Code standards
- Python 3.11+, standard library only unless a dependency already exists in `requirements.txt`.
- Type hints on all public functions. Google-style docstrings with Args, Returns, Raises.
- Tests use `pytest`; one behavior per test; test names describe the behavior (`test_window_larger_than_data_returns_plain_mean`).
- Prefer small, pure functions. Do not introduce global state.

## Security and data
- Never hardcode credentials, hostnames, or file paths to internal systems.
- Treat all CSV input as untrusted: validate types, handle missing values explicitly.
- Do not add network calls or telemetry.

## Intellectual property
- Do not reproduce code from external repositories verbatim. Write implementations from first principles.
- Do not include proprietary algorithms or internal identifiers in examples or comments.

## Workflow
- When asked to fix a bug, first propose a failing test, then the fix.
- When you are unsure of an expected behavior, ask rather than assume — and say what you assumed.
- Summaries of pull requests must list: what changed, why, how it was tested, and any follow-ups.
```

## Step 1 — Read the issue and find the code

| Copilot Chat | Any chat tool |
|---|---|
| `@workspace explain issues/ISSUE-1-moving-average-crash.md and locate the code involved` | Paste the issue and the file, then ask |

```
Here is a GitHub issue and the file it concerns. Explain the bug in two sentences and point at the exact line that fails.

--- issues/ISSUE-1-moving-average-crash.md ---
# Issue #1 — `moving_average` crashes when window is larger than the data

**Labels:** bug, demo

## Steps to reproduce

```bash
python run_report.py data/sensors_short.csv 5
```

Sensor `S-104` has only 3 readings. With the default window of 5 the report dies with
`IndexError: list index out of range` in `sensor_pipeline/analytics.py`.

## Expected

The report should still be produced. For a sensor with fewer readings than the window,
either return the plain average of the readings it has, or skip the sensor with a note.
Empty input should return an empty list, and `window <= 0` should raise `ValueError`.

## Acceptance criteria

- [ ] A failing test that reproduces the crash, then passes
- [ ] `moving_average([], 5) == []`
- [ ] `moving_average([1, 2, 3], 5)` returns `[2.0]` (mean of what exists)
- [ ] `moving_average([1, 2, 3], 0)` raises `ValueError`
- [ ] Existing behavior unchanged when `window <= len(data)`
- [ ] Google-style docstring documents the edge-case behavior

--- sensor_pipeline/analytics.py ---
from collections import defaultdict


def moving_average(data, window):
    """Return the simple moving average of `data` using `window` points."""
    result = []
    first = sum(data[i] for i in range(window)) / window
    result.append(first)
    total = first * window
    for i in range(window, len(data)):
        total += data[i] - data[i - window]
        result.append(total / window)
    return result


def per_sensor_series(readings, field="temperature_c"):
    """Group readings by sensor_id and return {sensor_id: [values in time order]}."""
    series = defaultdict(list)
    for r in sorted(readings, key=lambda r: r.timestamp):
        series[r.sensor_id].append(getattr(r, field))
    return dict(series)
```

## Step 2 — Reproduce with a failing test

| Copilot Chat | Any chat tool |
|---|---|
| Select `moving_average`, type `/tests` (or run the `generate-tests` prompt file) | Ask for the test; the code is already in the conversation |

```
Write a pytest file tests/test_analytics.py with ONE test that reproduces this bug: moving_average([1, 2, 3], 5) currently raises IndexError. The test should assert the behavior the issue asks for (it returns [2.0]), so it fails now and passes after the fix. Import with `from sensor_pipeline.analytics import moving_average`.
```

Save the file, run `pytest -q`. It must be red.

## Step 3 — Fix

| Copilot Chat | Any chat tool |
|---|---|
| Select the function, `/fix`, paste the traceback in the same message | Paste the traceback and ask for a minimal fix |

```
Here is the traceback:

Traceback (most recent call last):
  File "run_report.py", line 9, in <module>
    print(build_report(load_readings(path), window))
  File "sensor_pipeline/report.py", line 9, in build_report
    ma = moving_average(values, window)
  File "sensor_pipeline/analytics.py", line 7, in moving_average
    first = sum(data[i] for i in range(window)) / window
IndexError: list index out of range

Fix moving_average with the smallest change that makes the test pass. Do not change the signature. Show the full function.
```

**The planned "the AI is wrong" moment:** the first fix usually handles the short-data case and
nothing else. Ask the room: did it handle empty input? `window = 0`? Then:

```
Does your fix handle moving_average([], 5) and moving_average([1, 2, 3], 0)? The issue says the first returns [] and the second raises ValueError. If not, update the function and add one test for each.
```

## Step 4 — Edge cases you have not thought of

```
What edge cases have I not covered for this function? List them, then write one additional pytest test for the most likely one in real sensor data.
```

## Step 5 — Document

| Copilot Chat | Any chat tool |
|---|---|
| Select the function, `/doc`; then `Update README.md to describe the edge-case behavior` | Ask directly |

```
Add a Google-style docstring (Args, Returns, Raises) to moving_average that documents the edge-case behavior. Then write a short "Edge cases" paragraph I can paste into README.md.
```

## Step 6 — Pull request description

| Copilot Chat | Any chat tool |
|---|---|
| Run the `draft-pr` prompt file | Ask directly |

```
Draft a pull request description for these changes. Sections in order: Summary (2-3 sentences), What changed (bullets by file), Why, How it was tested (commands and results), Follow-ups / risks. Reference issue #1. Under 250 words.
```

Read every line before you would open the PR. The reviewer, not the author, decides what merges.

## Step 7 — Agent mode preview (Copilot only)

In Copilot Chat switch to **Agent** mode and type `Implement issue #2 and make the tests pass`.
Let it run for two minutes, then stop it. Watch which files it edits and which commands it runs.
A chat tool has no equivalent: that gap is the difference between an assistant and an agent.
