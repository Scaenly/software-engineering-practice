def analyze_marks(marks, pass_mark=50):
    if not marks:
        raise ValueError("The marks list cannot be empty.")
    
    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError(f"Invalid value '{mark}': Marks must be numeric (int or float).")
        if not (0 <= mark <= 100):
            raise ValueError(f"Invalid mark '{mark}': Marks must be between 0 and 100 inclusive.")
            
    total_marks = sum(marks)
    total_students = len(marks)
    passed_students = sum(1 for mark in marks if mark >= pass_mark)
    
    return {
        "average": total_marks / total_students,
        "highest": max(marks),
        "lowest": min(marks),
        "pass_rate": (passed_students / total_students) * 100
    }


# Test Suite
def run_tests():
    # 1. Base Example
    res = analyze_marks([40, 60, 80], 50)
    assert res["average"] == 60.0
    assert res["highest"] == 80
    assert res["lowest"] == 40
    assert round(res["pass_rate"], 2) == 66.67

    # 2. Single mark
    res_single = analyze_marks([75])
    assert res_single == {"average": 75.0, "highest": 75, "lowest": 75, "pass_rate": 100.0}

    # 3. Decimal marks
    res_decimal = analyze_marks([45.5, 60.25, 88.0], 50)
    assert res_decimal["highest"] == 88.0
    assert res_decimal["lowest"] == 45.5

    # 4. Custom pass mark
    res_custom = analyze_marks([40, 60, 80], pass_mark=70)
    assert res_custom["pass_rate"] == (1 / 3) * 100

    # 5. Exception: Empty list
    try:
        analyze_marks([])
        assert False, "Should have raised ValueError for empty list"
    except ValueError:
        pass

    # 6. Exception: Text/Non-numeric value
    try:
        analyze_marks([50, "eighty", 70])
        assert False, "Should have raised ValueError for non-numeric value"
    except ValueError:
        pass

    # 7. Exception: Mark below 0
    try:
        analyze_marks([-5, 50, 75])
        assert False, "Should have raised ValueError for mark < 0"
    except ValueError:
        pass

    # 8. Exception: Mark above 100
    try:
        analyze_marks([50, 75, 105])
        assert False, "Should have raised ValueError for mark > 100"
    except ValueError:
        pass

    print("All tests passed successfully!")

run_tests()