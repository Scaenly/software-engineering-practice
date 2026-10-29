# AI Usage Disclosure — SIS #03

AI-integrated task, Level D. The following records what is supported by the work history. Edit to reflect every actual tool and exchange. The draft of this disclosure and the replacement report was generated with ChatGPT on 2026-10-29; this must not be hidden.

| Tool | Exact model / plan | Used for | Which files it touched | Reused from |
| --- | --- | --- | --- | --- |
| ChatGPT (web) | not displayed for historical sessions; GPT-6 for this draft if shown in UI | Plan, explanations, Python final code/test guidance and report drafting | `code/booking.py`, `code/test_booking.py`, `report.md`, `AI_USAGE.md` | week-05 + this SIS |
| Previous AI coding assistant (confirm) | not displayed | Original Python v1 | `code/original/booking_v1.py` (kept unedited) | week-05 |
| Bolt.new | not displayed | Original client-side prototype | `web/original/` | week-06 |
| ChatGPT (web) | not displayed | Critique, branch review and decisions | `report.md` sections 3, 8, 9 | this SIS |
| Bolt.new (confirm full agent transcripts) | not displayed | Targeted fixes to blocked-room feedback and UI cleanup | `web/final/src/components/RoomList.tsx`, `web/final/src/App.tsx` | week-06 |
| ChatGPT (web) | GPT-6 (check model display) | Drafting the report and disclosure using observed evidence, including assistance on Section 2 previously | `report.md`, `AI_USAGE.md`, proposed `submission.yml` | this SIS |

**The assistant wrote, or helped write, my tests in `code/`:** yes. ChatGPT supplied Python final code and a 30-test suite. The expected test outcomes were checked against AC1–AC5 and compared with `py tests/check_sis.py`, which reported 30 tests OK, and 10 mutation faults caught.

**`code/original/` and `web/original/` hold the AI's first versions exactly as returned:** verify before marking yes. They were copied from Week 05 and Week 06 respectively; they must remain unchanged.

**Every result in report.md section 5 was actually run or seen, not assumed:** verify personally before marking yes. The report flags T11 repetition and unmatched original-clock conditions.

**Everything I submitted, I can explain and defend in class — including the overlap condition and what the agent did in section 9:** verify personally before marking yes.

**Anything I accepted from the AI without fully understanding it:** Review the half-open overlap condition `start < booked_end and booked_start < end`, the fixed test clock `?test=1`, and generated React components; if understood, state so in your own words, otherwise name the specific question and file.

Signed: Yerassyl Arystanbek (confirm official registration form)
Date: 2026-10-29 (update to actual date signed)
