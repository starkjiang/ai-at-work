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
