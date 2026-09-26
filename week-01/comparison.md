Comparison & Reflection

1.facts:
Manual(Part1):
Language:Python 3 , Next.js, Typescript, Tailwind css
Time to first version that ran: 8 min 
Time to all 4 test cases passing: 18 min 
Number of attempts / prompts needed:1 / 1 prompt + 1 clarification
Lines of code you actually wrote: 40 / 0
Did it handle invalid marks (case B)?	Yes (handled via Python exception logic) / Yes (skipped invalid entries with warning)
Did it handle an empty list (case D)? 
Did it use the ≥ 50 pass threshold? / Yes / yes 
Output format matches the spec? / Yes / Yes
Can you explain every line of it? / Yes / Partially


Test Results:
Case A: 85, 23, 45, 90, 92
output: Total marks:5 | Class Average: 67 | Highest Mark: 92 | Lowest Mark: 23 | Pass Rate: 60.00%
Match: Yes

Case B: 88, 47, -5, 101, abc, 73, 50, , 100	
output: avg 71.60 · high 100 · low 47 · pass 80.0%	
Match:Yes

Case C: 10, 20, 30
output: avg 20.00 · high 30 · low 10 · pass 0.0%
Match:Yes

Case D: abc, , xyz
output: Could not parse any valid marks. Issues found: "abc" is not a number, "xyz" is not a number.
Match:Yes

What the AI added that I never asked for
Rocket generated a full Next.js web application with responsive Bento grid metric cards, an interactive pass threshold slider (0–100), extra statistics (Median, Standard Deviation, Fail Count), and a grade distribution bar chart.

What the AI got wrong or silently skipped
Initial setup required prompt clarifications to establish input boundary conditions. Additionally, Rocket chose a heavy web framework stack (Next.js/TypeScript) for a task that only required simple array statistics.

 
Reflection: 
Which parts of the work did the AI genuinely speed up? The AI tool Rocket genuinely sped up the entire UI creation, styling, and framework setup. Building a web interface with Next.js, TypeScript, responsive Bento grid cards, and interactive threshold sliders from scratch would have taken hours manually. Rocket scaffolded the complete frontend layout and initial calculation logic within 3 minutes.

Where did the AI cost you time, or give you something that looked right but was not?The AI cost me extra time during initial requirement alignment and edge-case handling. It generated a heavily over-engineered framework stack for simple array calculations, and it initially handled invalid inputs silently. I had to issue a follow-up prompt to ensure skipped non-numeric values and out-of-bounds numbers (< 0 or > 100) displayed an explicit warning message instead of disappearing without feedback.



Which of these two artefacts would you be willing to put your name on, and why?



What must a human engineer still be responsible for after this experiment?A human engineer remains strictly responsible for defining boundary conditions, verifying data validation logic, ensuring edge-case compliance, and testing for hidden bugs. AI can handle visual boilerplate quickly, but the engineer must guarantee correctness, security, and specification adherence.