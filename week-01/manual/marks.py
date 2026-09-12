import sys

def process_marks(raw_input: str):
    tokens = raw_input.split(",")
    valid_marks = []

    for token in tokens:
        cleaned = token.strip() # оширемиз барлык пробелдер осы кодта оны очистка жасаймыз керек емес пробел 
        if not cleaned:
            continue
        try:
            val = float(cleaned)

            if 0 <= val <= 100: # 0 ден 100 ге дейн аралык 
                # если число болса немесе сохранияем int пен немесе float (90,0= true 85,5= false)
                valid_marks.append(int(val)if val.is_integer() else val) 
        except ValueError:
            continue        

    count = len(valid_marks)
    if count == 0:
        print("NO VALID MARKS FOUND (")
        return

    avg = sum(valid_marks) / count
    highest = max(valid_marks)  
    lowest = min(valid_marks)
    passing_count = sum(1 for m in valid_marks if m >= 50) # осы жерде валидта коп немесе тен 50 ге 1 for m in возвращает единичку 1 для каждого совпадения пример [85,15,30,90,92] 85 90 92

    pass_rate = (passing_count / count) * 100 # процент есептеймиз мысалы 3 5 * 100 = 60%

    print(f"Valid marks count: {count}")
    print(f"Average: {avg:.2f}")
    print(f"Highest:{highest}")
    print(f"Lowest:{lowest}")
    print(f"Pass rate:{pass_rate:.1f}%")
if __name__  == "__main__":
    if len(sys.argv) > 1:
        raw_input = " ".join(sys.argv[1:])
    else:
        raw_input = input("Enter marks (comma - seperated): ")  

    process_marks(raw_input)        

