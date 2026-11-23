# AI Usage Disclosure — SIS #04

| Tool | Exact model / plan | Date | Used for | Which files it touched |
| --- | --- | --- | --- | --- |
| ChatGPT Work / Codex | GPT-6 | 2026-11-23 | Reading the assignment and repository; risks and small-step plan | report.md sections 1–3 |
| ChatGPT Work / Codex | GPT-6 | 2026-11-23 | Room catalog, filters and selected-room checks | app/src/rooms.ts, filter.ts, booking.ts |
| ChatGPT Work / Codex | GPT-6 | 2026-11-23 | Refactoring, UI and diagrams | App.tsx, availability.ts, components/, diagrams/; removed sampleData.ts and types.ts |
| ChatGPT Work / Codex | GPT-6 | 2026-11-23 | Tests and actual automated runs | app/src/catalog.test.ts, App.test.tsx; boundary IDs in booking.test.ts; evidence/*.txt |
| ChatGPT Work / Codex | GPT-6 | 2026-11-23 | Technical report, declaration and PR preparation | report.md, AI_USAGE.md, submission.yml, app/README.md, tests/browser-smoke.cjs, .github/workflows/sis04-evidence.yml |

The session identifies GPT-6; no more specific snapshot was displayed. No subagents were used.
The initial message was the assignment, and later short user replies selected or discussed
assistant questions. Section 8 identifies their exact origin and labels excerpts.

**The assistant wrote, or helped write, tests in app/:** yes. It added 14 catalog cases and
three UI cases and labelled four existing boundary cases. Expected results are derived from
AC1–AC5, F1–F5 and B1–B6 and mapped in report section 6.1. All 29 inherited cases remain.

**Every run pasted in report.md is unedited:** yes; the assistant ran them in the Codex Linux
workspace. These were not runs personally executed on the student's computer.

**Every number in report.md section 7 was measured the way its row says:** yes.

**Credentials or keys supplied to the assistant:** none. The connected GitHub app was used to
read and write this assignment branch and prepare its PR. No credential was extracted or pasted.

**Personal understanding and defence:** pending student review; no student signature is claimed.
The assistant cannot verify that the student can explain every line.

**Anything accepted without personal verification:** the new implementation, tests and report
are assistant-prepared until the student reviews them. The assistant's automated checks are
listed separately from personal verification.

**Student reflection:** section 10 was supplied by the student in this chat and preserved verbatim. The reference to 43 tests is the intermediate run before the three UI cases; final automated results are 46/46. No assistant text replaced the student reflection.

**Browser evidence:** the local launch failed and was saved. GitHub Actions then executed the real application, passed the capture assertions and produced all five committed PNGs. provenance.json records the final source commit, run, artifact and file hashes. CI runner compatibility and capture transition settings were corrected based on real failed/output evidence.

**Personal source review:** still pending, as explicitly stated in the student reflection. No completed personal review or signature is claimed.
No new SKILL.md was submitted. The supplied checker, validator, README and starter are unchanged.

Signature: pending student review
Date prepared: 2026-11-23
