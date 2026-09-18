def analyze_marks(marks, pass_mark=50):
    if not marks:
        raise ValueError("Marks list cannot be empty")
    
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