from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    course: str


class StudentUpdate(BaseModel):
    name: str
    email: EmailStr
    age: int
    course: str