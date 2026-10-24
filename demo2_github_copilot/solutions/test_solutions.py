"""Reference tests. Run after copying the *_fixed.py files into sensor_pipeline/."""
from datetime import datetime
from pathlib import Path

import pytest

from sensor_pipeline.analytics import daily_summary, moving_average
from sensor_pipeline.ingest import Reading, load_readings

DATA = Path(__file__).resolve().parents[1] / "data"


# --- Issue #1 -----------------------------------------------------------
def test_window_larger_than_data_returns_plain_mean():
    assert moving_average([1, 2, 3], 5) == [2.0]


def test_empty_input_returns_empty_list():
    assert moving_average([], 5) == []


def test_zero_window_raises():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)


def test_normal_window_unchanged():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


# --- Issue #2 -----------------------------------------------------------
def test_missing_values_are_skipped_and_counted(tmp_path):
    csv = tmp_path / "r.csv"
    csv.write_text(
        "timestamp,sensor_id,temperature_c,vibration_mm_s\n"
        "2026-09-01 08:00:00,S-1,70.0,3.0\n"
        "2026-09-01 08:15:00,S-1,NA,3.0\n"
        "2026-09-01T08:30:00,S-1,71.0,\n"
        "2026-09-01T08:45:00,S-1,72.0,3.1\n"
    )
    readings, skipped = load_readings(csv)
    assert skipped == 2
    assert [r.temperature_c for r in readings] == [70.0, 72.0]
    assert readings[1].timestamp == datetime(2026, 9, 1, 8, 45)


def test_sample_file_loads():
    readings, skipped = load_readings(DATA / "sensors_sample.csv")
    assert skipped == 3
    assert len(readings) == 144


# --- Issue #3 -----------------------------------------------------------
def test_daily_summary_two_sensors_two_days():
    rs = [
        Reading(datetime(2026, 9, 1, 8), "A", 70.0, 2.0),
        Reading(datetime(2026, 9, 1, 9), "A", 90.0, 8.0),   # temp + vib alerts
        Reading(datetime(2026, 9, 2, 8), "A", 71.0, 2.0),
        Reading(datetime(2026, 9, 1, 8), "B", 60.0, 1.0),
    ]
    s = daily_summary(rs)
    assert set(s) == {("A", datetime(2026, 9, 1).date()), ("A", datetime(2026, 9, 2).date()), ("B", datetime(2026, 9, 1).date())}
    day1 = s[("A", datetime(2026, 9, 1).date())]
    assert day1["min_temp"] == 70.0 and day1["max_temp"] == 90.0 and day1["mean_temp"] == 80.0
    assert day1["alerts"] == 2
