from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from app.core.config import get_settings
from app.services.tools import current_time_tool, incident_triage_tool
from app.services.mcp_client import MCPClient


class AgentState(TypedDict):
    prompt: str
    triage: str
    timestamp: str
    response: str


async def run_tools(state: AgentState) -> AgentState:
    settings = get_settings()
    mcp = MCPClient(settings.mcp_server_url)

    # Fallback keeps the app usable even if MCP server is unavailable.
    try:
        triage = await mcp.call_tool("incident_classifier", {"input": state["prompt"]})
        now = await mcp.call_tool("current_time", {"input": state["prompt"]})
    except Exception:
        triage = await incident_triage_tool(state["prompt"])
        now = await current_time_tool(state["prompt"])

    return {**state, "triage": triage["output"], "timestamp": now["output"]}


async def run_llm(state: AgentState) -> AgentState:
    settings = get_settings()
    if not settings.openai_api_key:
        fallback = (
            "OpenAI API key is not configured. "
            f"Triage route: {state['triage']}. "
            "Recommended next step: gather logs, impact scope, and rollback readiness."
        )
        return {**state, "response": fallback}

    llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)
    messages = [
        SystemMessage(
            content=(
                "You are a production incident response agent. "
                "Give concise, practical guidance."
            )
        ),
        HumanMessage(
            content=(
                f"User issue: {state['prompt']}\n"
                f"Auto-triage: {state['triage']}\n"
                f"Timestamp UTC: {state['timestamp']}"
            )
        ),
    ]
    output = await llm.ainvoke(messages)
    return {**state, "response": output.content}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("tools", run_tools)
    graph.add_node("llm", run_llm)
    graph.add_edge(START, "tools")
    graph.add_edge("tools", "llm")
    graph.add_edge("llm", END)
    return graph.compile()


async def run_agent(prompt: str) -> AgentState:
    app_graph = build_graph()
    initial: AgentState = {
        "prompt": prompt,
        "triage": "",
        "timestamp": "",
        "response": "",
    }
    return await app_graph.ainvoke(initial)
