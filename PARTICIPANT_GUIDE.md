# Participant guide — how to follow the demos and do the labs

Everything in this workshop can be done **two ways**. Pick the one that fits you; the
lessons are identical.

| | Path A — Python scripts | Path B — Any AI tool |
|---|---|---|
| Who | Developers, anyone comfortable with a terminal | Everyone else |
| What you need | Python 3.11+, this repo, 5 minutes of setup | A browser and whichever AI assistant your organization allows: ChatGPT, Claude, Gemini, Copilot Chat, Microsoft 365 Copilot |
| How you follow a demo | Run the same commands the instructor runs | Paste the same prompts the instructor uses, from the `copy-paste-prompts.md` file in each folder |
| Labs | Lab 1 via `run_skill.py`; Lab 2 developer track with GitHub Copilot | All labs have a paste-into-your-tool version (see below) |

> **Rule for the whole day:** only paste real company data into tools your organization
> has approved. Every example in this repo is synthetic, so it is safe in any tool.

---

## Path B — Any AI tool (no setup)

You copy prompts from three files and paste them into your assistant. Each prompt is
self-contained: the data is already inside it, so you don't need to upload anything.
(If your tool supports file upload, you can attach the CSV instead. Both work.)

**Following the demos**

| When | Open this file | What you do |
|---|---|---|
| Live Demo 1 (10:40) | `demo1_prompt_engineering/copy-paste-prompts.md` | Paste runs 1–6 as the instructor runs them; compare your output with the screen |
| Live Demo 2 (1:40) | `demo2_github_copilot/copy-paste-prompts.md` | Paste the code and the issue into your assistant and follow the same steps without Copilot |

**Doing the labs** — each lab has a complete AI-tool version; you do not need Python or Copilot for any of them.

| Lab | Open this file | Deliverable |
|---|---|---|
| Lab 1 (11:15) — prompt and skill | `demo1_prompt_engineering/lab1/with-any-ai-tool.md` | A before/after pair and a reusable skill saved in your tool |
| Lab 2 (2:50) — office track | `office_lab/copy-paste-prompts.md` (steps) + `office_lab/INSTRUCTIONS.md` (what good looks like) | A cleaned summary, an email, a 5-slide outline |
| Lab 2 (2:50) — developer track | `demo2_github_copilot/lab2/without-copilot.md` | A fixed issue with passing tests and a PR description (you run `pytest`; the assistant writes) |

Habits that matter more than the tool:
- Start a **new chat** for each run in Demo 1 so earlier answers don't leak into later ones. In Demo 2 and Lab 2, keep **one chat per issue** so the assistant remembers the code.
- Paste the **whole** prompt, including the data block at the bottom.
- When the output is wrong, don't just retry. Add the missing context and ask again. That is the lesson of the day.

---

## Path A — Python scripts

### Setup (once, ideally before the workshop)

```bash
git clone <repo-url> ai-at-work-demos
cd ai-at-work-demos
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

Leave `.env` as is for **mock mode**: the scripts replay realistic canned outputs with no
API key and no network, so everything works on a locked-down laptop. To run against a real
model, set `LLM_PROVIDER` to `anthropic`, `openai`, or `azure` and add the matching key.

Check it works:

```bash
cd demo1_prompt_engineering
python prompt_lab.py --run 1 --no-pause
```

### Live Demo 1 — follow along

```bash
cd demo1_prompt_engineering
python prompt_lab.py                     # all six runs; press Enter between them
python prompt_lab.py --run 3             # a single run
python prompt_lab.py --compare 1 3       # two runs side by side
python run_skill.py --list               # the reusable skills
python run_skill.py analyze-sales-data --file data/q4_sales.csv
python agent.py                          # two skills chained, with a human checkpoint
```

### Lab 1

Follow `demo1_prompt_engineering/lab1/INSTRUCTIONS.md`. Your deliverable is a skill file:

```bash
cp lab1/my-skill.yaml lab1/summarize-incident.yaml   # name it as a verb
# edit the four blocks, then:
python run_skill.py summarize-incident --file <some input file> --show-prompt
python prompt_lab.py --file my_prompt.txt            # run any free-form prompt
```

In mock mode your own prompts get a placeholder reply (there is no canned answer for them).
Either set a real provider in `.env`, or paste the rendered prompt (`--show-prompt`) into your chat tool.

### Live Demo 2 — follow along (GitHub Copilot)

Open `demo2_github_copilot/` **as the workspace folder** in VS Code (File → Open Folder),
with the GitHub Copilot and Copilot Chat extensions signed in. Then:

```bash
cd demo2_github_copilot
pip install -r requirements.txt
python run_report.py data/sensors_clean.csv    # works
python run_report.py data/sensors_short.csv    # crashes: this is Issue #1
```

The instructor's exact Copilot prompts are in `demo2_github_copilot/copy-paste-prompts.md`.
Type them into Copilot Chat as they appear on screen.

### Lab 2, developer track

Follow `demo2_github_copilot/lab2/INSTRUCTIONS.md`. Issues #2 and #3 are yours.
No Copilot? Use `lab2/without-copilot.md`.

### Lab 2, office track

```bash
cd office_lab
python office_demo.py            # the six office steps
python office_demo.py --check    # the answer key for step 3
```

or follow `office_lab/INSTRUCTIONS.md` in Excel, Outlook, and PowerPoint.

---

## If something breaks

- `ModuleNotFoundError` → the virtual environment isn't active, or `pip install -r requirements.txt` didn't run.
- `No module named llm` from `office_demo.py` → run it from inside `office_lab/`.
- `[mock mode] No canned response` → expected for your own prompts in mock mode; see Lab 1 above.
- Anything else → switch to Path B for the current exercise and ask a helper at the break.
