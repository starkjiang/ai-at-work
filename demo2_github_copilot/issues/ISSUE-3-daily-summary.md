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
