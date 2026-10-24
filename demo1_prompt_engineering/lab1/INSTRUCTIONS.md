# Lab 1 — Build your own prompt and skill (45 minutes)

You can do this lab in **any** approved tool: Copilot Chat, Microsoft 365 Copilot,
or the `prompt_lab.py` CLI in this folder. The skill file at the end is the deliverable.

## Two ways to do this lab

- **Python:** `python run_skill.py <your-skill> --file <input> --show-prompt` (set a real provider in `../.env`, or paste the rendered prompt into your chat tool).
- **Any AI tool:** use the step-by-step worksheet in [`with-any-ai-tool.md`](with-any-ai-tool.md). It has the fill-in template and tells you where to save a skill in ChatGPT, Claude, Gemini, or Copilot.

## Steps

1. **Pick a real task** you did this week — a bug, a report, an email, a spreadsheet question.
   Small and concrete beats big and vague.
2. **Write the weak version.** Type the prompt the way you would have yesterday.
   Save the output (paste it into `lab1/before.md`).
3. **Rebuild it with the formula:** Task + Context + Constraints + Output Format.
   Paste the real content — do not describe it. Save the output to `lab1/after.md`.
4. **Try two strategies.** Add a few-shot example, or ask for step-by-step reasoning,
   and rerun. Change one thing at a time so you know what mattered.
5. **Save it as a skill.** Copy `my-skill.yaml`, rename it as a verb
   (`summarize-…`, `review-…`, `draft-…`), and fill in the four blocks.
   Test it: `python run_skill.py <your-skill-name> --file <some input>`
6. **Share at your table.** Show before/after; each table presents one skill (3 minutes).

## What good looks like

- The "after" output needs little or no editing to be used.
- Someone else at your table can run your skill on their own input.
- The constraints block mentions what the AI must **not** do (data it cannot see,
  formats it cannot use, decisions it cannot make).
