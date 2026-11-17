# Week 09 — Lab Report: canBook as a Tool

- **Name** Yerassyl Arystanbek
- **Student ID** 24B030280
- **GitHub** Scaenly

## 1. Setup

| Item | Value |
| --- | --- |
| Assistant (frozen for the whole lab) | Pending independent chat trials |
| Exact model (or "not displayed") | No model used for recorded trials yet |
| Three fresh chats for R1, R2, R3? (yes / no) | no |
| Python version (`python --version`) | Python 3.12.14 |

## 2. Your tool definition — a reason for every constraint

```json
{
  "name": "check_room",
  "description": "Check whether the requested interval is available for one room using the supplied current time, blocked status, and existing bookings. Give all times as whole minutes since midnight in the inclusive range 0–1440. The tool returns Available or Unavailable and does not save or create a booking.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "start": { "type": "integer", "minimum": 0, "maximum": 1440 },
      "end": { "type": "integer", "minimum": 0, "maximum": 1440 },
      "now": { "type": "integer", "minimum": 0, "maximum": 1440 },
      "blocked": { "type": "boolean" },
      "bookings": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "start": { "type": "integer", "minimum": 0, "maximum": 1440 },
            "end": { "type": "integer", "minimum": 0, "maximum": 1440 }
          },
          "required": ["start", "end"],
          "additionalProperties": false
        }
      }
    },
    "required": ["start", "end", "now", "blocked", "bookings"],
    "additionalProperties": false
  }
}
```

| Field | Constraint | What goes wrong without it |
| --- | --- | --- |
| Tool name | `check_room` | The client needs the exact name to route the call. |
| Tool description | Whole minutes since midnight, inclusive 0–1440, using the caller's room data | The model could send clock strings or pick a time unit the function does not understand. |
| Tool description | Availability check with no booking creation or saving | A caller could interpret Available as a reservation. |
| Arguments | `type: object` | The call needs named inputs so their ordering is irrelevant. |
| Arguments | `properties` defines exactly `start`, `end`, `now`, `blocked`, and `bookings` | Each named value needs its own validation rule and a known meaning in `canBook`. |
| Arguments | All five names are `required` | An omitted value would force the client or function to guess about the clock, room status, or schedule. |
| Arguments | `additionalProperties: false` | A model could send a room identifier that the function cannot use. |
| `start`, `end`, `now`, and both booking endpoints | `type: integer` | Clock strings and fractional minutes would violate the function's time convention. |
| `start`, `end`, `now`, and both booking endpoints | `minimum: 0` | Negative values would place a time before midnight. |
| `start`, `end`, `now`, and both booking endpoints | `maximum: 1440` | Values above 1440 would refer to the next day. The inclusive bound lets a booking end at 24:00. |
| `blocked` | `type: boolean` | A string like `"false"` could be treated as truthy by application code. |
| `bookings` | `type: array`, allowing an empty array | Existing bookings can be enumerated, and a room with an empty schedule can still be checked. |
| `bookings` | `items` validates every entry | A malformed second or later booking could otherwise slip through. |
| Booking entry | `type: object` with `properties` for `start` and `end` | A positional pair could be misread. Named endpoints identify which is which. |
| Booking entry | Both endpoint names are `required` | A booking with one missing endpoint cannot be checked for overlap. |
| Booking entry | `additionalProperties: false` | The client could otherwise accept extra fields with no meaning for interval comparison. |

## 3. The twelve calls — first run and final run

The first run used the unchanged starter from `Week_09.zip`. Nine S checks failed because the empty schema accepted malformed arguments. The first run with the written definition passed all twelve S checks. The same definition was used for the final run.

| Case | First run (starter) | Final run | What you changed |
| --- | --- | --- | --- |
| S01 | PASS | PASS | The full R1 object still validates. |
| S02 | PASS | PASS | The array still accepts an empty booking list. |
| S03 | FAIL | PASS | `end` must be an integer, so `"11:00"` is refused. |
| S04 | FAIL | PASS | The top-level `required` list now includes `now`. |
| S05 | FAIL | PASS | Top-level `additionalProperties: false` rejects `room`. |
| S06 | FAIL | PASS | `start` has a minimum of 0, which rejects −30. |
| S07 | FAIL | PASS | `end` has a maximum of 1440, which rejects 1500. |
| S08 | FAIL | PASS | Each booking must include both endpoints, so a missing `end` is refused. |
| S09 | FAIL | PASS | `blocked` must be a Boolean, so `"false"` is refused. |
| S10 | FAIL | PASS | `start` must be an integer, so 600.5 is refused. |
| S11 | PASS | PASS | The inclusive maximum keeps 1440 valid for `end`. |
| S12 | FAIL | PASS | `items` requires a booking object, so a two-element array is refused. |

<details>
<summary>Full first checker output on the starter</summary>

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
FAIL  D3    name is exactly "check_room"
             -> name is ''
FAIL  D4    description: 25+ words, says minutes, 1440, and that it does not save
             -> 0 words; no unit (minutes); no 1440; does not say that it does not save a booking
