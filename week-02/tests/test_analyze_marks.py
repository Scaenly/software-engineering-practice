import sys
import math

# Add code directory to path
sys.path.append('week-02/code')

if len(sys.argv) < 2:
    print("Usage: python tests/test_analyze_marks.py code/prompt_a.py")
    sys.exit(1)

module_name = sys.argv[1].replace('.py', '').split('/')[-1].split('\\')[-1]

# Try importing module (ERROR if function missing or broken signature)
try:
    solution = __import__(module_name)
    analyze_marks = getattr(solution, 'analyze_marks')
except Exception as e:
    print(f"--- Testing module: {module_name}.py ---")
    print(f"ERROR: Could not load analyze_marks from {module_name}.py ({e})")
    sys.exit(1)

def is_close(val1, val2, tol=0.01):
    return abs(val1 - val2) <= tol

# The 6 exact test cases from the specification
cases = [
    (1, lambda: analyze_marks([40, 60, 80], 50), {"average": 60, "highest": 80, "lowest": 40, "pass_rate": 66.67}, False),
    (2, lambda: analyze_marks([100], 50), {"average": 100, "highest": 100, "lowest": 100, "pass_rate": 100}, False),
    (3, lambda: analyze_marks([49.5, 50], 50), {"average": 49.75, "highest": 50, "lowest": 49.5, "pass_rate": 50}, False),
    (4, lambda: analyze_marks([], 50), None, True),
    (5, lambda: analyze_marks([40, "60"], 50), None, True),
    (6, lambda: analyze_marks([-1, 50, 101], 50), None, True),
]

print(f"--- Testing module: {module_name}.py ---")

for num, test_fn, expected, should_raise in cases:
    try:
        res = test_fn()
        if should_raise:
            print(f"Case {num}: FAIL (Returned result where ValueError was required)")
        elif isinstance(res, dict) and all(k in res for k in ("average", "highest", "lowest", "pass_rate")):
            # Check values with 0.01 tolerance
            matches = all(is_close(float(res[k]), float(expected[k])) for k in expected)
            if matches:
                print(f"Case {num}: PASS")
            else:
                print(f"Case {num}: FAIL (Incorrect output values: {res})")
        else:
            print(f"Case {num}: FAIL (Wrong return format or missing keys)")
            
    except ValueError:
        if should_raise:
            print(f"Case {num}: PASS")
        else:
            print(f"Case {num}: FAIL (Raised ValueError unexpectedly)")
    except Exception as e:
        print(f"Case {num}: ERROR (Raised unexpected exception: {type(e).__name__})")