"""Usage: python run_report.py data/sensors_sample.csv [window]"""
import sys

from sensor_pipeline import build_report, load_readings

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/sensors_sample.csv"
    window = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(build_report(load_readings(path), window))