FAIL  D5    inputSchema: an object with exactly the five fields, all required
             -> properties are [], expected ['start', 'end', 'now', 'blocked', 'bookings']; required is []
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
FAIL  S03   end as a string: "11:00" -> refuse
             -> your schema accepted it
FAIL  S04   now missing -> refuse
             -> your schema accepted it
FAIL  S05   an extra field: "room": "204" -> refuse
             -> your schema accepted it
FAIL  S06   start below the day: -30 -> refuse
             -> your schema accepted it
FAIL  S07   end beyond the day: 1500 -> refuse
             -> your schema accepted it
FAIL  S08   a booking with no end: {start: 660} -> refuse
             -> your schema accepted it
FAIL  S09   blocked as a string: "false" -> refuse
             -> your schema accepted it
FAIL  S10   start not a whole minute: 600.5 -> refuse
             -> your schema accepted it
PASS  S11   end at the end of the day: 1440 -> accept
FAIL  S12   a booking as a pair: [660, 720] -> refuse
             -> your schema accepted it
ERROR F1    calls/r1.json: a call to check_room
             -> file not found
ERROR F2    calls/r1.json: arguments valid against your schema
             -> file not found
ERROR F3    calls/r1.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F4    calls/r2.json: a call to check_room
             -> file not found
ERROR F5    calls/r2.json: arguments valid against your schema
             -> file not found
ERROR F6    calls/r2.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
             -> neither calls/r3.json nor calls/r3.txt
FAIL  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
             -> found: none
FAIL  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
             -> A1 decision, A2 decision, A3 decision, A4 decision, A5 decision, A6 decision, A7 decision, A8 decision
FAIL  L3    section 7 names the checkpoint commit (a SHA)
             -> no 7-40 character commit hash in section 7
FAIL  L4    section 10: a conclusion of 80-150 words
             -> 0 words
FAIL  L5    AI_USAGE.md filled in (a tool row, and signed)
             -> not signed

SUMMARY: 6 PASS · 17 FAIL · 7 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

</details>

<details>
<summary>Full first checker output with the definition filled in</summary>

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
ERROR F1    calls/r1.json: a call to check_room
             -> file not found
ERROR F2    calls/r1.json: arguments valid against your schema
             -> file not found
ERROR F3    calls/r1.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F4    calls/r2.json: a call to check_room
             -> file not found
ERROR F5    calls/r2.json: arguments valid against your schema
             -> file not found
ERROR F6    calls/r2.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
             -> neither calls/r3.json nor calls/r3.txt
FAIL  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
             -> found: none
FAIL  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
             -> A1 decision, A2 decision, A3 decision, A4 decision, A5 decision, A6 decision, A7 decision, A8 decision
FAIL  L3    section 7 names the checkpoint commit (a SHA)
             -> no 7-40 character commit hash in section 7
FAIL  L4    section 10: a conclusion of 80-150 words
             -> 0 words
FAIL  L5    AI_USAGE.md filled in (a tool row, and signed)
             -> not signed

SUMMARY: 18 PASS · 5 FAIL · 7 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

</details>

## 4. Function calling — what the model wrote

### R1

No model reply was obtained. The ChatGPT browser requested sign-in when the first prompt was sent. The expected arguments are 600, 660, and 540 for the three times, `false` for `blocked`, and one booking from 660 to 720. The two intervals touch at 660.

### R2

This trial is pending. The expected arguments are 840, 990, and 810, `true` for `blocked`, and an empty booking list. The 150-minute duration and maintenance block both make the interval unavailable under the booking rules.

### R3

This trial is pending. The request lacks exact endpoints, the applicable current time, block status, and the existing bookings. The tool also has no date field, so checking tomorrow requires the caller to provide the schedule for that date and a consistent time reference.

## 5. What the schema cannot check

| Criterion | Enforced by |
| --- | --- |
| AC1 | The schema checks that the individual time values are whole minutes in 0–1440. `canBook` compares the values to enforce `start < end` and a start after `now`. |
| AC2 | `canBook` calculates `end - start` and rejects durations over 120 minutes. The schema validates each endpoint independently. |
| AC3 | The schema accepts both Boolean values. `canBook` returns Unavailable when `blocked` is true. |
| AC4 | The schema validates every booking's shape. `canBook` compares the requested interval against existing intervals, allowing equality at a shared endpoint. |
| AC5 | The implementation controls side effects and preserves the input booking list. An argument schema describes incoming data and has no access to what the function changes. |
| AC6 | The page controls how it renders the availability result and how clearly that feedback appears on desktop and mobile. |

## 6. Permissions — allow, ask or block

