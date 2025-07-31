from fastapi import FastAPI
from schemas import StudentInput, CGPAOutput
from utils import calculate_cgpa

app = FastAPI(title="Student CGPA Calculator")

@app.post("/calculate-cgpa", response_model=CGPAOutput)
def calculate_cgpa_endpoint(student: StudentInput):
    cgpa = calculate_cgpa(student)
    return CGPAOutput(
        student_id=student.student_id,
        name=student.name,
        cgpa=cgpa
    )
