from pydantic import BaseModel
from typing import List

class SubjectGrade(BaseModel):
    subject_name: str
    credit_hours: int
    grade_point: float  # On a 4.0 or 10.0 scale depending on your system

class StudentInput(BaseModel):
    student_id: str
    name: str
    grades: List[SubjectGrade]

class CGPAOutput(BaseModel):
    student_id: str
    name: str
    cgpa: float
