import { CodeBlock } from "./CodeBlock";

interface ClaimsViewerProps {
  title: string;
  claims: Record<string, unknown>;
  showHeader?: boolean;
}

export function ClaimsViewer({ title, claims, showHeader = true }: ClaimsViewerProps) {
  if (!claims || Object.keys(claims).length === 0) {
    return <p className="muted">No hay claims disponibles para este token.</p>;
  }

  return <CodeBlock title={title} value={claims} showHeader={showHeader} />;
}
