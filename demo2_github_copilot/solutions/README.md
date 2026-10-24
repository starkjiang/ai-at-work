# Instructor solutions

Reference implementations and tests for the three issues. Copy a file into place to check a
participant's approach, or to reset the demo:

```bash
# from demo2_github_copilot/
cp solutions/analytics_fixed.py sensor_pipeline/analytics.py
cp solutions/ingest_fixed.py    sensor_pipeline/ingest.py
cp solutions/report_fixed.py    sensor_pipeline/report.py
cp solutions/test_solutions.py  tests/
pytest -q
```

To reset to the buggy state: `git checkout -- sensor_pipeline/ && rm -f tests/test_*.py`.

Copilot will not produce exactly these files, and it should not have to. Judge participant
work against the acceptance criteria in `issues/`, not against this code.
