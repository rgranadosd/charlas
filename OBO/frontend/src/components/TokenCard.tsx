import { useState } from "react";
import type { TokenArtifact } from "../types/models";
import { ClaimsViewer } from "./ClaimsViewer";
import { CodeBlock } from "./CodeBlock";
import { ScopeChips } from "./ScopeChips";
import { StatusBadge } from "./StatusBadge";

interface TokenCardProps {
  title: string;
  artifact: TokenArtifact;
  defaultExpanded?: boolean;
}

interface TokenSubPanelProps {
  title: string;
  subtitle?: string;
  defaultExpanded?: boolean;
  statusLabel?: string;
  actions?: React.ReactNode;
  children: React.ReactNode;
}

function TokenSubPanel({
  title,
  subtitle,
  defaultExpanded = false,
  statusLabel,
  actions,
  children,
}: TokenSubPanelProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <section className="panel token-card">
      <div className="panel__header">
        <div className="panel-collapsible-title">
          <button
            type="button"
            className="collapse-toggle"
            onClick={() => setExpanded((current) => !current)}
            aria-label={expanded ? "Colapsar panel" : "Expandir panel"}
            title={expanded ? "Colapsar panel" : "Expandir panel"}
          >
            {expanded ? "▼" : "▶"}
          </button>
          <div>
            <h3>{title}</h3>
            {subtitle ? <p>{subtitle}</p> : null}
          </div>
        </div>
        {statusLabel ? <StatusBadge label={statusLabel} /> : actions ?? null}
      </div>

      {expanded ? <div className="panel-collapsible-content">{children}</div> : null}
    </section>
  );
}

export function TokenCard({ title, artifact, defaultExpanded = false }: TokenCardProps) {
  const previewValue = artifact.raw ?? artifact.preview ?? "missing";
  const claimsValue = artifact.claims ?? {};

  async function copyValue(value: unknown) {
    const text = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "true");
      textarea.style.position = "absolute";
      textarea.style.left = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
    }
  }

  return (
    <>
      <TokenSubPanel
        title={title}
        subtitle={artifact.explanation ?? "Artifact not available yet."}
        statusLabel={artifact.status}
        defaultExpanded={defaultExpanded}
      >
        <dl className="meta-grid">
          <div>
            <dt>Emitido por</dt>
            <dd>{artifact.issuer ?? "n/a"}</dd>
          </div>
          <div>
            <dt>Consumido por</dt>
            <dd>{artifact.consumer ?? "n/a"}</dd>
          </div>
          <div>
            <dt>sub</dt>
            <dd>{artifact.subject ?? "n/a"}</dd>
          </div>
          <div>
            <dt>act</dt>
            <dd>{artifact.actor ?? "none"}</dd>
          </div>
          <div>
            <dt>exp</dt>
            <dd>{artifact.expires_at ?? "n/a"}</dd>
          </div>
        </dl>
      </TokenSubPanel>

      <TokenSubPanel
        title={`${title} preview`}
        actions={
          <button
            type="button"
            className="ghost-button icon-button"
            onClick={() => void copyValue(previewValue)}
            aria-label="Copiar preview"
            title="Copiar"
          >
            ⧉
          </button>
        }
      >
        <CodeBlock value={previewValue} showHeader={false} />
      </TokenSubPanel>

      <TokenSubPanel title={`${title} scopes`}>
        <ScopeChips scopes={artifact.scopes} />
      </TokenSubPanel>

      <TokenSubPanel
        title={`${title} claims`}
        actions={
          <button
            type="button"
            className="ghost-button icon-button"
            onClick={() => void copyValue(claimsValue)}
            aria-label="Copiar claims"
            title="Copiar"
          >
            ⧉
          </button>
        }
      >
        <ClaimsViewer title={`${title} claims`} claims={artifact.claims} showHeader={false} />
      </TokenSubPanel>
    </>
  );
}
