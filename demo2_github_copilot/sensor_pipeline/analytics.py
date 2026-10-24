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
