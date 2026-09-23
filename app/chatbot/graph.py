import json
import os
from typing import TypedDict

from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, START, END

from app.chatbot.tools import (
    get_all_students,
    get_student_by_id,
    search_student_by_name,
    semantic_student_search,
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured in .env")

client = genai.Client(api_key=api_key)


class ChatState(TypedDict):
    message: str
    response: str


def chatbot_node(state: ChatState):

    user_message = state["message"]

    prompt = f"""
You are an AI assistant for a Student Database Application.

The application contains student information such as:
- Student ID
- Name
- Email
- Age
- Course

The user may ask questions about students.

User message:
{user_message}

Choose exactly ONE appropriate action.

Available actions:

1. all_students
Use when the user asks to list, show, or display all students.

Return:
{{
    "action": "all_students"
}}

2. student_by_id
Use when the user asks about a specific student ID.

Return:
{{
    "action": "student_by_id",
    "student_id": 1
}}

3. search_by_name
Use when the user searches for a student by name.

Return:
{{
    "action": "search_by_name",
    "name": "Gautam"
}}

4. semantic_search
Use when the user asks a general, meaning-based, or semantic question
about students, courses, or student information.

Return:
{{
    "action": "semantic_search",
    "query": "students studying computer science"
}}

5. general
Use for greetings or questions unrelated to the student database.

Return:
{{
    "action": "general"
}}

IMPORTANT:
- Do not invent student information.
- Return ONLY valid JSON.
- Do not use markdown.
"""

    result = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    raw_response = result.text.strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.replace("```json", "")
        raw_response = raw_response.replace("```", "")
        raw_response = raw_response.strip()

    try:
        action_data = json.loads(raw_response)

    except json.JSONDecodeError:
        return {
            "response": "I could not understand the request."
        }

    action = action_data.get("action")


    # --------------------------------
    # Get all students
    # --------------------------------

    if action == "all_students":

        database_result = get_all_students.invoke({})

        return {
            "response": database_result
        }


    # --------------------------------
    # Get student by ID
    # --------------------------------

    elif action == "student_by_id":

        student_id = action_data.get("student_id")

        if student_id is None:
            return {
                "response": "Please provide a valid student ID."
            }

        database_result = get_student_by_id.invoke({
            "student_id": int(student_id)
        })

        return {
            "response": database_result
        }


    # --------------------------------
    # Search student by name
    # --------------------------------

    elif action == "search_by_name":

        name = action_data.get("name")

        if not name:
            return {
                "response": "Please provide a student name."
            }

        database_result = search_student_by_name.invoke({
            "name": name
        })

        return {
            "response": database_result
        }


    # --------------------------------
    # Semantic search using ChromaDB
    # --------------------------------

    elif action == "semantic_search":

        query = action_data.get("query")

        if not query:
            return {
                "response": "Please provide a search query."
            }

        database_result = semantic_student_search.invoke({
            "query": query
        })

        return {
            "response": database_result
        }


    # --------------------------------
    # General conversation
    # --------------------------------

    else:

        general_prompt = f"""
You are a helpful AI assistant for a Student Database Application.

User message:
{user_message}

Give a short and friendly response.

Do not invent student information.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=general_prompt
        )

        return {
            "response": response.text
        }


# --------------------------------
# LangGraph
# --------------------------------

graph_builder = StateGraph(ChatState)

graph_builder.add_node(
    "chatbot",
    chatbot_node
)

graph_builder.add_edge(
    START,
    "chatbot"
)

graph_builder.add_edge(
    "chatbot",
    END
)

chatbot_graph = graph_builder.compile()