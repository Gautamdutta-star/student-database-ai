# 🎓 Student Database Application System – Backend

A modular backend application for managing student records with CRUD APIs, AI-powered chatbot interaction, LangGraph, Google Gemini API, and ChromaDB semantic search.

## 🚀 Project Overview

The **Student Database Application System** is a backend application developed using **FastAPI**.

It provides REST APIs for student management and an AI-powered chatbot that allows users to interact with student database information using natural language.

The project follows a modular backend architecture and integrates **LangGraph**, **Google Gemini API**, and **ChromaDB** for intelligent student data interaction.

---

## ✨ Features

- ✅ Modular backend architecture
- ✅ Student CRUD operations
- ✅ FastAPI REST APIs
- ✅ Swagger API documentation
- ✅ AI-powered chatbot
- ✅ LangGraph-based chatbot workflow
- ✅ Google Gemini API integration
- ✅ ChromaDB vector database
- ✅ Semantic student search
- ✅ Student database interaction through chatbot
- ✅ Deployable backend service
- ✅ GitHub-ready project structure

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Student database |
| LangGraph | AI chatbot workflow |
| Google Gemini API | Natural language processing |
| ChromaDB | Vector database and semantic search |
| Uvicorn | ASGI server |
| Swagger / OpenAPI | API documentation |

---

## 📁 Project Structure

```
student-database-backend/
│
├── app/
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   └── tools.py
│   │
│   ├── database/
│   │
│   ├── models/
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   └── students.py
│   │
│   ├── schemas/
│   │
│   ├── vectorstore/
│   │   ├── __init__.py
│   │   └── chroma.py
│   │
│   └── main.py
│
├── student-database-frontend/
│
├── .gitignore
├── requirements.txt
└── README.md
---

🔌 API Endpoints
Student APIs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/students/` | Get all students |
| POST | `/students/` | Create a new student |
| GET | `/students/{student_id}` | Get student by ID |
| PUT | `/students/{student_id}` | Update student |
| DELETE | `/students/{student_id}` | Delete student |

AI Chatbot
| Method | Endpoint | Description |
|---|---|---|
| POST | `/chatbot/chat` | Interact with the AI chatbot |

🤖 AI Chatbot
The chatbot uses LangGraph to process user queries and select the appropriate operation.
It supports different types of student-related queries such as:
What is the age and course of Rahul Kumar?
Show me all students.
Find the student named Rahul.
Find students related to computer science.

🧠 LangGraph Workflow
The chatbot workflow uses different actions for processing student queries:
                    User Query
                        │
                        ▼
                 LangGraph Agent
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
    All Students    Student ID    Search by Name
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                 Semantic Search
                    ChromaDB
                        │
                        ▼
                   Gemini API
                        │
                        ▼
                  Final Response

🗄️ Vector Database
ChromaDB was selected as the vector database for this project.
It is used to perform semantic similarity searches over student information.
Example:
User Query
    ↓
"Find students related to computer science"
    ↓
ChromaDB Semantic Search
    ↓
Relevant Student Records
    ↓
AI Chatbot Response

📚 Database
The project uses SQLite with SQLAlchemy.
Student Fields
id
name
email
age
course

Example Student
{
  "name": "Rahul Kumar",
  "email": "rahul.kumar@gmail.com",
  "age": 22,
  "course": "B.Tech CSE"
}

⚙️ Installation
1. Clone the Repository
git clone https://github.com/Gautamdutta-star/student-database-ai.git

2. Navigate to the Project
cd student-database-ai

3. Create Virtual Environment
Windows:
python -m venv venv

4. Activate Virtual Environment
venv\Scripts\activate

5. Install Dependencies
pip install -r requirements.txt

6. Configure Environment Variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key
Important: Never commit your actual Gemini API key to GitHub.

7. Run the Backend
uvicorn app.main:app --reload
The backend will run at:
http://127.0.0.1:8000

📖 Swagger API Documentation
FastAPI automatically provides interactive Swagger documentation.
Local Swagger:
http://127.0.0.1:8000/docs
Live Swagger:
https://student-database-ai.onrender.com/docs
Swagger can be used to test all CRUD APIs and the AI chatbot API directly from the browser.

🌐 Deployment
The backend is deployed using Render.
Live Backend
https://student-database-ai.onrender.com
Live Swagger Documentation
https://student-database-ai.onrender.com/docs
The deployed service provides the FastAPI backend and API documentation.

🔐 Environment Variables
The application requires the following environment variable:
GEMINI_API_KEY
The API key should be configured securely in the local .env file or deployment platform environment variables.
API keys must not be committed to the GitHub repository.

🧪 API Testing
The APIs can be tested using:
- Swagger UI
- Postman
- REST API clients
- Frontend application
Create Student Example
Endpoint:
POST /students/
Request Body:
{
  "name": "Rahul Kumar",
  "email": "rahul.kumar@gmail.com",
  "age": 22,
  "course": "B.Tech CSE"
}

Chatbot Example
Endpoint:
POST /chatbot/chat
Request Body:
{
  "message": "What is the age and course of Rahul Kumar?"
}

📌 Project Requirements Coverage
| Requirement | Implementation |
|---|---|
| Modular Backend Architecture | FastAPI modular project structure |
| CRUD Operations | Student CRUD REST APIs |
| FastAPI APIs | FastAPI |
| Swagger API Documentation | FastAPI OpenAPI / Swagger UI |
| Deployable Backend Service | Render |
| Gemini API Integration | Google Gemini API |
| AI Chatbot | LangGraph |
| Student Database Interaction | Database tools and chatbot |
| Vector Database | ChromaDB |

🎯 Project Architecture
                    ┌──────────────────────┐
                    │      Client/User     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌──────────────────┐             ┌──────────────────┐
     │ Student CRUD APIs│             │   AI Chatbot     │
     └────────┬─────────┘             └────────┬─────────┘
              │                                │
              ▼                                ▼
     ┌──────────────────┐             ┌──────────────────┐
     │ SQLite Database  │             │    LangGraph     │
     └──────────────────┘             └────────┬─────────┘
                                               │
                                  ┌────────────┴────────────┐
                                  │                         │
                                  ▼                         ▼
                         ┌──────────────────┐     ┌──────────────────┐
                         │    ChromaDB      │     │   Gemini API     │
                         │ Semantic Search  │     │ AI Response      │
                         └──────────────────┘     └──────────────────┘

📊 Key Highlights
- Modular and maintainable backend architecture
- RESTful CRUD APIs for student management
- Interactive Swagger API documentation
- Natural-language student database interaction
- LangGraph-powered AI workflow
- Gemini-powered conversational responses
- ChromaDB-based semantic search
- Successfully deployed backend service using Render
```
🔗 Project Links
GitHub Repository
https://github.com/Gautamdutta-star/student-database-ai
```
```
Live Backend
https://student-database-ai.onrender.com
```
```
Live Swagger Documentation
https://student-database-ai.onrender.com/docs
```

👨‍💻 Author
Gautam Kumar Dutta
B.Tech Computer Science and Engineering

📄 License
This project was developed for educational and internship project purposes.
