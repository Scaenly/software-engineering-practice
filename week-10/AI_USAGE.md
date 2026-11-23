# AI Usage Disclosure — Week 10

Course policy: Level D. This file distinguishes executed assistant work from student actions.

| Tool | Exact model / plan | Used for | Which files it touched |
| --- | --- | --- | --- |
| ChatGPT / Codex | not displayed; Work Mode | Read-only risk review from the exact supplied prompt | none in app during the review phase |
| ChatGPT / Codex | not displayed | AGENTS.md audit and minimal patch draft | app/AGENTS.md after explicit student approval |
| ChatGPT / Codex | not displayed | R1 regression and pure-module mitigation | app/src/booking.test.ts, bookingRules.ts, booking.ts, availability.ts |
| ChatGPT / Codex | not displayed | One-room scope correction, documentation and VS Code tasks | app/src/sampleData.ts, app/src/App.tsx, app/README.md, Week10.code-workspace |
| ChatGPT / Codex | not displayed | Source challenge, risk scoring, audit, scripts and report preparation; real terminal checks | lab-report.md sections 1–9, submission.yml, evidence/, scripts/, START_HERE_RU.md, PR_DESCRIPTION.md |

**The review in Task 2 ran in a mode where the assistant could not edit, and git status showed no change afterwards:** no — the review phase was read-only in practice and git status was empty before/after, but the tool set was not technically locked. No separate Plan-mode or independent-model session is claimed. The prompts were handled in the present session from the supplied task text.

**I labelled every claim in lab-report.md §3.2 after opening the cited file myself:** no — the assistant inspected the files and prepared the labels; the student's own independent verification is pending.

**Every change to app/ was reviewed by me as a diff before I accepted it:** no — the student explicitly approved the AGENTS proposal after presentation. Code changes were reviewed by the assistant; the student's code-diff acceptance remains pending. A separate before-edit file-list reply for the refactor was not captured and is not claimed.

**I used another assistant as well (to explain a risk, to draft text in lab-report.md, …):** no other assistant session is claimed. This same ChatGPT/Codex session drafted sections 1–9 and the supporting documents. Section 10's Russian conclusion was supplied by the student and is preserved verbatim with separately labelled editorial risk references.

**Every terminal output in lab-report.md was pasted from a real run, unedited:** yes — logs are captured from actual processes. The red run retains captured stdout followed by stderr; no expected result or test count was substituted. Runtime timestamps and paths are retained. All final test assertions are committed, with 30 tests total.

**I can explain every score in my register, and why my release decision follows from it, without the assistant:** no — this has not been certified by the student. The student's own NO-GO paragraph explains the remaining CI and stale-result concerns; independent defence of each score still needs preparation.

**Anything I accepted from the AI without fully understanding it:** not yet declared by the student. Review the shared-predicate diff, the limited reachability of the NaN regression, all risk scores, and the remaining UI/CI/clock limitations before submission. No student understanding or signature is fabricated.

The UI attempts did not succeed: Chromium launch was denied socket creation and the separate browser could not reach loopback. Desktop/mobile screenshot failures E1 and E2 remain openly declared. No screenshot or manual UI success was invented. No production service was used, no background agent was spawned and no merge or deployment was performed.

Prepared for: Yerassyl Arystanbek. Student signature remains pending.
Date: 2026-11-23
