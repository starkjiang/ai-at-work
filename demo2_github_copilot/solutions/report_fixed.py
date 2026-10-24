from .alerts import check_thresholds
from .analytics import daily_summary, moving_average, per_sensor_series


def build_report(readings, window: int = 5, skipped: int = 0) -> str:
    lines = ["# Sensor report", ""]
    if skipped:
        lines += [f"_{skipped} rows skipped due to missing or invalid values._", ""]
    for sensor_id, values in per_sensor_series(readings).items():
        ma = moving_average(values, window)
        lines.append(f"- {sensor_id}: {len(values)} readings, latest {window}-pt avg temp {ma[-1]:.1f} C")
    alerts = check_thresholds(readings)
    lines += ["", f"## Alerts ({len(alerts)})", ""]
    lines += [f"- {ts} {sid} {field}={value}" for ts, sid, field, value in alerts]
    lines += ["", "## Daily summary", "", "| Sensor | Date | Min °C | Max °C | Mean °C | Mean vib | Alerts |", "|---|---|---|---|---|---|---|"]
    for (sid, day), s in sorted(daily_summary(readings).items()):
        lines.append(f"| {sid} | {day} | {s['min_temp']:.1f} | {s['max_temp']:.1f} | {s['mean_temp']:.1f} | {s['mean_vib']:.2f} | {s['alerts']} |")
    return "\n".join(lines)
