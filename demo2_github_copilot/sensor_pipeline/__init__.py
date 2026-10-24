"""sensor_pipeline — ingest sensor CSV logs, compute rolling statistics, raise alerts, write a report.

Deliberately small, deliberately imperfect. Used for the GitHub Copilot demo and Lab 2.
"""
from .ingest import load_readings
from .analytics import moving_average, per_sensor_series
from .alerts import check_thresholds
from .report import build_report

__all__ = ["load_readings", "moving_average", "per_sensor_series", "check_thresholds", "build_report"]
