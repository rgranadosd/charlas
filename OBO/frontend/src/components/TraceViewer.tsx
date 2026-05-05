import type { TraceEntry } from "../types/models";
import { CodeBlock } from "./CodeBlock";

interface TraceViewerProps {
  traces: TraceEntry[];
}

export function TraceViewer({ traces }: TraceViewerProps) {
  function formatTimestamp(timestamp: string) {
    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
      return timestamp;
    }

    return date.toLocaleString();
  }

  return (
    <section className="panel trace-panel">
      <div className="panel__header">
        <div>
          <p className="eyebrow">Historia del flujo</p>
          <h2>Explicacion paso a paso</h2>
        </div>
      </div>
      {traces.length === 0 ? <p className="muted">Todavia no hay pasos registrados en el flujo.</p> : null}
      <div className="trace-list">
        {traces.map((trace, index) => (
          <details key={`${trace.timestamp}-${trace.action}`} open={index === 0} className="trace-item">
            <summary>
              <div className="trace-summary-main">
                <strong>{trace.action}</strong>
                <p className="trace-summary-caption">{trace.security_interpretation}</p>
              </div>
              <div className="trace-summary-side">
                <span className="trace-chip">{trace.method}</span>
                <span className="trace-chip trace-chip--status">{trace.response_status}</span>
                <span className="trace-meta">{formatTimestamp(trace.timestamp)}</span>
              </div>
            </summary>
            <div className="trace-item__body">
              <div className="trace-explanation-grid">
                <div className="trace-note-card">
                  <p className="trace-note-card__label">Que ha pasado</p>
                  <p className="trace-note-card__value">{trace.functional_interpretation}</p>
                </div>
                <div className="trace-note-card trace-note-card--security">
                  <p className="trace-note-card__label">Lectura de seguridad</p>
                  <p className="trace-note-card__value">{trace.security_interpretation}</p>
                </div>
              </div>
              <p className="trace-endpoint">{trace.endpoint}</p>
              <details className="trace-technical-details">
                <summary>Ver detalle tecnico</summary>
                <div className="trace-technical-details__body">
                  <CodeBlock title="Request parameters" value={trace.request_parameters} collapsible />
                  <CodeBlock title={`Response (${trace.response_status})`} value={trace.response_body} collapsible />
                </div>
              </details>
            </div>
          </details>
        ))}
      </div>
    </section>
  );
}
