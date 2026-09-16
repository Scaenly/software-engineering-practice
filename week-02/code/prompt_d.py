def analyze_marks(marks, pass_mark=50):

    if not isinstance(marks, list) or not marks:
        raise ValueError("Input 'marks' must be a non-empty list.")


    if isinstance(pass_mark,bool) or not isinstance(pass_mark, (int, float)):
        raise  ValueError("pass_mark must be a number.")
    if not (0 <= pass_mark <= 100):
        raise ValueError("pass_mark must be between 0 and 100.")


    for mark in marks:

        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("All marks must be numeric and not booleans")
        if not(0 <= mark <= 100):
            raise ValueError("All marks must be between 0 and 100")

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    passed_count = sum(1 for mark in mark if mark >= pass_mark)
    pass_rate = round((passed_count / len(marks)) * 100, 2)

    return {
        "average": float(average),
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }  
          