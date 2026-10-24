# Lab 1 with any AI tool — worksheet (45 minutes)

For ChatGPT, Claude, Gemini, Copilot Chat, or Microsoft 365 Copilot. No Python, no repo.
Keep a blank text document open next to your chat; you will paste four things into it.

> Use only tasks and content you are allowed to put into the tool you are using. If in
> doubt, make the content up or use the sample files at the bottom.

## Step 1 — Pick a real task (3 min)

Something you did this week that took 15 minutes or more of typing or thinking:
an email, a summary, a status update, an Excel question, a bug, a document to review.

Write it in your text doc: `Task: ______`

## Step 2 — The weak version (5 min)

In a **new chat**, type the prompt the way you would have typed it yesterday. One line is fine.
Paste the prompt and the answer into your doc under `BEFORE`. Do not fix anything yet.

## Step 3 — Rebuild with the formula (12 min)

Open a **new chat**. Fill in this template and paste the whole thing:

```
Task: <verb + object: "Summarize", "Draft", "Review", "Explain", "Rewrite"...>

Context:
<paste the ACTUAL material: the email thread, the data, the code, the notes.
 Do not describe it — paste it.>

Constraints:
- <length, tone, audience>
- <what to leave out, what not to assume>
- <standards or rules it must follow>

Output format:
<bullets / a table with these columns: ... / an email with subject line / JSON / numbered list>
```

Paste prompt and answer under `AFTER`. Compare with BEFORE. Which single line made the biggest difference? Note it.

## Step 4 — Try two strategies (10 min)

Same chat, one change at a time:

| Strategy | Add this to your prompt | Use it when |
|---|---|---|
| Few-shot | "Here is an example of the output I want: `<one example>`" | The format keeps coming back wrong |
| Chain-of-thought | "Before the answer, list the steps or the calculation you used." | You need to check the reasoning |
| Role | Custom instructions / first line: "You are a <role> writing for <audience>." | Tone or depth is off |
| Iterative refinement | "Good. Now make it shorter / more formal / add X." | The answer is 80% there |

Note which one helped and which one did nothing. Both are findings.

## Step 5 — Save it as a skill (10 min)

A skill is just your Step 3 prompt with the specifics replaced by placeholders, saved where you can reuse it. Write it in your doc:

```
SKILL: <verb-first name, e.g. summarize-status-thread>
Use when: <one sentence>

Task: ...
Context: {paste the thread here}
Constraints: ...
Output format: ...
```

Then put it somewhere that persists, depending on your tool:

- **ChatGPT:** Settings → Personalization → Custom instructions, or create a Project / GPT with it as the instructions.
- **Claude:** create a Project and paste it as the project instructions.
- **Gemini:** create a Gem with it as the instructions.
- **Copilot Chat / M365 Copilot:** save it in a Notebook or a OneNote page; paste it each time. Many organizations also have a shared prompt library — ask.
- **Any tool:** a text file in a folder your team shares.

Test it once on a *different* input than the one you built it on. If it still works, it is a skill.

## Step 6 — Share at your table (5 min)

Show your BEFORE and AFTER side by side. Each table picks one skill to present in 3 minutes.

---

## Sample material if you do not have your own

**Meeting notes** (for a summarize skill):

```
Weekly sync, Tuesday. Priya: Q4 on-time is 71% for our main Gulf Coast supplier, down from 84%; three late shipments stopped a line. Marcus: Canada's target was set 20% over Q3 without a demand signal, wants to re-baseline on trailing four quarters. Dana: agreed; can we ship the scorecard to regional leads Friday? Priya: yes, and I'll pull return root-cause codes for Southwest and Gulf Coast by Wednesday. Marcus takes the Canada re-baseline, Thursday. Dana drafts the supplier email, Friday. Open: escalate to procurement leadership this quarter?
```

**Email brief** (for a draft-email skill):

```
To: our Gulf Coast supplier's account manager. Q4 on-time delivery was 71% against the 95% in our service terms; three late shipments blocked production. Goal: get a corrective action plan with a date, keep the relationship constructive. Ask: confirm receipt by end of week; plan due in 10 business days.
```

**Data** (for an analyze skill): the Q3 and Q4 sales tables in `../copy-paste-prompts.md`.

## What good looks like

- Your AFTER output needs little or no editing before you would actually use it.
- Someone else at your table can run your skill on their own input and get a similar result.
- Your constraints say what the AI must **not** do (data it cannot see, decisions it cannot make).
