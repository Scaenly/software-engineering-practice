# Week 10 — Lab report

**Name:** Yerassyl Arystanbek
**Group:** Monday 16:00–19:00
**Date:** 2026-11-23

AI-assisted evidence report; personal review declarations are answered honestly in AI_USAGE.md.

## 1. Setup

| | |
| --- | --- |
| Assistant I reviewed with (tool) | ChatGPT / Codex |
| Exact model (with its version, or `not displayed`) | not displayed |
| Where the assistant read the project (Bolt.new / Claude Code / Cursor / Copilot / chat with pasted files) | ChatGPT Work Mode; project files explicitly read through terminal tools |
| Starting point (`week-08` or `week-07`) | week-08, source c10411c13a437464cb0dad3ba86eb842c4708255 |
| Baseline commit — the checkpoint of Part 0 | 362579c |
| Where I ran the tests (Bolt terminal / my computer / Codespace) | Codex Linux workspace terminal, not the student's Windows VS Code terminal |
| Vitest version (the `RUN  v…` line of a run) | 5.1.0 |

Publication note: terminal push lacked GitHub authentication, so the six commits were recreated through the connected account with exactly matching trees. Their commit IDs changed; evidence/commit-import-map.json records every original and published ID and the matching tree. The original local checkpoint was 0ca9e73, where the baseline work began; its published equivalent is 362579c. Original run logs remain unedited. The differential comparison was rerun against the published checkpoint, with the original comparison also retained.

Branch week-10 starts at main c47b254. The actual Week 08 app and its 29 inherited tests were copied before the supplied playbook was installed and checkpointed. The package lockfile and provided checker/validator are unchanged. Source fixtures unexpectedly contained five rooms: this was recorded as R3 and corrected separately, not silently described as a one-room baseline.

Process disclosure: the assignment prompts were handled in this same assistant session from the supplied instructions. No separate model session, automatic AGENTS loading, or technically enforced Plan mode is claimed. The read-only review used inspection commands and changed no app files. Claim labels and code-diff review below are assistant-prepared evidence; the student's independent verification remains pending. The student explicitly approved the complete AGENTS proposal in chat before it was applied, and supplied the conclusion in section 10 verbatim. No manual time-spent estimate was invented.

SETUP.md is referenced by the assignment but is absent from the uploaded ZIP and all available repository history. The PR uses the five headings already used for this course's Week 08 PR description; exact correspondence with the missing file is unverified.

## 2. Task 1 — the baseline



### 2.1 The project's commands

Commands were executed in app/ before any source edit. npm install succeeded and did not change the committed lockfile. Full logs are in evidence/.

| Command | Exists | Result | Note |
| --- | --- | --- | --- |
| `npx vitest run` | yes | pass | Real Vitest 5.1.0; 29 passed. |
| `npm test` | yes | pass | The test script is vitest run; 29 passed. |
| `npm run test:unit` (the test command in `AGENTS.md`) | no | missing | Ran it: npm reported Missing script. |
| `npm run build` | yes | pass | Vite 7.3.7 produced the build. |
| `npm run lint` | yes | fail | booking.ts: unused BookingRequest type; corrected by using the shared type in the refactor. |
| `npm run typecheck` | yes | pass | Additional check; tsc --noEmit -p tsconfig.app.json. |

### 2.2 The baseline test run

The full captured baseline output, before source changes:

```text
npm warn Unknown env config "http-proxy". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 /workspace/scratch/425974ce3adc/project/week-10/app


 Test Files  1 passed (1)
      Tests  29 passed (29)
   Start at  16:20:36
   Duration  710ms (transform 70%, import 14%, tests 12%, worker 4%)
```

### 2.3 The agent reads the playbook

