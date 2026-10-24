# Lab 2 (Developers) — Fix, test, document (45 minutes)

Work in pairs. One person drives, the other reviews; swap at step 4.

## Steps

1. **Claim an issue.** Pair A takes `issues/ISSUE-2-missing-readings.md` (a parsing bug).
   Pair B takes `issues/ISSUE-3-daily-summary.md` (a new feature). Create a branch named
   `issue-2-…` or `issue-3-…` so the PR prompt can pick up the number.
2. **Build context.** In Copilot Chat: `@workspace where is <the relevant code>?` Open every
   file it names. Reproduce the failure and paste the **exact** traceback into chat.
3. **Test first.** Write the failing test with `/tests` or the `generate-tests` prompt file.
   Run `pytest` — it must be red before you touch the code.
4. **Implement and iterate.** Use chat, inline edits, or agent mode. Rerun tests after every
   change. If Copilot loops on the same wrong answer, add context; don't just retry.
5. **Review like a senior.** Run the `review-security` prompt file on your own diff.
   Fix anything High or Med.
6. **Open the PR.** Docstrings, README section, PR description via the `draft-pr` prompt file.
   Then swap PRs with the neighboring pair and review each other's work against the
   acceptance criteria in the issue.

## What good looks like

- Every acceptance box in the issue is checked, with a test that proves it.
- You can explain every line Copilot wrote. If you can't, ask Copilot to explain it — then decide.
- The PR description says how it was tested, not just what changed.
- At least one thing Copilot suggested was rejected, and you can say why.
