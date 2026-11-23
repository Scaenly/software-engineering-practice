## What I built

Audited the actual Week 08 Smart Campus app and preserved all 29 inherited tests. Added a failing R1 regression, then extracted shared pure booking predicates; the final suite passes 30/30. Corrected the student-approved AGENTS.md with a minimal nine-line patch and restored the required one-fictional-room scope. The report contains eight challenged claims, six risks, a twelve-row readiness audit (Level 1), two required mitigations, residual scores and the student's verbatim NO-GO conclusion.

The PR is a draft pending personal source/diff review and real desktop/mobile UI screenshots. Final local test, lint, typecheck and build commands pass. The audit currently reports 29 PASS / 0 FAIL / 2 ERROR: E1 and E2 are openly declared missing screenshots. The shape validator passing does not certify the missing manual work.

## AI tools used

ChatGPT/Codex read the repository, performed a read-only review phase, prepared the source challenge, report, regression, patches and VS Code instructions, and ran the recorded terminal checks. The exact model version was not displayed. The student explicitly approved the AGENTS proposal before application and supplied the Russian release conclusion. AI_USAGE.md distinguishes these actions from pending student verification; it does not fabricate Plan-mode isolation, student signatures or manual UI success.

## What the AI got wrong

No claim that old BUG-B still mutates data is supported: it was already fixed. The review's dependency concern remains plausible rather than a confirmed vulnerability. The R1 NaN case has limited reachability through the current UI parser. A separate before-edit file-list reply for the refactor was not captured. Local browser execution failed, so no replacement screenshots or visual pass claims were invented. SETUP.md was missing from the uploaded materials and repository history; these five headings follow the prior course PR description, with that limitation disclosed.

## Time spent

No measured student/AI time split was kept. The work and logs were created on 23 November 2026, after the assignment deadline; no backdated completion is claimed.

## What I would do differently

Capture the explicit file plan before the first patch, conduct the student's independent source/diff review as it happens, and verify UI behavior in a reachable browser before preparing submission. Before production reuse, add real CI checks and a controlled-clock test/fix for stale feedback. Leave this PR open until grading; do not merge or deploy.