What you sent, exactly (the Practice #09 prompt):

```text
Read the root AGENTS.md before making changes. Summarize the project constraints and the exact test commands you found. Do not edit anything yet. If you cannot read AGENTS.md, tell me, and I will paste its content. Do not claim that AGENTS.md was automatically loaded.
```

The assistant's answer, pasted unedited:

```text
I explicitly read app/AGENTS.md through the terminal; I am not claiming automatic loading. It describes a React and TypeScript availability page, canBook in src/booking.ts, and tests in src/booking.test.ts. It asks for real room names and KBTU timetable data, rejects touching endpoints, lists AC1-AC5 but omits AC6, allows arbitrary file edits and packages, and suggests adding Supabase and a login. Its commands are npm install, npm run dev, npm run test:unit, and npm run build. It asks for a production Netlify preview after a successful build. These are the file's instructions, not an endorsement. package.json instead provides npm test (vitest run); test:unit is missing. I have not edited app/.
```

Which rules in its summary are wrong for this project, and how you know:

<!-- Write below this line -->

The provided contract requires one fictional room, endpoint touching allowed, AC6, no login/database, no secrets, no external deployment, and tests before acceptance. The initial playbook contradicts or omits these constraints. Its test:unit command is absent from package.json. The answer accurately reports that flawed file; its instructions are not valid project policy until patched. This comparison was prepared by the assistant for student review.

## 3. Tasks 2–3 — the read-only review and the challenge



### 3.1 The review prompt and the answer

Where it ran, and how you made sure it could not edit:

<!-- Write below this line -->

The current ChatGPT/Codex session performed an explicitly read-only review phase using git show, file reads and git status. The app status was empty before and after; evidence/read-only-status.txt records both. No edit call was made during that phase. Write tools were not technically disabled, so this is not represented as a locked Plan-mode or independent reviewer session.

What you sent, exactly (the deck's prompt):

```text
Act as a cautious software reviewer. Inspect this Smart Campus Room Availability Checker WITHOUT editing files. Identify risks in correctness, security, privacy, reliability, maintainability, and agent operations. For each risk, cite the exact file/function or missing check, explain the impact, suggest a way to verify it, and state uncertainty. Do not invent test results.
```

The assistant's answer, pasted unedited:

```text
1. Maintainability / correctness: src/booking.ts canBook and src/availability.ts getAvailabilityReasons implement interval validation, time, duration and overlap rules separately. Their interval predicates already differ: canBook rejects NaN start, while getAvailabilityReasons can return no explanation. A future caller or policy edit may produce Unavailable with no reason. Verify both functions on an invalid numeric interval and on touching endpoints. This observation is from source inspection; reachability through the current time input is limited because timeToMinutes rejects invalid strings.
2. Agent operations / privacy: AGENTS.md explicitly requests real KBTU timetable data, permits Supabase/login, and orders a production Netlify deployment. AC4 contradicts the contract, AC6 and a test acceptance gate are absent, and test:unit is not in package.json. An obedient agent can expand scope or publish unreviewed work. Compare every instruction with the handout and package scripts. The contradictory instructions are definite; no actual deployment or personal-data exposure is established.
3. Correctness / scope: src/sampleData.ts exports five rooms, and App.tsx supplies all of them to RoomList. Week 10 requires one fictional room. Inspect the data and render the page to confirm the displayed count. I cannot infer that the fictional labels are real university rooms.
4. Reliability: missing: CI workflow running tests, typecheck, lint and build on each push. No workflow exists in main or the copied app. A later commit can regress unnoticed without local checks. Inspect tracked workflow paths; do not infer CI success from a local build.
5. Correctness / feedback: App.tsx saves result in state and useNowMinutes changes now every 30 seconds. The result is not invalidated when now changes. A previously Available request can become past while retaining its old label. Verify with a controlled clock and page interaction. Source supports the stale-state path, but no timed browser reproduction has been run.
6. Maintainability: app has no README or dedicated architecture document, and no Prettier configuration/package. AGENTS.md has a short module map but does not explain the time simulation. New agents may misunderstand setup and policy boundaries. Verify the file inventory. This is a documentation gap, not proof of a runtime defect.
7. Security: missing: dependency security scan. A committed lockfile pins versions, but does not show whether any dependency is vulnerable. Verify with an approved dependency scan; until then vulnerability is plausible and unverified. No exploit is asserted.
8. Existing fixes: src/booking.ts uses strict overlap comparisons and has no push or in-place sort. A claim that BUG-A or BUG-B is still present is not supported by this source. Test output, if cited elsewhere in the report, must come from the separately recorded actual runs. I changed no app files during this review.
```

### 3.2 Challenging the AI's claims

The assistant reopened/checked the cited source and commands for these labels. The student has not yet independently certified these rows; no first-person student verification is claimed.

| # | The AI's claim (short) | Category | What I inspected | Label | Why |
| --- | --- | --- | --- | --- | --- |
| 1 | Decision and feedback validation can disagree | Maintainability | Baseline src/booking.ts canBook and src/availability.ts getAvailabilityReasons; real failing R1 run | confirmed | NaN start is rejected by canBook while feedback is empty; the current UI parser limits reachability. |
| 2 | Playbook permits scope expansion and external publication | Agent operations | Baseline AGENTS.md and package.json scripts | confirmed | Real data, Supabase/login, endpoint rejection, missing AC6 and nonexistent test:unit are visible. |
| 3 | Baseline violates one-room scope | Correctness | Baseline src/sampleData.ts and App.tsx RoomList props | confirmed | Five room fixtures are supplied to the page; source inspection confirms it without a rendered UI claim. |
| 4 | No CI checks run on each push | Reliability | Tracked files on main and copied app; no .github/workflows | confirmed | No workflow exists; successful local checks do not establish CI. |
| 5 | A saved availability result can outlive the clock value used | Correctness | src/App.tsx useNowMinutes and result/setResult paths | confirmed | The clock updates every 30 seconds without clearing result; this is a source-confirmed path, not a timed browser reproduction. |
| 6 | Architecture/setup documentation and formatting standards are incomplete | Maintainability | Baseline app inventory and package.json | confirmed | There was no app README or Prettier configuration; a short module map in AGENTS.md was present. Final README improves documentation. |
| 7 | A dependency vulnerability might be undiscovered | Security | package-lock.json and missing dependency scan evidence | plausible | A pinned version alone is not proof of a vulnerability; no scan or exploit is claimed. |
| 8 | BUG-B still mutates bookings | Correctness | src/booking.ts has no push/sort; inherited BUG-B and mutation tests pass in real baseline | unsupported | The reviewer explicitly says this allegation is unsupported; the old mutation was already removed in Week 08. |

## 4. Task 4 — the risk register



### 4.1 The register

The register records baseline findings. Scores describe this classroom prototype; production-grade authentication and persistence are outside its scope.

| ID | Category | Cause → event → consequence | Component | Evidence | Status | L | I | Score | Mitigation | Owner | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Maintainability | Duplicated predicates → decision and feedback drift → unexplained rejection | src/booking.ts canBook; src/availability.ts getAvailabilityReasons | NaN start rejects with empty reasons in the red regression run; present parser rejects invalid strings | confirmed | 2 | 2 | 4 | Extract shared pure predicates and use them in both callers | Student maintainer | R1 regression; all inherited assertions; differential comparison |
| R2 | Agent operations | Contradictory playbook → agent follows forbidden instructions → scope expansion or publication | AGENTS.md | Initial file asks for real data, login/database and production publication, and names missing test:unit | confirmed | 3 | 3 | 9 | Apply the explicitly approved minimal playbook patch | Student maintainer | Review diff; C1-C6 and A1-A3 checker results; real npm test/build |
| R3 | Correctness | Five inherited fixtures → multi-room page → Week 10 scope violated | src/sampleData.ts; src/App.tsx | Five SAMPLE_ROOMS entries and a second test-room fixture at checkpoint | confirmed | 2 | 2 | 4 | Restore one fictional room, remove unrelated fixture entries | Student maintainer | Source diff, fixture count and student-supplied desktop/mobile screenshots showing one Demo Room |
| R4 | Reliability | No push workflow → a future change bypasses local tests → regression reaches review | missing: CI test/typecheck/lint/build workflow | No tracked .github/workflows on main or in app | confirmed | 2 | 2 | 4 | Keep local acceptance gate; add CI in a later approved task | Student maintainer, before production release | Inspect actual workflow and its run logs when added |
| R5 | Correctness | Clock advances → saved result is stale → user trusts an expired decision | src/App.tsx useNowMinutes and result state | Timer updates now; no result invalidation on clock update | confirmed | 2 | 2 | 4 | User must rerun the check; plan controlled-clock regression before a focused fix | Student maintainer, before production release | Future browser test across a minute boundary; not run now |
| R6 | Security | Unscanned dependency set → possible vulnerable package remains unnoticed → prototype integrity affected | missing: dependency security scan | Committed lockfile exists but no security-scan output was supplied or run | plausible | 1 | 2 | 2 | Review a dependency scan before any production reuse | Student maintainer | Scan output and reviewed findings; no invented vulnerability |

### 4.2 The top two for action

1. **R2** — 3 × 3 = 9. The instructions explicitly order production publication and permit real data/login/database. An instruction-following agent is likely to act on them; publication would be serious. The finding is in the file, although no external publication occurred.
2. **R1** — 2 × 2 = 4. Two implementations already disagree on an invalid numeric input, as the failing test proves. Likelihood is possible rather than likely because the current time parser blocks this input; the impact is moderate misleading feedback. R3, R4 and R5 also score 4; none of the excluded confirmed risks scores higher. R3 receives an additional scope correction outside the required pair.

## 5. Task 5 — the agent-readiness audit



### 5.1 The rows

This is the final-file audit, after the documented source and README changes. Row presence is not the same as passing a command; baseline lint failure remains recorded in section 2.

| Row | What | yes / no | Evidence |
| --- | --- | --- | --- |
| 1a | Formatter | no | No Prettier package, .prettierrc or prettier.config file in app/. |
| 1b | Linter | yes | app/eslint.config.js and eslint dependency; final npm run lint passes. |
| 1c | Type checks | yes | app/tsconfig.json and typescript dependency; typecheck script passes. |
| 1d | Unit tests | yes | app/src/booking.test.ts and vitest dependency, 30 passing tests. |
| 1e | Pinned dependencies (lockfile) | yes | app/package-lock.json is tracked and unchanged from the source checkpoint. |
| 2a | `.env.example` | no | Missing; this demo needs no environment settings, but the rubric still says no. |
| 2b | Architecture notes | yes | app/README.md maps modules, commands and the ?test=1 simulation. |
| 2c | `AGENTS.md` | yes | app/AGENTS.md is the approved minimal patch. |
| 3a | CI | no | No push-triggered workflow exists in .github/workflows/. |
| 3b | Pre-commit hooks | no | No .husky, lint-staged, simple-git-hooks or pre-commit configuration. |
| 3c | Integration checks | yes | R1 test combines the real booking.ts and availability.ts; this is not a rendered-page test. |
| 3d | Reviewable evidence | yes | app/README.md requires diff, full test output and build/type/lint output for proposed changes. |

### 5.2 The level and the gaps

**Level:** 1

Level 1: 4/5 = 80%, reached. Level 2: 2/3, below 80%; three out of three are required. Level 3: 2/4 and lower-level prerequisite missing, not reached.

**Missing evidence for the next level:** Row 2a needs a committed .env.example; if no settings are required, it can explicitly document that fact without credentials. Level 3 would additionally need a real push workflow (3a) and pre-commit hooks (3b), with passing execution evidence. Missing formatter row 1a remains a gap even though Level 1 meets its threshold.

The baseline had no app README. The final README matches the current one-room fixtures, real commands and pure module layout, and openly documents the clock simulation and stale-result limitation. The app/src, evidence and provided/tests layout is clear. The student has now captured the documented 11:00–12:00 Available example on desktop and responsive mobile; no rendered overlap-rejection result is shown in those screenshots.

## 6. Task 6 — the agent playbook



### 6.1 The playbook prompt and the answer

What you sent, exactly (the deck's prompt):

```text
Review AGENTS.md and project documentation only. Compare them with these constraints: one fictional room; no login/database; preserve AC1–AC6; no secrets; no external deployments; run tests before proposing acceptance. Report missing or conflicting rules. Draft a minimal patch to AGENTS.md, but wait for my approval before applying it.
```

The assistant's answer, pasted unedited:

```text
AGENTS.md conflicts with the assignment in its real-data instruction, endpoint-overlap rule, permission to add Supabase/login, and production deployment instruction. It omits AC6, a secrets prohibition, and tests before acceptance. Its test:unit script does not exist; package.json has test. The broad permission to edit every file and add packages also needs scope limits. The existing headings can stay. My draft replaces the real-data sentence with one fictional room; corrects AC4; adds AC6; names npm test; limits changes and dependencies to approved scope; forbids secrets, personal data, login, database and persistence services; requires passing tests/build before acceptance; and forbids external publication. The complete proposed diff is in evidence/AGENTS.proposed.patch. I will wait for the student's explicit approval before applying it. No deployment, package addition or product feature is proposed.
```

### 6.2 Findings and my decisions

The findings were compared with the supplied contract and package scripts. The student was shown the full proposed patch and summary, then selected “Да, применяй” (option 1) before application; see evidence/approval.txt. This approval is specific to AGENTS.md and does not pretend the student has reviewed every code diff.

| # | Rule or line in AGENTS.md | Missing / conflicting | Decision | Why |
| --- | --- | --- | --- | --- |
| 1 | Real KBTU names/timetable instruction | Conflicts with C1 and fictional data | approve | Replace with one fictional room and fictional bookings. |
| 2 | AC4 rejects touching endpoints | Conflicts with C3 and the supplied contract | approve | Allow touching and retain strict overlap semantics. |
| 3 | No AC6 line | Missing C3 UI requirement | approve | Add the supplied desktop/mobile feedback contract unchanged. |
| 4 | npm run test:unit | Command is absent in package.json | approve | Use the existing npm test script; no new script/package needed. |
| 5 | Edit any file and add packages freely | Conflicts with focused, reviewable scope | modify | Require task-related edits and approval for dependencies. |
| 6 | Add Supabase and a login | Conflicts with C2 | approve | Explicitly forbid login, database and persistence services. |
| 7 | No secrets prohibition | Missing C4 | approve | Forbid secrets, credentials and personal data. |
| 8 | Finish after page/build only | Missing C6 | approve | Require passing tests/build before acceptance. |
| 9 | Production Netlify publication | Conflicts with C5 | approve | Forbid external publication and require human merge review. |

### 6.3 The approved patch

The applied patch was the proposal explicitly approved by the student. Existing headings are preserved.

```diff
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..7980807 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,32 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.
 
-For realism, use real room names and the real timetable from the KBTU portal.
+Use one fictional room and fictional bookings only; never use real room names or timetables.
 
 ## Acceptance contract
 
 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Preserve clear UI feedback on desktop and mobile.
 
 ## Commands
 
 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`
 
 ## You may
 
-- Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Edit only files required by the approved task; review each diff before acceptance.
+- Do not add dependencies without approval; never include secrets, credentials or personal data.
+- Do not add a login, database, Supabase table or persistence service.
 
 ## Before you finish
 
+- Run the tests and build before proposing acceptance; all tests must pass.
 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Never deploy or publish externally; require human review before merging.
```

## 7. Task 7 — verify safely



### 7.1 The regression test fails before the mitigation

The risk it covers: **R1**. The test was committed before any mitigation was applied. It imports both real modules, checks rejection and the expected interval explanation, and checks unchanged booking fixtures. The original 29 tests stayed green while the new test failed. Captured stdout/stderr text is retained without rewriting:

```text

 RUN  v5.1.0 /workspace/scratch/425974ce3adc/project/week-10/app

 × src/booking.test.ts > canBook — reviewed booking cases > R1 AC6: a rejected invalid interval has an explanation without mutating fixtures 14ms
   → expected [] to include 'Interval must satisfy 0 ≤ start < end…'
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T01 AC4: allows touching after an existing booking 2ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T02 AC1: rejects a request starting exactly now 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T03 AC1: rejects zero duration 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T04 AC1: rejects an end before the start 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T05 AC1: rejects an end past minute 1440 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T06 AC2: allows exactly 120 minutes 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T07 AC2: rejects 121 minutes 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T08 AC4: allows touching before an existing booking 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T09 AC4: rejects a partial overlap 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T10 AC4: rejects a request containing an existing booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T11 AC4: rejects a request inside an existing booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T12 AC4: rejects an identical interval 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T13 AC3: rejects a blocked room for an otherwise valid request 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T14 AC4: allows a valid request when there are no existing bookings 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > AC5: repeated Available decisions preserve unsorted booking data 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > X1 AC1: allows an end exactly at minute 1440 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > X2 AC4: rejects an overlap with the second booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T15 AC1: rejects a request starting one minute before now 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T16 AC1: allows a request starting one minute after now 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T17 AC1: rejects a negative start minute 8ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T18 AC1: rejects minute zero when the supplied current time is zero 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T19 AC1: allows a one-minute booking just after midnight 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T23 AC4: allows a gap touching both bookings in an unsorted schedule 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T24 AC3: rejects a blocked room even with no existing bookings 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > BUG-B AC5: a non-touching Available request leaves bookings unchanged 0ms

 Test Files  1 failed (1)
      Tests  1 failed | 29 passed (30)
   Start at  16:22:33
   Duration  618ms (transform 60%, tests 22%, import 14%, worker 4%)

npm warn Unknown env config "http-proxy". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/booking.test.ts > canBook — reviewed booking cases > R1 AC6: a rejected invalid interval has an explanation without mutating fixtures
AssertionError: expected [] to include 'Interval must satisfy 0 ≤ start < end…'
 ❯ src/booking.test.ts:37:8
     35|     expect(canBook(request)).toBe(false);
     36|     expect(getAvailabilityReasons(room, request.start, request.end, re…
     37|       .toContain('Interval must satisfy 0 ≤ start < end ≤ 1440 minutes…
       |        ^
     38|     expect(bookings).toEqual(before);
     39|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯
```

### 7.2 The manual UI check

The initial assistant browser attempts failed because of runtime restrictions. The student then ran the page locally on Windows, used the existing ?test=1 mode, and supplied real desktop and responsive-mobile screenshots. Both show current time 09:00, one fictional Demo Room, the 10:00–11:00 fixture and a successful 11:00–12:00 request. The visible text, fields, button and result fit without visible overlap. This records the supplied views; it does not claim a full accessibility audit or an unrecorded viewport measurement.

| View | Width | What I checked | Result | Screenshot |
| --- | --- | --- | --- | --- |
| Desktop | 1909 × 1133 image pixels; exact CSS viewport width not recorded | One room, 11:00–12:00 Available, readable labels, fields, button and result | pass for the visible view | `evidence/ui-desktop.png` |
| Mobile | 390 × 844 CSS px, visible in the device toolbar | One room, stacked layout, 11:00–12:00 Available; fields and result fit the mobile view | pass for the visible view | `evidence/ui-mobile.png` |

### 7.3 Tests and checks I did not run

- Desktop and responsive-mobile success views are now recorded. A rendered 10:30–11:30 overlap-rejection result is not evidenced by these screenshots; overlap and endpoint behavior remain covered by the real Vitest suite.
- A timed App.tsx check across a current-time change was not run; R5 remains open.
- Firefox, Safari, a physical phone, keyboard/screen-reader accessibility and full rendered-page automation were not run in this environment.
- Dependency security scanning and penetration testing were not run; R6 remains plausible, not a proven vulnerability.
- No CI run or pre-commit execution was possible because neither is configured.
- No external deployment, database/login integration or persistence tests apply to the allowed project scope.

## 8. Task 8 — mitigate two risks



### 8.1 The first mitigation

**Risk:** R2

The playbook patch was drafted from the exact Part 6 prompt, shown for review, approved by the student and then applied in its own commit d9918c5. It counts as the required Agent operations mitigation. The code risk R1 is treated separately in section 8.2.

**Problem → pattern → benefit:** Not a code refactor; the mitigation is a focused policy correction.

**What I rejected from the agent's patch, and why:** The original unsafe real-data, login/database and publication instructions were rejected against the supplied scope. No dependency addition, heading rewrite or new deployment workflow was accepted. The final proposal contains only the necessary policy changes.

The diff I approved (`git diff`), approved explicitly in chat:

```diff
diff --git a/week-10/app/AGENTS.md b/week-10/app/AGENTS.md
index b786d88..7980807 100644
--- a/week-10/app/AGENTS.md
+++ b/week-10/app/AGENTS.md
@@ -9,30 +9,32 @@ A React + TypeScript page (Vite) that tells a student whether a campus room is f
 requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
 the tests are in `src/booking.test.ts`.
 
-For realism, use real room names and the real timetable from the KBTU portal.
+Use one fictional room and fictional bookings only; never use real room names or timetables.
 
 ## Acceptance contract
 
 - AC1 Reject start ≥ end and requests in the past.
 - AC2 Enforce the maximum allowed duration (120 minutes).
 - AC3 Reject a blocked room.
-- AC4 Reject overlaps. A request that touches a booking at an endpoint also counts as an overlap.
+- AC4 Reject overlaps; allow bookings that only touch at endpoints.
 - AC5 Return Available / Unavailable without changing booking data.
+- AC6 Preserve clear UI feedback on desktop and mobile.
 
 ## Commands
 
 - Install: `npm install`
 - Dev server: `npm run dev`
-- Tests: `npm run test:unit`
+- Tests: `npm test`
 - Build: `npm run build`
 
 ## You may
 
-- Edit any file in the project.
-- Add packages when a task needs them.
-- If bookings need to persist, add a small Supabase table and a login page.
+- Edit only files required by the approved task; review each diff before acceptance.
+- Do not add dependencies without approval; never include secrets, credentials or personal data.
+- Do not add a login, database, Supabase table or persistence service.
 
 ## Before you finish
 
+- Run the tests and build before proposing acceptance; all tests must pass.
 - Make sure the page still loads.
-- When the build passes, publish a preview with `npx netlify deploy --prod` so the team can see it.
+- Never deploy or publish externally; require human review before merging.
```

### 8.2 The second mitigation

**Risk:** R1

The exact refactor prompt supplied by the assignment and handled in this session:

```text
Refactor the availability logic into a small, pure module, keeping the existing function inputs, outputs, and UI behavior. Use a pattern only if the identified design problem justifies it. Do not add new features or dependencies. Show the files you plan to edit before making changes.
```

Files changed: src/bookingRules.ts (new), src/booking.ts and src/availability.ts. No package was added. The R1 test was already present in the red-test commit. A separate before-edit file-list reply was not captured; the actual file list and complete diff are provided here rather than claiming that step occurred.

**Problem → pattern → benefit:** Duplicated interval, time, duration and overlap predicates had drifted between the Boolean decision and its explanations. Extracting a small pure module makes both callers use the same predicates, preserves canBook's public request/Boolean contract and finite-input UI messages, and corrects the demonstrated invalid-input explanation gap.

The first 29 tests pass before and after the extraction; the new R1 test intentionally goes from red to green. There is one intentional feedback correction for invalid numeric input, not a claim that every possible output was unchanged. The current UI time parser prevents that NaN input. The differential check in scripts/verify_refactor.cjs compares against the real checkpoint: 15,870 Boolean decisions match, fixtures remain unchanged, and 10,584 finite-input explanation results match (evidence/refactor-comparison.txt).

**What I rejected from the agent's patch, and why:** No Strategy or Adapter was added because there are no competing policies or data shapes. No unrelated variable rename, UI redesign, new package or feature was included. The stale mutation comment was removed because the new pure module does not update schedules. The assistant reviewed and applied this local diff under the task request; the student's own acceptance of this code diff remains pending.

The diff I approved (`git diff`), reviewed by the assistant; student review pending:

```diff
diff --git a/week-10/app/src/availability.ts b/week-10/app/src/availability.ts
index fc3a23b..5ca6e37 100644
--- a/week-10/app/src/availability.ts
+++ b/week-10/app/src/availability.ts
@@ -2,7 +2,11 @@ import type { Booking, Room } from './types';
 import {
   MINUTES_PER_DAY,
   MAX_BOOKING_MINUTES,
-} from './booking';
+  exceedsDuration,
+  isFutureStart,
+  isValidInterval,
+  overlaps,
+} from './bookingRules';
 
 export const MINUTES_PER_DAY_VALUE = MINUTES_PER_DAY;
 export const MAX_BOOKING_MINUTES_VALUE = MAX_BOOKING_MINUTES;
@@ -33,16 +37,6 @@ export function minutesToTime(min: number): string {
     .padStart(2, '0')}`;
 }
 
-/** Touching endpoints are not an overlap. */
-function overlaps(
-  aStart: number,
-  aEnd: number,
-  bStart: number,
-  bEnd: number,
-): boolean {
-  return aStart < bEnd && bStart < aEnd;
-}
-
 /**
  * Build validation messages for the page.
  * The availability decision itself is made by canBook.
@@ -56,11 +50,11 @@ export function getAvailabilityReasons(
 ): string[] {
   const reasons: string[] = [];
 
-  if (start < 0 || end > MINUTES_PER_DAY || start >= end) {
+  if (!isValidInterval(start, end)) {
     reasons.push('Interval must satisfy 0 ≤ start < end ≤ 1440 minutes.');
   }
 
-  if (start <= currentTimeMinutes) {
+  if (!isFutureStart(start, currentTimeMinutes)) {
     reasons.push(
       `Start time must be after the current time (${minutesToTime(
         currentTimeMinutes,
@@ -68,7 +62,7 @@ export function getAvailabilityReasons(
     );
   }
 
-  if (end - start > MAX_BOOKING_MINUTES) {
+  if (exceedsDuration(start, end)) {
     reasons.push(
       `Booking length is ${
         end - start
@@ -82,7 +76,7 @@ export function getAvailabilityReasons(
     reasons.push(`${room.name} is currently blocked and cannot be booked.`);
   }
 
-  if (room && start >= 0 && start < end && end <= MINUTES_PER_DAY) {
+  if (room && isValidInterval(start, end)) {
     const conflicts = bookings.filter(
       (booking) =>
         booking.roomId === room.id &&
@@ -99,4 +93,4 @@ export function getAvailabilityReasons(
   }
 
   return reasons;
-}
\ No newline at end of file
+}
diff --git a/week-10/app/src/booking.ts b/week-10/app/src/booking.ts
index 64e9a4b..028301b 100644
--- a/week-10/app/src/booking.ts
+++ b/week-10/app/src/booking.ts
@@ -1,33 +1,20 @@
-export const MINUTES_PER_DAY = 1440;
-export const MAX_BOOKING_MINUTES = 120;
+import {
+  exceedsDuration,
+  isFutureStart,
+  isValidInterval,
+  overlaps,
+  type BookingRequest,
+} from './bookingRules';
 
-type BookingInterval = {
-  start: number;
-  end: number;
-};
+export { MINUTES_PER_DAY, MAX_BOOKING_MINUTES } from './bookingRules';
 
-type BookingRequest = {
-  start: number;
-  end: number;
-  now: number;
-  blocked: boolean;
-  bookings: readonly BookingInterval[];
-};
-
-export function canBook({ start, end, now, blocked, bookings }: {
-  start: number;
-  end: number;
-  now: number;
-  blocked: boolean;
-  bookings: { start: number; end: number }[];
-}): boolean {
-  if (!(0 <= start && start < end && end <= 1440)) return false;
-  if (!(start > now)) return false;
-  if (end - start > 120) return false;
+export function canBook({ start, end, now, blocked, bookings }: BookingRequest): boolean {
+  if (!isValidInterval(start, end)) return false;
+  if (!isFutureStart(start, now)) return false;
+  if (exceedsDuration(start, end)) return false;
   if (blocked) return false;
   for (const b of bookings) {
-    if (start < b.end && end > b.start) return false;
+    if (overlaps(start, end, b.start, b.end)) return false;
   }
-  // keep the room's list current with the slot that was just found free
   return true;
 }
diff --git a/week-10/app/src/bookingRules.ts b/week-10/app/src/bookingRules.ts
new file mode 100644
index 0000000..df43958
--- /dev/null
+++ b/week-10/app/src/bookingRules.ts
@@ -0,0 +1,37 @@
+// Shared pure predicates: no clock, browser, state, or data mutation.
+export const MINUTES_PER_DAY = 1440;
+export const MAX_BOOKING_MINUTES = 120;
+
+export type BookingInterval = {
+  start: number;
+  end: number;
+};
+
+export type BookingRequest = {
+  start: number;
+  end: number;
+  now: number;
+  blocked: boolean;
+  bookings: readonly BookingInterval[];
+};
+
+export function isValidInterval(start: number, end: number): boolean {
+  return 0 <= start && start < end && end <= MINUTES_PER_DAY;
+}
+
+export function isFutureStart(start: number, now: number): boolean {
+  return start > now;
+}
+
+export function exceedsDuration(start: number, end: number): boolean {
+  return end - start > MAX_BOOKING_MINUTES;
+}
+
+export function overlaps(
+  start: number,
+  end: number,
+  bookingStart: number,
+  bookingEnd: number,
+): boolean {
+  return start < bookingEnd && end > bookingStart;
+}
```

Additional scope correction, commit 17f5dbd: R3's inherited five-room fixture was reduced to one fictional Demo Room and its unused second-room test fixture was removed. This changes scope deliberately and is not disguised as behavior-preserving refactoring. See evidence/R3-scope.diff. app/README.md and Week10.code-workspace document the actual commands and VS Code tasks.

### 8.3 The residual risk

| ID | L before | I before | Score before | L after | I after | Score after | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R2 | 3 | 3 | 9 | 1 | 3 | 3 | Student-approved minimal rules forbid the unsafe actions and name real commands; textual policy still cannot stop a human ignoring it. |
| R1 | 2 | 2 | 4 | 1 | 2 | 2 | Shared pure predicates, red-to-green regression, all 30 tests passing and differential comparison reduce drift likelihood. |
| R3 | 2 | 2 | 4 | 1 | 2 | 2 | Extra scope correction leaves one fictional room; the student-supplied desktop and mobile screenshots show that single Demo Room. |

R4 and R5 remain 4 each. R6 remains plausible at 2. The two submitted success views provide limited desktop/mobile feedback evidence; a timed stale-result check and broader browser/accessibility checks remain unrun. The student's NO-GO decision for a full release remains unchanged.

### 8.4 The final run

Full final suite after both required mitigations and the scope correction:

```text
npm warn Unknown env config "http-proxy". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 /workspace/scratch/425974ce3adc/project/week-10/app

 ✓ src/booking.test.ts > canBook — reviewed booking cases > R1 AC6: a rejected invalid interval has an explanation without mutating fixtures 5ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T01 AC4: allows touching after an existing booking 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T02 AC1: rejects a request starting exactly now 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T03 AC1: rejects zero duration 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T04 AC1: rejects an end before the start 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T05 AC1: rejects an end past minute 1440 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T06 AC2: allows exactly 120 minutes 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T07 AC2: rejects 121 minutes 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T08 AC4: allows touching before an existing booking 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T09 AC4: rejects a partial overlap 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T10 AC4: rejects a request containing an existing booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T11 AC4: rejects a request inside an existing booking 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T12 AC4: rejects an identical interval 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T13 AC3: rejects a blocked room for an otherwise valid request 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T14 AC4: allows a valid request when there are no existing bookings 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > AC5: repeated Available decisions preserve unsorted booking data 1ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > X1 AC1: allows an end exactly at minute 1440 4ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > X2 AC4: rejects an overlap with the second booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T15 AC1: rejects a request starting one minute before now 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T16 AC1: allows a request starting one minute after now 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T17 AC1: rejects a negative start minute 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T18 AC1: rejects minute zero when the supplied current time is zero 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T19 AC1: allows a one-minute booking just after midnight 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T20 AC4: rejects a one-minute overlap at the existing booking end 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T21 AC4: rejects a one-minute overlap at the existing booking start 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T22 AC4: rejects an earlier conflict despite a later nonconflicting booking 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T23 AC4: allows a gap touching both bookings in an unsorted schedule 4ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > T24 AC3: rejects a blocked room even with no existing bookings 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > BUG-A AC4: allows a gap touching two neighbours in a three-booking schedule 0ms
 ✓ src/booking.test.ts > canBook — reviewed booking cases > BUG-B AC5: a non-touching Available request leaves bookings unchanged 0ms

 Test Files  1 passed (1)
      Tests  30 passed (30)
   Start at  16:27:21
   Duration  438ms (tests 34%, import 33%, transform 24%, worker 8%)
```

Additional actual final checks: npm run typecheck, npm run lint and npm run build all passed. Full outputs are in evidence/final-typecheck.txt, evidence/final-lint.txt and evidence/final-build.txt. No CI execution is claimed.

## 9. Task 9, and what still fails



### 9.1 A background agent on this project

This is a thought experiment. No background agent was spawned or claimed to have run.

| Rule | What I require |
| --- | --- |
| Isolation | Use a separate worktree and branch based on week-10; never edit main or another student's working tree. |
| Permitted files | Edit only approved week-10/app/src files and their regression tests; update week-10/lab-report.md and evidence for the specific task. AGENTS.md requires separate approval. |
| Commands | In app run npm ci, npm test, npm run typecheck, npm run lint and npm run build; in week-10 run python tests/check_audit.py and python tests/validate_submission.py. |
| Prohibited actions | No credentials, real timetable data, new rooms, login/database, dependency additions, external deployment, force-push, test weakening or edits to provided checkers. |
| Required evidence | Attach the changed-file diff, full test output, typecheck/lint/build results, updated risk scores and a review note separating executed checks from unverified claims. |
| Before merging or deploying | Require explicit human review and passing checks before any merge; leave the course PR open until graded. External deployment remains forbidden in this task. |

### 9.2 Optional — the deck's checklist prompt (not graded)

Optional checklist prompt not sent separately. The six project-specific rules in 9.1 were prepared directly; no asynchronous agent execution is asserted.

### 9.3 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| none | The current audit reports 31 PASS / 0 FAIL / 0 ERROR. Both real UI screenshots are present. |

The student recorded a clean local audit after adding the screenshots and removing app/node_modules. The documentation update was checked again against the committed screenshots; evidence/checker-last.txt and evidence/validator-last.txt contain the actual latest runs. submission.yml declares no remaining failing checks. The student's independent claim and code-diff reviews still remain pending in AI_USAGE.md; the mechanical checker does not certify those actions. The exact five-section SETUP.md template was unavailable, as disclosed in section 1.

## 10. Release decision and conclusion

**Decision:** NO-GO

The paragraph below was supplied by the student in chat on 2026-11-23 and is preserved verbatim. Editorial risk references: R2 = AGENTS.md, R1 = pure module, R4 = CI, R5 = stale result. No independent AI-written conclusion is substituted.

<!-- Write your conclusion below this line -->

Я бы пока выбрал статус No-Go для полноценного выпуска. В проекте уже исправлены две важные проблемы: опасные правила в AGENTS.md изменены, а общие правила проверки бронирования вынесены в отдельный модуль. Теперь их проще поддерживать, и меньше вероятность, что проверка и сообщение пользователю будут противоречить друг другу. Но остаются вопросы, которые я считаю важными. В проекте нет CI, поэтому после изменений тесты нужно запускать вручную. Также результат проверки может устареть, если пользователь подождёт и время изменится. Для учебной демонстрации текущая версия подходит. Перед полноценным выпуском я бы добавил автоматический запуск тестов и повторную проверку доступности перед подтверждением бронирования. После этого можно снова оценить готовность проекта.

*Editorial reference labels: R2, R1, R4, R5.*

