import { useMemo, useState } from "react";
import { runAgent } from "./api";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<{ triage: string; timestamp: string; response: string } | null>(null);

  const sessionId = useMemo(() => crypto.randomUUID(), []);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await runAgent(sessionId, prompt);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="card">
        <h1>Incident Command Agent</h1>
        <p>LangGraph + MCP + API + DB orchestration demo for production workflows.</p>

        <form onSubmit={onSubmit} className="form">
          <label htmlFor="issue">Describe your incident or scenario</label>
          <textarea
            id="issue"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Checkout payments fail for users in EU after deployment"
            rows={6}
            required
          />
          <button disabled={loading || !prompt.trim()}>{loading ? "Running agent..." : "Run Agent"}</button>
        </form>

        {error ? <div className="error">{error}</div> : null}

        {result ? (
          <article className="result">
            <h2>Agent Response</h2>
            <p><strong>Triage:</strong> {result.triage}</p>
            <p><strong>Timestamp:</strong> {result.timestamp}</p>
            <pre>{result.response}</pre>
          </article>
        ) : null}
      </section>
    </main>
  );
}
