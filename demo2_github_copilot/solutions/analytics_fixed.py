from collections import defaultdict
from datetime import date

from .alerts import check_thresholds


def moving_average(data: list[float], window: int) -> list[float]:
    """Simple moving average.

    Args:
        data: Values in time order.
        window: Number of points per average. Must be positive.

    Returns:
        One value per full window. If ``data`` is shorter than ``window`` the
        plain mean of the available points is returned as a single element.
        Empty input returns an empty list.

    Raises:
        ValueError: If ``window`` is not positive.
    """
    if window <= 0:
        raise ValueError(f"window must be positive, got {window}")
    if not data:
        return []
    if len(data) < window:
        return [sum(data) / len(data)]
    total = sum(data[:window])
    result = [total / window]
    for i in range(window, len(data)):
        total += data[i] - data[i - window]
        result.append(total / window)
    return result


def per_sensor_series(readings, field: str = "temperature_c") -> dict[str, list[float]]:
    """Group readings by sensor_id and return {sensor_id: [values in time order]}."""
    series: dict[str, list[float]] = defaultdict(list)
    for r in sorted(readings, key=lambda r: r.timestamp):
        series[r.sensor_id].append(getattr(r, field))
    return dict(series)


def daily_summary(readings, thresholds=None) -> dict[tuple[str, date], dict[str, float]]:
    """Per-sensor, per-day min/max/mean temperature, mean vibration, and alert count."""
    groups: dict[tuple[str, date], list] = defaultdict(list)
    for r in readings:
        groups[(r.sensor_id, r.timestamp.date())].append(r)
    out = {}
    for key, rs in groups.items():
        temps = [r.temperature_c for r in rs]
        vibs = [r.vibration_mm_s for r in rs]
        out[key] = {
            "min_temp": min(temps),
            "max_temp": max(temps),
            "mean_temp": sum(temps) / len(temps),
            "mean_vib": sum(vibs) / len(vibs),
            "alerts": len(check_thresholds(rs, thresholds)),
        }
    return out
