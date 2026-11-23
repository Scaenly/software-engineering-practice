# SIS #04 — Report: Evolving the Smart Campus Room Availability Checker

## 1. Setup and starting point

| Item | Value |
| --- | --- |
| Assistant (tool) | ChatGPT Work / Codex |
| Assistant model | GPT-6 |
| Starting point | week-08 |
| Baseline commit | 039c22ce703a858362c23ce2a6bded1fd3af5d9f |
| Language (ts or js) | ts |
| Vitest version | 5.1.0 |
| Where I ran the tests | Codex Linux workspace, Node 24.22.3, npm 11.19.1 |

The source is Week 08 at c10411c13a437464cb0dad3ba86eb842c4708255.
The baseline app tree is byte-for-byte identical: `git diff origin/week-08:week-08/app 039c22c:sis-04/app` produced no output.
The session identifies the assistant as GPT-6; no more specific model snapshot was shown.
Tests and shell checks were run by the assistant in this workspace, not personally by the student.

### 1.1 Baseline run

Command from app/: `npx vitest run`. Unedited combined terminal output:

```text
npm warn Unknown env config "http-proxy". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 /workspace/scratch/8806a2606eda/repo/sis-04/app


 Test Files  1 passed (1)
      Tests  29 passed (29)
   Start at  17:44:04
   Duration  632ms (transform 66%, import 16%, tests 13%, worker 5%)

```

## 2. Context for the assistant

### 2.1 Repository map

The assistant obtained this map by reading the unchanged Week 08 source.

```text
src/App.tsx — form, clock, test bookings and result state.
src/sampleData.ts — five rooms and six separate global bookings.
src/types.ts — Room, Booking and AvailabilityResult types.
src/booking.ts — canBook; strict overlap, future start, 120-minute limit.
src/availability.ts — time conversion and a second set of rule checks for reasons.
src/components/RoomList.tsx — room buttons and schedule rendering.
src/booking.test.ts — 29 inherited Vitest regression tests.
```

### 2.2 The context message as sent

The actual initial request was the assignment plus the two attachments. The following is an
explicitly marked excerpt of that user message; it is not a manufactured analysis prompt.

```text
Smart Campus Room Availability Checker: extend your working app with a room

catalog and filters, refactor it into clear modules, keep AC1-AC6, and prove it

with tests and measured evidence. The report is Markdown in your repository

(sis-04/report.md). The PR link pasted here is the submission. No file uploads,

no e-mail. This is NOT Practice #08 again: no planted bugs, no new SKILL.md.
[…]
2\. Feature: 4+ fictional rooms (id, name, capacity, equipment, blocked,

   bookings) in src/rooms; filterRooms in src/filter (F1 capacity >=

   attendees, F2 ALL selected equipment); checkRoom in src/booking (F3 blocked

   never available, F5 the chosen room's own bookings); F4 empty state.

   Five screenshots in evidence/.
```

The assistant built the map by reading the repository; the user did not send a separate
fresh-chat message containing that map. This process difference is disclosed. The attached
README/handout supplied the full AC1–AC6 and F1–F5 meanings and the constraints: fictional data
only; no login, payments, live APIs or database. Section 8 preserves the later actual requests.

## 3. Codebase analysis (Task 1)

### 3.1 Maintainability risks

| # | Risk | Where (file / function) | Evidence | Priority |
| --- | --- | --- | --- | --- |
| 1 | Two implementations can disagree | `src/availability.ts`, `getAvailabilityReasons()`; `src/booking.ts`, `canBook()` | Both check time order, now, duration, blocked and overlap; direct source inspection confirmed five repeated rule locations. | High |
| 2 | A result can describe the previous room | `src/App.tsx`, room selection | `onSelect={setSelectedRoomId}` changes the room without clearing `result`; only time input handlers clear it. | High |
| 3 | Catalog lacks required room-owned data | `src/sampleData.ts`; `src/types.ts`, `Room` | Room has no equipment/bookings fields. Six global bookings use roomId; App filters and groups them separately. F2/F5 need one consistent owner. | High |
| 4 | Nondeterministic demo and inline fixtures | `src/App.tsx`, `useNowMinutes()` and bookings initializer | Clock depends on Date unless ?test=1; test bookings are hardcoded inside the UI. This makes screenshots and rule ownership harder to review. | Medium |

### 3.2 Improvement plan — before editing

