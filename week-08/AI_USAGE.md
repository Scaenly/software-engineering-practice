# AI Usage Disclosure — Week 08

This is an INCOMPLETE preparation record, not a signed claim that all lab activities are finished.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| ChatGPT / Codex | not displayed | Retrieved the actual public Week 07 branch, copied its app, ran the real 27-test baseline and buggy suites, and added BUG-A/BUG-B regression tests | app/src/booking.test.ts; lab-report.md; evidence/01–03 logs |
| ChatGPT / Codex | not displayed | Drafted identical diagnostic inputs, factual observations, this disclosure, the declaration and a guarded repair/checking helper | prompts/; lab-report.md; AI_USAGE.md; submission.yml; repair_and_check.py; PR_DESCRIPTION.md; START_HERE_RU.md |
| Not yet performed | not displayed | diagnosis without the skill (Task 4) | none — "Do not edit code" |
| Not yet performed | not displayed | diagnosis with bug-detector (Task 5) | none — "Do not edit code" |

**skills/bug-detector/SKILL.md was typed by me from the deck's text, not generated:** no — not created yet. The provided deck text must be typed by the student.

**I applied the patches myself, one minimal change per bug, after reviewing what the assistant proposed:** no — no repair has been applied yet. If repair_and_check.py is used, disclose that the Codex-authored helper applies and commits the two reviewed one-line changes.

**I used another assistant as well:** yes — Codex prepared factual report material and the helper before the two controlled chats. This assistance is disclosed above.

**Every terminal output currently in lab-report.md was pasted from a real run, unedited:** yes. Captured stdout/stderr is saved in full; NO_COLOR=1 and FORCE_COLOR=0 were set before the runs. No success output or screenshot was invented.

**I can explain both bugs and both fixes without the assistant:** not assessed; student must answer after reviewing the code and runs.

**Anything accepted from AI without fully understanding it:** student review pending. The helper, regression tests and factual report draft were prepared by Codex. A personal hypothesis before AI assistance was not captured and must not be invented retroactively.

The two fresh chats, skill typing/packaging, screenshot, comparison, personal limitation, conclusion and self-assessment remain incomplete. Update this disclosure with the actual models and activities when completed.

Signed: not signed — student review pending
Date: 8 November 2026
