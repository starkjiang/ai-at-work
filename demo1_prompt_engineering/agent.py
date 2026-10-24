"""A minimal agentic workflow: chain skills, gate on a human checkpoint, log everything.

    python agent.py --notes lab1/sample_meeting_notes.txt

Pipeline:  summarize-meeting  ->  draft-exec-email  ->  [human approves?]  ->  "send"

The point of the demo is the checkpoint and the log, not the chain itself.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from llm import complete, PROVIDER
from run_skill import find_skill, render

HERE = Path(__file__).resolve().parent
console = Console()


def step(name: str, skill_name: str, fills: dict, log: list) -> str:
    skill = find_skill(skill_name)
    prompt = render(skill, fills)
    t0 = time.time()
    out = complete(prompt, skill.get("system"), mock_key=skill.get("mock_key"))
    log.append({"step": name, "skill": skill_name, "seconds": round(time.time() - t0, 2),
                "prompt_chars": len(prompt), "output": out})
    console.print(Panel(Markdown(out), title=f"{name} ({PROVIDER})", border_style="green"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--notes", type=Path, default=HERE / "lab1" / "sample_meeting_notes.txt")
    ap.add_argument("--tone", default="firm but collaborative")
    args = ap.parse_args()

    log: list[dict] = []
    summary = step("1. Summarize meeting", "summarize-meeting", {"file": str(args.notes)}, log)

    # Output of step 1 becomes the brief for step 2.
    brief_path = HERE / "agent_runs" / "brief.txt"
    brief_path.parent.mkdir(exist_ok=True)
    brief_path.write_text("Write to the supplier named in the action items about their on-time delivery.\n\n" + summary)
    email = step("2. Draft email", "draft-exec-email", {"file": str(brief_path), "tone": args.tone}, log)

    # Human checkpoint — nothing leaves the building without a person saying so.
    console.rule("[bold yellow]3. Human checkpoint")
    decision = console.input("Send this email? [y/N/edit] ").strip().lower()
    if decision == "edit":
        console.print("[dim]In a real system this opens the draft in your mail client.[/dim]")
    sent = decision == "y"
    log.append({"step": "3. Human checkpoint", "decision": decision, "sent": sent})
    console.print("[green]Sent (simulated).[/green]" if sent else "[yellow]Not sent. Draft kept for review.[/yellow]")

    run_file = HERE / "agent_runs" / f"run-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    run_file.write_text(json.dumps(log, indent=2))
    console.print(f"[dim]Audit log written to {run_file.relative_to(HERE)}[/dim]")


if __name__ == "__main__":
    main()