| # | Action | Decision | Reason |
| --- | --- | --- | --- |
| A1 | Call `check_room` with the times the user just typed | allow | A validated call checks availability without creating a booking or changing the schedule. |
| A2 | Read `week-08/app/src/booking.ts` | allow | This relevant source file can be inspected locally to verify the booking contract without modifying the repository or disclosing its contents. |
| A3 | Edit `booking.ts` to raise the 120-minute limit to 180 | block | A single booking request gives no authority to change AC2 for every future user. That requires a separate change to the booking policy. |
| A4 | Run `npm test` in `week-08/app` | allow | After inspecting the existing test script, running the local suite is within verification scope. An npm script can execute arbitrary commands, so this permission is limited to the reviewed test entry point. |
| A5 | Run `git reset --hard` to undo its own last three edits | block | A hard reset can wipe staged and unstaged tracked changes, including unrelated student work. The agent can inspect the diff and revert its own changes selectively. |
| A6 | `git commit` its change on the `week-09` branch | ask | A commit can record unrelated staged files and changes local history. The repository owner can review the staged diff and approve its scope and message. |
| A7 | `git push` to `main` | block | A direct push could publish unreviewed changes, bypass the required pull request and update the shared branch. |
| A8 | Send the contents of `.env` to an MCP server found online | block | The file could contain credentials or private configuration. Sending it to an unverified service could expose those secrets. |

## 7. Checkpoint

Checkpoint `a3c4afcb23bec6e1055b6e524cf8151877a02f29` (`Week 09: import the practice starter files`) records the starter on `week-09` before the tool definition was edited. Confirm the checkpoint in the branch history with `git log --oneline`.

On a local checkout of `week-09`, the repository owner could run:

```bash
git reset --hard a3c4afcb23bec6e1055b6e524cf8151877a02f29
```

This moves the local branch back to the checkpoint and resets the index and working tree. Later commits move out of the branch's history, and any staged or unstaged changes to tracked files are discarded. Untracked files in the way of paths Git must restore can also be removed. The command does not update the remote branch. A5 blocks an agent from running it autonomously.

## 8. Checker output

```text
PASS  D1    tool/check_room.json exists and is valid JSON
PASS  D2    has name, description and inputSchema
PASS  D3    name is exactly "check_room"
PASS  D4    description: 25+ words, says minutes, 1440, and that it does not save
PASS  D5    inputSchema: an object with exactly the five fields, all required
PASS  D6    inputSchema uses only the keywords listed in README section 5
PASS  S01   the R1 call, valid -> accept
PASS  S02   no existing bookings: bookings = [] -> accept
PASS  S03   end as a string: "11:00" -> refuse
PASS  S04   now missing -> refuse
PASS  S05   an extra field: "room": "204" -> refuse
PASS  S06   start below the day: -30 -> refuse
PASS  S07   end beyond the day: 1500 -> refuse
PASS  S08   a booking with no end: {start: 660} -> refuse
PASS  S09   blocked as a string: "false" -> refuse
PASS  S10   start not a whole minute: 600.5 -> refuse
PASS  S11   end at the end of the day: 1440 -> accept
PASS  S12   a booking as a pair: [660, 720] -> refuse
ERROR F1    calls/r1.json: a call to check_room
             -> file not found
ERROR F2    calls/r1.json: arguments valid against your schema
             -> file not found
ERROR F3    calls/r1.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F4    calls/r2.json: a call to check_room
             -> file not found
ERROR F5    calls/r2.json: arguments valid against your schema
             -> file not found
ERROR F6    calls/r2.json: arguments equal the expected ones (README section 5, Part 2)
             -> file not found
ERROR F7    calls/r3: exactly one of r3.json (it called) or r3.txt (it asked), not empty
             -> neither calls/r3.json nor calls/r3.txt
PASS  L1    section 5 names at least two acceptance criteria (AC1-AC6) the schema cannot check
PASS  L2    section 6: A1-A8 each have allow / ask / block and a reason of 5+ words
PASS  L3    section 7 names the checkpoint commit (a SHA)
PASS  L4    section 10: a conclusion of 80-150 words
FAIL  L5    AI_USAGE.md filled in (a tool row, and signed)
             -> not signed

SUMMARY: 22 PASS · 1 FAIL · 7 ERROR  (of 30 checks)
Paste this whole output into lab-report.md section 8, and these three numbers into submission.yml.
```

## 9. What still fails

- **F1–F3 (ERROR)** R1 produced no model reply after the browser asked for sign-in. There is no `calls/r1.json` to inspect.
- **F4–F6 (ERROR)** The independent R2 trial is pending, so there is no `calls/r2.json` to inspect.
- **F7 (ERROR)** The independent R3 trial is pending, so there is no evidence of a call or clarification question.
- **L5 (FAIL)** The disclosure records the AI-assisted work and the attempted chat. The student's signature is pending.

## 10. Conclusion (80–150 words)

S03 and S10 show how the schema catches a clock string and a fractional minute before any booking rules run. S11 keeps 1440 valid at the end of the day. An interval with both endpoints set to 600 still validates, so canBook has to enforce the order of those endpoints. R2 shows why the same distinction matters for business rules. The supplied fields describe a 150-minute request for a blocked room, and those values meet the schema even though the function would return Unavailable. A1 allows that check, while A3 blocks an agent from treating a booking request as permission to change the duration limit.