1. Preserve the 29-test baseline and keep canBook behaviour. Add required B1–B4 IDs to existing boundary tests.
2. Add a fixed independent test catalog and failing F1/F2/B5/B6 tests, then implement rooms.ts and filter.ts.
3. Add failing F3/F5/INT tests, then checkRoom(rooms, roomId, request), using the chosen room only.
4. Move room-owned bookings and equipment into rooms.ts; remove the duplicated validation messages and obsolete global booking data. Keep time formatting separate.
5. Adapt the existing RoomList and form in small patches, add filter controls and empty feedback, and refresh the result when selection changes.
6. Run the complete suite after each step; typecheck, lint, build and exercise the actual page. Capture five screenshots, compare measured quality and prepare an open PR.
7. Ask the student for the independent reflection and review; disclose any unfinished personal work instead of filling it with assistant prose.

### 3.3 One AI suggestion I rejected or modified

| Suggestion (as the assistant made it) | Decision | Why — with the AC, F-rule, test or file behind it |
| --- | --- | --- |
| “prepare the sis-04 branch with checks and an open PR” (initial assistant response) | Modified | Prepare an open draft PR while the student reflection and personal review remain incomplete. The handout requires section 10 in the student's own words, so an assistant draft cannot satisfy it. |

## 4. Feature extension (Task 2)

### 4.1 What I added

Five fictional rooms now contain id, name, capacity, equipment, blocked and their own bookings.
The existing names/buildings and six fictional bookings were retained and regrouped by room.
Attendees must be a positive integer. Capacity uses >=; every selected equipment item must be present.
Blocked rooms remain visible with their label. `checkRoom` finds the chosen room and delegates to
`canBook`; unknown IDs return false. No login, payment, API, database, network or storage was added.

The empty state says “No rooms match” and suggests reducing attendees or equipment.
The check button is disabled without a matching room. After submitting, switching rooms immediately
recomputes feedback for the current selection. Editing filters or times clears the prior feedback.
The clock is fixed at 09:00, visibly labelled as a demo. All checks are read-only.

### 4.2 Demonstration

These are the scenarios implemented by `tests/browser-smoke.cjs`, not claimed screenshots.
None of the five PNGs exists yet. The launch failure is retained in `evidence/browser-checks.txt`.
The local Vite server works on 127.0.0.1; Chromium launch failed with a socket permission error.
A separate cloud browser could not connect to that local server. No screenshot or successful browser run is fabricated.

| Screenshot | What it shows |
| --- | --- |
| `evidence/filter-match.png` | Pending capture: 24 attendees plus projector and whiteboard; Thesis Hall and Innovation Lab match. |
| `evidence/filter-empty.png` | Pending capture: 300 attendees; No rooms match; check button disabled. |
| `evidence/switch-a.png` | Pending capture: one attendee, no equipment, Thesis Hall, 10:00–11:00, Available. |
| `evidence/switch-b.png` | Pending capture: same times, Innovation Lab, Unavailable because of its 10:00–11:30 booking. |
| `evidence/narrow.png` | Pending capture: 390px portrait, eight attendees and whiteboard, form and result visible. |

jsdom UI tests verify F3/F4/F5 behaviour but do not prove responsive layout or replace screenshots.
Run `npm run dev -- --host 127.0.0.1 --port 5173 --strictPort` in app/, then in a second terminal:
`npx playwright install chromium` and `npm run evidence`. Update this table only after actual captures.

## 5. Refactoring (Task 3)

### 5.1 Module responsibilities after

| Module or component | Responsibility |
| --- | --- |
| `src/rooms.ts` | Room type, five complete room records, equipment options and fixed demo clock. |
| `src/booking.ts` | Original canBook decisions and checkRoom selecting the room's blocked/bookings data. |
| `src/filter.ts` | Pure capacity and all-equipment filtering; invalid attendee input yields an empty list. |
| `src/App.tsx` | Form state, filtered selection and derived availability; imports both rule functions. |
| `src/components/RoomFilters.tsx` | Accessible attendee and equipment inputs; reports changes through callbacks. |
| `src/components/RoomList.tsx` | Renders room buttons, equipment, blocked labels and each room's schedule. |
| `src/availability.ts` | Time parsing/formatting only; minute 1440 displays as 24:00. |

`sampleData.ts` and `types.ts` were removed after moving their active responsibilities.
Both PlantUML diagrams show the actual module dependencies. No new SKILL.md was created.

### 5.2 Design decisions

