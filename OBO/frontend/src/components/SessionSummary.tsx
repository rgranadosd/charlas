import type { SessionResponse } from "../types/models";
import { StatusBadge } from "./StatusBadge";

interface SessionSummaryProps {
  session: SessionResponse | null;
  authStateLabel: string;
  currentUserLabel: string;
}

export function SessionSummary({ session, authStateLabel, currentUserLabel }: SessionSummaryProps) {
  return (
    <section className="panel">
      <div className="panel__header">
        <div>
          <p className="eyebrow">Session Summary</p>
          <h2>Identity Separation</h2>
        </div>
        <StatusBadge label={authStateLabel} />
      </div>

      <div className="summary-grid">
        <div>
          <span className="summary-label">Demo session</span>
          <strong>{session?.session_id ?? "initializing"}</strong>
        </div>
        <div>
          <span className="summary-label">Current user</span>
          <strong>{currentUserLabel}</strong>
        </div>
        <div>
          <span className="summary-label">Configured agent</span>
          <strong>{session?.configured_agent_id ?? "not configured"}</strong>
        </div>
        <div>
          <span className="summary-label">OAuth client</span>
          <strong>{session?.oauth_client_id ?? "not requested"}</strong>
        </div>
      </div>

      <div className="session-mini-list">
        {(session?.comparison_rows ?? []).map((row) => (
          <article key={row.artifact} className="session-mini-card">
            <div className="session-mini-card__header">
              <strong>{row.artifact}</strong>
              <StatusBadge label={row.status} />
            </div>
            <p className="session-mini-card__meta">Sujeto: {row.subject ?? "n/a"}</p>
            <p className="session-mini-card__meta">Uso: {row.use}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
