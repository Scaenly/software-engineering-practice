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