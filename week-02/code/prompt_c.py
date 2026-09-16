def analyze_marks(marks, pass_mark=50):
    if not marks:
        raise ValueError("Marks list cannot be empty")

    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError("All marks must be numeric")

        if mark < 0 or mark > 100:
            raise ValueError("Marks must be between 0 and 100")

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    passed = 0
    for mark in marks:
        if mark >= pass_mark:
            passed += 1

    pass_rate = (passed / len(marks)) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": round(pass_rate, 2)
    }


# Tests

# 1. Normal case
print(analyze_marks([40, 60, 80], 50))
# {'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 66.67}

# 2. One mark
print(analyze_marks([75]))
# {'average': 75.0, 'highest': 75, 'lowest': 75, 'pass_rate': 100.0}

# 3. Decimal marks
print(analyze_marks([70.5, 80.5, 90.0]))
# {'average': 80.33, 'highest': 90.0, 'lowest': 70.5, 'pass_rate': 100.0}

# 4. Custom pass_mark
print(analyze_marks([40, 60, 80], 70))
# {'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 33.33}

# 5. Empty list
try:
    analyze_marks([])
except ValueError as e:
    print("Empty list:", e)

# 6. Text value
try:
    analyze_marks([40, "60", 80])
except ValueError as e:
    print("Text value:", e)

# 7. Mark below 0
try:
    analyze_marks([40, -5, 80])
except ValueError as e:
    print("Below 0:", e)

# 8. Mark above 100
try:
    analyze_marks([40, 105, 80])
except ValueError as e:
    print("Above 100:", e)