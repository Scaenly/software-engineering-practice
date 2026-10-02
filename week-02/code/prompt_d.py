def analyze_marks(marks, pass_mark=50):
    if not isinstance(marks, list) or not marks:
        raise ValueError("Invalid input: marks must be a non-empty list.")
    
    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("Invalid element: marks must contain numbers only.")
        if not (0 <= mark <= 100):
            raise ValueError("Mark out of range: must be between 0 and 100.")
            
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)) or not (0 <= pass_mark <= 100):
        raise ValueError("Invalid pass_mark value.")

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)
    passed_count = sum(1 for m in marks if m >= pass_mark)
    pass_rate = (passed_count / len(marks)) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }


if __name__ == "__main__":
    # Tests inside main block won't break imports in test_analyze_marks.py
    
    # One mark
    assert analyze_marks([80]) == {
        "average": 80.0,
        "highest": 80,
        "lowest": 80,
        "pass_rate": 100.0
    }

    # Decimals
    result = analyze_marks([70.5, 80.5, 90])
    assert result["average"] == 80.33333333333333
    assert result["highest"] == 90
    assert result["lowest"] == 70.5
    assert result["pass_rate"] == 100.0

    # Custom pass_mark (checking exact float precision)
    assert analyze_marks([40, 60, 80], 70)["pass_rate"] == 33.33333333333333

    # Empty list
    try:
        analyze_marks([])
        assert False
    except ValueError:
        pass

    # Text value
    try:
        analyze_marks([50, "abc", 80])
        assert False
    except ValueError:
        pass

    # Below 0
    try:
        analyze_marks([-5, 50, 80])
        assert False
    except ValueError:
        pass

    # Above 100
    try:
        analyze_marks([50, 101, 80])
        assert False
    except ValueError:
        pass

    print(analyze_marks([40, 60, 80], 50))