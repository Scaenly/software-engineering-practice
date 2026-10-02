# Rocket Prompts Log

## Initial Prompt
```text
Build a small program that processes a list of student marks and prints: average, highest, lowest, and pass rate.

Questions asked by Rocket:
1.How should marks be entered into the app? Paste or bulk-enter a list (Paste a comma-separated or multi-line list of marks at once)
2.Who is this tool primarily for? Personal use or learning (A developer or student building it for practice or demos)

Test result with 4 cases:
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

