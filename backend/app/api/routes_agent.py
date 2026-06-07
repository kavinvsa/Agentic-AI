from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ConversationTurn
from app.services.langgraph_agent import run_agent

router = APIRouter(prefix="/api/v1", tags=["agent"])


class AgentRequest(BaseModel):
    session_id: str
    prompt: str


class AgentResponse(BaseModel):
    triage: str
    timestamp: str
    response: str


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/agent/run", response_model=AgentResponse)
async def agent_run(payload: AgentRequest, db: Session = Depends(get_db)) -> AgentResponse:
    db.add(ConversationTurn(session_id=payload.session_id, role="user", content=payload.prompt))
    result = await run_agent(payload.prompt)
    db.add(ConversationTurn(session_id=payload.session_id, role="assistant", content=result["response"]))
    db.commit()
    return AgentResponse(
        triage=result["triage"],
        timestamp=result["timestamp"],
        response=result["response"],
    )
