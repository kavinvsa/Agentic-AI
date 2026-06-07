const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type AgentRunResponse = {
  triage: string;
  timestamp: string;
  response: string;
};

export async function runAgent(sessionId: string, prompt: string): Promise<AgentRunResponse> {
  const res = await fetch(`${API_BASE}/api/v1/agent/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, prompt }),
  });

  if (!res.ok) {
    throw new Error(`Request failed with ${res.status}`);
  }

  return res.json();
}
