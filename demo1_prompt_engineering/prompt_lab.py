"""Live Demo 1 — the same task, six increasingly strong prompts.

    python prompt_lab.py                 # run all six, pausing between runs
    python prompt_lab.py --run 3         # run one
    python prompt_lab.py --compare 1 3   # show two side by side
    python prompt_lab.py --file my.txt   # run any prompt from a file

Each run in prompts/runs.yaml adds exactly one ingredient from the formula
    [ Task ] + [ Context ] + [ Constraints ] + [ Output Format ]
or one strategy (few-shot, chain-of-thought, role + structured output),
so the audience can see which change moved the output.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.markdown import Markdown

from llm import complete, PROVIDER

HERE = Path(__file__).resolve().parent
console = Console()


def load_runs() -> list[dict]:
    return yaml.safe_load((HERE / "prompts" / "runs.yaml").read_text())["runs"]


def build_prompt(run: dict) -> str:
    """Substitute {data_sample} etc. into the prompt template."""
    sample = (HERE / "data" / "q3_sales.csv").read_text().splitlines()
    fills = {
        "data_header": sample[0],
        "data_sample": "\n".join(sample[:6]),
        "data_full": "\n".join(sample),
    }
    return run["prompt"].format(**fills)


def show_run(run: dict, output: str) -> None:
    console.rule(f"[bold]Run {run['id']} — {run['name']}")
    console.print(Panel(build_prompt(run), title="Prompt", border_style="cyan"))
    console.print(Panel(f"[italic]{run['adds']}[/italic]", title="What changed", border_style="yellow"))
    console.print(Panel(Markdown(output), title=f"Output ({PROVIDER})", border_style="green"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", type=int, help="run a single numbered prompt")
    ap.add_argument("--compare", nargs=2, type=int, metavar=("A", "B"), help="show two runs side by side")
    ap.add_argument("--file", type=Path, help="run an arbitrary prompt from a text file")
    ap.add_argument("--no-pause", action="store_true")
    args = ap.parse_args()

    if args.file:
        prompt = args.file.read_text()
        console.print(Panel(prompt, title="Prompt", border_style="cyan"))
        console.print(Panel(Markdown(complete(prompt)), title=f"Output ({PROVIDER})", border_style="green"))
        return

    runs = {r["id"]: r for r in load_runs()}

    if args.compare:
        a, b = (runs[i] for i in args.compare)
        outs = [complete(build_prompt(r), r.get("system"), mock_key=f"run{r['id']}") for r in (a, b)]
        console.print(Columns([
            Panel(Markdown(o), title=f"Run {r['id']} — {r['name']}", expand=True)
            for r, o in zip((a, b), outs)
        ], equal=True, expand=True))
        return

    selected = [runs[args.run]] if args.run else list(runs.values())
    for run in selected:
        output = complete(build_prompt(run), run.get("system"), mock_key=f"run{run['id']}")
        show_run(run, output)
        if not args.no_pause and run is not selected[-1]:
            console.input("[dim]Enter for next run…[/dim]")


if __name__ == "__main__":
    main()
