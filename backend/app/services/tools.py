from datetime import datetime
from typing import TypedDict


class ToolResult(TypedDict):
    output: str


async def current_time_tool(_: str) -> ToolResult:
    return {"output": datetime.utcnow().isoformat() + "Z"}


async def incident_triage_tool(user_input: str) -> ToolResult:
    text = user_input.lower()
    if "payment" in text:
        return {"output": "Routed to fintech-payment-ops queue."}
    if "latency" in text or "timeout" in text:
        return {"output": "Routed to platform-reliability queue."}
    return {"output": "Routed to general-support queue."}
