import chromadb

from app.database.connection import SessionLocal
from app.models.student import Student


# ChromaDB persistent storage
CHROMA_PATH = "./chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Student collection
student_collection = client.get_or_create_collection(
    name="students"
)


def add_student_to_chroma(student):
    """
    Add or update one student in ChromaDB.
    """

    document = (
        f"Student ID: {student.id}. "
        f"Name: {student.name}. "
        f"Email: {student.email}. "
        f"Age: {student.age}. "
        f"Course: {student.course}."
    )

    student_collection.upsert(
        ids=[str(student.id)],
        documents=[document],
        metadatas=[
            {
                "student_id": student.id,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "course": student.course,
            }
        ],
    )

    return document


def add_all_students_to_chroma(students):
    """
    Add all students to ChromaDB.
    """

    if not students:
        return 0

    ids = []
    documents = []
    metadatas = []

    for student in students:

        ids.append(str(student.id))

        documents.append(
            f"Student ID: {student.id}. "
            f"Name: {student.name}. "
            f"Email: {student.email}. "
            f"Age: {student.age}. "
            f"Course: {student.course}."
        )

        metadatas.append(
            {
                "student_id": student.id,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "course": student.course,
            }
        )

    student_collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return len(students)


def sync_students_from_database():
    """
    Read all students from SQLite database
    and sync them into ChromaDB.
    """

    db = SessionLocal()

    try:
        students = db.query(Student).all()

        count = add_all_students_to_chroma(students)

        return count

    finally:
        db.close()


def search_students(query: str, limit: int = 5):
    """
    Perform semantic search in ChromaDB.
    """

    results = student_collection.query(
        query_texts=[query],
        n_results=limit,
    )

    return results