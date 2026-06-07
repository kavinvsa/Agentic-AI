from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="MCP Tools Server", version="0.1.0")


class ToolRequest(BaseModel):
    input: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tools/{tool_name}")
def run_tool(tool_name: str, payload: ToolRequest) -> dict[str, str]:
    if tool_name == "current_time":
        return {"output": datetime.utcnow().isoformat() + "Z"}
    if tool_name == "incident_classifier":
        text = payload.input.lower()
        if "payment" in text:
            return {"output": "payment-critical"}
        if "latency" in text or "timeout" in text:
            return {"output": "sre-high"}
        return {"output": "support-normal"}
    raise HTTPException(status_code=404, detail="tool not found")
