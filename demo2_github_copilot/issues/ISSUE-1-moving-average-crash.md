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
