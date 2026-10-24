# Lab 2 (Developers) — without GitHub Copilot

The same lab as `INSTRUCTIONS.md`, done by pasting into any chat assistant. You still need
Python and the repo so you can run `pytest`; the assistant only writes, you run and judge.

Keep **one conversation** per issue. Start it with the standards file:

```
I am working on a small Python project. Follow these rules for everything you write:

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

## The loop

Every step is the same four moves. Do them in order, every time.

1. **Paste context** — the issue, the file(s) involved, and the exact error output. Never paraphrase an error.
2. **Ask for one thing** — a test, a fix, a review, a docstring. Not "do the issue".
3. **Run it** — put the code in the file, run `pytest -q`. The assistant cannot run anything; you are the executor.
4. **Paste the result back** — passing or failing, verbatim. Then ask for the next thing.

If the assistant gives the same wrong answer twice, you are missing context, not luck. Paste more.

## Issue #2 (Pair A) — opening message

```
# Issue #2 — Ingest fails on files with missing or blank readings

**Labels:** bug, lab

## Steps to reproduce

```bash
python run_report.py data/sensors_sample.csv
```

Real exports contain `NA` and blank cells. `load_readings` calls `float()` on them and
raises `ValueError: could not convert string to float: 'NA'`, so one bad cell kills the
whole report.

## Expected

- Rows with a missing numeric value are skipped, not fatal.
- `load_readings` reports how many rows were skipped (return value or logging — propose one and justify it in the PR).
- Timestamps in `YYYY-MM-DDTHH:MM:SS` (ISO with a `T`) should also be accepted.

## Acceptance criteria

- [ ] Failing test with a small inline CSV containing `NA`, blank, and ISO timestamp rows
- [ ] `data/sensors_sample.csv` produces a report
- [ ] Skipped-row count is visible to the caller
- [ ] No change to the `Reading` dataclass fields

--- sensor_pipeline/ingest.py ---
import csv
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reading:
    timestamp: datetime
    sensor_id: str
    temperature_c: float
    vibration_mm_s: float


def load_readings(path):
    """Load readings from a CSV with columns timestamp,sensor_id,temperature_c,vibration_mm_s."""
    readings = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append(
                Reading(
                    timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    sensor_id=row["sensor_id"],
                    temperature_c=float(row["temperature_c"]),
                    vibration_mm_s=float(row["vibration_mm_s"]),
                )
            )
    return readings

Running `python run_report.py data/sensors_sample.csv` gives:
ValueError: could not convert string to float: 'NA'

Start by writing ONE failing pytest test in tests/test_ingest.py (use tmp_path to write a 4-row CSV containing an NA, a blank, and an ISO 'T' timestamp) that encodes the acceptance criteria. Do not fix the code yet.
```

## Issue #3 (Pair B) — opening message

```
# Issue #3 — Add a per-sensor daily summary to the report

**Labels:** enhancement, lab

## Request

Operations wants a table per sensor per day: min, max, mean temperature, mean vibration,
and alert count. Add a `daily_summary(readings)` function in `sensor_pipeline/analytics.py`
and a `## Daily summary` section in `build_report` rendered as a Markdown table.

## Acceptance criteria

- [ ] `daily_summary` returns `{(sensor_id, date): {"min_temp", "max_temp", "mean_temp", "mean_vib", "alerts"}}`
- [ ] Alert counting reuses `check_thresholds`; do not duplicate threshold logic
- [ ] Unit tests cover a two-sensor, two-day fixture
- [ ] README documents the new section
- [ ] Standard library only

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

--- sensor_pipeline/alerts.py ---
DEFAULT_THRESHOLDS = {"temperature_c": 85.0, "vibration_mm_s": 7.1}


def check_thresholds(readings, thresholds=None):
    """Return a list of (timestamp, sensor_id, field, value) tuples for readings over threshold."""
    thresholds = thresholds or DEFAULT_THRESHOLDS
    alerts = []
    for r in readings:
        for field, limit in thresholds.items():
            value = getattr(r, field)
            if value > limit:
                alerts.append((r.timestamp, r.sensor_id, field, value))
    return alerts

--- sensor_pipeline/report.py ---
from .alerts import check_thresholds
from .analytics import moving_average, per_sensor_series


def build_report(readings, window=5):
    lines = ["# Sensor report", ""]
    series = per_sensor_series(readings)
    for sensor_id, values in series.items():
        ma = moving_average(values, window)
        lines.append(f"- {sensor_id}: {len(values)} readings, latest {window}-pt avg temp {ma[-1]:.1f} C")
    alerts = check_thresholds(readings)
    lines += ["", f"## Alerts ({len(alerts)})", ""]
    for ts, sid, field, value in alerts:
        lines.append(f"- {ts} {sid} {field}={value}")
    return "\n".join(lines)

Start by writing ONE failing pytest test for daily_summary using a two-sensor, two-day fixture of Reading objects (from sensor_pipeline.ingest import Reading). Do not implement the function yet.
```

## Review step (both pairs)

When the tests pass, paste your full diff and ask:

```
Review this diff like a senior engineer. Flag (1) security issues, (2) performance bottlenecks, (3) missing error handling, (4) violations of the rules I gave you at the start. Numbered list; each item: Severity (High/Med/Low) - Issue - Why it matters - minimal suggested change. Do not rewrite whole files.
```

Then use the PR-description prompt from `../copy-paste-prompts.md`, Step 6.

## What good looks like

Same as the Copilot version, plus one thing: you can name a point where pasting more context
changed the answer. That is the skill you take back to work, whatever tool you use there.
