## What I built

Continued the Week 08 Smart Campus app and kept all 29 inherited tests. Added an R1 regression that failed before extracting shared pure booking rules. The final suite passes 30/30. Patched AGENTS.md after approval, kept the patch to nine changed lines, and restored one fictional room.

The report contains eight challenged claims, six risks, the twelve-row readiness audit (Level 1), two required mitigations and residual scores. Real desktop and mobile screenshots are now included. The audit passes 31/31 checks; the submission validator passes 15/15. The recorded test, lint, typecheck and build runs pass. The release decision remains NO-GO for a full release because CI and stale-result concerns remain. The PR stays Draft pending personal source/diff review.

## AI tools used

ChatGPT/Codex helped inspect the code, prepare the regression and patches, run checks and draft the report. The exact model version was not displayed. I approved the AGENTS.md patch, wrote the release conclusion and captured the UI screenshots locally. AI_USAGE.md records the assistance and remaining personal review items.

## What the AI got wrong

The old BUG-B mutation was already fixed, so a claim that it remains is unsupported. The dependency concern is plausible, not a proven vulnerability. The R1 NaN case has limited reachability through the current UI parser. A separate before-edit file-plan reply was not captured. Initial assistant browser checks failed; I later supplied real screenshots from my browser. The referenced SETUP.md was unavailable, so these five headings follow the previous course PR description.

## Time spent

Work recorded on 23 November 2026. No accurate manual/AI time split was recorded.

## What I would do differently

Record the file plan and review decisions as the work happens. Before a full release, add CI and a controlled-clock test and fix for stale availability feedback. Keep this PR open until grading; do not merge or deploy.
