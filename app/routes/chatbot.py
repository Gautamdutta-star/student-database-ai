from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.chatbot.graph import chatbot_graph


router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = chatbot_graph.invoke({
            "message": request.message,
            "response": ""
        })

        return {
            "response": result["response"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chatbot error: {str(e)}"
        )