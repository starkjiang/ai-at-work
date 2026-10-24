# AI at Work — Demo Codebase

Companion code for the one-day **AI at Work: Productivity & Productivity Tools** workshop
run by the Translational AI Center (TrAC), Iowa State University.

The repo is deliberately company-agnostic. Every example uses a generic
"sensor pipeline" and "supplier performance" scenario; swap in your own data,
standards, and approved tools before delivering to a specific client
(see [Customizing for a client](#customizing-for-a-client)).

| Folder | Used in | What it is |
|---|---|---|
| `demo1_prompt_engineering/` | Morning — Live Demo 1, Lab 1 | `copy-paste-prompts.md` for any AI tool, plus a small "prompt lab" CLI: run the same task with six increasingly strong prompts, run reusable skill files, and chain skills into an agent with a human checkpoint. Works offline in mock mode. |
| `demo2_github_copilot/` | Afternoon — Live Demo 2, Lab 2 (developers) | `copy-paste-prompts.md` and `lab2/without-copilot.md` for any AI tool, plus a realistic Python package with real bugs, no tests, and three open issues. Open it in VS Code with GitHub Copilot and work an issue to a pull request. |
| `office_lab/` | Afternoon — Lab 2 (office users) | Sample supplier data, ready-to-use prompts for Excel/Word/Outlook/PowerPoint Copilot, and `office_demo.py` — runs the same six steps with any model or offline, so no Microsoft 365 Copilot license is needed (see `office_lab/without-copilot.md`). |

## Participants: start here

Read **[PARTICIPANT_GUIDE.md](PARTICIPANT_GUIDE.md)**. It explains the two ways to follow along: run the Python scripts, or paste the same prompts into any AI tool (ChatGPT, Claude, Gemini, Copilot). Each demo folder has a `copy-paste-prompts.md` for the second path.

## Quick start (Python path)

```bash
git clone <your-fork-url> ai-at-work-demos
cd ai-at-work-demos
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # optional: add an API key
```

**No API key?** Everything in `demo1_prompt_engineering/` runs with `LLM_PROVIDER=mock`
(the default). Mock mode replays realistic canned outputs so the six-run demo works
on a locked-down laptop. Demo 2 needs only VS Code + GitHub Copilot.

## Day plan

| Time | Block | Material |
|---|---|---|
| 9:00 – 10:40 | Session 1 fundamentals and role practice (break 10:10) | Slides |
| 10:40 – 11:15 | **Live Demo 1** — prompt engineering | `demo1_prompt_engineering/` |
| 11:15 – 12:00 | **Lab 1** — build your own prompt and skill | `demo1_prompt_engineering/lab1/` |
| 1:00 – 1:40 | Session 2 fundamentals (GitHub Copilot) | Slides |
| 1:40 – 2:25 | **Live Demo 2** — Copilot on a real project | `demo2_github_copilot/` |
| 2:25 – 2:40 | Microsoft 365 Copilot overview | Slides |
| 2:50 – 3:35 | **Lab 2** — developer and office tracks | `demo2_github_copilot/lab2/`, `office_lab/` |
| 3:35 – 4:30 | Responsible use, 30-day plan, takeaways, Q&A | Slides |

## Customizing for a client

1. Replace `sensor_pipeline` examples with a domain your audience recognizes
   (the structure stays the same: ingest → compute → alert → report).
2. Edit `demo2_github_copilot/.github/copilot-instructions.md` with the client's
   coding standards, security rules, and IP constraints.
3. Update `demo1_prompt_engineering/skills/*.yaml` constraints with the client's
   approved-tool policy.
4. Set `LLM_PROVIDER` to whatever the client has approved (Azure OpenAI is the
   common case for M365 shops); never paste client data into an unapproved tool.

## License

MIT — fork freely for your own team's training.
