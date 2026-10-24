# Demo 1 — Prompt Engineering Lab

> **Following along without Python?** Every prompt in this demo is in [`copy-paste-prompts.md`](copy-paste-prompts.md), ready for ChatGPT, Claude, Gemini, or Copilot Chat.


Everything here runs offline by default (`LLM_PROVIDER=mock`). Switch providers in `../.env`.

## Live demo script (35 minutes, 10:40–11:15)

| Min | Do | Say |
|---|---|---|
| 0–3 | `python prompt_lab.py --run 1` | "This is the prompt most people type. Notice it is not wrong — it is useless." |
| 3–9 | `--run 2`, then `--run 3` | "Two changes: we pasted the real data, then we said exactly what we wanted back. Which one mattered more?" |
| 9–12 | `--compare 1 3` | Side-by-side. Ask the room what they would have to do by hand with each output. |
| 12–18 | `--run 4`, `--run 5` | Few-shot fixes format; chain-of-thought makes the arithmetic checkable. Point at the "close behind" note in run 5 — the model surfaced a judgment call. |
| 18–22 | `--run 6` | Role plus JSON. "This output can go straight into a dashboard. Same data, same model — only the prompt changed." |
| 22–28 | `cat skills/analyze-sales-data.yaml` then `python run_skill.py analyze-sales-data --file data/q4_sales.csv` | "We just froze the good prompt into a file. Now it runs on Q4 data it has never seen." |
| 28–34 | `python agent.py` | Chain two skills, stop at the human checkpoint, show the JSON audit log. "The checkpoint is the design, not an afterthought." |
| 34–35 | `python run_skill.py --list` | Hand off to Lab 1. |

## Files

- `prompt_lab.py` — the six-run demo (`--run N`, `--compare A B`, `--file any.txt`)
- `prompts/runs.yaml` — the six prompts; each adds exactly one ingredient
- `prompts/mock_responses.yaml` — canned outputs for offline mode
- `skills/*.yaml` — reusable skill files (task / context / constraints / output)
- `run_skill.py` — render a skill with `--key value` inputs and run it
- `agent.py` — two skills chained with a human approval gate and an audit log
- `lab1/` — instructions, a skill template, and sample inputs
