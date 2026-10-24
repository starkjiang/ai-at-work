import csv
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reading:
    timestamp: datetime
    sensor_id: str
    temperature_c: float
    vibration_mm_s: float


def load_readings(path):
    """Load readings from a CSV with columns timestamp,sensor_id,temperature_c,vibration_mm_s."""
    readings = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append(
                Reading(
                    timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    sensor_id=row["sensor_id"],
                    temperature_c=float(row["temperature_c"]),
                    vibration_mm_s=float(row["vibration_mm_s"]),
                )
            )
    return readings
