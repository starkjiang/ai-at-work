"""Run a reusable skill file on new input.

    python run_skill.py analyze-sales-data --file data/q4_sales.csv
    python run_skill.py draft-exec-email --file lab1/sample_brief.txt --tone "firm but collaborative"
    python run_skill.py --list
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from llm import complete, PROVIDER

HERE = Path(__file__).resolve().parent
SKILL_DIRS = [HERE / "skills", HERE / "lab1"]
console = Console()


def find_skill(name: str) -> dict:
    for d in SKILL_DIRS:
        path = d / f"{name}.yaml"
        if path.exists():
            skill = yaml.safe_load(path.read_text())
            skill["_path"] = path
            return skill
    sys.exit(f"No skill named {name!r} in {', '.join(str(d) for d in SKILL_DIRS)}")


def render(skill: dict, fills: dict) -> str:
    """Fill placeholders; any {file} input is also exposed as {file_contents}."""
    if "file" in fills:
        fills["file_contents"] = Path(fills["file"]).read_text()
    try:
        return skill["prompt"].format(**fills)
    except KeyError as e:
        sys.exit(f"Skill needs input {e}. Declared inputs: {list(skill.get('inputs', {}))}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill", nargs="?", help="skill name (file stem in skills/ or lab1/)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--show-prompt", action="store_true", help="print the rendered prompt too")
    args, extra = ap.parse_known_args()

    if args.list or not args.skill:
        for d in SKILL_DIRS:
            for p in sorted(d.glob("*.yaml")):
                s = yaml.safe_load(p.read_text())
                console.print(f"[bold]{p.stem}[/bold] — {s.get('description', '')}")
        return

    # Any --key value pair becomes a placeholder fill.
    fills: dict[str, str] = {}
    for i in range(0, len(extra) - 1, 2):
        fills[extra[i].lstrip("-")] = extra[i + 1]

    skill = find_skill(args.skill)
    for key, desc in skill.get("inputs", {}).items():
        if key not in fills and "default:" in str(desc):
            fills[key] = str(desc).split("default:")[1].strip(" )")
    prompt = render(skill, fills)

    if args.show_prompt:
        console.print(Panel(prompt, title=f"Rendered prompt — {skill['name']}", border_style="cyan"))
    out = complete(prompt, skill.get("system"), mock_key=skill.get("mock_key"))
    console.print(Panel(Markdown(out), title=f"{skill['name']} ({PROVIDER})", border_style="green"))


if __name__ == "__main__":
    main()
