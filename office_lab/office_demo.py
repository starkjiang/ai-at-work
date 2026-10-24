"""Office-track demo and lab runner that needs no Microsoft 365 Copilot license.

Runs the same six lab prompts against whatever model is configured in ../.env
(mock mode by default, so it works offline), using the supplier dataset as context.

    python office_demo.py               # run all steps, pausing between them
    python office_demo.py --step 2      # one step
    python office_demo.py --check       # print the ground-truth numbers to verify against

The lesson is identical to the Copilot version: the prompt formula does the work,
not the button in the ribbon.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "demo1_prompt_engineering"))
from llm import complete, PROVIDER  # noqa: E402

import yaml  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.markdown import Markdown  # noqa: E402
from rich.panel import Panel  # noqa: E402

console = Console()
DATA = HERE / "supplier_performance.csv"


def load_rows() -> list[dict]:
    with open(DATA, newline="") as f:
        return list(csv.DictReader(f))


def ground_truth() -> str:
    """The numbers a participant should reach by hand in step 3 of the lab."""
    rows = load_rows()
    seen, dups = set(), 0
    for r in rows:
        key = tuple(r.values())
        dups += key in seen
        seen.add(key)
    blank_region = sum(1 for r in rows if not r["region"])
    by_sup: dict[str, list[float]] = defaultdict(list)
    by_reg: dict[str, dict[str, float]] = defaultdict(lambda: {"spend": 0.0, "defects": 0, "on": [], "n": 0})
    for r in rows:
        by_sup[r["supplier_name"]].append(float(r["on_time_pct"]))
        reg = r["region"] or "(blank)"
        by_reg[reg]["spend"] += float(r["spend_usd"])
        by_reg[reg]["defects"] += int(r["defects"])
        by_reg[reg]["on"].append(float(r["on_time_pct"]))
    worst = sorted(by_sup.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))[:3]
    out = [f"Rows: {len(rows)}  duplicate rows: {dups}  blank region: {blank_region}", "",
           "Lowest average on-time %:"]
    out += [f"  {n}: {sum(v)/len(v):.1f}%" for n, v in worst]
    out += ["", "By region (spend, defects, avg on-time %):"]
    out += [f"  {reg}: ${d['spend']:,.0f}, {d['defects']}, {sum(d['on'])/len(d['on']):.1f}%" for reg, d in sorted(by_reg.items())]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", type=int)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-pause", action="store_true")
    args = ap.parse_args()

    if args.check:
        console.print(Panel(ground_truth(), title="Ground truth (compute this by hand in step 3)", border_style="yellow"))
        return

    steps = yaml.safe_load((HERE / "office_prompts.yaml").read_text())["steps"]
    csv_text = DATA.read_text()
    selected = [s for s in steps if not args.step or s["id"] == args.step]
    for s in selected:
        prompt = s["prompt"].replace("{csv}", csv_text)
        console.rule(f"[bold]Step {s['id']} — {s['name']}  [dim]({s['app']} equivalent)")
        console.print(Panel(s["prompt"].replace("{csv}", "<supplier_performance.csv, 482 rows>"), title="Prompt", border_style="cyan"))
        out = complete(prompt, s.get("system"), mock_key=f"office{s['id']}")
        console.print(Panel(Markdown(out), title=f"Output ({PROVIDER})", border_style="green"))
        if not args.no_pause and s is not selected[-1]:
            console.input("[dim]Enter for next step…[/dim]")


if __name__ == "__main__":
    main()
