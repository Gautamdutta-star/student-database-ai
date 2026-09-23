from langchain_core.tools import tool

from app.database.connection import SessionLocal
from app.models.student import Student


@tool
def get_all_students() -> str:
    """
    Get all students from the student database.
    Use this when the user asks to see, list, or show all students.
    """

    db = SessionLocal()

    try:
        students = db.query(Student).all()

        if not students:
            return "There are currently no students in the database."

        result = []

        for student in students:
            result.append(
                f"ID: {student.id}, "
                f"Name: {student.name}, "
                f"Email: {student.email}, "
                f"Age: {student.age}, "
                f"Course: {student.course}"
            )

        return "\n".join(result)

    finally:
        db.close()


@tool
def get_student_by_id(student_id: int) -> str:
    """
    Get a specific student from the database using the student ID.
    """

    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            return f"No student was found with ID {student_id}."

        # Keep the same format as search_student_by_name()
        return (
            f"ID: {student.id}, "
            f"Name: {student.name}, "
            f"Email: {student.email}, "
            f"Age: {student.age}, "
            f"Course: {student.course}"
        )

    finally:
        db.close()


@tool
def search_student_by_name(name: str) -> str:
    """
    Search for students by name.
    """

    db = SessionLocal()

    try:
        students = (
            db.query(Student)
            .filter(Student.name.ilike(f"%{name}%"))
            .all()
        )

        if not students:
            return f"No student found with the name '{name}'."

        result = []

        for student in students:
            result.append(
                f"ID: {student.id}, "
                f"Name: {student.name}, "
                f"Email: {student.email}, "
                f"Age: {student.age}, "
                f"Course: {student.course}"
            )

        return "\n".join(result)

    finally:
        db.close()
@tool
def semantic_student_search(query: str) -> str:
    """
    Search students semantically using ChromaDB.
    Use this when the user asks a general or meaning-based
    question about students.
    """

    from app.vectorstore.chroma import search_students

    results = search_students(query, limit=5)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return "No matching students were found."

    response = []

    for document, metadata in zip(documents, metadatas):

        response.append(
            f"ID: {metadata.get('student_id')}\n"
            f"Name: {metadata.get('name')}\n"
            f"Email: {metadata.get('email')}\n"
            f"Age: {metadata.get('age')}\n"
            f"Course: {metadata.get('course')}"
        )

    return "\n\n".join(response)        
