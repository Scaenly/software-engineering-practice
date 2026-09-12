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

 
