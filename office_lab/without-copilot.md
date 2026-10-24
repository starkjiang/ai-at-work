# Running the office track without Microsoft 365 Copilot

The office track teaches the prompt formula on office tasks. Copilot inside Excel, Outlook,
and PowerPoint is the *delivery vehicle* at most clients, but it is not required to run the
demo or the lab. Use whichever of these fits the room, from most to least Copilot-like.

## Option A — Any approved chat assistant with file upload

Claude, ChatGPT, Gemini, or the client's own approved assistant. Upload `supplier_performance.csv`
and paste the prompts from `office_prompts.yaml` (they are app-independent). For step 5, paste
the outline into PowerPoint's outline view or Word. Say once at the start:

> "At your company the button lives inside Excel. The prompt is the same. Learn the prompt."

## Option B — The `office_demo.py` runner (no licenses, no internet)

```bash
cd office_lab
python office_demo.py           # all six steps, mock mode by default
python office_demo.py --step 3  # one step
python office_demo.py --check   # ground-truth numbers for the verify-by-hand moment
```

Mock mode replays realistic outputs; set `LLM_PROVIDER` in `../.env` to run against a real model.
The `--check` output is the answer key for step 3 — the mock output deliberately contains
figures the participants should not take on faith.

## Option C — Recorded clips

If the client will buy Microsoft 365 Copilot, they will want to see it in the app. Record
3–4 minutes from a licensed account (Excel insight + chart, Outlook draft, PowerPoint
generate) and play the clip after the live prompts. Do not stage a "live" demo on a
licensed account you cannot rehearse on.

## What to change in the lab

- Step 1–5: identical prompts; change only where they are typed.
- Step 6 (Teams recap): Teams meeting recap needs the paid add-on even where Copilot Chat
  exists. Replace it with the version in `INSTRUCTIONS.md`: paste your table's discussion
  notes into the assistant and ask for decisions, action items, and open questions.
  This reuses the `summarize-meeting` skill from Demo 1 and lands the same lesson.
