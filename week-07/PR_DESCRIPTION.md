## What I built

Continued the Week 06 Smart Campus prototype and extracted the page's booking decision into canBook. Preserved the first 17-test Vitest suite, reviewed and improved it to 27 tests, and recorded real runs plus five UI screenshots. All three specified mutants were detected and the correct implementation was restored before the final 27/27 run.

## AI tools used

ChatGPT assisted extraction, the test plan including suggested X1/X2, test generation and review, the mutation runner, and report drafting. Exact model versions were not displayed in the supplied records. Contributions are disclosed in week-07/AI_USAGE.md; the personal conclusion and self-assessment require the student's own completion.

## What the AI got wrong

No incorrect Boolean expectations were found in the first suite. Its dedicated AC5 test duplicated T01 and did not exercise unsorted data or repeated successful calls. The improved suite strengthened AC5 and added ten boundary/state cases. The first run passed 17/17; the restored final run passed 27/27; real mutation trials detected M1, M2 and M3. A visible 00:00–00:00 end-of-day label issue remains documented.

## Time spent

Manual: not recorded in the supplied evidence · AI-assisted: not recorded in the supplied evidence.

Replace the preceding line with your honest estimates in minutes if available; no duration has been invented for this draft.

## What I would do differently

Plan additional booking orders and small boundary cases before requesting generated tests, and capture the entire mobile form together with the room schedule. Define a policy for malformed existing bookings before adding tests for that behaviour.