| Decision | Alternative I did not take | Why |
| --- | --- | --- |
| Store bookings directly on each room; checkRoom takes catalog, id and request. | Retain a global booking list and filter/group it again in App. | F5 needs the selected room's own bookings; C08 changes only the ID and asserts opposite results. This also removes the risk of two inconsistent associations. |
| Derive feedback from current selected room and submitted form state. | Store a Boolean result unrelated to later room changes. | UI01 detects the stale-result defect: one click on Beta must change Available to Unavailable without another submit. |
| Keep blocked rooms visible with a Blocked label. | Remove every blocked room during filtering. | F1/F2 describe capacity and equipment, while F3 belongs to availability. C14 proves matching a filter never overrides the block. |
| Remove the duplicated reason engine and show a result, room, times, schedule and rule guidance. | Maintain detailed explanatory checks separately from canBook. | The five parallel rule locations in risk 1 could disagree. This reduces explanation specificity but preserves one Boolean decision source and all regression outcomes. |

### 5.3 Duplication removed

Each row is one repeated rule location in the baseline message engine, not a measured complexity score.

| Before (file / function, what was repeated) | After (where it lives now) |
| --- | --- |
| `availability.ts/getAvailabilityReasons()`: time bounds and start/end order duplicated canBook. | `booking.ts/canBook()` is the only decision implementation. |
| `availability.ts/getAvailabilityReasons()`: start <= current time duplicated canBook. | `booking.ts/canBook()` future-start check. |
| `availability.ts/getAvailabilityReasons()`: duration > 120 duplicated canBook. | `booking.ts/canBook()` maximum-duration check. |
| `availability.ts/getAvailabilityReasons()`: blocked flag duplicated canBook. | `booking.ts/canBook()` blocked check, supplied by checkRoom. |
| `availability.ts/overlaps()` and its conflict filter duplicated canBook overlap logic. | `booking.ts/canBook()` strict overlap loop. |

The full `canBook` decision body was retained, apart from deleting a misleading old comment.
Unused type aliases were removed. Its original 29 cases still pass.

## 6. Automated tests (Task 4)

### 6.1 Test plan

Expected values were specified from the handout before implementing the new functions.
The inherited suite remains 29 cases; catalog.test.ts adds 14 and App.test.tsx adds three.
Every new suite uses a fixed catalog defined inside the test file. No real rule is mocked.

| ID | Test title (as in the file) | Input → expected |
| --- | --- | --- |
| AC1 | T02 AC1: rejects a request starting exactly now | start=now=540 → false. Other original cases cover reversed and out-of-day intervals. |
| AC2 | T06 B1 AC2: allows exactly 120 minutes | 720–840, now=540 → true. |
| AC3 | T13 AC3: rejects a blocked room for an otherwise valid request | otherwise valid request, blocked=true → false. |
| AC4 | T01 B3 AC4: allows touching after an existing booking | 660–720 next to 600–660 → true. |
| AC5 | C10 AC5: filtering and checking leave the complete catalog unchanged | Repeated successful checks → true; original catalog, request and criteria deep-equal saved copies. |
| F1 | C01 F1 B5: capacity equal to attendees is included | attendees=8 → a, b, d; a has eight seats. |
| F2 | C03 F2: all selected equipment is required | projector + whiteboard → a and d, excluding b with projector alone. |
| F3 | C07 F3 AC3: a blocked room is never available | blocked c, 660–720 → false. |
| F4 | C05 F4: impossible capacity gives the empty-state input | attendees=21 → empty array; UI02 checks the actual message/button. |
| F5 | C08 F5: switching room uses its own bookings at identical times | 600–630, a → false, b → true. UI01 checks immediate feedback refresh. |
| B1 | T06 B1 AC2: allows exactly 120 minutes | 720–840 → true. |
| B2 | T07 B2 AC2: rejects 121 minutes | 720–841 → false. |
| B3 | T01 B3 AC4: allows touching after an existing booking | 660–720 next to 600–660 → true. |
| B4 | T09 B4 AC4: rejects a partial overlap | 630–690 overlapping 600–660 → false. |
| B5 | C01 F1 B5: capacity equal to attendees is included | eight seats, eight attendees → included. |
| B6 | C02 F1 B6: capacity one below attendees is excluded | seven seats, eight attendees → excluded. |
| INT | C11 INT: check a room returned by the combined filter | nine attendees + projector/whiteboard → d; 600–630 → true. |

### 6.2 Commands

From app/, actual commands (their combined outputs are kept in evidence/):

