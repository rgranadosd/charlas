import type { TraceEntry } from "../types/models";
import { CodeBlock } from "./CodeBlock";

interface TraceViewerProps {
  traces: TraceEntry[];
  selectedStepOrder?: number | null;
}

const STEP_TRACE_ACTIONS: Record<number, string[]> = {
  1: ["Sincronizar USER_TOKEN"],
  2: ["Obtener AGENT_TOKEN"],
  3: ["Probar acceso con AGENT_TOKEN"],
  4: ["Iniciar delegacion OBO"],
  5: ["Recibir authorization_code"],
  6: ["Intercambiar code por OBO_TOKEN"],
  7: ["Leer mis ficheros con OBO_TOKEN"],
};

export function TraceViewer({ traces, selectedStepOrder = null }: TraceViewerProps) {
  function formatTimestamp(timestamp: string) {
    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
      return timestamp;
    }

    return date.toLocaleString();
  }

  const selectedActions = selectedStepOrder ? STEP_TRACE_ACTIONS[selectedStepOrder] ?? [] : [];

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
        {traces.map((trace, index) => {
          const isCurrent = index === 0;
          const isSelectedStepTrace = selectedActions.includes(trace.action);
          const traceClasses = ["trace-item"];

          if (isCurrent) {
            traceClasses.push("is-current");
          }

          if (isSelectedStepTrace) {
            traceClasses.push("is-step-focus");
          }

          if (!isCurrent && !isSelectedStepTrace) {
            traceClasses.push("is-historical");
          }

          return (
            <details
              key={`${trace.timestamp}-${trace.action}`}
              open={isCurrent}
              className={traceClasses.join(" ")}
            >
              <summary>
                <div className="trace-summary-main">
                  <strong>{trace.action}</strong>
                  <p className="trace-summary-caption">{trace.security_interpretation}</p>
                </div>
                <div className="trace-summary-side">
                  <span
                    className={`trace-chip trace-chip--phase ${isCurrent ? "is-current" : isSelectedStepTrace ? "is-step-focus" : "is-historical"}`}
                  >
                    {isCurrent ? "Actual" : isSelectedStepTrace ? "Paso actual" : "Previo"}
                  </span>
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
          );
        })}
      </div>
    </section>
  );
}
