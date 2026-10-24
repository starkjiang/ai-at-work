import csv
import logging
from dataclasses import dataclass
from datetime import datetime

log = logging.getLogger(__name__)

_TIMESTAMP_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S")


@dataclass
class Reading:
    timestamp: datetime
    sensor_id: str
    temperature_c: float
    vibration_mm_s: float


def _parse_timestamp(text: str) -> datetime:
    for fmt in _TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognized timestamp {text!r}")


def load_readings(path) -> tuple[list[Reading], int]:
    """Load readings from CSV, skipping rows with missing or non-numeric values.

    Args:
        path: CSV with columns timestamp,sensor_id,temperature_c,vibration_mm_s.

    Returns:
        A tuple of (readings, skipped_row_count). A tuple keeps the skip count
        visible to callers without a global or a side channel.
    """
    readings: list[Reading] = []
    skipped = 0
    with open(path, newline="") as f:
        for n, row in enumerate(csv.DictReader(f), start=2):
            try:
                readings.append(
                    Reading(
                        timestamp=_parse_timestamp(row["timestamp"]),
                        sensor_id=row["sensor_id"],
                        temperature_c=float(row["temperature_c"]),
                        vibration_mm_s=float(row["vibration_mm_s"]),
                    )
                )
            except (ValueError, KeyError) as e:
                skipped += 1
                log.warning("skipping line %d: %s", n, e)
    return readings, skipped