```text
npm install --ignore-scripts --no-audit --no-fund
npx vitest run
npm install -D @testing-library/react@16.3.0 jsdom@26.1.0 playwright@1.56.1 --ignore-scripts --no-audit --no-fund
npx vitest run
npm run typecheck
npm run lint
npm run build
```

The filter step first failed to import the missing module, then passed 35/35.
The checkRoom step first failed six assertions because checkRoom did not exist, then passed 43/43.
These are the unedited filter-red/green and check-room-red/green logs in evidence/.
The final run below adds the three rendered UI cases. Typecheck, lint and build also exited 0.
Dependencies were subsequently moved outside app/ and generated dist removed for the source-only checker.

### 6.3 Final run

Unedited combined terminal output from `npx vitest run`:

```text
npm warn Unknown env config "http-proxy". This will stop working in the next major version of npm. See `npm help npmrc` for supported config options.

 RUN  v5.1.0 /workspace/scratch/8806a2606eda/repo/sis-04/app


 Test Files  3 passed (3)
      Tests  46 passed (46)
   Start at  17:55:38
   Duration  1.97s (tests 30%, environment 28%, transform 24%, import 16%, worker 1%)

```

## 7. Quality evaluation (Task 5)

| Measure | Original | Final | How I obtained it |
| --- | --- | --- | --- |
| Automated tests passed / total | 29/29 | 46/46 | The Tests lines in the unedited runs in sections 1.1 and 6.3; 29 + 14 + 3 literal test declarations in the three files. |
| Duplicated logic locations removed | 0 removed; five repeated rule locations present | 5 removed; no second validation engine | Compare baseline availability.ts/getAvailabilityReasons and overlaps with final source; the five located rows in 5.3 define the count. |
| Code structure: modules and their responsibilities | App mixes clock/fixtures/selection; sampleData and types hold separate rooms/bookings; availability repeats rules | rooms owns complete records; filter selects; booking decides; UI composes; availability formats | `git ls-tree -r --name-only 039c22c sis-04/app/src` and `git ls-files sis-04/app/src`, saved in structure-before-after.txt, then read the files against 5.1. |
| Remaining limitation | Live clock or hidden test mode; no capacity/equipment filter | Fixed 09:00 demo, no real booking writes; generic rejection guidance; mobile screenshots unverified | Inspect DEMO_NOW and the read-only API; C10 verifies immutability. Browser launch log explains missing visual verification. This is a deterministic demo, not a production booking service. |

No maintainability percentage, timing improvement, complexity or coverage metric is claimed.

## 8. AI evidence appendix

This is a continuing chat, not three fresh chats. The assistant drafted this report and ran the
checks. The replies below are the actual user messages and recorded assistant responses; brief
prompts selected a detailed question already presented by the assistant. They are not invented
long prompts attributed to the student. Personal review is still pending.

### 8.1 Exchange 1

**Tool and model:** ChatGPT Work / Codex, GPT-6
**Date:** 2026-11-23
**Purpose:** Inspect the provided assignment and Week 08 repository before changes.

**Prompt:**

```text
Excerpt of the actual initial user assignment message (omissions marked):
Smart Campus Room Availability Checker: extend your working app with a room

catalog and filters, refactor it into clear modules, keep AC1-AC6, and prove it

with tests and measured evidence. The report is Markdown in your repository

(sis-04/report.md). The PR link pasted here is the submission. No file uploads,

no e-mail. This is NOT Practice #08 again: no planted bugs, no new SKILL.md.
[…]
```

**Output used:**

```text
Исходная версия Week 08 прошла все 29 тестов. Нашёл три конкретные проблемы для доработки: правила доступности повторяются в двух файлах, бронирования хранятся отдельно от комнат, а смена комнаты оставляет на экране старый результат.

Сохраню сначала неизменённую версию, затем отдельным коммитом — анализ и план. После этого добавлю каталог и фильтры небольшими шагами.
```

**Problems found:** The user supplied the assignment, not a fresh standalone context containing a repository map. No retrospective map prompt has been invented. The initial assistant statement about preparing an open PR needed qualification while personal work remains pending.
**Changes made:** Read real sources, retained the unchanged baseline, recorded four located risks and the plan before any source edits; prepare an open draft PR.
**Verified by:** Empty git diff between baseline app tree and Week 08 app tree; evidence/baseline-run.txt, 29/29; the analysis commit precedes the first app/src change.

### 8.2 Exchange 2

**Tool and model:** ChatGPT Work / Codex, GPT-6
**Date:** 2026-11-23
**Purpose:** Choose the small-step plan before implementation.

**Prompt:**

