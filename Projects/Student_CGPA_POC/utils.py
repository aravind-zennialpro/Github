from schemas import StudentInput

def calculate_cgpa(student: StudentInput) -> float:
    total_points = 0.0
    total_credits = 0

    for subject in student.grades:
        total_points += subject.grade_point * subject.credit_hours
        total_credits += subject.credit_hours

    if total_credits == 0:
        return 0.0
    
    cgpa = total_points / total_credits
    return round(cgpa, 2)
