from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.routes.students import router as student_router
from app.routes.chatbot import router as chatbot_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI app
app = FastAPI(
    title="Student Database Application System",
    description="Backend API for Student Database with AI Chatbot",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================

app.include_router(student_router)
app.include_router(chatbot_router)


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Student Database Backend is Running!"
    }