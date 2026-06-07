from typing import Any
import httpx


class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def call_tool(self, tool_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"{self.base_url}/tools/{tool_name}", json=payload
            )
            response.raise_for_status()
            return response.json()
