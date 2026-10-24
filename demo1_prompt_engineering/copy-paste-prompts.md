# Live Demo 1 — copy-paste prompts (any AI tool)

Use these if you are following the demo in ChatGPT, Claude, Gemini, Copilot Chat, or any other assistant instead of running `prompt_lab.py`. The data is already inside each prompt.

**Start a new chat for every run.** Paste everything in the box, including the data. Then compare your output with the instructor's.

| Run | What this run adds | Watch for |
|---|---|---|
| 1 | Nothing. The prompt most people type | A generic answer, or a request for data |
| 2 | The real data, pasted | References to actual columns and regions |
| 3 | A specific task, scope, and output format | Exactly the table you asked for |
| 4 | One worked example (few-shot) | Format matches on the first try |
| 5 | Show the arithmetic (chain-of-thought) | Numbers you can check |
| 6 | A role, and JSON output | Something a program could consume |

## Run 1 — Zero-shot, vague

*Adds:* Nothing. This is the prompt most people type.

```
Analyze this data.
```

## Run 2 — Add context

*Adds:* The actual data (header + sample rows) instead of a description of it.

```
Analyze this data.

Here is the Q3 regional sales sheet (CSV):
region,actual_usd,target_usd,units,returns
Midwest,1240000,1300000,3100,42
Northeast,980000,1100000,2450,61
Southeast,1510000,1400000,3775,38
Southwest,720000,950000,1800,90
West,1330000,1350000,3325,35
... (12 rows total)
```

## Run 3 — Add constraints + output format

*Adds:* A specific task verb, a scope limit (top 3), and the exact output shape.

```
Analyze the Q3 regional sales sheet below. Identify the top 3 underperforming
regions versus target. Return the findings as a 3-row table with columns
Region, Actual, Target, Gap %. No commentary before the table.

region,actual_usd,target_usd,units,returns
Midwest,1240000,1300000,3100,42
Northeast,980000,1100000,2450,61
Southeast,1510000,1400000,3775,38
Southwest,720000,950000,1800,90
West,1330000,1350000,3325,35
Mountain,610000,700000,1525,20
Great Lakes,1105000,1050000,2760,29
Pacific NW,870000,1000000,2175,47
Gulf Coast,690000,800000,1725,52
Mid-Atlantic,1010000,1020000,2525,33
Canada,540000,650000,1350,18
Mexico,480000,500000,1200,15
```

## Run 4 — Few-shot

*Adds:* One worked example of the row format we want.

```
Analyze the Q3 regional sales sheet below. Identify the top 3 underperforming
regions versus target. Return a 3-row table exactly like this example:

| Region | Actual | Target | Gap % |
|---|---|---|---|
| Example-North | 812,000 | 900,000 | -9.8% |

region,actual_usd,target_usd,units,returns
Midwest,1240000,1300000,3100,42
Northeast,980000,1100000,2450,61
Southeast,1510000,1400000,3775,38
Southwest,720000,950000,1800,90
West,1330000,1350000,3325,35
Mountain,610000,700000,1525,20
Great Lakes,1105000,1050000,2760,29
Pacific NW,870000,1000000,2175,47
Gulf Coast,690000,800000,1725,52
Mid-Atlantic,1010000,1020000,2525,33
Canada,540000,650000,1350,18
Mexico,480000,500000,1200,15
```

## Run 5 — Chain-of-thought

*Adds:* A request to show the calculation before the answer, so errors are visible.

```
Analyze the Q3 regional sales sheet below. First, list each region's gap %
as (actual - target) / target, showing the arithmetic. Then give the final
3-row table of the top 3 underperforming regions: Region, Actual, Target, Gap %.

region,actual_usd,target_usd,units,returns
Midwest,1240000,1300000,3100,42
Northeast,980000,1100000,2450,61
Southeast,1510000,1400000,3775,38
Southwest,720000,950000,1800,90
West,1330000,1350000,3325,35
Mountain,610000,700000,1525,20
Great Lakes,1105000,1050000,2760,29
Pacific NW,870000,1000000,2175,47
Gulf Coast,690000,800000,1725,52
Mid-Atlantic,1010000,1020000,2525,33
Canada,540000,650000,1350,18
Mexico,480000,500000,1200,15
```

## Run 6 — Role + structured output

*Adds:* A persona for tone/expertise and JSON output for downstream tools.