```text
Assistant question shown to the user:
Для отчёта нужны настоящие сообщения твоего диалога с ИИ. Сейчас обнаружены риски Week 08: правила повторяются в booking.ts и availability.ts; данные комнат и бронирований хранятся отдельно в sampleData.ts; при смене комнаты App.tsx сохраняет старый результат. Что разобрать первым? Твой ответ запишу как реальный запрос для раздела 8.
Option 1: Составь небольшой план исправлений с сохранением AC1–AC6 и добавлением F1–F5.

Exact user reply:
1
```

**Output used:**

```text
План такой:
1. Сохранить canBook и все 29 исходных тестов.
2. Добавить комнаты с собственными бронированиями, затем тесты границ вместимости и правила «всё выбранное оборудование».
3. Добавить checkRoom, который передаёт в canBook данные выбранной комнаты.
4. Убрать повторение правил и подключить фильтры к интерфейсу.
5. Проверить смену комнаты, пустой список и мобильный экран; сохранить вывод тестов и пять скриншотов.

Заблокированные комнаты оставлю видимыми с пометкой Blocked: так пользователь увидит причину недоступности, а F3 проверит запрет.
```

**Problems found:** No incorrect boundary expectation was observed. The proposed screenshot step was later blocked by the execution environment; it could not be claimed completed.
**Changes made:** Implemented the plan in separate catalog, checkRoom and UI/refactoring commits. Removed unused aliases and a misleading comment without changing canBook decisions. Kept blocked rooms visible.
**Verified by:** filter-red.txt → filter-green.txt (35/35); check-room-red.txt → check-room-green.txt (43/43); final-run.txt (46/46); C14 checks that filter matches cannot override blocking.

### 8.3 Exchange 3

**Tool and model:** ChatGPT Work / Codex, GPT-6
**Date:** 2026-11-23
**Purpose:** Select and explain requirement/boundary tests, including room-owned bookings.

**Prompt:**

```text
Assistant question shown to the user:
Перед реализацией выбери следующий запрос для отчёта. Я предлагаю сохранить исходный canBook, проверять вместимость через >=, оборудование через every(), а смену комнаты — на одинаковом интервале с разными бронированиями. Какую проверку разобрать подробнее?
Option 1: Покажи тесты F1–F5 и границ B1–B6, объясни ожидаемые результаты.
Option 2: Объясни checkRoom и тест, который обнаружит использование бронирований другой комнаты.

Exact user reply:
лучше какой выбрать ?
```

**Output used:**

```text
Лучше первый вариант — тесты F1–F5 и B1–B6. Он охватывает больше требований и пригодится на защите. В него включу и проверку checkRoom: при одинаковом времени одна комната должна вернуть Unavailable, а другая — Available, исходя из их собственных бронирований. Продолжаю с этим вариантом.
```

**Problems found:** A Boolean helper test alone would not catch stale displayed feedback. The original page stored result separately from room selection. Browser capture failed, so no visual result was accepted as evidence.
**Changes made:** Added C08 with opposite decisions for the same interval, C10 immutability and C11 integration. Added UI01 to render the real component with independent fixtures and change rooms without resubmitting; added UI02/UI03 for empty/blocked behaviour.
**Verified by:** Section 6.1 maps all required IDs to literal test titles; the final 46/46 run includes three rendered UI cases, with real rules and no mocks. Typecheck, lint and build exited 0.

## 9. Checker results and known fails

The following work remains incomplete and is deliberately disclosed. The final exact checker
counts and commit are recorded in submission.yml and evidence/checker-run.txt.

| Check | Why it still fails |
| --- | --- |
| E1 | filter-match.png and filter-empty.png do not exist; browser capture was blocked. |
| E2 | switch-a.png and switch-b.png do not exist; browser capture was blocked. |
| E3 | narrow.png does not exist; portrait layout has not been visually verified. |
| L10 | The student's independent 200–300 word reflection has not been supplied. |

Workflow limitations: the initial context was an assignment message in a continuing chat, not
an independently composed fresh-chat map/context. AI wrote the technical report and code;
the student has not yet personally confirmed understanding, source review or active time.
The screenshot runner is provided for local completion. SETUP.md was absent from the supplied
archive and repository, so the PR follows the five headings stated in README section 14 and
previous course PRs. Keep the PR draft and open until personal work and evidence are complete.

## 10. AI reflection (Task 6)

Awaiting the student's own 200–300 words. The assistant has asked for the five required topics
and has not generated or signed a reflection on the student's behalf.
