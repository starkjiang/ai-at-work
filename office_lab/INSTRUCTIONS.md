# Lab 2 (Office users) — Analyze, draft, present (45 minutes)

> All six prompts, ready to paste into any AI tool, are in [`copy-paste-prompts.md`](copy-paste-prompts.md).


Use Microsoft 365 Copilot in Excel, Outlook, and PowerPoint if you have it. If you don't,
use any approved chat assistant with the CSV attached, or `python office_demo.py`
(see `without-copilot.md`). The prompts are identical either way.

Data: `supplier_performance.csv` — 40 suppliers, 12 months of shipments, late shipments,
on-time %, defects, and spend. Open it in Excel and **Format as Table** first
(Copilot works best on a formatted table with a header row).

The file has deliberate flaws: two duplicated rows and some blank regions. Finding them is part of the lab.

## Steps

1. **Open the data.** Select the table, open Copilot, and ask:
   > Describe this table: what does each column mean and what time range does it cover?
2. **Ask for insight.**
   > Which 3 suppliers have the lowest average on-time % across the year? Show the monthly trend for each as a line chart suitable for an executive audience.
3. **Clean and summarize.**
   > Find duplicate rows and rows with a blank region. Then summarize total spend, average on-time %, and total defects by region in a new sheet.
   Verify **one** number by hand (a SUMIF or a filter) before you trust the rest.
4. **Draft the email.** In Outlook, "Draft with Copilot":
   > Draft an email to the account manager at [worst supplier] about their on-time delivery falling below our 95% target. Tone: firm but collaborative. Under 150 words. End with a specific ask and a date.
5. **Build the deck.** In PowerPoint, "Create presentation about…":
   > A 5-slide supplier performance review for a leadership meeting: summary, three lowest performers with trend, regional comparison, defects vs. spend, recommended actions. One idea per slide, add speaker notes.
6. **Recap and compare.** Have one person take rough notes while your table compares what
   each person's best prompt included. Paste the notes into your assistant and ask:
   > Summarize these notes for someone who wasn't here: Decisions, Action items (Owner | Action | Due), Open questions. Under 150 words.
   (Teams Copilot does this automatically for meetings if your organization licenses it.)

## What good looks like

- You caught the duplicates and the blanks before they reached the summary.
- Your email names the number, the target, and the ask — nothing else.
- Your deck has one idea per slide and you could present it without editing.
- You can say which single phrase in your prompt made the biggest difference.