If your tool has a system / custom-instructions field, put this there; otherwise paste it as the first line:

```
You are a senior supply-chain analyst. Be precise, cite numbers, and never speculate beyond the data.
```

```
Analyze the Q3 regional sales sheet below. Identify the top 3 underperforming
regions versus target. Return ONLY valid JSON:
{"regions": [{"region": str, "actual": int, "target": int, "gap_pct": float, "likely_driver": str}],
  "recommended_action": str}

region,actual_usd,target_usd,units,returns
Midwest,1240000,1300000,3100,42
Northeast,980000,1100000,2450,61
Southeast,1510000,1400000,3775,38
Southwest,720000,950000,1800,90
West,1330000,1350000,3325,35
Mountain,610000,700000,1525,20
Great Lakes,1105000,1050000,2760,29
Pacific NW,870000,1000000,2175,47
Gulf Coast,690000,800000,1725,52
Mid-Atlantic,1010000,1020000,2525,33
Canada,540000,650000,1350,18
Mexico,480000,500000,1200,15
```

## Part 2 — From prompt to skill

A *skill* is Run 3 saved as a template. In a chat tool you get the same effect two ways:

- **Custom instructions / Projects / GPTs / Gems:** paste the block below into a reusable instruction set, then just attach a CSV and say "go".
- **A text file you keep:** save the block, swap the data block each time.

```
Task: Analyze the sales data below and answer this question: which regions are off target and why

Context (CSV contents):
<paste the CSV here>

Constraints:
- Use only the numbers in the data; do not invent causes you cannot support.
- Treat gap % as (actual - target) / target.
- Do not include confidential figures beyond what is in the file.

Output format:
- "Key trends": 3 bullets max
- "Anomalies": bullets, or "None found"
- "Suggested chart": one line naming the chart type and axes
```

Try it on **Q4** data (the skill has never seen this file):

```
region,actual_usd,target_usd,units,returns
Midwest,1390000,1350000,3475,40
Northeast,1020000,1150000,2550,58
Southeast,1480000,1500000,3700,44
Southwest,810000,950000,2025,71
West,1290000,1400000,3225,39
Mountain,720000,720000,1800,17
Great Lakes,1130000,1100000,2825,31
Pacific NW,940000,1050000,2350,45
Gulf Coast,650000,850000,1625,63
Mid-Atlantic,1060000,1070000,2650,30
Canada,600000,680000,1500,16
Mexico,530000,520000,1325,12
```

## Part 3 — The two-step agent, by hand

`agent.py` chains two skills with a human approval gate. In a chat tool, do it in two messages:

**Message 1** (summarize the meeting):

```
Task: Summarize the meeting below for people who were not there.

Context:
Supplier performance review — weekly sync (transcript excerpt)

Priya: Q4 on-time is at 71% for Gulf Coast's main supplier, down from 84%. Three late shipments stopped a line.
Marcus: Canada's target was set 20% above Q3 without a demand signal. I'd like to re-baseline it on trailing four quarters.
Dana: Agreed. Can we ship the supplier scorecard to regional leads Friday?
Priya: Yes. I'll pull return root-cause codes for Southwest and Gulf Coast by Wednesday.
Marcus: I'll take the Canada re-baseline, done Thursday.
Dana: I'll draft the email to the Gulf Coast supplier for Friday.
Priya: One more — should we freeze new-vendor onboarding in Gulf Coast until the returns review is done?
Dana: Yes, let's freeze it. Escalating to procurement leadership is still an open question.

Constraints:
- Only include decisions that were explicitly agreed, not proposals.
- Every action item needs an owner; write "unassigned" if none was named.
- Keep it under 200 words.

Output format (Markdown):
**Decisions** — bullets
**Action items** — table: Owner | Action | Due
**Open questions** — bullets
```

**Message 2** (draft the email from that summary):

```
Task: Draft a professional email from the brief below.

Context:
Write to the supplier named in the action items about their on-time delivery.

<paste the summary from message 1 here>

Constraints:
- Tone: firm but collaborative
- Under 150 words. No jargon. No apologies for things we did not do.
- Use [placeholders] for any name, date, or figure not in the brief.

Output format:
Subject line, then the email body. End with one specific, answerable ask.
```

**Message 3 is you.** Read the draft. Would you send it? That decision is the checkpoint, and it is the part no tool should skip.
