# Sample student data
students = [
    {"Student_ID": 101, "Name": "Alice", "Mark": 88},
    {"Student_ID": 102, "Name": "Bob", "Mark": 42},
    {"Student_ID": 103, "Name": "Charlie", "Mark": 95},
    {"Student_ID": 104, "Name": "David", "Mark": 67},
    {"Student_ID": 105, "Name": "Eva", "Mark": 58},
    {"Student_ID": 106, "Name": "Frank", "Mark": 74},
]

# Define passing threshold
PASSING_MARK = 50

# Assign Letter Grade
def assign_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    elif mark >= 50:
        return "E"
    else:
        return "F"

# Assign Pass/Fail status and letter grade
for student in students:
    student["Status"] = "Pass" if student["Mark"] >= PASSING_MARK else "Fail"
    student["Grade"] = assign_grade(student["Mark"])

# Calculate key metrics
marks = [student["Mark"] for student in students]
average_mark = sum(marks) / len(marks)
highest_mark = max(marks)
lowest_mark = min(marks)
pass_count = sum(student["Status"] == "Pass" for student in students)
fail_count = sum(student["Status"] == "Fail" for student in students)

# Display summary report
print("--- Student Performance Summary ---")
print(f"Total Students: {len(students)}")
print(f"Average Mark:   {average_mark:.2f}")
print(f"Highest Mark:   {highest_mark}")
print(f"Lowest Mark:    {lowest_mark}")
print(f"Passed:         {pass_count}")
print(f"Failed:         {fail_count}\n")

# Display detailed table
print("--- Detailed Marks Table ---")
headers = ["Student_ID", "Name", "Mark", "Status", "Grade"]
widths = [max(len(header), max(len(str(student[header])) for student in students)) for header in headers]
print(" ".join(header.ljust(width) for header, width in zip(headers, widths)))
for student in students:
    print(" ".join(str(student[header]).ljust(width) for header, width in zip(headers, widths)))