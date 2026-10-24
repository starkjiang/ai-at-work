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
