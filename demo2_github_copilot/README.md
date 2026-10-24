# Demo 2 — GitHub Copilot on a real project

> **No Copilot, or following along in a chat tool?** The instructor's prompts, with their chat-tool equivalents, are in [`copy-paste-prompts.md`](copy-paste-prompts.md). The lab version is [`lab2/without-copilot.md`](lab2/without-copilot.md).


`sensor_pipeline` is a small Python package that ingests sensor CSV logs, computes rolling
statistics, raises threshold alerts, and writes a Markdown report. It has **real bugs, no
tests, and thin docs** — which is what most code looks like when Copilot shows up.

Three issues are waiting in `issues/`. Demo 2 works Issue #1 live; Lab 2 hands #2 and #3
to participants.

## Setup

- VS Code with the GitHub Copilot and Copilot Chat extensions, signed in
- Python 3.11+, `pip install -r requirements.txt`
- Open **this folder** (`demo2_github_copilot/`) as the workspace so `.github/copilot-instructions.md` is picked up

Sanity check before the session:

```bash
python run_report.py data/sensors_clean.csv    # works
python run_report.py data/sensors_short.csv    # IndexError  -> Issue #1
python run_report.py data/sensors_sample.csv   # ValueError  -> Issue #2
```

## Live demo script (45 minutes)

| Min | Step | What to do in VS Code | Talking point |
|---|---|---|---|
| 0–4 | Tour | Open `sensor_pipeline/`, `issues/`, `.github/copilot-instructions.md` | "Copilot reads the instructions file on every request. This is where your standards live." |
| 4–8 | Inline completions | In `analytics.py`, below `per_sensor_series`, type a comment `# return the sensor with the highest mean temperature` then a signature `def hottest_sensor(series: dict[str, list[float]]) -> str:` and wait | Comment + signature = context. Show Tab / Esc / Alt+] cycling. |
| 8–12 | Read the issue | Copilot Chat: `@workspace explain issues/ISSUE-1-moving-average-crash.md and locate the code involved` | Copilot finds `moving_average`; you didn't have to. |
| 12–17 | Reproduce | Select `moving_average`, run `/tests` — or use the `generate-tests` prompt file | **Test first.** Run `pytest` and show the red. |
| 17–24 | Fix | Select the function, `/fix`, paste the traceback in the same message | Ask the room: did it handle `[]`? `window=0`? It usually misses one — **this is the planned "Copilot is wrong" moment.** Add the case, rerun. |
| 24–29 | Edge cases | Chat: `What edge cases have I not covered for this function?` | Copilot suggests; you decide. Add one test. |
| 29–34 | Document | Select the function, `/doc`; then `Update README.md to describe the edge-case behavior` | Google-style docstring per the instructions file. |
| 34–40 | PR | Use the `draft-pr` prompt file; walk through the summary line by line | "The author writes with Copilot. The reviewer reads without it." |
| 40–45 | Agent mode preview | Chat in agent mode: `Implement issue #2 and make the tests pass` — let it run for 2 minutes, stop it | Show the multi-file edits and the terminal runs. Then hand off to Lab 2. |

Reset between deliveries: `git checkout -- sensor_pipeline/ README.md && rm -f tests/test_*.py`.

## Repo map

```
sensor_pipeline/      the package (ingest -> analytics -> alerts -> report)
data/                 sensors_clean.csv (works), sensors_short.csv (issue #1), sensors_sample.csv (issue #2)
issues/               three issues with acceptance criteria
.github/              copilot-instructions.md + reusable prompt files
tests/                empty on purpose
lab2/                 participant instructions
solutions/            instructor-only reference fixes and tests
run_report.py         CLI entry point
```
