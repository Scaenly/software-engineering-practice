# AI Usage Disclosure — Week 08

This disclosure records preparation, the actual controlled diagnostic chats, repair automation and subsequent AI-assisted writing. Independent personal understanding was not assessed.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| ChatGPT / Codex | not displayed | Retrieved the actual public Week 07 branch, copied its app, ran the real 27-test baseline and buggy suites, and added BUG-A/BUG-B regression tests | app/src/booking.test.ts; lab-report.md; evidence/01–03 logs |
| ChatGPT / Codex | not displayed | Drafted identical diagnostic inputs, factual observations, this disclosure, the declaration and a guarded repair/checking helper | prompts/; lab-report.md; AI_USAGE.md; submission.yml; repair_and_check.py; PR_DESCRIPTION.md; START_HERE_RU.md |
| ChatGPT | not displayed | diagnosis without the skill in a fresh chat (Task 4) | none — "Do not edit code" |
| ChatGPT | not displayed | diagnosis with the supplied bug-detector procedure in a separate fresh chat; prompt-only simulation (Task 5) | none — "Do not edit code" |
| ChatGPT / Codex | not displayed | Supplied final-writing drafts, clarified disclosure and prepared the PR description | lab-report.md sections 9.2–10; AI_USAGE.md; PR_DESCRIPTION.md |

**skills/bug-detector/SKILL.md was typed by me from the deck's text, not generated:** manual keystrokes were not independently verified. The student created and committed the prescribed file and ZIP in VS Code; the supplied screenshot records commit 2c6fdf6. The report-update packages did not create or overwrite that source file or ZIP.

**I applied the patches myself, one minimal change per bug, after reviewing what the assistant proposed:** no — after the diagnostic replies and comparison, the Codex-authored repair_and_check.py applied the reviewed strict-comparison change for BUG-A and deleted only bookings.push for BUG-B. Each change has its own targeted/full runs and separate commit; the comment was retained.

**I used another assistant as well:** yes — Codex prepared factual report material and the helper before the two controlled chats. This assistance is disclosed above.

**Every terminal output currently in lab-report.md was pasted from a real run, unedited:** yes. Captured stdout/stderr is saved in full; NO_COLOR=1 and FORCE_COLOR=0 were set before the runs. No success output or screenshot was invented.

**I can explain both bugs and both fixes without the assistant:** not independently assessed; no independent student explanation was recorded in this session.

**Anything accepted from AI without fully understanding it:** independent understanding was not assessed. The helper, regression tests, comparison and report writing were assisted by Codex. A personal hypothesis before AI assistance was not captured and must not be invented retroactively.

The two controlled chat replies, the prompt-only screenshot and an AI-assisted comparison draft have now been supplied. An earlier unsuccessful skill request is also disclosed. Codex subsequently supplied suggested wording for sections 9.2 and 10 at the student's explicit request. The published conclusion uses the AI-drafted text and is not claimed as independently written personal reflection. Raw project terminal evidence is separate from assistant claims of isolated execution.

Signed: Yerassyl Arystanbek 
Date: 8 November 2026

## Subsequent diagnosis and report assistance

Codex transcribed the two complete student-supplied diagnostic replies into evidence files and report sections 5–6, drafted the factual comparison in section 7, recorded the earlier failed skill attempt, and prepared update_diagnosis.py. Both replies proposed deleting an unnecessary comment; the reviewed repair retains it so BUG-B changes one line. No independent personal pre-AI hypothesis is claimed. Codex also drafted suggested text for sections 9.2 and 10 at the student's explicit request; the published conclusion uses that AI-drafted text. This subsequent writing assistance is disclosed here.

## Time accounting

The student supplied retrospective estimates of 5–6 hours of manual work and 3 hours of AI-assisted work. No measured time breakdown was kept.
