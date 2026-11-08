## What I built

Continued the actual Week 07 Smart Campus app and preserved its 27 tests. The unchanged provided function failed 9/27 tests. After adding independent BUG-A and BUG-B regressions, it failed 11/29 tests. Compared two actual fresh-chat replies on identical inputs, using a declared prompt-only simulation for bug-detector. Fixed each bug with one changed line in its own commit. The final Windows suite passed 29/29 tests.

## AI tools used

ChatGPT / Codex assisted preparation, regression tests, diagnostic inputs, comparison, repair automation and report drafting. ChatGPT provided the two diagnostic replies. Sections 9.2 and 10 were also drafted with AI at the student's explicit request. Exact model versions were not displayed in the supplied evidence. Contributions and process deviations are disclosed in week-08/AI_USAGE.md.

## What the AI got wrong

Both replies correctly identified BUG-A and BUG-B but unnecessarily proposed deleting the comment above bookings.push. The applied repair retained the comment and deleted only the push. An earlier request could not locate the skill, so the successful comparison explicitly supplied the procedure as a prompt-only simulation. Claims of isolated execution were not accepted as proof that the project suite passed.

## Time spent

Manual active time: 5-6 hours.

AI-assisted active time: 2 hours.

No measured breakdown or reliable numerical estimate was supplied, so durations are unavailable.

## What I would do differently

AI-assisted draft requested by the student: record personal hypotheses before asking for a diagnosis, verify the skill or simulation context before sending the controlled input, and capture full terminal outputs as they occur. Review each proposed deletion against the minimal-change requirement, keep UI verification separate from function tests, and record active working time during the lab.