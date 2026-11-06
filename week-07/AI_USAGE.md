AI Usage Disclosure — Week 07
Required by the course academic policy (Generative AI use level D — AI-integrated).
Tool	Exact model / plan	Used for	Which files it touched
ChatGPT — separate generation conversation	not displayed	First 17-test suite using the required prompt, attached ACs, plan and real module	suites/first/booking.test.ts; initial app/src/booking.test.ts
ChatGPT — same test-generation conversation	not displayed	Required improvement prompt using the real 17-pass run; strengthened AC5 and added T15–T24	app/src/booking.test.ts
ChatGPT — guided project conversation	not displayed	Extract canBook, preserve page feedback and connect the real function to the page	app/src/booking.ts; app/src/availability.ts; app/src/App.tsx
ChatGPT — guided project conversation	not displayed	Draft section 3 reasons and suggest X1/X2; assist review before the first run; inspect supplied UI screenshots; draft sections 1–9 and declaration/PR material from actual evidence	lab-report.md; AI_USAGE.md; submission.yml; PR_DESCRIPTION.md
ChatGPT — guided project conversation	not displayed	Write the automated one-at-a-time mutation runner and the declaration synchronizer	run_mutants.py; sync_submission.py


I used an assistant to extract canBook (Task 1), or to fix a defect in it: yes.

ChatGPT helped move the existing decision into app/src/booking.ts and connect App.tsx to it. Existing comparisons were preserved. The build and typecheck passed; manual 11:00–12:00 and 10:30–11:30 checks matched the earlier behaviour. No implementation fix was made merely to satisfy a test. The deliberate defects were temporary and restored.

I used another assistant as well: yes — a separate ChatGPT conversation generated and improved the tests, while this conversation assisted extraction, planning, review, tooling and report drafting. Exact model versions were not displayed in the supplied records.

suites/first/ holds the assistant's first test file exactly as it generated it: yes. The 17-test file was copied there before replacing the working file. The runner confirmed that the frozen copy remained unchanged during mutation trials.

Every terminal output in lab-report.md was pasted from a real run, unedited: yes as to the visible output content. All reported test names, counts, failures, paths and timings come from the supplied real logs. ANSI colour-control sequences are omitted only for Markdown display. Original raw logs remain unchanged in evidence/.

I can explain every test in my final suite — its input, expected result and AC — without the assistant: STUDENT ANSWER REQUIRED: replace this sentence with yes or no after reviewing the tests.

Anything I accepted from the AI without fully understanding it: STUDENT ANSWER REQUIRED: name any remaining unclear test or code, or write none after your own review. The assistant cannot assess this on your behalf.

Section 10 of lab-report.md has deliberately not been drafted as a student's personal conclusion. It must be completed in the student's own words before submission.

Name: Yerassyl Arystanbek
Date: 6 November 2026