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
