# Lab report - Practice #02: The Prompt Is an Engineering Input
Name : Yerassyl Arystanbek
Date: 18.09.2026

1. The frozen experiment
Al assistant - ChatGPT
Exact model name - GPT-4o
Implementation language - python
Date of the runs - 2026-09-18

Each prompt was sent in a fresh chat: yes

No follow-up questions were asked before Part 7: yes

Every output was saved before any editing: yes


2. Prompt A — minimal
Write Python a code to analyze student marks.
Assumptions the AI made that I never gave it — list them, one per line. A data format, a pass threshold, a rounding rule, an input method, an invented feature all count.

Assumed the function signature should be analyze_marks(marks, pass_mark=50) with a default pass mark of 50.

Assumed all elements in marks would be valid numbers (int or float) without checking types.

Assumed elements in marks were already constrained to the [0, 100] range.

Assumed pass_mark requires no range or type checks.


Questions it should have asked and did not:

What function signature and parameters should be used?

How should invalid, non-numeric, or out-of-range marks be validated?

Is the function named analyze_marks with the required signature? yes

3. Prompt B — structured context
Prompt sent: 
You are a Python developer. Implement analyze_marks(marks, pass_mark=50). Return average, highest, lowest, and pass_rate in a dictionary. Accept marks from 0 to 100; raise ValueError for an empty list, non-numeric values, or out-of-range values. Use no external libraries. Return code plus a short explanation.

What B fixed compared to A:

Added explicit checks for numbers using isinstance(mark, (int, float)) and actively filtered out bool types.

Actually enforced the mark range limit with 0 <= mark <= 100.

What B still leaves open:

It forgot to validate pass_mark itself (e.g., if someone passes a string or negative number as the pass threshold).

Doesn't check if marks is None before trying to check its length or iterate through it.


4. Prompt C — examples and tests
What I appended to Prompt B:

Example: analyze_marks([40, 60, 80], 50) → average 60, highest 80, lowest 40, pass_rate 66.67. Include tests for: one mark, decimals, custom pass_mark, empty list, text value, and marks below 0 or above 100. State any remaining assumptions before the code.


5. Prompt D — my combined prompt

The complete prompt I wrote (one message, sent to a fresh chat):

You are an expert Python developer. Implement the function analyze_marks(marks, pass_mark=50) and a comprehensive test suite using standard library assertions.

Function Requirements
Signature & Default: def analyze_marks(marks, pass_mark=50)

Input Validation:

Raise a ValueError if marks is empty or not a collection.

Raise a ValueError if any element in marks is non-numeric (specifically, isinstance(mark, (int, float)) must be True and isinstance(mark, bool) must be False).

Raise a ValueError if any element in marks is less than 0 or greater than 100.

Raise a ValueError if pass_mark is non-numeric or outside the range [0, 100].

Calculations & Output:

Return a Python dictionary containing average (float), highest (int/float), lowest (int/float), and pass_rate (float).

pass_rate must be calculated as (passed_students / total_students) * 100.

Do NOT round values internally within analyze_marks.

What I deliberately added that A, B and C did not have:

Validation for the pass_mark argument itself so invalid threshold settings raise errors.

An if __name__ == "__main__": guard so test assertions don't execute automatically when importing the file into another script.

Explicit instructions on how to handle booleans so Python doesn't treat True as 1.



6. Test results — the evidence
1.analyze_marks([40, 60, 80], 50) required: avg 60 · high 80 · low 40 · rate 66.67 A:PASS B:PASS C:PASS D:PASS
2.analyze_marks([100], 50) required: avg 100 · high 100 · low 100 · rate 100 A:PASS B:PASS C:PASS D:PASS
3.analyze_marks([49.5, 50], 50) required: avg 49.75 · high 50 · low 49.5 · rate 50 A:PASS B:PASS C:PASS D:PASS
4.analyze_marks([], 50) required: raises ValueError A:PASS B:PASS C:PASS D:PASS
5.analyze_marks([40, "60"], 50) required: raises ValueError A:ERROR B:PASS C:PASS D:PASS
6.analyze_marks([-1, 50, 101], 50) required: raises ValueError A:FAIL B:PASS C:PASS D:PASS


Pasted terminal output — all four runs
--- Testing module: prompt_a.py ---
Case 1: PASS
Case 2: PASS
Case 3: PASS
Case 4: PASS
Case 5: ERROR (Raised unexpected exception: TypeError)
Case 6: FAIL (Returned result where ValueError was required)

--- Testing module: prompt_b.py ---
Case 1: PASS
Case 2: PASS
Case 3: PASS
Case 4: PASS
Case 5: PASS
Case 6: PASS

--- Testing module: prompt_c.py ---
Case 1: PASS
Case 2: PASS
Case 3: PASS
Case 4: PASS
Case 5: PASS
Case 6: PASS

--- Testing module: prompt_d.py ---
Case 1: PASS
Case 2: PASS
Case 3: PASS
Case 4: PASS
Case 5: PASS
Case 6: PASS

7. Scoring
Criterion                 A         B          C      D
Correctness               1         2          2      2
Requirement coverage      0         2          2      2
Verifiability (tests)     0         0          2      2
Assumptions stated        0         1          2      2
Noise (2 = none)          1         2          2      2
Total / 10                2         7          9      10

8. Conclusion — 150–200 words
Prompt D scored the highest (10/10) and is the prompt structure I would actually use at work. The single addition that brought the biggest leap in correctness was explicitly specifying input validation rules (0 <= mark <= 100 and type checking). This fixed Case 5 (which crashed with a TypeError in Prompt A) and Case 6 (which quietly calculated invalid results for [-1, 50, 101] in Prompt A), turning both into clean PASS verdicts across Prompts B, C, and D. Adding script execution guards (if __name__ == "__main__":) in Prompt D also prevented imports from triggering test suite executions when imported by the harness. Asking for conversational explanations in Prompt A was pure noise that added no functional value to the output. The primary ambiguity in the task was float precision and boolean handling, which was resolved in Prompt D by specifying raw float returns and blocking bool types explicitly.

Word count: 151 words



