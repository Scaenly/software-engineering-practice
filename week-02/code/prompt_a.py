import pandas as pd

# Sample student data
data = {
    "Student_ID": [101, 102, 103, 104, 105, 106],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank"],
    "Mark": [88, 42, 95, 67, 58, 74]
}

df = pd.DataFrame(data)

# Define passing threshold
PASSING_MARK = 50

# Assign Pass/Fail status
df["Status"] = df["Mark"].apply(lambda x: "Pass" if x >= PASSING_MARK else "Fail")

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

df["Grade"] = df["Mark"].apply(assign_grade)

# Calculate key metrics
average_mark = df["Mark"].mean()
highest_mark = df["Mark"].max()
lowest_mark = df["Mark"].min()
pass_count = (df["Status"] == "Pass").sum()
fail_count = (df["Status"] == "Fail").sum()

# Display summary report
print("--- Student Performance Summary ---")
print(f"Total Students: {len(df)}")
print(f"Average Mark:   {average_mark:.2f}")
print(f"Highest Mark:   {highest_mark}")
print(f"Lowest Mark:    {lowest_mark}")
print(f"Passed:         {pass_count}")
print(f"Failed:         {fail_count}\n")

# Display detailed table
print("--- Detailed Marks Table ---")
print(df.to_string(index=False))