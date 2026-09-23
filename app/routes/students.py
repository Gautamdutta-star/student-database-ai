from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Add a new student
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this email already exists"
        )

    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# READ - Get all students
@router.get("/")
def get_students(
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    return students


# READ - Get student by ID
@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


# UPDATE - Update student by ID
@router.put("/{student_id}")
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check if another student already uses this email
    existing_student = db.query(Student).filter(
        Student.email == student_data.email,
        Student.id != student_id
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Another student already uses this email"
        )

    student.name = student_data.name
    student.email = student_data.email
    student.age = student_data.age
    student.course = student_data.course

    db.commit()
    db.refresh(student)

    return student


# DELETE - Delete student by ID
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }